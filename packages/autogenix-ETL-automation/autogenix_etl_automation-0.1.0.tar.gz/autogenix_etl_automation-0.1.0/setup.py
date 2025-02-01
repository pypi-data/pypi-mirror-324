from setuptools import setup, find_packages

setup(
    name="autogenix-ETL-automation",
    version="0.1.0",
    author="Rishikeswaran S",
    author_email="rishikeswaran17@gmail.com",
    description="A package for automating ETL processes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autogenix-ETL-automation",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
    ],
)
