from setuptools import setup, find_packages

setup(
    name="duckducksearch",
    version="0.1.0",
    description="A Python library for searching using DuckDuckGo.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Sergei Belousov aka bes-dev",
    author_email="sergei.o.belousov@gmail.com",
    url="https://github.com/bes-dev/duckducksearch",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "duckduckgo_search>=7.3.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
