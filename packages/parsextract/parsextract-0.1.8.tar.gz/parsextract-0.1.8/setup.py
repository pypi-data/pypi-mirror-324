from setuptools import setup, find_packages

setup(
    name="parsextract",
    version="0.1.8",
    packages=find_packages(),
    install_requires=[],
    author="Deepak Kumar",
    author_email="deepak.kumar@cyware.com",
    description="A library to extract IPs, domains, and emails from text",
    url="https://github.com/deepakkumar/parsextract",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
