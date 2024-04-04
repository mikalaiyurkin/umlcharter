import setuptools
import re

with open("README.md", "rt") as f:
    long_description = f.read()

with open("umlcharter/__init__.py", "rt") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

setuptools.setup(
    name="umlcharter",
    version=version,
    author="Mikalai Yurkin",
    author_email="yurkin.mikalai@gmail.com",
    description="Python package for quick diagrams creation without a need to learn new DSL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikalaiyurkin/charter",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
    ],
)
