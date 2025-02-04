from setuptools import setup, find_packages

setup(
    name="Fcode_Calculator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    author="F-Code 101",
    author_email="techwbro@example.com",
    description="A Python package for scientific and electronic calculations",
    long_description=open("README.md" , encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fcode101/pyscience.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
