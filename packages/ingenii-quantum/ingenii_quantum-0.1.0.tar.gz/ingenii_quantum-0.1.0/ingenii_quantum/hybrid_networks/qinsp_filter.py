import numpy as np
from PIL import Image
from numpy.lib.stride_tricks import sliding_window_view
from scipy.signal import find_peaks


class QuantumInspiredImageProcessor:
    """
    Applies a quantum-inspired image filter.

    This transformation weighs each pixel's original intensity by a relative measure 
    of pairwise intensity difference versus total neighborhood contribution.

    **Class Parameters**:
        - **mu (float):** Steepness factor. Higher values lead to sharper curves, 
          whereas lower values provide smoother transitions.
        - **neighbor_size (int):** Neighborhood size for intensity computations.
        - **percentile (int):** Percentile to determine cluster values w.
        - **max_iter (int):** Maximum iterations for transformation.
        - **threshold (float):** Convergence threshold based on Mean Absolute Difference.
        - **L (int):** Number of cluster levels.

    **Example Parameters**:
        - mu = 0.4
        - neighbor_size = 3
        - percentile = 50
        - max_iter = 10
        - threshold = 1e-5
        - L = 12
    """

    def __init__(self, mu=0.40, neighbor_size = 3, percentile=95, max_iter=10, threshold=0.0001, L=8):
        
        self.mu = mu
        self.neighbor_size = neighbor_size
        self.percentile = percentile
        self.max_iter = max_iter
        self.threshold = threshold
        self.L = L
        self.info = {}

    def check_convergence(self, w1, w2):
        '''
        Check convergence of the quantum-inspired model.

        If the Mean Absolute Difference (MAD) of two consecutive matrices 
        is smaller than the threshold, the method has converged.

        Args:
            w1 (np.array): Previous image matrix.
            w2 (np.array): Current image matrix.

        Returns:
            bool: True if the model has converged, False otherwise.
            float: Mean Absolute Difference.
        '''
        mae = np.mean(np.abs(w1- w2))
        if mae < self.threshold:
            print('Final Mean Absolute Difference: {:0.4f}'.format(mae))
            return True, mae
        return False, mae

    def sum_neighbours(self, image):
        '''
        Computes the sum of the neighborhood of each pixel.

        Args:
            image (np.array): Input image.

        Returns:
            np.array: Sum of neighboring pixels for each pixel.
        '''
        # 1. Calculate image shape
        ht,_ = image.shape
        # 2. Calculate necessary padding
        pad = int(np.ceil((np.ceil(ht/self.neighbor_size)*self.neighbor_size - ht)/2))
        if pad>0: # Pad image with 0s if the size of the image is not a multiple of the neighbouring size
            image = np.pad(image, (pad,pad), mode='constant', constant_values=(0,0))
        # 3. Create a window view of the image
        window_view = sliding_window_view(image, (self.neighbor_size, self.neighbor_size))
        # 4. Sum the elements of the view
        sum_neighbourhood = np.sum(window_view, axis=(2,3))
        return sum_neighbourhood

    def transformation(self, I, cluster):
        """
        Applies a quantum-inspired transformation.

        Args:
            I (np.array): Input image.
            cluster (np.array): Array containing the cluster values [w0, w1, ..., wn].

        Returns:
            np.array: Quantum-inspired image transformation (one iteration).

            np.array: Alpha values calculated as `1 - (I_{i+p,j+q} - I_{ij})`.
        """
        I[I<0] = 0
        I[I>1] = 1
        ht, wt = I.shape[1], I.shape[0] 
        # 1. Calculate the sum of intensities of the 3x3 window for each pixel
        S = self.sum_neighbours(I)

        # Select cluster
        cluster = np.array(cluster)
        d = cluster.shape[0]
        # f is the quantum-inspired activation function f = sum( 1/(lamb + e^-mu(x-S)) ) 
        f = np.zeros((ht, wt))
        Alpha = np.zeros((ht, wt))
        idx = np.arange(d)
        for i in range(ht):
            for j in range(wt):
                p_vals = np.clip(np.arange(i - 1, i + 2), 0, ht - 1) # Indices [i-1, i, i+1] padding with 0s at the edges
                q_vals = np.clip(np.arange(j - 1, j + 2), 0, wt - 1) # Indices [j-1, j, j+1] padding with 0s at the edges
                # Find the index where I[i,j] >= cluster[k] and I[i,j] <= cluster[k + 1]
                if len(idx[I[i,j]>=cluster])==0:
                    print(I[i,j], cluster)
                k = min(idx[I[i,j]>=cluster][-1], d-2)
                if k+1 >=len(cluster):
                    lamb = S[i, j] / (1. - cluster[k])
                else:
                    lamb = S[i, j] / (cluster[k+1] - cluster[k])            
                sum_ = 0.
                alpha_ = 0.
                for p in p_vals:
                    for q in q_vals:
                        alpha = (1 - (I[p, q] - I[i, j]))
                        x = I[p, q] * np.cos((np.pi * 2) *(alpha - S[i, j]))
                        y = 1 / (lamb + np.exp(-self.mu * (x - S[i, j])))
                        sum_ += y
                        alpha_+=alpha
                #print('Lambda: ',lamb, 'x: ', x, 'S: ', S[i,j])
                f[i, j] = sum_
                Alpha[i, j] = alpha_

        return f, Alpha


    def select_image(self, mae_list, image_list):
        """
        Selects the output of the image transformation after multiple iterations.

        The selection is based on detecting peaks in the Mean Absolute Differences (MAD).

        Args:
            mae_list (list): List of Mean Absolute Differences between iterations.
            image_list (list): List of image transformations.

        Returns:
            np.array: Final selected image.

            int: Iteration index at which the best image was selected.
        """
        # We select the image that has a peak in the mae
        mae_list = mae_list[1:]
        if len(mae_list)==1:
            return image_list[1], 1
        peaks, _ = find_peaks(mae_list, height=0)
        if len(peaks)==0:
            selected_peak = np.argmin(np.abs(np.diff(mae_list))/mae_list[1:]) + 1
        else:
            # If there are more than 1 peaks, we select the mean value
            selected_peak = int(np.mean(peaks))
            # For longer iterations, we add 1 to the output
            if selected_peak>5:
                selected_peak+= 1
        # Return the final selected image
        selected_peak = max(selected_peak,1)
        # If the images converge to a constant color, choose intermediate steps
        density, _ = np.histogram(image_list[selected_peak].flatten()/255, bins=20, density=False)
        density = density/np.sum(density)
        if np.max(density)>0.8:
            for i in range(len(image_list)-1, 0, -1):
                density, _ = np.histogram(image_list[i].flatten()/255, bins=20, density=False)
                density = density/np.sum(density)
                if np.max(density)<0.75:
                    selected_peak = i
                    return image_list[selected_peak], selected_peak
            selected_peak = 1
        return image_list[selected_peak], selected_peak


    def process(self, im, save=True, image_path='./filtered_image.png'):
        """
        Applies the quantum-inspired transformation until convergence.

        Args:
            im (np.array): Input image.
            save (bool, optional): If True, saves the final image. Defaults to True.
            image_path (str, optional): Path to save the final image. Defaults to './filtered_image.png'.

        Returns:
            np.array: Final processed image.

            list: List of Mean Absolute Differences between iterations.

            list: List of image transformations.
        """
        
        wt, ht = im.shape[1], im.shape[0]  # Dimensions of the matrix    
        self.info['num_circuits'] = wt*ht
        self.info['nqbits'] = 3
        self.info['depth'] = 4
        self.info['gates'] = {'RX':2, 'CCX': 1, 'H': 2}
        self.info['num_nonlocal_gates'] = 1
        # Determine cluster values w
        min_val, max_val = np.percentile(im.flatten()/255, self.percentile), 1
        dw = (max_val - min_val)/(self.L-3)
        w = [0] + list(np.arange(min_val, max_val+dw, dw)) 
        
        transformed_image = im.copy().astype(float) / 255  # Initial image 
        #transformed_image *= (np.pi / 2) # Normalize initial image to [0, pi/2]

        w1 = np.zeros((ht, wt))
        mae_list = [0]
        image_list = [im]
        # Evolve Quantum inspired image until convergence
        for t in range(self.max_iter):  # Limit iterations 
            if t==0:
                cluster=w
            else:
                cluster = [0 ,0.16, 0.32, 0.48 ,0.64, 0.80, 0.96, 1]

            intermediate_matrix, _, = self.transformation(transformed_image, cluster)  
            transformed_image, w2 = self.transformation(intermediate_matrix, cluster)
            stop, mae = self.check_convergence(w2, w1)
            mae_list.append(mae)
            image_list.append((transformed_image * 255).astype(np.uint8))
            if stop:# Check for convergence
                break
            w1 = w2
        print('Number of iterations: ', t+1)
        out, selected_image=  self.select_image(mae_list, image_list)
        print('Selected image: ', selected_image)
        if save:
            Image.fromarray(out).save(image_path)

        return out, mae_list, image_list
