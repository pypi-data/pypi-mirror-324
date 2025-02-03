[![Documentation Status](https://readthedocs.org/projects/imagenie/badge/?version=latest)](https://imagenie.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/github/UBC-MDS/ImaGenie/graph/badge.svg?token=Dd6MnDTOH7)](https://codecov.io/github/UBC-MDS/ImaGenie)
![Python version](https://img.shields.io/pypi/pyversions/ImaGenie)
![Last commit](https://img.shields.io/github/last-commit/UBC-MDS/ImaGenie)


# ImaGenie

`imagenie` is a Python package for image augmentation and modification, providing a variety of functions to manipulate images for machine learning, computer vision, or creative purposes. Whether you need to flip, scale, convert to grayscale, or blur images, `imagenie` is your one-stop solution for fast and efficient image manipulation.

## Features

* Flipping: `flip(image, direction=0)`
    flips the input image either horizontally or vertically. Useful for augmenting datasets by introducing mirror-image variations. `0` = horizontal flip, `1` = vertical flip 

* Scaling: `scale(image, N)`
    resizes the input image by a given scale factor `N`. This is crucial for normalizing or creating variations in image resolution.

* Blurring: `blur(image, stdev=1.0)`
    applies a Gaussian blur effect to the image. Helps simulate real-world noise or reduce sharpness for specific use cases.

* Grayscaling: `grayscale(image)`
    converts the image to grayscale. Ideal for models that only require intensity information, excluding color features.

* Augmenting with a sequence of operations: `augment(images, operations)`
    applies a sequence of user-defined augmentation operations to a list of images. Useful for image generating images for computer vision tasks.

## Installation
To install from pypi:
```bash
$ pip install imagenie
```


To build from the github repo follow the following steps:
Clone the repository using the following command :

```bash
$ git clone https://github.com/UBC-MDS/ImaGenie.git
```
then navigate to the repository by running the following command 

```bash
$ cd ImaGenie
```
Then run the following command:
```bash
$ poetry install
```

## Running Test Suite
In the package directory run the following command to run the test suit for this package:
```bash
$ pytest
```

## Usage
A few exampls to get you started with `imagenie`:

1. Import the functions from the package

    ```
    from imagenie.flip import flip
    from imagenie.scale import scale
    from imagenie.blur import blur
    from imagenie.grayscale import grayscale
    from imagenie.augment import augment
    ```

2. Load the images as Numpy arrays

    ```
    import matplotlib.pyplot as plt
    image = plt.imread(IMAGE_PATH)
    image2 = plt.imread(IMAGE_PATH)
    ```

3. Leverage `imagenie`'s image modification functions

    - Flip image horizontally or vertically
    ```
    flipped_image = flip(image, direction = 1)
    ```

    - Scale image by a desired scaling factor
    ```
    scaled_image = scale(image, N = 0.4)
    ```

    - Blur image with a defined standard deviation
    ```
    blurred_image = blur(image, stdev = 2.0)
    ```

    - Convert RGB to grayscaled images
    ```
    grayed_image = grayscale(image)
    ```


## Python Ecosystem Integration

This package fits well within the Python ecosystem by providing functionality for image manipulation and augmentation. There are several popular libraries for image processing, that offer more complex functionalities, but this package provides a simple, user-friendly interface for common operations tailored for specific image manipulation tasks. 

Reference for other image processing libraries:
- PIL (Python Imaging Library): [PIL](https://python-pillow.org/)
- OpenCV: [OpenCV](https://opencv.org/)
- Augmentor: [Augmentor](https://github.com/mdbloice/Augmentor)

## Contributors

- Agam Sanghera
- Gurmehak Kaur
- Yuhan Fan
- Yichun Liu

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`imagenie` was created by Agam Sanghera, Gurmehak Kaur, Yuhan Fan, Yichun Liu. It is licensed under the terms of the MIT license.

## Credits

`imagenie` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

