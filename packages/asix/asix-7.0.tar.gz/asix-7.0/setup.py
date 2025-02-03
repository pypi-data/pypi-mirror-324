from setuptools import setup, find_packages

setup(
    name="asix",            # A neutral name for the library
    version="7.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.1.0"
    ],
    author="Coataoc",
    author_email="coataoctrader@gmail.com",
    description="A collection of utilities for Pygame",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CoataocCreate/ASIX",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
