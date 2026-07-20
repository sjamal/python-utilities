"""Setup configuration for sjamal-utilities.

This file is provided for compatibility with older tools and direct invocation.
Modern tools should prefer pyproject.toml.
"""

from setuptools import setup, find_packages

setup(
    name="sjamal-utilities",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
        "yaml": ["pyyaml>=5.0"],
    },
    author="Jamal Siadat",
    author_email="jamals@example.com",
    description="Reusable Python utilities: file I/O, config loading, logging, retries, and environment validation.",
    long_description=open("README.md").read() if __name__ == "__main__" else "",
    long_description_content_type="text/markdown",
    url="https://github.com/sjamal/python-utilities",
    project_urls={
        "Documentation": "https://github.com/sjamal/python-utilities#readme",
        "Repository": "https://github.com/sjamal/python-utilities.git",
        "Issues": "https://github.com/sjamal/python-utilities/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
)
