import numpy as np
import warnings
from sharpedge._utils.utility import Utility

def frame_image(img, h_border=20, w_border=20, inside=False, color=0):
    """
    Add a decorative frame around the image with a customizable color.

    This function adds a border around the input image, either inside the image 
    (preserving its original size) or outside (increasing its size). The border 
    color can be specified for both grayscale and RGB images.

    Parameters
    ----------
    img : ndarray
        The input image as a 2D numpy array (grayscale) or 3D numpy array (RGB).
    h_border : int, optional
        The height of the border in pixels. Default is 20.
    w_border : int, optional
        The width of the border in pixels. Default is 20.
    inside : bool, optional
        If True, the border is added **inside** the image (maintaining the image size). 
        If False, the border is added **outside** the image (increasing the image size). 
        Default is False.
    color : int or tuple of int, optional
        The color of the border. Can be:
        - A single value for grayscale frames (e.g., 0 for black, 255 for white).
        - A tuple of 3 values for RGB frames (e.g., (0, 0, 0) for black).
        Default is 0 (black) for grayscale frames.

    Returns
    -------
    ndarray
        The framed image with the applied border.

    Examples
    --------
    >>> img = np.random.rand(100, 100)
    >>> framed_img = frame_image(img, h_border=30, w_border=30, inside=True, color=255)
    >>> framed_img_rgb = frame_image(img_rgb, h_border=20, w_border=20, inside=False, color=(255, 0, 0))
    """
    # Input validation
    Utility._input_checker(img)
    
    # Warning: when image size is below 3 x 3
    if img.shape[0] < 3 or img.shape[1] < 3:
        warnings.warn("The image is too small for meaningful visual information. Proceeding may not yield interpretable results.", UserWarning)
      
    # Check the *_border inputs are correct: integers and non-negative
    if not isinstance(h_border, int) or not isinstance(w_border, int):
        raise TypeError("Both h_border and w_border must be integers.")

    if h_border < 0 or w_border < 0:
        raise ValueError("Both h_border and w_border must be non-negative integers.")
    
    # Warning: when any border size is 0
    if h_border == 0 or w_border == 0:
        warnings.warn("Border size of 0 doesn't add any visual effect to the image.", UserWarning)

    # Check that the color input is correct for grayscale or RGB image
    if isinstance(color, (tuple, list)):
        if len(color) != 3:
            raise ValueError("For RGB frames, color must be a tuple or list of 3 integers.")
        for rgb_c in color:
            if not isinstance(rgb_c, int):
                raise TypeError("Each color component must be an integer.")
            if not (0 <= rgb_c <= 255):
                raise ValueError("Each color component must be in the range 0 to 255.")
    elif isinstance(color, int):
        if not (0 <= color <= 255):
            raise ValueError("For grayscale frames, color must be an integer in the range 0 to 255.")
    else:
        raise TypeError("Color must be either an integer for grayscale frames or a tuple/list of 3 integers for RGB frames.")

    # Check for relationship between image size and border size
    if inside:
        # Error: the image is too small to fit the inside border
        if img.shape[0] <= 2 * h_border or img.shape[1] <= 2 * w_border:
            raise ValueError("The inside border is too large for this small image. The image cannot be processed.")
        # Warning: when the inside border is greater than 50% of image size
        elif (2 * h_border > 0.5 * img.shape[0]) or (2 * w_border > 0.5 * img.shape[1]):
            warnings.warn("The inside border exceeds 50% image size and may shrink the image significantly.", UserWarning)
        
    # Warning: when single side outside border is larger than the image dimensions
    if not inside and (h_border >= img.shape[0] or w_border >= img.shape[1]):
        warnings.warn("Single side border size exceeds image size.", UserWarning)

    # Convert `color` grayscale integer to same RGB tuple
    if isinstance(color, int):
        color = (color, color, color)
    
    # Represent grayscale image in 3-channel image format
    if img.ndim == 2:  # Grayscale image (2D)
        # Convert grayscale to RGB by repeating the grayscale values across 3 channels
        img = np.stack([img] * 3, axis=-1)

    # Handle slicing for inside padding (keeping size constant)
    if inside:
        img = img[h_border:-h_border or None, w_border:-w_border or None, :]
    
    # Calculate the new shape for the image with the border
    new_height = img.shape[0] + 2 * h_border
    new_width = img.shape[1] + 2 * w_border

    # Create the border: a full array of the border color
    frame = np.full((new_height, new_width, 3), color, dtype=np.uint8)

    # Insert the image in the center of the border
    frame[h_border:h_border + img.shape[0], w_border:w_border + img.shape[1]] = img

    return frame
