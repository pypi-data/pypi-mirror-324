"""Setup script"""
from setuptools import setup, find_packages
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")


def get_version():
    init = open(os.path.join(HERE, "sarif_manager", "version.py")).read()
    return VERSION_RE.search(init).group(1)


def get_description():
    return open(
        os.path.join(os.path.abspath(HERE), "README.md"), encoding="utf-8"
    ).read()


setup(
    name="sarif_manager",
    version=get_version(),
    description="A tool to manage SARIF files and integrations",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    author="Kinnaird McQuade",
    author_email="kinnaird@nightvision.net",
    url="https://github.com/NimblerSecurity/sarif-manager",
    packages=find_packages(exclude=["test*"]),
    python_requires=">=3.11",
    install_requires=[
        "beautifulsoup4>=4.12.3",
        "click",
        "click-option-group",
        "loguru",
        "markdown>=3.5.0",
        "requests>=2.31.0",
        "python-dotenv==0.21.0",
        "slack_sdk",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0"
        ],
    },
    entry_points={
        "console_scripts": [
            "sarif-manager=sarif_manager.bin.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords=["sarif"],
    zip_safe=True,
)

