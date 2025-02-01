from setuptools import setup, find_packages, Extension
import numpy
import os
import sys
from setuptools.command.build_ext import build_ext

core_dir = os.path.join("NChess", "core")
build_path = core_dir

def find_c_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.c')]

nchess_module = Extension(
    'nchess',
    sources=[*find_c_files(f'{core_dir}/src'), *find_c_files(core_dir)],
    include_dirs=[
        'src',
        numpy.get_include(),
    ],
)

setup(
    name='NChess',
    version='1.0.17',
    packages=find_packages(),
    ext_modules=[
        nchess_module
    ],
    include_package_data=True,
)