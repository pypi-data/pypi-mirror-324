from setuptools import setup, find_packages

setup(
    name="farabi",
    version="0.3.1",
    packages=find_packages(),
    description="A very simple math operations library",
    author="Tezeghdenti Mohamed",
    author_email="mohamed.tezeghdenti@ensi-uma.tn",
    url="https://github.com/yourusername/my_simple_lib",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)