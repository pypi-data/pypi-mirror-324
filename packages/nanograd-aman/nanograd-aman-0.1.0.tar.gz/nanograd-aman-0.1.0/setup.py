from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nanograd-aman",
    version="0.1.0",
    author="Aman Anand",
    author_email="coursesxyz403@gmail.com",
    description="A lightweight backpropagation package for neural networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeuralNoble/nanograd",
    packages=find_packages(),  # This will find all the sub-packages automatically
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=[  # List of dependencies
        "numpy",
        "graphviz",
    ],
)
