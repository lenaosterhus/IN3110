# Assignment 4

This assignment was solved using macOS.

# 4.1 & 4.2 Python for Instagram

The `instapy` package contains two subpackages, `grayscale` and `sepia`. In each of these packages you will find three modules for a python-, numba- and numpy-implementation - each containing two functions: 
1. `grayscale_filter()` / `sepia_filter()` saving the converted image
2. A function for the conversion

All six reports can be found in the `reports` folder.

# 4.3 Package: instapy

The 'instapy'-package contains one main module: `filters.py`

`filters.py` contain two functions:
1. `grayscale_image(input_filename, output_filename=None, implementation="numpy", scale=1.0)`
2. `sepia_image(input_filename, output_filename=None, implementation="numpy", scale=1.0)`

The sub-packages are described above.
The `setup.py` file is found in this main directory.

# 4.4 User interface

The script (instapy) for the user interface is in the `bin` folder.

## Installation

To install the package/script for system wide use, call the following in the `assignment4` directory containing the project, using the package manager pip3:
```bash
pip3 install . --user  # For single-user installation. "."=path
pip3 install .         # For system wide installation (requires root)
```
The package/script can now be used system wide.

## Usage examples

```bash
instapy -h  # Will display a helpful message showing flags and usage of instapy
instapy -f FILE_IN -o FILE_OUT -g  # Will save a grayscale version of FILE_IN as FILE_OUT
```

## Testing

To test the package, call the following in the directory containing the project:

```bash
py.test
```

## Dependencies
### OpenCV
Version: 4.4.0.42. OpenCV can be installed using **pip**
```bash
pip install opencv-python
```
### NumPy
Version: 1.18.5. NumPy is a standard package that can be installed via **conda**
```bash
conda install numpy
```
https://numpy.org/install/

### pytest
Version: 6.0.1. Pytest can be installed using **pip**
```bash
pip install -U pytest
```

### setuptools
Version: 50.3.0. Setuptools can be installed using **pip**
```bash
pip install setuptools
```

### Numba
Version: 0.50.1. Numba can be installed using **pip**
```bash
pip install numba
```