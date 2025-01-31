from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="walmart-access-token-manager",
    version="0.1.3",
    author="ThinkBig Products",
    author_email="your.email@example.com",
    description="A package for managing Walmart Marketplace API access tokens",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThinkBig-Products/walmart_access_token_manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "boto3",
        "requests",
        "pycryptodome",
        "mysql-connector-python",
    ],
)