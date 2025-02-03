from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pyModManager",
    version="0.1.1",
    description="A Python package that simplifies import management.",
    long_description=long_description,  # <== Add this line
    long_description_content_type="text/markdown",  # <== Add this line
    author="Syed Sadiq",
    author_email="syedsadiq201415@gmail.com",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
)