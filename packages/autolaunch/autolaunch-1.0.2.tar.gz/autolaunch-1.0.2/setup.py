from setuptools import setup, find_packages

setup(
    name="autolaunch",
    version="1.0.2",  
    author="Daniel DONGAR",
    author_email="contact@daneia.fr",
    description="Bibliothèque pour enregistrer et lancer des applications Python depuis n'importe où",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/daneia/autolaunch",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
