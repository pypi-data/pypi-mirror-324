import numpy as np
import matplotlib.pyplot as plt
import cv2
import warnings


def scale(image, N = None):
    """
    Scale an image file by a factor of N.

    Parameters
    ----------
    image : np.ndarray
        The input image to be scaled. Must be a NumPy array.
    
    N: float
        An positive float specifying the scaling factor.

    Returns
    -------
    np.ndarray
        The scaled image that is represented as np array.

    Examples
    --------
    Scale the image 2 times larger. 
    >>> img = scale(image, 2)
    """
    if N is not None:
        if not isinstance(N, (int, float)):
            raise TypeError("Scaling factor must be a numeric value (int or float).")
        if N <= 0:
            raise ValueError("Scaling factor must be a positive number.")
    # Calculate new size. If N is None, return original image numpy array
    else:
        return image
    
    
    if not isinstance(image, np.ndarray):
        raise TypeError("Image must be a numpy array")
    
    #Warn if the original image exceeds 1028 * 1028
    if image.shape[0] > 1028 or image.shape[1] > 1028:
        warnings.warn("The input image exceeds the maximum size of 1028x1028.")

    # Resize the image
    scaled_img = cv2.resize(image, (0, 0), fx = N, fy = N)
    
    #Warn if the scaled impage exceeds 1028 * 1028
    if scaled_img.shape[0] > 1028 or scaled_img.shape[1] > 1028:
        warnings.warn("The scaled image exceeds the maximum size of 1028x1028 and need resizing.")
     
    else:
        return scaled_img

