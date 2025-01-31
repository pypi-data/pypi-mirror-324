from setuptools import setup, find_packages

setup(
    name="valtra",
    version="0.1.0",
    author="Marco Sousa-Poza",
    author_email="marco.sousapoza@gmail.com",
    description="A PyTorch DataLoader wrapper for dynamic train-test switching.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/marcosousapoza/valtra",
    packages=find_packages(),
    install_requires=["torch>=1.10.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
