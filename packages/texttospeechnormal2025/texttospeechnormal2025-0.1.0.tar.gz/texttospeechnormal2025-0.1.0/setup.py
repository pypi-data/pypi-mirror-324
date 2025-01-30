from setuptools import setup, find_packages

setup(
    name="texttospeechnormal2025",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for text normalization in speech processing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/texttospeechnormal2025",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
