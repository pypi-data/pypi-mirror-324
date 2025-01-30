"""
Filename: setup.py
Project Name: videotoooimage
Title: Setup file for PYPI Package
Author: Raghava | Github: @raghavavidyapriya
Date Created: March 18, 2024 | Last Updated: May 14, 2023
Language: Python | Version : 3.10.14
"""

# Importing required libraries
from setuptools import setup, find_packages

# Read the content of the README file
with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

setup(
    name="videotoooimage",
    version="2024.05.14.1.0.0",
    description="Video to Image frames converter",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    url="https://github.com/raghavavidyapriya/videotoooimage",
    author="Raghava",
    author_email="raghavavidyapriya@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["opencv-python"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
