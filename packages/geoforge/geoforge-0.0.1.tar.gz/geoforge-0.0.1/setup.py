from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geoforge",
    version="0.0.1",
    author="Samapriya Roy",
    author_email="samapriya.roy@gmail.com",
    description="A comprehensive toolkit for geospatial data processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/geoforge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.1.8",
        "rasterio>=1.3.9",
        "tqdm>=4.67.1",
    ],
    entry_points={
        "console_scripts": [
            "geoforge=geoforge.geoforge:cli",
        ],
    },
)
