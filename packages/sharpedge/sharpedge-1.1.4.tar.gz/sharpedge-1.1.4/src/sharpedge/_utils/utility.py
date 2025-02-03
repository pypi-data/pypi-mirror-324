import numpy as np


class Utility:
    """
    This module contains utility classes and functions for internal use only.

    Validate that all color values in the image are integers and within the
    correct range (0 to 255). If the image contains any float values or
    out-of-range values, it will raise a ValueError.

    Parameters
    ----------
    image : numpy.ndarray
        The image array to validate (can be RGB or Grayscale).

    Raises
    ------
    ValueError
        If any value in the image is invalid (float or out-of-range).
    """
    @staticmethod
    def _input_checker(img_array):
        """
        Validate the input image array for proper format, shape, and value range.

        This function checks if the input image array meets the following conditions:
        - It is a NumPy array.
        - It is either a 2D array (grayscale) or a 3D array with three channels (RGB).
        - It is non-empty and has no zero-sized dimensions.
        - It has an integer data type.
        - All values in the array are within the range [0, 255].

        Parameters
        ----------
        img_array : numpy.ndarray
            The image array to validate.

        Returns
        -------
        bool
            Returns True if all validation checks pass.

        Raises
        ------
        TypeError
            If the input is not a NumPy array or does not have an integer data type.
        ValueError
            If the input array is not 2D or 3D with three channels, is empty, has zero-sized dimensions, 
            or contains values outside the range [0, 255].
        """
        # Check the image array format: must be a numpy array
        if not isinstance(img_array, np.ndarray):
            raise TypeError("Image format must be a numpy array.")
        # Check input image array shape
        if not (img_array.ndim == 2 or (img_array.ndim == 3 and img_array.shape[2] == 3)):
            raise ValueError("Image array must be 2D or 3D.")
        # Check if the array is empty or contains zero-sized dimensions
        if img_array.size == 0 or any(dim == 0 for dim in img_array.shape):
            raise ValueError("Image size must not be zero in any dimension.")
        # Check if the data type is integer
        if not np.issubdtype(img_array.dtype, np.integer):
            raise TypeError(f"Image array must have integer data type.")
        # Check if any values are out of range (0 to 255)
        if np.any(img_array < 0) or np.any(img_array > 255):
            raise ValueError("Color values must be integers between 0 and 255.")
        # If all checks pass, return True
        return True
