from setuptools import setup, find_packages
 
classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Education",
  "Operating System :: Microsoft :: Windows :: Windows 10",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3"
]
 
setup(
  name="small_scripts_manager",
  version="1.0.1",
  description="This module provides a simple and responsive GUI interface to navigate your collection of small scripts.",
  long_description=open("README.rst").read(),
  long_description_content_type="text/x-rst",
  url="",  
  author="CPUcademy",
  author_email="cpucademy@gmail.com",
  license="MIT", 
  classifiers=classifiers,
  keywords="cpucademy small scripts manager application gui",
  packages=find_packages(),
  install_requires=["cryptography"] 
)