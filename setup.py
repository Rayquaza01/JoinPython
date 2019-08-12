#!/usr/bin/env python3
from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name="joinpython",
      version="1.0.2",
      description="A python script that allows for pushing to Join by Joaoapps from the command line.",
      long_description=long_description,
      url="https://github.com/Rayquaza01/JoinPython",
      author="Rayquaza01",
      author_email="rayquaza01@outlook.com",
      license="MIT",
      scripts=["bin/join.py"],
      packages=["joinpython"],
      include_package_data=True,
      package_data={"": ["README.md"]},
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"
      ])
