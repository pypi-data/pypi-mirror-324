from setuptools import setup, find_packages
import os

# Read the README for a long description (ensure you have a README.md in your project root)
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="SyntaxMatrix",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="SyntaxMUI: A customizable UI framework for Python Retrieval-Augmented Generation projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/SyntaxMatrix",  # Replace with your repository URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.0",
        "openai",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or your chosen license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
