from setuptools import setup, find_packages

setup(
    name="axonml",
    version="0.1.1",
    author="Akshaya Ramesh Nagarajan",
    author_email="akshayaramesh03@gmail.com",
    description="A lightweight machine learning library implementing fundamental ML algorithms",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)