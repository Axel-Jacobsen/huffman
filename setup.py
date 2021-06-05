import pathlib

from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="huffman_coding",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages("src"),
    description="very basic huffman coding",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Axel Jacobsen",
    license="BSD 3-clause",
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ],
    install_requires= [],
    entry_points={
        "console_scripts": "hc=huffman_coding.__main__:main"
    }
)
