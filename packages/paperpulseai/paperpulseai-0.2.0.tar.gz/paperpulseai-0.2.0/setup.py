from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="paperpulseai",
    version="0.2.0",
    author="SemiQuant",
    author_email="Jason.Limberis@ucsf.edu",
    description="An AI-powered tool for processing and analyzing scientific papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.semiquant.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "biopython>=1.83",
        "click>=8.1.7",
        "diskcache>=5.6.3",
        "pandas>=2.2.1",
        "PyPDF2>=3.0.1",
        "reportlab>=4.1.0",
        "requests>=2.31.0",
        "rich>=13.7.1",
        "scikit-learn>=1.4.1.post1",
        "tenacity>=8.2.3",
        "beautifulsoup4>=4.12.3",
        "openpyxl>=3.1.2",
        "numpy>=1.24.0",
        "pyyaml>=6.0.1",
        "transformers>=4.37.2",
        "huggingface-hub>=0.20.3"
    ],
    extras_require={
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    entry_points={
        "console_scripts": [
            "paperpulseai=paperpulseai.core:cli",
        ],
    },
    test_suite='tests',
) 