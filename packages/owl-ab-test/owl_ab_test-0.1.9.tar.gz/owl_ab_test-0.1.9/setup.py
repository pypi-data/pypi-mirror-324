from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="owl_ab_test",
    version="0.1.9",
    author="owl_ab_test",
    author_email="anika.ranginani@gmail.com",
    description="A Python package for A/B testing statistical analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anika-academia/owl_ab_test",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Statistics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.22.1",
        "pandas>=1.4.4",
        "scipy>=1.7.3",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "pytest-cov>=2.0"],
    },
)
