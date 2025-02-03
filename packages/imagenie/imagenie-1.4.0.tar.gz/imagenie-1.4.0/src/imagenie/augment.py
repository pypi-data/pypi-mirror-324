import numpy as np
import warnings

# Allowed functions
ALLOWED_FUNCTIONS = ['flip', 'scale', 'blur','grayscale']

def augment(images, operations):
    """
    Applies a sequence of augmentation operations to a list of images.

    Parameters:
    ----------
    images : list of np.ndarray
        A list of images (as NumPy arrays) to process.
    operations : list of tuple
        A list of operations to apply, where each operation is a tuple
        (function, *args, **kwargs).
        Example: [(flip, 1), (scale, 0.5), (blur, 5)]

    Returns:
    -------
    list of np.ndarray
        The list of augmented images.
    """
    
    augmented_images = []
    
    for image in images:
        # Validate input image
        if not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a NumPy array.")
        
        # Validate size limit
        if image.shape[0] > 1028 or image.shape[1] > 1028:
            raise ValueError("Input image size exceeds the 1028x1028 limit.")
        
        # Break down the operations into functions and their respective parameters
        for operation in operations:
            func, *params = operation
            
            # Check if function is allowed
            if func.__name__ not in ALLOWED_FUNCTIONS:
                raise ValueError(f"Function {func.__name__} is not allowed. Allowed functions are: {', '.join(ALLOWED_FUNCTIONS)}")
            
            # Apply each operation in the sequence
            image = func(image, *params)  
        
        # Append modified images in a list
        augmented_images.append(image)
    
    return augmented_images
