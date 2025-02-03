from setuptools import setup

setup(
    name="donut-cli",
    version="0.1.6",
    py_modules=["donut_cli"],
    install_requires=[
        "torch",
        "transformers",
        "Pillow",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "Donut=donut_cli:main",
        ],
    },
    author="Badraa BatUlzii",
    author_email="badraa@andsystems.tech",
    description="A CLI tool for Donut classification",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
