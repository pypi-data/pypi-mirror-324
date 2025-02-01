from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="autolaunch",
    version="1.0",
    author="Daniel DONGAR",
    author_email="contact@daneia.fr",
    description="Bibliothèque pour enregistrer et lancer des applications Python depuis n'importe où",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/morgan7street/AutoLaunch",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
