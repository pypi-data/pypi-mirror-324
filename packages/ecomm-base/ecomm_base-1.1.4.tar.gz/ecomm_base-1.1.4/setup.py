from setuptools import setup, find_packages

with open   ("README.md", "r") as f:
    description = f.read()

setup(
    name="ecomm_base",  # Name of package
    version="1.1.4",  # Initial version
    author="Novacept",
    author_email="mahesh.chavan@novacept.io",
    # password="Novacept@2025",
    description="This package contains base code for all services e.g. Query DTO and Model Enums",
    packages=find_packages(),  # Automatically find the `ecomm_base` directory
    # install_requires=[],  # Add dependencies if any
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
