from setuptools import setup, find_packages
from auto_requirements.manager import CustomInstall, CustomUninstall

setup(
    name="auto-requirements",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    cmdclass={
        "install": CustomInstall,
        "uninstall": CustomUninstall,
    },
    author="Renish Ponkiya",
    author_email="ponkiyarenish@gmail.com",
    description="Automatically updates requirements.txt when installing/uninstalling packages",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/renish-1111/auto-requirements",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
