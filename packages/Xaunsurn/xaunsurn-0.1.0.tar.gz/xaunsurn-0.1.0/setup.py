from setuptools import setup, find_packages

setup(
    name="Xaunsurn",
    version="0.1.0",
    author="Parth",
    author_email="contact@xaunsurn.com",
    description="Xaunsurn - Interactively Integrating Imaginations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://xaunsurn.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
