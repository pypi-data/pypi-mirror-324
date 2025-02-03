import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OylanAPI",
    version="0.1.0",
    author="Your Name",
    author_email="dari4ok.vsl@gmail.com",
    description="A Python client for the Oylan Assistant API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dari4ok/OylanAPI",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests>=2.20.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)