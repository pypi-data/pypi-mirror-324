# setup.py
from setuptools import setup, find_packages

setup(
    name="bodoTK",
    version="1.1",
    packages=find_packages(),
    install_requires=[],  # No external dependencies, since you're building from scratch
    author="Sudem S Daimari",
    author_email="ssdaimari44@gmail.com",  # Replace with your email
    description="A tokenization library for Bodo language",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tsong44/bodoTK",  # Replace with your actual GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
