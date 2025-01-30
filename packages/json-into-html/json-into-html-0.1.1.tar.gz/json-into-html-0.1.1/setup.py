import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json-into-html",
    version="0.1.1",
    author="Master Shayan",
    author_email="mastershayan@proton.me",
    description="json2html is a Python library that fetches data from APIs, allows users to define the structure of the JSON response, and generates responsive HTML pages to display the data in a user-friendly format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mastershayan/json-into-html",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)