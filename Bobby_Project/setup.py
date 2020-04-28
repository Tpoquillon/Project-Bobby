import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ProjectBobby", # Replace with your own username
    version="0.0.1",
    author="POQUILLON Titouan, FLOREAU Julian, SORIN Baptiste",
    author_email="",
    description="This Python 3.6 package is a individual-centered genetic algorithm programmed for optimizing and resolving puzzles such as platform games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tpoquillon/Project-Bobby",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
