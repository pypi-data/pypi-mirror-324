# setup.py
from setuptools import setup, find_packages

with open("README.md","r") as f:
    description = f.read()

setup(
    name="scdhelper",
    version="0.1.1",
    description="A Python package for handling Slowly Changing Dimension",
    author="Krishnanand A",
    author_email="krishnanand654@gmail.com",
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=description,
    long_description_content_type="text/markdown",
)
