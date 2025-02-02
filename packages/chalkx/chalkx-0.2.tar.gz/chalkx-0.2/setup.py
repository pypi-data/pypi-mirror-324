from setuptools import setup,find_packages
setup(
    name="chalkx",
    version="0.2",
    author="triple7inc",
    packages=find_packages(),
    description="A simple package to change text color in CMD prompt using ANSI escape codes",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    url="https://github.com/triple7inc/chalk",
    license_files=("LICENSE"),
    install_requires=[],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.0"
)