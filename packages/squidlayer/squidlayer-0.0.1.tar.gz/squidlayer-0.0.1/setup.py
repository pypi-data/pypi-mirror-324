from setuptools import setup, find_packages

setup(
    name="squidlayer",
    version="0.0.1",
    author="Andrei Paulavets",
    author_email="nadrewss@gmail.com",
    description="Intelligent layer for AI and data processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/squidlayer/squidlayer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)