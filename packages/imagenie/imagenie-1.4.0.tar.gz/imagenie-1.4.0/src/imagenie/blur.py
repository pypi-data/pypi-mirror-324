import numpy as np
def blur(image, stdev=1.0):
    """Add noise to image using a Gaussian filter.

    Parameters
    ----------
    image : np.ndarray
        The input image to be blurred, represented as a NumPy array\n 
        or similar format.
    
    stdev : Float 
        Standard deviation for Gaussian/Normal distribution used to\n
        calculate the value of image pixels after filtering.
        Default is 1.0 for Standard Normal Distribution.

    Returns
    -------
    np.ndarray
        The blurred image as a NumPy array.

    Examples
    --------
    >>> print(image)
        [0.10196079, 0.627451  , 0.74509805],
        [0.11372549, 0.6666667 , 0.78431374],
        [0.1254902 , 0.7058824 , 0.81960785]
    >>> blur(image)
        [0.2991612 , 0.5070358 , 0.66973376],
        [0.30862695, 0.52062243, 0.6859944 ],
        [0.31771535, 0.53367144, 0.70153326]
    >>> print(image2)
        [0.09803922, 0.5882353 , 0.70980394],
        [0.1254902 , 0.70980394, 0.8235294 ],
        [0.1254902 , 0.70980394, 0.8235294 ]
    >>> blur(image2,stdev=2)
        [0.49137527, 0.5290323 , 0.56662756],
        [0.49490717, 0.53276986, 0.5705702 ],
        [0.4977027 , 0.5357282 , 0.5736908 ]
    """
    if stdev is not None:
        if not isinstance(stdev, (int, float)):
            raise TypeError("Standard deviation must be a numeric value (int or float).")
        if stdev <= 0:
            raise ValueError("Standard deviation must be a positive number.")
    
    if not isinstance(image, np.ndarray):
        raise TypeError("Image must be a numpy array")
    
    #Warn if the original image exceeds 1028 * 1028
    if image.shape[0] > 1028 or image.shape[1] > 1028:
        raise ValueError("The input image exceeds the maximum size of 1028x1028.")
    
    filter_size = 2 * int(4 * stdev + 0.5) + 1
    gaussian_filter = np.zeros((filter_size, filter_size), np.float32)
    m = filter_size//2
    n = filter_size//2
    
    for x in range(-m, m+1):
        for y in range(-n, n+1):
            x1 = 2*np.pi*(stdev**2)
            x2 = np.exp(-(x**2 + y**2)/(2* stdev**2))
            gaussian_filter[x+m, y+n] = (1/x1)*x2
    
    im_filtered = np.zeros_like(image, dtype=np.float32)
    for c in range(3):
        #im_filtered[:, :, c] = convolution(image[:, :, c], gaussian_filter)
        kernel_h = gaussian_filter.shape[0]
        kernel_w = gaussian_filter.shape[1]
        if(len(image[:,:,c].shape) == 3):
            image_pad = np.pad(image[:,:,c], pad_width=((kernel_h // 2, kernel_h // 2),(kernel_w // 2, kernel_w // 2),(0,0)), mode='constant', constant_values=0).astype(np.float32)
        elif(len(image[:,:,c].shape) == 2):
            image_pad = np.pad(image[:,:,c], pad_width=((kernel_h // 2, kernel_h // 2),(kernel_w // 2, kernel_w // 2)), mode='constant', constant_values=0).astype(np.float32)
    
        h = kernel_h // 2
        w = kernel_w // 2
        
        image_conv = np.zeros(image_pad.shape)
        
        for i in range(h, image_pad.shape[0]-h):
            for j in range(w, image_pad.shape[1]-w):
                x = image_pad[i-h:i-h+kernel_h, j-w:j-w+kernel_w]
                x = x.flatten()*gaussian_filter.flatten()
                image_conv[i][j] = x.sum()
                
        h_end = -h
        w_end = -w
        if(h == 0):
            im_filtered[:, :, c]= image_conv[h:,w:w_end]
        if(w == 0):
            im_filtered[:, :, c]= image_conv[h:h_end,w:]

        im_filtered[:,:,c]=image_conv[h:h_end,w:w_end]

    return(im_filtered.round().astype(np.int32))