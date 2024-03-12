from setuptools import setup
import os


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(name="customtkinter",
      version="0.3",
      author="Tom Schimansky",
      license="Creative Commons Zero v1.0 Universal",
      url="https://github.com/TomSchimansky/CustomTkinter",
      description="Create modern looking gui with tkinter and python",
      long_description_content_type="text/markdown",
      long_description=read('Readme.md'),
      packages=["customtkinter", "customtkinter/examples", "documentation_images"],
      classifiers=["Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"],
      install_requires=["darkdetect"])