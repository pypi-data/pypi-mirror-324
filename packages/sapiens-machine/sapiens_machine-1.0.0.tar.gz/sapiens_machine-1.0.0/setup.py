"""
    ########################################################################################################################################################
    # This algorithm is part of a code library for optimizing the Artificial Intelligence models of Sapiens Technology®, and its disclosure, distribution, #
    # or reverse engineering without the company's prior consent will be subject to legal proceedings and actions pursued by our legal department.         #
    ########################################################################################################################################################
"""
from glob import glob
from os import path
from setuptools import setup, find_packages
libs = list(glob("./bitsandbytes/lib_sapiens_machine*.so"))
libs = [path.basename(lib) for lib in libs]
package_name = 'sapiens_machine'
version = '1.0.0'
setup(
    name=package_name,
    version=version,
    author='OPENSAPI',
    packages=find_packages(),
    package_data={"": libs},
    install_requires=['scipy==1.15.1'],
    url='https://github.com/',
    license='Proprietary Software'
)
"""
    ########################################################################################################################################################
    # This algorithm is part of a code library for optimizing the Artificial Intelligence models of Sapiens Technology®, and its disclosure, distribution, #
    # or reverse engineering without the company's prior consent will be subject to legal proceedings and actions pursued by our legal department.         #
    ########################################################################################################################################################
"""
