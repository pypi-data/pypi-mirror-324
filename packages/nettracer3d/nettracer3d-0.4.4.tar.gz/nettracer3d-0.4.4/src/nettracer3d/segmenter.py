from sklearn.ensemble import RandomForestClassifier
import numpy as np
import cupy as cp
import torch
from concurrent.futures import ThreadPoolExecutor
import threading
import cupyx.scipy.ndimage as cpx


class InteractiveSegmenter:
    def __init__(self, image_3d, use_gpu=True):
        self.image_3d = image_3d
        self.patterns = []

        self.use_gpu = use_gpu and cp.cuda.is_available()
        if self.use_gpu:
            print(f"Using GPU: {torch.cuda.get_device_name()}")
            self.image_gpu = cp.asarray(image_3d)
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            n_jobs=-1,
            max_depth=None
        )
        self.feature_cache = None
        self.lock = threading.Lock()

    def compute_feature_maps(self):
        """Compute all feature maps using GPU acceleration"""
        if not self.use_gpu:
            return super().compute_feature_maps()
        
        features = []
        image = self.image_gpu
        original_shape = self.image_3d.shape
        
        # Gaussian smoothing at different scales
        print("Obtaining gaussians")
        for sigma in [0.5, 1.0, 2.0, 4.0]:
            smooth = cp.asnumpy(self.gaussian_filter_gpu(image, sigma))
            features.append(smooth)
        
        print("Obtaining dif of gaussians")

        # Difference of Gaussians
        for (s1, s2) in [(1, 2), (2, 4)]:
            g1 = self.gaussian_filter_gpu(image, s1)
            g2 = self.gaussian_filter_gpu(image, s2)
            dog = cp.asnumpy(g1 - g2)
            features.append(dog)
        
        # Convert image to PyTorch tensor for gradient operations
        image_torch = torch.from_numpy(self.image_3d).cuda()
        image_torch = image_torch.float().unsqueeze(0).unsqueeze(0)
        
        # Calculate required padding
        kernel_size = 3
        padding = kernel_size // 2
        
        # Create a single padded version with same padding
        pad = torch.nn.functional.pad(image_torch, (padding, padding, padding, padding, padding, padding), mode='replicate')
        
        print("Computing sobel kernels")

        # Create sobel kernels
        sobel_x = torch.tensor([-1, 0, 1], device='cuda').float().view(1,1,1,1,3)
        sobel_y = torch.tensor([-1, 0, 1], device='cuda').float().view(1,1,1,3,1)
        sobel_z = torch.tensor([-1, 0, 1], device='cuda').float().view(1,1,3,1,1)
        
        # Compute gradients
        print("Computing gradiants")

        gx = torch.nn.functional.conv3d(pad, sobel_x, padding=0)[:,:,:original_shape[0],:original_shape[1],:original_shape[2]]
        gy = torch.nn.functional.conv3d(pad, sobel_y, padding=0)[:,:,:original_shape[0],:original_shape[1],:original_shape[2]]
        gz = torch.nn.functional.conv3d(pad, sobel_z, padding=0)[:,:,:original_shape[0],:original_shape[1],:original_shape[2]]
        
        # Compute gradient magnitude
        print("Computing gradiant mags")

        gradient_magnitude = torch.sqrt(gx**2 + gy**2 + gz**2)
        gradient_feature = gradient_magnitude.cpu().numpy().squeeze()
        
        features.append(gradient_feature)
        
        # Verify shapes
        for i, feat in enumerate(features):
            if feat.shape != original_shape:
                raise ValueError(f"Feature {i} has shape {feat.shape}, expected {original_shape}")
        
        return np.stack(features, axis=-1)

    def gaussian_filter_gpu(self, image, sigma):
        """GPU-accelerated Gaussian filter"""
        # Create Gaussian kernel
        result = cpx.gaussian_filter(image, sigma=sigma)

        return result


    def train(self):
        """Train random forest on accumulated patterns"""
        if len(self.patterns) < 2:
            return
        
        X = []
        y = []
        for pattern in self.patterns:
            X.extend(pattern['features'])
            y.extend([pattern['is_foreground']] * len(pattern['features']))
        
        X = np.array(X)
        y = np.array(y)
        self.model.fit(X, y)
        self.patterns = []

    def process_chunk(self, chunk_coords):
        """Process a chunk of coordinates"""
        features = [self.feature_cache[z, y, x] for z, y, x in chunk_coords]
        predictions = self.model.predict(features)
        
        foreground = set()
        background = set()
        for coord, pred in zip(chunk_coords, predictions):
            if pred:
                foreground.add(coord)
            else:
                background.add(coord)
        
        return foreground, background

    def segment_volume(self, chunk_size=32):
        """Segment volume using parallel processing of chunks"""
        if self.feature_cache is None:
            with self.lock:
                if self.feature_cache is None:
                    self.feature_cache = self.compute_feature_maps()
        
        # Create chunks of coordinates
        chunks = []
        for z in range(0, self.image_3d.shape[0], chunk_size):
            for y in range(0, self.image_3d.shape[1], chunk_size):
                for x in range(0, self.image_3d.shape[2], chunk_size):
                    chunk_coords = [
                        (zz, yy, xx) 
                        for zz in range(z, min(z + chunk_size, self.image_3d.shape[0]))
                        for yy in range(y, min(y + chunk_size, self.image_3d.shape[1]))
                        for xx in range(x, min(x + chunk_size, self.image_3d.shape[2]))
                    ]
                    chunks.append(chunk_coords)
        
        foreground_coords = set()
        background_coords = set()
        
        # Process chunks in parallel
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_chunk, chunk) for chunk in chunks]
            
            for i, future in enumerate(futures):
                fore, back = future.result()
                foreground_coords.update(fore)
                background_coords.update(back)
                if i % 10 == 0:
                    print(f"Processed {i}/{len(chunks)} chunks")
        
        return foreground_coords, background_coords

    def cleanup(self):
        """Clean up GPU memory"""
        if self.use_gpu:
            cp.get_default_memory_pool().free_all_blocks()
            torch.cuda.empty_cache()

    def train_batch(self, foreground_array, background_array):
        """Train directly on foreground and background arrays"""
        if self.feature_cache is None:
            with self.lock:
                if self.feature_cache is None:
                    self.feature_cache = self.compute_feature_maps()
        
        # Get foreground coordinates and features
        z_fore, y_fore, x_fore = np.where(foreground_array > 0)
        foreground_features = self.feature_cache[z_fore, y_fore, x_fore]
        
        # Get background coordinates and features
        z_back, y_back, x_back = np.where(background_array > 0)
        background_features = self.feature_cache[z_back, y_back, x_back]
        
        # Combine features and labels
        X = np.vstack([foreground_features, background_features])
        y = np.hstack([np.ones(len(z_fore)), np.zeros(len(z_back))])
        
        # Train the model
        self.model.fit(X, y)

        print("Done")









        def segment_volume_subprocess(self, chunk_size=32, current_z=None, current_x=None, current_y=None):
            """
            Segment volume prioritizing chunks near user location.
            Returns chunks as they're processed.
            """
            if self.feature_cache is None:
                with self.lock:
                    if self.feature_cache is None:
                        self.feature_cache = self.compute_feature_maps()
            
            # Create chunks with position information
            chunks_info = []
            for z in range(0, self.image_3d.shape[0], chunk_size):
                for y in range(0, self.image_3d.shape[1], chunk_size):
                    for x in range(0, self.image_3d.shape[2], chunk_size):
                        chunk_coords = [
                            (zz, yy, xx) 
                            for zz in range(z, min(z + chunk_size, self.image_3d.shape[0]))
                            for yy in range(y, min(y + chunk_size, self.image_3d.shape[1]))
                            for xx in range(x, min(x + chunk_size, self.image_3d.shape[2]))
                        ]
                        
                        # Store chunk with its corner position
                        chunks_info.append({
                            'coords': chunk_coords,
                            'corner': (z, y, x),
                            'processed': False
                        })

            def get_chunk_priority(chunk):
                """Calculate priority based on distance from user position"""
                z, y, x = chunk['corner']
                priority = 0
                
                # Priority based on Z distance (always used)
                if current_z is not None:
                    priority += abs(z - current_z)
                
                # Add X/Y distance if provided
                if current_x is not None and current_y is not None:
                    xy_distance = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5
                    priority += xy_distance
                    
                return priority

            with ThreadPoolExecutor() as executor:
                futures = {}  # Track active futures
                
                while True:
                    # Sort unprocessed chunks by priority
                    unprocessed_chunks = [c for c in chunks_info if not c['processed']]
                    if not unprocessed_chunks:
                        break
                        
                    # Sort by distance from current position
                    unprocessed_chunks.sort(key=get_chunk_priority)
                    
                    # Submit new chunks to replace completed ones
                    while len(futures) < executor._max_workers and unprocessed_chunks:
                        chunk = unprocessed_chunks.pop(0)
                        future = executor.submit(self.process_chunk, chunk['coords'])
                        futures[future] = chunk
                        chunk['processed'] = True
                    
                    # Check completed futures
                    done, _ = concurrent.futures.wait(
                        futures.keys(),
                        timeout=0.1,
                        return_when=concurrent.futures.FIRST_COMPLETED
                    )
                    
                    # Process completed chunks
                    for future in done:
                        chunk = futures[future]
                        fore, back = future.result()
                        
                        # Yield chunk results with position information
                        yield {
                            'foreground': fore,
                            'background': back,
                            'corner': chunk['corner'],
                            'size': chunk_size
                        }
                        
                        del futures[future]

