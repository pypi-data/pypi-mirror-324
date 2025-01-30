from os import path

from setuptools import find_packages
from setuptools import setup

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="liferaft_python_lib",
    version="0.0.3",
    author="ORION",
    author_email="orion@liferaftinc.com",
    packages=find_packages(include=["liferaft_python_lib", "liferaft_python_lib.*"]),
    install_requires=[
        "pika>=1.3.0",
        "pydantic>=2.0.3",
        "tenacity>=8.3.0",
        "pyyaml>=5.4",
    ],
    description="A shared library for reusable abstracted components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    include_package_data=True,
)
