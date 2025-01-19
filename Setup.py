from setuptools import setup, find_packages

setup(
    name="topsis_package",
    version="0.1.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="A Python implementation of the TOPSIS decision-making method",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_package.topsis:execute",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Decision Making"
    ],
    python_requires=">=3.7",
)
