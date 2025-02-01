import os
from setuptools import setup, find_packages

# Read the version from executorx/__version__.py
version = {}
with open(os.path.join("executorx", "__version__.py")) as fp:
    exec(fp.read(), version)

# Read the content of the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]

setup(
    name="ExecutorX",
    version=version["__version__"],  # Dynamically loaded version
    author="Yuting Zhang",
    author_email="opensource@yuting.link",
    description="An advanced executor library for Python with progress tracking, throttling, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YutingZhang/executorx",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=parse_requirements("requirements.txt"),  # Load dependencies dynamically
)
