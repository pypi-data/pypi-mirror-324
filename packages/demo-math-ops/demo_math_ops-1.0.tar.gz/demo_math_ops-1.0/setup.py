# setup.py
from setuptools import setup, find_packages

setup(
    name="demo_math_ops", 
    version="1.0",        
    packages=find_packages(),  # Automatically discover the modules in all_math_ops/
    author="Raghu",
    author_email="raghu@abc.com",
    description="A demo package for math operations",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # Adjust based on your Python version
)
