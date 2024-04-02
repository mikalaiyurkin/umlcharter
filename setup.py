import setuptools
import re

with open("README.md", "rt") as f:
    long_description = f.read()

with open("charter/metadata.py", "rt") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

setuptools.setup(
    name="charter",
    version=version,
    author="Mikalai Yurkin",
    author_email="yurkin.mikalai@gmail.com",
    description="Python package for quick diagrams creation without a need to learn new DSL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikalaiyurkin/charter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
    ]
)
