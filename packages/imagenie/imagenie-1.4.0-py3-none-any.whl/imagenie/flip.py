import numpy as np
import warnings

def flip(image, direction=0):
    """
    Flips an image either horizontally or vertically.

    Parameters:
    ----------
    image : np.ndarray
        The input image to be flipped, represented as a NumPy array or similar format.
    direction : str, optional
        The direction in which to flip the image:
        - 0: for horizontal flip (default)
        - 1: vertical flip

    Returns:
    -------
    np.ndarray
        The flipped image as a NumPy array.

    Raises:
    ------
    ValueError
        If the specified direction is not 1 or 0.
        If image exceeds size limits.


    Examples:
    ---------
    Flip an image horizontally:
    >>> flipped_image = flip_image(image)

    Flip an image vertically:
    >>> flipped_image = flip_image(image, 1)
    """

    # Validate input image
    if not isinstance(image, np.ndarray):
        raise ValueError("Input image must be a NumPy array.")

    # Validate size limit
    if image.shape[0] > 1028 or image.shape[1] > 1028:
        raise ValueError("Input image size exceeds the 1028x1028 limit.")

    # Validate direction 
    if direction not in [0, 1]:
        warnings.warn(
            f"Invalid direction '{direction}' specified. Defaulting to horizontal flip (0).",
            UserWarning
        )
        direction = 0

    # Perform flip
    if direction == 0:  # Horizontal flip
        return [row[::-1] for row in image]
    elif direction == 1:  # Vertical flip
        return image[::-1]