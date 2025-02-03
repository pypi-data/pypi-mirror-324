import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="litepipe",
    version="2.0.1",
    author="Conall Daly",
    author_email="conalldalydev@gmail.com",
    description="Lightweight Python library for data pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tunnelWithAC/litepipe',
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.9'
)