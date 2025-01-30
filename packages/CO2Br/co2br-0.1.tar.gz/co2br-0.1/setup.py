from setuptools import setup, find_packages
import os

dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(dir, "README.md"), encoding='utf-8') as f:
    long_desc = f.read()

setup(
    name = 'CO2Br',
    version = '0.1',
    packages = find_packages(),
    author = "Sayan Sen",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    install_requires = [],
)