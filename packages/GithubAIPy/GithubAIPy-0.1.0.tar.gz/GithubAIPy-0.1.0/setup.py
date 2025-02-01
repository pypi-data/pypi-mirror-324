from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="GithubAIPy",
    version="0.1.0",
    author="Ramona-Flower",
    description="A Python package to interact with GitHub AI models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ramona-Flower/GithubAIPy",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)