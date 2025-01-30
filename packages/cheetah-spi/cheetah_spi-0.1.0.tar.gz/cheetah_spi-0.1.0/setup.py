# setup.py
import platform
from setuptools import setup, find_packages

# Decide which extension name to include:
ext = '.dll' if platform.system() == 'Windows' else '.so'

setup(
    name='cheetah_spi',  # The name of your Python package/distribution
    version='0.1.0',
    description='Cheetah wrapper functions (pre-compiled shared library)',
    packages=find_packages(),
    include_package_data=True,  # Tells setuptools to include package_data
    package_data={
        'cheetah_spi': [f'cheetah{ext}'],  # Include the DLL/so file in the package
    },
)