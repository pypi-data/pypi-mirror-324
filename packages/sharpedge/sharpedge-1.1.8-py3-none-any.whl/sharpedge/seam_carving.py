import numpy as np
import warnings
from scipy.ndimage import convolve


# Reference: UBC-MDS DSCI 512 Lab 4
def _energy(img):
    """
    Computes the energy map of an image.

    This function calculates the energy of each pixel. The
    energy map highlights areas with high contrast, which
    are less likely to be removed during seam carving.
    Private function to be invoked by seam_carve().

    Parameters
    ----------
    img : numpy.ndarray
        A color image represented as a 3D numpy array of shape (height, width, 3).

    Returns
    -------
    numpy.ndarray
        A 2D array of shape (height, width) containing the energy values
        for each pixel in the original image.

    Raises
    ------
    ValueError
        If the input image is not a 3D numpy array with 3 channels.

    Examples
    --------
    >>> img = np.random.rand(8, 5, 3)
    >>> e = _energy(img)
    >>> print(e.shape)
    (8, 5)
    """
    dy = np.array([-1, 0, 1])[:, None, None]
    dx = np.array([-1, 0, 1])[None, :, None]

    # Calculate the energy map
    energy_map = convolve(img, dx)**2 + convolve(img, dy)**2

    # Sum the energy across the color channels
    return np.sum(energy_map, axis=2)


def _find_vertical_seam(energy):
    """
    Find the vertical seam of lowest total energy in the image.
    Private function to be invoked by seam_carve().

    Parameters
    ----------
    energy : numpy.ndarray
        A 2D array representing the energy of each pixel.

    Returns
    -------
    list
        A list indicating the seam of column indices.

    Raises
    ------
    ValueError
        If the energy map is not a 2D numpy array.

    Examples
    --------
    >>> e = np.array([[0.6625, 0.3939], [1.0069, 0.7383]])
    >>> seam = _find_vertical_seam(e)
    >>> print(seam)
    [1, 1]
    """
    rows, cols = energy.shape

    # Initialize cumulative energy matrix
    CME = np.zeros((rows, cols + 2))
    CME[:, 0] = np.inf
    CME[:, -1] = np.inf
    CME[:, 1:-1] = energy

    # Compute cumulative minimum energy
    for i in range(1, rows):
        prev_row = CME[i - 1]
        parents = np.vstack([
            prev_row[:-2],
            prev_row[1:-1],
            prev_row[2:]
        ])
        CME[i, 1:-1] += np.min(parents, axis=0)

    # Find seam array
    seam = np.zeros(rows, dtype=int)
    seam[-1] = np.argmin(CME[-1, 1:-1]) + 1

    for r in range(rows - 2, -1, -1):
        pos = seam[r + 1]
        offset = np.argmin(CME[r, pos - 1:pos + 2]) - 1
        seam[r] = pos + offset

    return seam - 1


def _find_horizontal_seam(energy):
    """
    Find the horizontal seam of lowest total energy
    in the image by transposing the energy map.
    Private function to be invoked by seam_carve().

    Parameters
    ----------
    energy : numpy.ndarray
        A 2D array representing the energy of each pixel.

    Returns
    -------
    list
        A list indicating the seam of row indices.

    Raises
    ------
    ValueError
        If the energy map is not a 2D numpy array.

    Examples
    --------
    >>> e = np.array([[0.6625, 0.3939], [1.0069, 0.7383]])
    >>> seam = _find_horizontal_seam(e)
    >>> print(seam)
    [0, 0]
    """
    return _find_vertical_seam(energy.T)


def _remove_vertical_seam(img, seam):
    """
    Remove a vertical seam from an image.
    Private function to be invoked by seam_carve().

    Parameters
    ----------
    img : numpy.ndarray
        A 3D array representing the original image (height, width, 3).
    seam : numpy.ndarray
        A 1D array (or list) of column indices indicating
        which pixel to remove in each row.

    Returns
    -------
    numpy.ndarray
        A new image with one less column, of shape (height, width - 1, 3).

    Raises
    ------
    ValueError
        - If the input img is not a 3D numpy array with 3 channels.
        - If the input seam is not a 1D array or a list.
        - If the length of the seam does not match the height of the image.

    Examples
    --------
    >>> img = np.random.rand(8, 5, 3)
    >>> seam = [2, 1, 3, 2, 0, 1, 4, 3]
    >>> new_img = _remove_vertical_seam(img, seam)
    >>> print(new_img.shape)
    (8, 4, 3)
    """
    # Get dimensions of the image
    height, width, num_channels = img.shape

    # Calculate linear indices of seam pixels
    linear_indices = np.array(seam) + np.arange(height) * width

    # Create output image array with one less column
    resized_image = np.zeros((height, width-1, num_channels), dtype=img.dtype)

    # Remove seam pixels and reshape the channel data
    for channel in range(num_channels):
        channel_data = np.delete(img[:, :, channel], linear_indices.astype(int))
        channel_data = np.reshape(channel_data, (height, width-1))
        resized_image[:, :, channel] = channel_data

    return resized_image


def _remove_horizontal_seam(img, seam):
    """
    Remove a horizontal seam from an image.
    Private function to be invoked by seam_carve().

    Parameters
    ----------
    img : numpy.ndarray
        A 3D array representing the original image (height, width, 3).
    seam : numpy.ndarray
        A 1D array (or list) of row indices indicating
        which pixel to remove in each column.

    Returns
    -------
    numpy.ndarray
        A new image with one less row, of shape (height - 1, width, 3).

    Raises
    ------
    ValueError
        - If the input img is not a 3D numpy array with 3 channels.
        - If the input seam is not a 1D array or a list.
        - If the length of the seam does not match the width of the image.

    Examples
    --------
    >>> img = np.random.rand(5, 8, 3)
    >>> seam = [2, 1, 3, 2, 0, 1, 4, 3]
    >>> new_img = _remove_horizontal_seam(img, seam)
    >>> print(new_img.shape)
    (4, 8, 3)
    """
    return np.transpose(_remove_vertical_seam(np.transpose(img, (1, 0, 2)), seam), (1, 0, 2))


def seam_carve(img, target_height, target_width):
    """
    Seam carve an image to resize it to the target dimensions.

    Parameters
    ----------
    img : numpy.ndarray
        A 3D array representing the original image (height, width, 3).
    target_height : int
        The desired height of the resized image.
    target_width : int
        The desired width of the resized image.

    Returns
    -------
    numpy.ndarray
        The resized image with dimensions (target_height, target_width, 3).

    Raises
    ------
    ValueError
        - If the input img is not a 3D numpy array with 3 channels.
        - If target_height or target_width is not an integer.
        - If target_height is greater than the original height or less than 1.
        - If target_width is greater than the original width or less than 1.

    Warnings
    --------
    UserWarning
        - If the target size is the same as the original size (no resizing needed).
        - If only one dimension is resized (height or width remains the same).
        - If the original image or target size is reduced to a single pixel.
        - If the resizing is significant (difference of 200+ pixels), which may cause long processing times.

    Examples
    --------
    >>> img = np.random.rand(5, 5, 3)
    >>> resized_img = seam_carve(img, 3, 3)
    >>> print(resized_img.shape)
    (3, 3, 3)
    """
    # Validate input image format: must be a numpy array
    if not isinstance(img, np.ndarray):
        raise TypeError("Image format must be a numpy array.")

    # Check if the array is empty or contains zero-sized dimensions
    if img.size == 0 or any(dim == 0 for dim in img.shape):
        raise ValueError("Image size must not be zero in any dimension.")

    # Validate input image dimensions
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("Input image must be a 3D numpy array with 3 channels.")

    # Validate target dimensions
    if not isinstance(target_height, int) or not isinstance(target_width, int):
        raise ValueError("Target dimensions must be integers.")

    height, width = img.shape[:2]

    # Check if target dimensions are valid
    if target_height > height:
        raise ValueError("Target height cannot be greater than original height.")
    if target_width > width:
        raise ValueError("Target width cannot be greater than original width.")
    if target_height < 1:
        raise ValueError("Target height must be at least 1.")
    if target_width < 1:
        raise ValueError("Target width must be at least 1.")

    # Check for edge cases using pytest warnings
    if target_height == height and target_width == width:
        warnings.warn("Both target height and width are the same as that of the original image. No resizing needed.", UserWarning)
    elif target_height == height:
        warnings.warn("Target height is the same as the original height.", UserWarning)
    elif target_width == width:
        warnings.warn("Target width is the same as the original width.", UserWarning)
    if target_height == 1 and target_width == 1:
        warnings.warn("Warning! Resizing to a single pixel.", UserWarning)
    if (height - target_height) >= 200 or (width - target_width) >= 200:
        warnings.warn("Significant resizing is required. It may take a long while.", UserWarning)

    result = img.copy()

    # Remove vertical seams until desired width is reached
    while width > target_width:
        energy_map = _energy(result)
        seam = _find_vertical_seam(energy_map)
        result = _remove_vertical_seam(result, seam)
        width = result.shape[1]

    # Remove horizontal seams until desired height is reached  
    while height > target_height:
        energy_map = _energy(result)
        seam = _find_horizontal_seam(energy_map)
        result = _remove_horizontal_seam(result, seam)
        height = result.shape[0]

    return result
