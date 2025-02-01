from setuptools import setup, find_packages

setup(
    name="csv_optimizer",
    version="0.20",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0"
    ],
    author="Tim Müller",
    author_email="timmueller0@gmail.com",
    description="A Python package for efficiently loading CSV files with optimized data types.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/timmueller0/csv_optimizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
