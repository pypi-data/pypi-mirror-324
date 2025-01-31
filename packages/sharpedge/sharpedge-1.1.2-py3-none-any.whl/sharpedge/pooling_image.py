import numpy as np
from sharpedge._utils.utility import Utility

def pooling_image(img, window_size, pooling_method=np.mean):
    """
    Perform pooling on an image using a specified window size and pooling function.

    Parameters
    ----------
    img : numpy.ndarray
        The input image as a 2D numpy array (grayscale) or 3D numpy array (RGB).
    window_size : int
        The size of the pooling window (e.g., 10 for 10x10 windows).
    pooling_method : callable, optional
        The pooling function to apply to each window. Common options include 
        `numpy.mean`, `numpy.median`, `numpy.max`, and `numpy.min`. Default is `numpy.mean`.

    Returns
    -------
    numpy.ndarray
        The resized image, reduced by the pooling operation based on the specified 
        window size and pooling function. For grayscale images, the result is a 2D array. 
        For RGB images, the result is a 3D array normalized to the range [0.0, 1.0].

    Raises
    ------
    TypeError
        If `window_size` is not an integer or `pooling_method` is not callable.
    ValueError
        If the image dimensions are not divisible by the window size.

    Examples
    --------
    >>> img = np.random.rand(100, 100)
    >>> pooled_img = pooling_image(img, window_size=10, pooling_method=np.mean)

    For an RGB image:
    >>> img_rgb = np.random.rand(100, 100, 3)
    >>> pooled_img = pooling_image(img_rgb, window_size=20, pooling_method=np.max)
    """
    # Input validation
    Utility._input_checker(img)

    if not isinstance(window_size, int):
        raise TypeError("window_size must be an integer.")
    
    if not callable(pooling_method):
        raise TypeError("pooling_method must be callable.")
    
    img_rows, img_cols = img.shape[:2]

    # Check if dimensions are divisible by window size
    if img_rows % window_size != 0 or img_cols % window_size != 0:
        raise ValueError("Image dimensions are not divisible by the window size.")

    # Ensure image is in float32 format for calculations
    img = img.astype(np.float32)

    # Initialize the result array with appropriate dimensions
    result_rows = img_rows // window_size
    result_cols = img_cols // window_size

    if img.ndim == 2:  # Grayscale image
        pooled_image = np.zeros((result_rows, result_cols))
        for i in range(result_rows):
            for j in range(result_cols):
                window = img[i*window_size:(i+1)*window_size, j*window_size:(j+1)*window_size]
                pooled_image[i, j] = pooling_method(window)
    else:  # RGB image
        pooled_image = np.zeros((result_rows, result_cols, img.shape[2]))
        for i in range(result_rows):
            for j in range(result_cols):
                window = img[i*window_size:(i+1)*window_size, j*window_size:(j+1)*window_size, :]
                for c in range(img.shape[2]):
                    pooled_image[i, j, c] = pooling_method(window[:, :, c])
        
        # Normalize RGB image to [0.0, 1.0]
        pooled_image /= 255.0

    return pooled_image
