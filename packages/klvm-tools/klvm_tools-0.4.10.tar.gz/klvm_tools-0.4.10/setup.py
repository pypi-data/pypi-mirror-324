#!/usr/bin/env python

from setuptools import setup

with open("README.md", "rt") as fh:
    long_description = fh.read()

dependencies = [
    "klvm>=0.9.2",
    "klvm_tools_rs>=0.1.37",
    "importlib_metadata",
    "setuptools",
]

dev_dependencies = [
    "pytest",
]

setup(
    name="klvm_tools",
    packages=[
        "ir",
        "klvm_tools",
        "klvm_tools.setuptools",
        "stages",
        "stages.stage_2",
    ],
    author="Chik Network, Inc.",
    entry_points={
        "console_scripts": [
            "read_ir = klvm_tools.cmds:read_ir",
            "opc = klvm_tools.cmds:opc",
            "opd = klvm_tools.cmds:opd",
            "run = klvm_tools.cmds:run",
            "brun = klvm_tools.cmds:brun",
        ],
    },
    package_data={
        "": ["py.typed"],
    },
    author_email="hello@chiknetwork.com",
    install_requires=dependencies,
    url="https://github.com/Chik-Network",
    license="Apache-2.0",
    description="KLVM compiler.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Security :: Cryptography",
    ],
    extras_require=dict(
        dev=dev_dependencies,
    ),
    project_urls={
        "Bug Reports": "https://github.com/Chik-Network/klvm_tools",
        "Source": "https://github.com/Chik-Network/klvm_tools",
    },
)
