from setuptools import setup, find_packages

# 使用 utf-8 编码读取 README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="midi-trans",
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for MIDI melody extraction and rearrangement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/midi-trans",
    packages=find_packages(),
    install_requires=[
        "mido",
        "musicpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)