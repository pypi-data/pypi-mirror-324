#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="vasu",
    version="0.1.0",
    author="Ankit Chaubey",
    author_email="m.ankitchaubey@gmail.com",
    description="Exclusive development toolkit for projects and services by Ankit Chaubey (aka Vasu).",
    long_description=(
        "Vasu is a specialized package designed exclusively for projects and services created by Ankit Chaubey (aka Vasu). "
        "This toolkit provides additional setup configurations, advanced development settings, and automation features to enhance workflow and project management."
    ),
    long_description_content_type="text/plain",
    url="https://github.com/ankit-chaubey/vasu",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "vasu=vasu.vasu:main",
        ],
    },
    python_requires=">=3.6",
    keywords="development automation project-configuration exclusive",
    project_urls={
        "Source": "https://github.com/ankit-chaubey/vasu",
        "Bug Tracker": "https://github.com/ankit-chaubey/vasu/issues",
    },
)
