# setup.py
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llmtricks",
    version="0.0.2",
    author="Delip Rao",
    author_email="none@none.com",
    description="A package for LLM tricks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/delip/llmtricks",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
