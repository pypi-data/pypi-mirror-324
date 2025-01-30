from setuptools import setup

setup(
    name="OptimaLab35",
    version="0.6.0a",  # You can set the version manually here or keep it dynamic
    author="Mr. Finchum",
    description="User interface for optima35.",
    long_description=open("pip_README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    url="https://gitlab.com/CodeByMrFinchum/OptimaLab35",
    packages=["OptimaLab35"],
    package_dir={"": "src"},
    install_requires=[
        "optima35>=1.0.0, <2.0.0",
        "pyside6",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "OptimaLab35=OptimaLab35.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
