from setuptools import setup, find_packages

setup(
    name="thoran_houdini_utils",  # Name of your module
    version="0.2.1",  # Version of your module
    description="A simple greeting module",
    author="Thoran Slock",
    author_email="thoranslock@hotmail.com",
    packages=find_packages(),  # Automatically finds the subpackages in your module
    install_requires=[],  # Add any dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)