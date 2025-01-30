from setuptools import setup, find_packages

setup(
    name="orbitalfetch",
    version="1.0.1",
    author="Hakimali",
    author_email="datardihakim440@gmail.com",
    description="A Python library for downloading high-resolution satellite imagery from Google or ESRI.",
    # Specify UTF-8 encoding when reading the README file
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "requests",
        "rasterio",
        "pillow",
        "mercantile"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
