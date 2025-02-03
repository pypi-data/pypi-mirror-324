from setuptools import setup, find_packages

setup(
    name="coscheduler",
    version="0.0.1",
    author="John Torr",
    author_email="john@inephany.com",
    description="Placeholder package for coscheduler",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/coscheduler",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or your choice
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)