import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aliceCSV",
    version="1.0.1",
    author="AliceDrop",
    author_email="alice.drop.ace@icloud.com",
    description="Operating CSV files as two-dimensional table",
    py_modules=["aliceCSV"], 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alice-Drop/aliceCSV",
    packages=setuptools.find_packages(),
    install_requires=[],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)