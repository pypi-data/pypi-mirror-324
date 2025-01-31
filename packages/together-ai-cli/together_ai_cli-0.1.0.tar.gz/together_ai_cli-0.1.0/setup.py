"""Setup script for your package"""

from setuptools import setup, find_packages

setup(
    name="together-ai-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests>=2.25.1"],
    author="Rodolfo Villaruz",
    author_email="rodolfovillaruz@gmail.com",
    description="A CLI tool for the Together AI API",
)
