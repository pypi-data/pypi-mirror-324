from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dylanswordsegmenter",
    version="0.1.2",
    description="A tool for segmenting concatenated words into valid words.",
    long_description=long_description,  # Add this line
    long_description_content_type="text/markdown",  # Specify the format
    author="Dylan Denney",
    author_email="dylandenney@gmail.com",
    packages=find_packages(),
    install_requires=["nltk"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    url="https://github.com/dylandenney/wordsegmenter.git",
)

