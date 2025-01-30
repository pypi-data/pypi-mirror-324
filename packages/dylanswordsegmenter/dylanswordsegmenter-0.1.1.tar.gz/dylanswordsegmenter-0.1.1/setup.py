from setuptools import setup, find_packages

setup(
    name="dylanswordsegmenter",               # Package name
    version="0.1.1",                        # Initial version
    description="A tool for segmenting concatenated words into valid words.",
    author="Dylan Denney",
    author_email="dylandenney@gmail.com",
    packages=find_packages(),               # Automatically find package directories
    install_requires=["nltk"],              # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    url="https://github.com/dylandenney/wordsegmenter.git",  # Add your GitHub repository URL here
)

