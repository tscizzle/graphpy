# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='graphpy',
    version='0.0.6',
    description='A Python implementation of a edges, vertices, and graphs',
    long_description=long_description,
    url='https://github.com/tscizzle/graphpy',
    author='Tyler Singer-Clark',
    author_email='tscizzle@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
    ],
    keywords='edge vertex graph',
    packages=find_packages(),
    install_requires=[],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
