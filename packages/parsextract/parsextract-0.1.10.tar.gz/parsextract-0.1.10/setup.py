from setuptools import setup, find_packages
import pathlib

# Read the README.md file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="parsextract",
    version="0.1.10",
    packages=find_packages(),
    install_requires=[],
    author="Deepak Kumar",
    author_email="deepak.kumar@cyware.com",
    description="A library to extract IPs, domains, and emails from text",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/deepakkumar/parsextract",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
