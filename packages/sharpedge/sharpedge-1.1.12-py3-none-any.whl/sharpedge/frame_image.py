import numpy as np
import warnings
from sharpedge._utils.utility import Utility

def _format_conversion(img, color):
    """
    Private function to be invoked by frame_image().
    
    Convert grayscale image to RGB if necessary, and ensure color format is valid.

    This function checks if the image is grayscale and converts it to RGB if needed.
    It also validates and converts the color input for the border to RGB format.

    Parameters
    ----------
    img : ndarray
        The input image as a 2D numpy array (grayscale) or 3D numpy array (RGB).
    
    color : int or tuple of int
        The color of the border. Can be:
        - A single value for grayscale frames (e.g., 0 for black, 255 for white).
        - A tuple of 3 values for RGB frames (e.g., (0, 0, 0) for black).
    
    Returns
    -------
    img : ndarray
        The image in RGB format (3D array).
    
    color : tuple of int
        The color for the border in RGB format (3 integers).
    
    Raises
    ------
    ValueError
        If the color is not in the correct format (for RGB or grayscale).
    TypeError
        If the color is not of the correct type (integer for grayscale, tuple/list for RGB).
    """

    # Check for RGB color validity
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
    
    # Convert `color` grayscale integer to same RGB tuple
    if isinstance(color, int):
        color = (color, color, color)
    
    # Represent grayscale image in 3-channel image format if needed
    if img.ndim == 2:  # Grayscale image (2D)
        img = np.stack([img] * 3, axis=-1)
    
    return img, color

def _image_resize(img, h_border, w_border, inside):
    """
    Private function to be invoked by frame_image().

    Resize the image by adding borders either inside or outside.

    This function handles resizing the image, ensuring that if borders are added inside,
    the image size is reduced, and if borders are added outside, the image size increases.

    Parameters
    ----------
    img : ndarray
        The input image array (either 2D or 3D).
    
    h_border : int
        The height of the border in pixels.
    
    w_border : int
        The width of the border in pixels.
    
    inside : bool
        If True, the border is added **inside** the image (maintaining the image size). 
        If False, the border is added **outside** the image (increasing the image size). 
    
    Returns
    -------
    img : ndarray
        The resized image, with borders applied.
    
    Raises
    ------
    ValueError
        If the inside border is too large for the image dimensions.
        If the `h_border` or `w_border` is negative or invalid.
    TypeError
        If the `h_border` or `w_border` is not an integer.
    """
    # Check the *_border inputs are correct: integers and non-negative
    if not isinstance(h_border, int) or not isinstance(w_border, int):
        raise TypeError("Both h_border and w_border must be integers.")

    if h_border < 0 or w_border < 0:
        raise ValueError("Both h_border and w_border must be non-negative integers.")
    
    # Warning: when any border size is 0
    if h_border == 0 or w_border == 0:
        warnings.warn("Border size of 0 doesn't add any visual effect to the image.", UserWarning)

    # Handle image resizing (inside or outside border)
    if inside:
        # Error: the image is too small to fit the inside border
        if img.shape[0] <= 2 * h_border or img.shape[1] <= 2 * w_border:
            raise ValueError("The inside border is too large for this small image. The image cannot be processed.")
        # Warning: when the inside border is greater than 50% of image size
        elif (2 * h_border > 0.5 * img.shape[0]) or (2 * w_border > 0.5 * img.shape[1]):
            warnings.warn("The inside border exceeds 50% image size and may shrink the image significantly.", UserWarning)
        
        # Handle slicing for inside padding (keeping size constant)
        img = img[h_border:-h_border or None, w_border:-w_border or None, :]
    
    # Warning: when single side outside border is larger than the image dimensions
    elif not inside and (h_border >= img.shape[0] or w_border >= img.shape[1]):
        warnings.warn("Single side border size exceeds image size.", UserWarning)

    return img

def _color_padding(img, h_border, w_border, color):
    """
    Private function to be invoked by frame_image().

    Apply color padding by adding a border around the image.

    This function adds a border of the specified color around the image, either inside 
    or outside the image.

    Parameters
    ----------
    img : ndarray
        The input image array (3D array with 3 color channels).
    
    h_border : int
        The height of the border in pixels.
    
    w_border : int
        The width of the border in pixels.
    
    color : tuple of int
        The RGB color for the border.
    
    Returns
    -------
    frame : ndarray
        The image with the color border applied.
    """
    # Calculate the new shape for the image with the border
    new_height = img.shape[0] + 2 * h_border
    new_width = img.shape[1] + 2 * w_border

    # Create the border: a full array of the border color
    frame = np.full((new_height, new_width, 3), color, dtype=np.uint8)

    # Insert the image in the center of the border
    frame[h_border:h_border + img.shape[0], w_border:w_border + img.shape[1]] = img

    return frame

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

    # Handle format conversion (grayscale to RGB) and color padding validation
    img, color = _format_conversion(img, color)

    # Handle image resizing (inside or outside border)
    img = _image_resize(img, h_border, w_border, inside)

    # Apply color padding (create the framed image with border)
    framed_img = _color_padding(img, h_border, w_border, color)

    return framed_img