# setup.py
from setuptools import setup, find_packages

setup(
    name="enccomslice",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "websockets",  # Required for WebSocket functionality
    ],
    description="A simple library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="soniya",
    author_email="prathpatil28@gmail.com",
    url="https://github.com/prathaaccount/enccomslice",  # Link to your GitHub or website
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
