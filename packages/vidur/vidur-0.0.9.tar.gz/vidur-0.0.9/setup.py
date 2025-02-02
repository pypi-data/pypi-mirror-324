import os
import re
from typing import List
from setuptools import find_packages, setup


ROOT_DIR = os.path.dirname(__file__)


def get_path(*filepath) -> str:
    return os.path.join(ROOT_DIR, *filepath)


def get_requirements() -> List[str]:
    """Get Python package dependencies from requirements.txt."""
    with open(get_path("requirements.txt")) as f:
        requirements = f.read().strip().split("\n")
    return requirements


def read_version():
    here = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(here, 'vidur', '_version.py')
    
    with open(version_file, 'r', encoding='utf-8') as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                f.read(), re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")

__version__ = read_version()

setup(
    author="Systems for AI Lab, Georgia Tech; Microsoft Corporation",
    python_requires='>=3.10',
    description="A LLM inference cluster simulator",
    include_package_data=True,
    keywords='Simulator, LLM, Inference, Cluster',
    name='vidur',
    packages=find_packages(include=['vidur', 'vidur.*']),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://mlsys.org/virtual/2024/poster/2667', 
    version=__version__,
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": [
            "vidur-data = vidur.cli.data_cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
