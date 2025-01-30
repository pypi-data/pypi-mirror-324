import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdklabs.cdk-proserve-lib",
    "version": "0.0.1",
    "description": "@cdklabs/cdk-proserve-lib",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-proserve-lib.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-proserve-lib.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdklabs.cdk_proserve_lib",
        "cdklabs.cdk_proserve_lib._jsii",
        "cdklabs.cdk_proserve_lib.aspects",
        "cdklabs.cdk_proserve_lib.constructs",
        "cdklabs.cdk_proserve_lib.interfaces",
        "cdklabs.cdk_proserve_lib.patterns"
    ],
    "package_data": {
        "cdklabs.cdk_proserve_lib._jsii": [
            "cdk-proserve-lib@0.0.1.jsii.tgz"
        ],
        "cdklabs.cdk_proserve_lib": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.177.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.103.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<5.0.0"
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
