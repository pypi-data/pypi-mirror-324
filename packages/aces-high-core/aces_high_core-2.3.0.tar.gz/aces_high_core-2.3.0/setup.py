import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aces-high-core",
    "version": "2.3.0",
    "description": "Base framework for card and deck functionality",
    "license": "MIT",
    "url": "https://github.com/rubyclimber/aces-high-core.git",
    "long_description_content_type": "text/markdown",
    "author": "Aaron Smith",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/rubyclimber/aces-high-core.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aces_high_core",
        "aces_high_core._jsii"
    ],
    "package_data": {
        "aces_high_core._jsii": [
            "aces-high-core@2.3.0.jsii.tgz"
        ],
        "aces_high_core": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "jsii>=1.106.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
