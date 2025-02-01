[![Documentation Status](https://readthedocs.org/projects/imagenie/badge/?version=latest)](https://imagenie.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/github/UBC-MDS/ImaGenie/graph/badge.svg?token=Dd6MnDTOH7)](https://codecov.io/github/UBC-MDS/ImaGenie)
# ImaGenie

ImaGenie is a Python package for image augmentation and modification, providing a variety of functions to manipulate images for machine learning, computer vision, or creative purposes. Whether you need to flip, scale, convert to grayscale, or blur images, ImaGenie is your one-stop solution for fast and efficient image manipulation.

## Features

* `flip(image, direction=0)`: Flips the input image either horizontally or vertically. Useful for augmenting datasets by introducing mirror-image variations. `0` = horizontal flip, `1` = vertical flip 
* `scale(image, N)`: Resizes the input image by a given scale factor `N`. This is crucial for normalizing or creating variations in image resolution.
* `blur(image, stdev=1.0)`: Applies a Gaussian blur effect to the image. Helps simulate real-world noise or reduce sharpness for specific use cases.
* `greyscale(image)`: Converts the image to grayscale. Ideal for models that only require intensity information, excluding color features.
* `augment(image)`: Applies a sequence of user-defined augmentation operations to a list of images. Useful for image generating images for computer vision tasks.

## Installation
To install from pypi:
```bash
$ pip install imagenie
```


## Python Ecosystem Integration

ImaGenie fits well within the Python ecosystem by providing functionality for image manipulation and augmentation. There are several popular libraries for image processing, that offer more complex functionalities, but this package provides a simple, user-friendly interface for common operations tailored for specific image manipulation tasks. 

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

