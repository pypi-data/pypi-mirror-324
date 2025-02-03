from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="treefile",
    version="1.0.0",
    author="Benevolence Messiah",
    author_email="benevolence.messiah@gmail.com",
    description="Generate file trees from .treefile configurations with integrated file icon support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenevolenceMessiah/treefile",
    packages=find_packages(),
    include_package_data=True,  # Ensures non-code files are included.
    package_data={'treefile': ['icons/*']},  # Explicitly include all files in treefile/icons.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "treefile=treefile.cli:main",
        ],
    },
)
