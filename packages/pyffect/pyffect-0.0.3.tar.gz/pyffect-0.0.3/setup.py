import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyffect",
    version="0.0.3",
    author="Nay Aung Kyaw",
    author_email="aknay@outlook.com",
    description="A small package for effect type in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aknay/pyffect",
    project_urls={
        "Bug Tracker": "https://github.com/aknay/pyffect/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['pyffect'],
    python_requires=">=3.8",
)
