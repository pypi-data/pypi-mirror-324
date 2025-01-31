import os
import subprocess
from setuptools import setup, find_packages


# Function to detect the CUDA version
def get_cuda_version():
    try:
        # Run `nvcc --version` to get the CUDA version
        output = subprocess.check_output(["nvcc", "--version"], stderr=subprocess.STDOUT)
        # Extract version number using regex
        version = output.decode("utf-8").split("release ")[1].split()[0]
        return version
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


# Get the installed CUDA version
cuda_version = get_cuda_version()

# Determine the appropriate CuPy version based on CUDA
if cuda_version:
    print(f"Detected CUDA version: {cuda_version}")
    if cuda_version.startswith("12"):
        cupy_version = "cupy-cuda12x"
    elif cuda_version.startswith("11"):
        cupy_version = "cupy-cuda11x"
    elif cuda_version.startswith("10"):
        cupy_version = "cupy-cuda10x"
    else:
        print("Unknown CUDA version. Defaulting to generic CuPy (no GPU support).")
        cupy_version = "cupy"
else:
    print("CUDA not detected. Defaulting to generic CuPy (no GPU support).")
    cupy_version = "cupy"

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define the setup function
setup(
    name='pycuda_plus',
    version='0.3.1',
    description='User-friendly library to enhance PyCUDA functionality',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specifies the format of the long description
    author='Phillip Chananda',
    author_email='takuphilchan@gmail.com',
    url='https://github.com/takuphilchan/pycuda_plus',
    packages=find_packages(),
    install_requires=[
        'pycuda',
        'numpy',
        'six',
        'matplotlib',
        'seaborn',
        'pandas',
        'dash', 
        'plotly',
        cupy_version,  
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    project_urls={
        "Bug Tracker": "https://github.com/takuphilchan/pycuda_plus/issues",
        "Documentation": "https://github.com/takuphilchan/pycuda_plus#readme",
        "Source Code": "https://github.com/takuphilchan/pycuda_plus",
    },
)
