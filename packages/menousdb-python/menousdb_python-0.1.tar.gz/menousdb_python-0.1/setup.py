from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="menousdb-python",  # Package name
    version="0.1",  # Version number
    author="Snehashish Laskar",  # Author name
    author_email="snehashish.laskar@gmail.com",  # Author email
    description="A Python client for interacting with the MenousDB database.",  # Short description
    long_description=long_description,  # Long description from README.md
    long_description_content_type="text/markdown",  # Content type of the long description
    url="https://github.com/MenousTech/menousdb-python-sdk",  # Project URL (GitHub repository)
    project_urls={
        "Bug Tracker": "https://github.com/MenousTech/menousdb-python-sdk/issues",  # Issue tracker URL
    },
    classifiers=[
        "Development Status :: 4 - Beta",  # Development status
        "Intended Audience :: Developers",  # Intended audience
        "License :: OSI Approved :: MIT License",  # License
        "Programming Language :: Python :: 3",  # Python version compatibility
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",  # OS compatibility
    ],
    package_dir={"": "src"},  # Directory where the package code is located
    packages=find_packages(where="src"),  # Automatically find packages in the "src" directory
    python_requires=">=3.7",  # Minimum Python version requirement
    install_requires=[
        "requests>=2.26.0",  # Dependencies
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",  # Testing framework
            "black>=21.0",  # Code formatter
            "flake8>=3.9",  # Linter
            "mypy>=0.9",  # Static type checker
        ],
    },
    keywords="database, menousdb, api, client",  # Keywords for PyPI
    license="MIT",  # License
)