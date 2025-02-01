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
    version='1.0.11',
    packages=find_packages(),
    ext_modules=[nchess_module],
    include_package_data=True,
    package_data={
        'NChess.core': ['*.pyd', '*.so'],
    },
    install_requires=['numpy>=1.18.0'],
    author='MNMoslem',
    author_email='normoslem256@gmail.com',
    description='chess library written in c',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MNourMoslem/NChess',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

# create new file called .so
this_dir = '.'
pyd_file = [os.path.join(this_dir, f) for f in os.listdir(this_dir) if f.endswith('.pyd')][0]

so_core_file = pyd_file.replace('.pyd', '.so')
so_core_file = os.path.join(core_dir, os.path.basename(so_core_file))
pyd_core_file = os.path.join(core_dir, os.path.basename(pyd_file))

with open(pyd_file, 'rb') as f:
    with open(so_core_file, 'wb') as new_f:
        new_f.write(f.read())

    with open(pyd_core_file, 'wb') as new_f:
        new_f.write(f.read())