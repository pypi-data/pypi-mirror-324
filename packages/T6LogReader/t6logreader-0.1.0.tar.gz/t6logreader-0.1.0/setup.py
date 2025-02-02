from setuptools import setup, find_packages

setup(
    name="T6LogReader",
    version="0.1.0",
    author="budiworld",
    author_email="budi.world@yahoo.com",
    description="A Python module for reading and searching Plutonium T6 logs",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Yallamaztar/T6LogReader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
