import numpy as np

def grayscale(image):
    """
    Converts an image to grayscale.

    Parameters:
    ----------
    image : np.ndarray
        The input image, represented as a NumPy array. It can be a 3D array (RGB) or a 2D array (already grayscale).

    Returns:
    -------
    np.ndarray
        The grayscale image as a 2D NumPy array (dtype=uint8).

    Raises:
    ------
    TypeError
        If the input is not a NumPy array.
    ValueError
        If the input is not a 2D or 3D NumPy array, or if the 3D array does not have 3 channels.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError("The input image must be a NumPy array.")
    if image.ndim == 2:
        return image
    elif image.ndim == 3:
        if image.shape[-1] != 3:
            raise ValueError("The input image must have 3 channels in the last dimension for RGB.")
        # Convert to grayscale with rounding and cast to uint8
        return np.round(np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])).astype(np.uint8)
    else:
        raise ValueError("The input image must be a 2D or 3D NumPy array.")

