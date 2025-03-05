from setuptools import setup, find_packages

setup(
    name="py-bdd-test",
    version="0.1.0",
    packages=find_packages(include=["bdd-test", "bdd-test.*"]),
    package_data={"bdd-test": ["features/**/*", "behave.ini"]},
    install_requires=[
        "kafka-python",
        "behave",
        "PyHamcrest",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for BDD testing with Kafka integration.",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/erebos12/py-bdd-test",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
