from setuptools import setup, find_packages
import os
from pathlib import Path

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="video-analyzer",
    version="0.1.0",
    author="Wahyu Bornok Augus Sinurat",
    author_email="bornouksyn@beaverhand.com",
    description="A tool for analyzing videos using Vision models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="video_analyzer"),
    package_dir={"": "video_analyzer"},
    install_requires=requirements,
    python_requires=">=3.11",
    include_package_data=True,
)