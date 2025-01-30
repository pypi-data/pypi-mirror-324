from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="list-task-cli",
    version="1.0.2",
    description="L.I.S.T :-  Log Important Simple Tasks",
    author="GeorgeET15 and codeNinja30",
    author_email="georgeemmanuelthomas@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pyfiglet",
        "inquirer",
        "tqdm",
        "rich",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "list = list:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
