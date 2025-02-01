from setuptools import setup, find_packages

setup(
    name="techtonique_cli",
    version="0.2.0",
    packages=find_packages(),  # Automatically finds the `cli` package
    entry_points={
        "console_scripts": [
            "techtonique=cli.cli:cli",  # Refers to `cli.py` inside the `cli` package
        ],
    },
    install_requires=[
        "click>=8.0.0",
        "requests>=2.0.0",
    ],
    description="A CLI tool for Techtonique API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Techtonique/cli/",
    author="Techtonique",
    author_email="support@techtonique.net",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
