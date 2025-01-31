from setuptools import setup, find_packages

setup(
    name="valdemarcord",
    version="0.0.7",
    packages=find_packages(),
    description="discord  module",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="valdemarkid",
    install_requires=[
        'requests>=2.25.1',
        'orjson>=3.9.10',
        'beautifulsoup4>=4.12.0',
        'colorama>=0.4.6',
    ],
    python_requires=">=3.6",
)