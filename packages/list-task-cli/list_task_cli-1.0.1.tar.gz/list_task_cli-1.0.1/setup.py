from setuptools import setup, find_packages

setup(
    name="list-task-cli",
    version="1.0.1",
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
