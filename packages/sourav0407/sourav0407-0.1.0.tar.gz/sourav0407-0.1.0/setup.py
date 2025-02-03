from setuptools import setup, find_packages

setup(
    name="sourav0407",
    version="0.1.0",
    author="souravroy0407",
    description="A simple package with a hello function",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
