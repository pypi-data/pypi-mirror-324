import numpy as np
import warnings
from sharpedge._utils.utility import Utility


def _flip_image(img, flip):
    """Flips the image based on the specified flip parameter.
    Private function to be invoked by reposition_image()"""
    if flip == "horizontal":
        return np.fliplr(img)
    elif flip == "vertical":
        return np.flipud(img)
    elif flip == "both":
        return np.fliplr(np.flipud(img))
    return img

def _rotate_image(img, rotate):
    """Rotates the image based on the specified rotate parameter.
    Private function to be invoked by reposition_image()"""
    if rotate == "left":
        return np.rot90(img, k=1)
    elif rotate == "right":
        return np.rot90(img, k=-1)
    elif rotate == "down":
        return np.rot90(img, k=2)
    return img

def _shift_image_x(img, shift_x):
    """Shifts the image along the x-axis.
    Private function to be invoked by reposition_image()"""
    return np.roll(img, shift_x, axis=1)

def _shift_image_y(img, shift_y):
    """Shifts the image along the y-axis.
    Private function to be invoked by reposition_image()"""
    return np.roll(img, shift_y, axis=0)


def reposition_image(img, flip='none', rotate='up', shift_x=0, shift_y=0):
    """
    Flip, rotate, and shift an image based on the specified requested action.

    This function allows repositioning of an image by applying one or more transformations 
    (flipping, rotating, and shifting). Each transformation can be controlled by the respective 
    parameters.

    Parameters
    ----------
    img : numpy.ndarray
        The input image as a 2D numpy array (grayscale) or 3D numpy array (RGB).
    flip : str, optional
        Argument used to flip the image. It can be
        - 'none': No flipping.
        - 'horizontal': Flip the image horizontally.
        - 'vertical': Flip the image vertically.
        - 'both': Flip the image both horizontally and vertically.
        Default is 'none'.
    rotate : str, optional
        Argument used to rotate the image. It can be
        - 'up': No rotation.
        - 'left': Rotate the image 90 degrees counter-clockwise.
        - 'right': Rotate the image 90 degrees clockwise.
        - 'down': Rotate the image 180 degrees (flip upside down).
        Default is 'up'.
    shift_x : int, optional
        Argument used to shift the image along the x-axis. Default is 0.
    shift_y : int, optional
        Argument used to shift the image along the y-axis. Default is 0.

    Returns
    -------
    numpy.ndarray
        The repositioned image that has been flipped, rotated, and/or shifted based on the 
        parameter values.

    Raises
    ------
    ValueError
        - If the input image is not a 2D or 3D numpy array.
        - or if the `flip` or `rotate` arguments are invalid.
    
    TypeError
        If `shift_x` or `shift_y` is not an integer.

    Warnings
    --------
    UserWarning
        - If the shift values are larger than the image dimensions.
        - If resizing causes unexpected behavior due to large shifts.

    Examples
    --------
    >>> img = np.random.rand(100, 100)
    >>> repositioned_img = reposition_image(img, flip='horizontal', rotate='left', shift_x=10, shift_y=20)

    For an RGB image:
    >>> img_rgb = np.random.rand(100, 100, 3)
    >>> repositioned_img = reposition_image(img_rgb, flip='both', rotate='down', shift_x=-5, shift_y=10)
    """
    # Input validation
    Utility._input_checker(img)

    # Validate parameters
    valid_flips = ["none", "horizontal", "vertical", "both"]
    if flip not in valid_flips:
        raise ValueError("flip must be one of 'none', 'horizontal', 'vertical', or 'both'.")

    valid_rotations = ["up", "left", "right", "down"]
    if rotate not in valid_rotations:
        raise ValueError("rotate must be one of 'up', 'left', 'right', or 'down'.")

    if not isinstance(shift_x, int):
        raise TypeError("shift_x must be an integer.")
    if not isinstance(shift_y, int):
        raise TypeError("shift_y must be an integer.")

    # Check image dimensions
    if len(img.shape) == 2:
        img_height, img_width = img.shape
    else:
        img_height, img_width, _ = img.shape

    # Issue warnings for large shifts
    if shift_x >= img_width or shift_y >= img_height:
        warnings.warn(f"Shift values ({shift_x}, {shift_y}) are larger than the image dimensions.", UserWarning)

    # Apply transformations
    img = _flip_image(img, flip)
    img = _rotate_image(img, rotate)
    img = _shift_image_x(img, shift_x)
    img = _shift_image_y(img, shift_y)

    return img





