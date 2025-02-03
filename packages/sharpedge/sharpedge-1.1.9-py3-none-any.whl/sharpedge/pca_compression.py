from sharpedge._utils.utility import Utility
import numpy as np
import warnings

def pca_compression(img, preservation_rate=0.9):
    """
    Compress the input image using Principal Component Analysis (PCA) via the Singular Value Decomposition (SVD) method.
    This function compresses the size of an image by applying the PCA method while retaining a specified 
    portion of the original data variance.
    It supports grayscale (2D) images.
    
    Parameters
    ----------
    img : numpy.ndarray
        Input image array. This needs to be a 2D numpy array (grayscale image).
    
    preservation_rate : float, optional
        The proportion of eigen values to preserve in the compressed image. Must be a value between 0 and 1.
        Higher values preserve more details from the original image, while lower values result in greater
        compression. Default is 0.9.

    Returns
    -------
    numpy.ndarray
        A numpy array representing the manipulated image. The output would be:
        - A grayscale image (2D array).
    
    Raises
    ------
    TypeError
        If `preservation_rate` is not a float.
    ValueError
        If the input image is not valid (not a 2D array).
        If `preservation_rate` is not between 0 and 1.
    Warning
        If `preservation_rate` is very low (< 0.1), as it may result in significant quality loss.
      
    Examples
    --------
    Compress a grayscale image by retaining 80% of the variance:
    >>> compressed_img = pca_compression(img, preservation_rate=0.8)

    Compress an RGB image with the default preservation rate (90%):
    >>> compressed_img = pca_compression(img)
    """
    # Validate Input
    Utility._input_checker(img)
    if img.ndim != 2:
        raise ValueError("Input image must be a 2D array.")
    if not isinstance(preservation_rate, (int, float)):
        raise TypeError("preservation_rate must be a number.")
    if not (0 < preservation_rate <= 1):
        raise ValueError("preservation_rate must be a float between 0 and 1.")
    # Raise a warning for low preservation_rate
    if preservation_rate < 0.1:
        warnings.warn("Very low preservation_rate may result in significant quality loss.", UserWarning)

    # Perform SVD
    U, S, Vt = np.linalg.svd(img, full_matrices=False)
    
    # Determine the number of largest singular values to keep
    total_singular_values = len(S)
    num_to_keep = max(1, int(total_singular_values * preservation_rate))  # At least 1 singular value
    
    # Truncate U, S, and Vt to keep the largest singular values
    U_k = U[:, :num_to_keep]
    S_k = np.diag(S[:num_to_keep])
    Vt_k = Vt[:num_to_keep, :]
    
    # Reconstruct the compressed image
    compressed_image = np.dot(U_k, np.dot(S_k, Vt_k))
    
    # Round values
    compressed_image = compressed_image.round()
    
    return compressed_image









