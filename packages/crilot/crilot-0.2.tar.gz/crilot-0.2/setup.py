from setuptools import setup, find_packages

setup(
    name="crilot",
    version="0.2",
    author="Axmadjon Qaxxorov",
    description="A Python library to convert Krill text to Latin and vice versa.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://youtube.com/@axmadjonqaxxorovc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
