# setup.py
from setuptools import setup, find_packages

setup(
    name="scdhelper",
    version="0.1.0",
    description="A Python package for handling Slowly Changing Dimension",
    author="Krishnanand A",
    author_email="krishnanand654@gmail.com",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pyspark',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
