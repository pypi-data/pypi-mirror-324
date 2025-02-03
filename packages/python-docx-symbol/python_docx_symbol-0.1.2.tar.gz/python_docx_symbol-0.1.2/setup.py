from setuptools import setup, find_packages

with open("README.md", "r") as fp:
  long_description = fp.read()

setup(
  name="python-docx-symbol",
  version="0.1.2",
  author="Smartmediq",
  author_email="dev@smartmediq.com",
  description="Convert docx Symbol characters to unicode characters.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/SmartMediQ/python-docx-symbol",
  packages=find_packages(
    exclude=["tests", "tests.*"],
  ),
  classifiers=[
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
  ],
  python_requires=">=3.9",
  install_requires=[
    "python-docx",
  ],
)
