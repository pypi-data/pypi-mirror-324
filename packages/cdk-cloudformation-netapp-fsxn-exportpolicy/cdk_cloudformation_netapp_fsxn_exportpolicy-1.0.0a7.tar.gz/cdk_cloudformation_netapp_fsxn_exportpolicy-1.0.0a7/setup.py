import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cloudformation-netapp-fsxn-exportpolicy",
    "version": "1.0.0.a7",
    "description": "An export policy defines a set of access rules for NFS clients, specifying which clients or networks can access a volume and with what permissions. Each volume is tied to an export policy which enforces these rules to control client access and provide security and management over FSx for ONTAP volumes. Once activated, you will need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you would need to first create the Link module.",
    "license": "Apache-2.0",
    "url": "https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-cloudformation.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudformation_netapp_fsxn_exportpolicy",
        "cdk_cloudformation_netapp_fsxn_exportpolicy._jsii"
    ],
    "package_data": {
        "cdk_cloudformation_netapp_fsxn_exportpolicy._jsii": [
            "netapp-fsxn-exportpolicy@1.0.0-alpha.7.jsii.tgz"
        ],
        "cdk_cloudformation_netapp_fsxn_exportpolicy": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.177.0, <3.0.0",
        "constructs>=10.4.2, <11.0.0",
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
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
