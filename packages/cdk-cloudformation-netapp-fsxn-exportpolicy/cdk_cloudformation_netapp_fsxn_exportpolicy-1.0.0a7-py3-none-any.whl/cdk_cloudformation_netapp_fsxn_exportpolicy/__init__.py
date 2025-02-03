r'''
# netapp-fsxn-exportpolicy

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NetApp::FSxN::ExportPolicy` v1.0.0.

## Description

An export policy defines a set of access rules for NFS clients, specifying which clients or networks can access a volume and with what permissions. Each volume is tied to an export policy which enforces these rules to control client access and provide security and management over FSx for ONTAP volumes. Once activated, you will need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you would need to first create the Link module.

## References

* [Source](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NetApp::FSxN::ExportPolicy \
  --publisher-id a25d267c2b9b86b8d408fce3c7a4d94d34c90946 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/a25d267c2b9b86b8d408fce3c7a4d94d34c90946/NetApp-FSxN-ExportPolicy \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NetApp::FSxN::ExportPolicy`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnetapp-fsxn-exportpolicy+v1.0.0).
* Issues related to `NetApp::FSxN::ExportPolicy` should be reported to the [publisher](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider).

## License

Distributed under the Apache-2.0 License.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnExportPolicy(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.CfnExportPolicy",
):
    '''A CloudFormation ``NetApp::FSxN::ExportPolicy``.

    :cloudformationResource: NetApp::FSxN::ExportPolicy
    :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
        name: builtins.str,
        svm: typing.Union["Svm", typing.Dict[builtins.str, typing.Any]],
        rules: typing.Optional[typing.Sequence[typing.Union["Rule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``NetApp::FSxN::ExportPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param name: The name of the export policy.
        :param svm: The SVM information associated with the export policy.
        :param rules: Rule(s) of an export policy. Used to create the export rule and populate the export policy with export rules in a single request.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5036e6a2101ae44b91e0723c721a9480aad118820ad067a0b125a65cea93bf7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnExportPolicyProps(
            file_system_id=file_system_id,
            fsx_admin_password_source=fsx_admin_password_source,
            link_arn=link_arn,
            name=name,
            svm=svm,
            rules=rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``NetApp::FSxN::ExportPolicy.ID``.

        :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnExportPolicyProps":
        '''Resource props.'''
        return typing.cast("CfnExportPolicyProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.CfnExportPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "fsx_admin_password_source": "fsxAdminPasswordSource",
        "link_arn": "linkArn",
        "name": "name",
        "svm": "svm",
        "rules": "rules",
    },
)
class CfnExportPolicyProps:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
        name: builtins.str,
        svm: typing.Union["Svm", typing.Dict[builtins.str, typing.Any]],
        rules: typing.Optional[typing.Sequence[typing.Union["Rule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''An export policy defines a set of access rules for NFS clients, specifying which clients or networks can access a volume and with what permissions.

        Each volume is tied to an export policy which enforces these rules to control client access and provide security and management over FSx for ONTAP volumes. Once activated, you will need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you would need to first create the Link module.

        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param name: The name of the export policy.
        :param svm: The SVM information associated with the export policy.
        :param rules: Rule(s) of an export policy. Used to create the export rule and populate the export policy with export rules in a single request.

        :schema: CfnExportPolicyProps
        '''
        if isinstance(fsx_admin_password_source, dict):
            fsx_admin_password_source = PasswordSource(**fsx_admin_password_source)
        if isinstance(svm, dict):
            svm = Svm(**svm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfbcd7770cf37e96eaaca1100d2ad70bca32ccb00f9f9594c252bf8afa506150)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument fsx_admin_password_source", value=fsx_admin_password_source, expected_type=type_hints["fsx_admin_password_source"])
            check_type(argname="argument link_arn", value=link_arn, expected_type=type_hints["link_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument svm", value=svm, expected_type=type_hints["svm"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_system_id": file_system_id,
            "fsx_admin_password_source": fsx_admin_password_source,
            "link_arn": link_arn,
            "name": name,
            "svm": svm,
        }
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.

        :schema: CfnExportPolicyProps#FileSystemId
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fsx_admin_password_source(self) -> "PasswordSource":
        '''The password source for the FSx admin user.

        :schema: CfnExportPolicyProps#FsxAdminPasswordSource
        '''
        result = self._values.get("fsx_admin_password_source")
        assert result is not None, "Required property 'fsx_admin_password_source' is missing"
        return typing.cast("PasswordSource", result)

    @builtins.property
    def link_arn(self) -> builtins.str:
        '''The ARN of the AWS Lambda function that will be invoked to manage the resource.

        :schema: CfnExportPolicyProps#LinkArn
        '''
        result = self._values.get("link_arn")
        assert result is not None, "Required property 'link_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the export policy.

        :schema: CfnExportPolicyProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def svm(self) -> "Svm":
        '''The SVM information associated with the export policy.

        :schema: CfnExportPolicyProps#SVM
        '''
        result = self._values.get("svm")
        assert result is not None, "Required property 'svm' is missing"
        return typing.cast("Svm", result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["Rule"]]:
        '''Rule(s) of an export policy.

        Used to create the export rule and populate the export policy with export rules in a single request.

        :schema: CfnExportPolicyProps#Rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["Rule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnExportPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.PasswordSource",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret"},
)
class PasswordSource:
    def __init__(
        self,
        *,
        secret: typing.Union["SecretSource", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param secret: A reference to the source of the password, typically an AWS Secrets Manager secret.

        :schema: PasswordSource
        '''
        if isinstance(secret, dict):
            secret = SecretSource(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983b5f685776359c32a76e90b6b818b923c465bb6bdec295e65fd87b027b066a)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }

    @builtins.property
    def secret(self) -> "SecretSource":
        '''A reference to the source of the password, typically an AWS Secrets Manager secret.

        :schema: PasswordSource#Secret
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast("SecretSource", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PasswordSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.Rule",
    jsii_struct_bases=[],
    name_mapping={
        "allow_device_creation": "allowDeviceCreation",
        "allow_suid": "allowSuid",
        "anonymous_user": "anonymousUser",
        "chown_mode": "chownMode",
        "clients": "clients",
        "index": "index",
        "ntfs_unix_security": "ntfsUnixSecurity",
        "protocols": "protocols",
        "ro_rule": "roRule",
        "rw_rule": "rwRule",
        "superuser": "superuser",
    },
)
class Rule:
    def __init__(
        self,
        *,
        allow_device_creation: typing.Optional[builtins.bool] = None,
        allow_suid: typing.Optional[builtins.bool] = None,
        anonymous_user: typing.Optional[builtins.str] = None,
        chown_mode: typing.Optional["RuleChownMode"] = None,
        clients: typing.Optional[typing.Sequence[typing.Union["RuleClients", typing.Dict[builtins.str, typing.Any]]]] = None,
        index: typing.Optional[jsii.Number] = None,
        ntfs_unix_security: typing.Optional["RuleNtfsUnixSecurity"] = None,
        protocols: typing.Optional[typing.Sequence["RuleProtocols"]] = None,
        ro_rule: typing.Optional[typing.Sequence["RuleRoRule"]] = None,
        rw_rule: typing.Optional[typing.Sequence["RuleRwRule"]] = None,
        superuser: typing.Optional[typing.Sequence["RuleSuperuser"]] = None,
    ) -> None:
        '''
        :param allow_device_creation: Specifies whether or not device creation is allowed.
        :param allow_suid: Specifies whether or not SetUID bits in SETATTR Op is to be honored.
        :param anonymous_user: User ID to which anonymous users are mapped.
        :param chown_mode: Specifies the chown mode, either 'restricted' or 'unrestricted'.
        :param clients: 
        :param index: The index of the export rule in the export policy.
        :param ntfs_unix_security: Specifies the NTFS Unix security options, either 'fail' or 'ignore'.
        :param protocols: Access protocol(s) that the export rule describes.
        :param ro_rule: Authentication flavors that the read-only access rule governs.
        :param rw_rule: Authentication flavors that the read/write access rule governs.
        :param superuser: Authentication flavors that the superuser security type governs.

        :schema: Rule
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8bb3bca01c8732d5dc3e40047c752c84ddb9c5f9f4722a6b52e87078088fd3)
            check_type(argname="argument allow_device_creation", value=allow_device_creation, expected_type=type_hints["allow_device_creation"])
            check_type(argname="argument allow_suid", value=allow_suid, expected_type=type_hints["allow_suid"])
            check_type(argname="argument anonymous_user", value=anonymous_user, expected_type=type_hints["anonymous_user"])
            check_type(argname="argument chown_mode", value=chown_mode, expected_type=type_hints["chown_mode"])
            check_type(argname="argument clients", value=clients, expected_type=type_hints["clients"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument ntfs_unix_security", value=ntfs_unix_security, expected_type=type_hints["ntfs_unix_security"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument ro_rule", value=ro_rule, expected_type=type_hints["ro_rule"])
            check_type(argname="argument rw_rule", value=rw_rule, expected_type=type_hints["rw_rule"])
            check_type(argname="argument superuser", value=superuser, expected_type=type_hints["superuser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_device_creation is not None:
            self._values["allow_device_creation"] = allow_device_creation
        if allow_suid is not None:
            self._values["allow_suid"] = allow_suid
        if anonymous_user is not None:
            self._values["anonymous_user"] = anonymous_user
        if chown_mode is not None:
            self._values["chown_mode"] = chown_mode
        if clients is not None:
            self._values["clients"] = clients
        if index is not None:
            self._values["index"] = index
        if ntfs_unix_security is not None:
            self._values["ntfs_unix_security"] = ntfs_unix_security
        if protocols is not None:
            self._values["protocols"] = protocols
        if ro_rule is not None:
            self._values["ro_rule"] = ro_rule
        if rw_rule is not None:
            self._values["rw_rule"] = rw_rule
        if superuser is not None:
            self._values["superuser"] = superuser

    @builtins.property
    def allow_device_creation(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether or not device creation is allowed.

        :schema: Rule#AllowDeviceCreation
        '''
        result = self._values.get("allow_device_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_suid(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether or not SetUID bits in SETATTR Op is to be honored.

        :schema: Rule#AllowSuid
        '''
        result = self._values.get("allow_suid")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def anonymous_user(self) -> typing.Optional[builtins.str]:
        '''User ID to which anonymous users are mapped.

        :schema: Rule#AnonymousUser
        '''
        result = self._values.get("anonymous_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chown_mode(self) -> typing.Optional["RuleChownMode"]:
        '''Specifies the chown mode, either 'restricted' or 'unrestricted'.

        :schema: Rule#ChownMode
        '''
        result = self._values.get("chown_mode")
        return typing.cast(typing.Optional["RuleChownMode"], result)

    @builtins.property
    def clients(self) -> typing.Optional[typing.List["RuleClients"]]:
        '''
        :schema: Rule#Clients
        '''
        result = self._values.get("clients")
        return typing.cast(typing.Optional[typing.List["RuleClients"]], result)

    @builtins.property
    def index(self) -> typing.Optional[jsii.Number]:
        '''The index of the export rule in the export policy.

        :schema: Rule#Index
        '''
        result = self._values.get("index")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ntfs_unix_security(self) -> typing.Optional["RuleNtfsUnixSecurity"]:
        '''Specifies the NTFS Unix security options, either 'fail' or 'ignore'.

        :schema: Rule#NtfsUnixSecurity
        '''
        result = self._values.get("ntfs_unix_security")
        return typing.cast(typing.Optional["RuleNtfsUnixSecurity"], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List["RuleProtocols"]]:
        '''Access protocol(s) that the export rule describes.

        :schema: Rule#Protocols
        '''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List["RuleProtocols"]], result)

    @builtins.property
    def ro_rule(self) -> typing.Optional[typing.List["RuleRoRule"]]:
        '''Authentication flavors that the read-only access rule governs.

        :schema: Rule#RoRule
        '''
        result = self._values.get("ro_rule")
        return typing.cast(typing.Optional[typing.List["RuleRoRule"]], result)

    @builtins.property
    def rw_rule(self) -> typing.Optional[typing.List["RuleRwRule"]]:
        '''Authentication flavors that the read/write access rule governs.

        :schema: Rule#RwRule
        '''
        result = self._values.get("rw_rule")
        return typing.cast(typing.Optional[typing.List["RuleRwRule"]], result)

    @builtins.property
    def superuser(self) -> typing.Optional[typing.List["RuleSuperuser"]]:
        '''Authentication flavors that the superuser security type governs.

        :schema: Rule#Superuser
        '''
        result = self._values.get("superuser")
        return typing.cast(typing.Optional[typing.List["RuleSuperuser"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Rule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.RuleChownMode")
class RuleChownMode(enum.Enum):
    '''Specifies the chown mode, either 'restricted' or 'unrestricted'.

    :schema: RuleChownMode
    '''

    RESTRICTED = "RESTRICTED"
    '''restricted.'''
    UNRESTRICTED = "UNRESTRICTED"
    '''unrestricted.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.RuleClients",
    jsii_struct_bases=[],
    name_mapping={"match": "match"},
)
class RuleClients:
    def __init__(self, *, match: builtins.str) -> None:
        '''
        :param match: Client IP address or range.

        :schema: RuleClients
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7d7ec697a5054c33572c8eda8a1e453b93df61d8514c2a40d2273e4a5029cf)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match": match,
        }

    @builtins.property
    def match(self) -> builtins.str:
        '''Client IP address or range.

        :schema: RuleClients#Match
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleClients(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.RuleNtfsUnixSecurity"
)
class RuleNtfsUnixSecurity(enum.Enum):
    '''Specifies the NTFS Unix security options, either 'fail' or 'ignore'.

    :schema: RuleNtfsUnixSecurity
    '''

    FAIL = "FAIL"
    '''fail.'''
    IGNORE = "IGNORE"
    '''ignore.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.RuleProtocols")
class RuleProtocols(enum.Enum):
    '''
    :schema: RuleProtocols
    '''

    ANY = "ANY"
    '''any.'''
    NFS = "NFS"
    '''nfs.'''
    CIFS = "CIFS"
    '''cifs.'''
    FLEXCACHE = "FLEXCACHE"
    '''flexcache.'''
    NFS3 = "NFS3"
    '''nfs3.'''
    NFS4 = "NFS4"
    '''nfs4.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.RuleRoRule")
class RuleRoRule(enum.Enum):
    '''
    :schema: RuleRoRule
    '''

    ANY = "ANY"
    '''any.'''
    NONE = "NONE"
    '''none.'''
    NEVER = "NEVER"
    '''never.'''
    KRB5 = "KRB5"
    '''krb5.'''
    KRB5I = "KRB5I"
    '''krb5i.'''
    KRB5P = "KRB5P"
    '''krb5p.'''
    NTLM = "NTLM"
    '''ntlm.'''
    SYS = "SYS"
    '''sys.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.RuleRwRule")
class RuleRwRule(enum.Enum):
    '''
    :schema: RuleRwRule
    '''

    ANY = "ANY"
    '''any.'''
    NONE = "NONE"
    '''none.'''
    NEVER = "NEVER"
    '''never.'''
    KRB5 = "KRB5"
    '''krb5.'''
    KRB5I = "KRB5I"
    '''krb5i.'''
    KRB5P = "KRB5P"
    '''krb5p.'''
    NTLM = "NTLM"
    '''ntlm.'''
    SYS = "SYS"
    '''sys.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.RuleSuperuser")
class RuleSuperuser(enum.Enum):
    '''
    :schema: RuleSuperuser
    '''

    ANY = "ANY"
    '''any.'''
    NONE = "NONE"
    '''none.'''
    NEVER = "NEVER"
    '''never.'''
    KRB5 = "KRB5"
    '''krb5.'''
    KRB5I = "KRB5I"
    '''krb5i.'''
    KRB5P = "KRB5P"
    '''krb5p.'''
    NTLM = "NTLM"
    '''ntlm.'''
    SYS = "SYS"
    '''sys.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.SecretSource",
    jsii_struct_bases=[],
    name_mapping={"secret_arn": "secretArn", "secret_key": "secretKey"},
)
class SecretSource:
    def __init__(self, *, secret_arn: builtins.str, secret_key: builtins.str) -> None:
        '''
        :param secret_arn: The ARN of the secret stored in AWS Secrets Manager.
        :param secret_key: Reference for the SecretKey. The actual password is stored in AWS Secret Manager.

        :schema: SecretSource
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1032e4d2df19bafa9cada47415c6ace5bf31853726f90ef33431e08a6b3ea4b)
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_arn": secret_arn,
            "secret_key": secret_key,
        }

    @builtins.property
    def secret_arn(self) -> builtins.str:
        '''The ARN of the secret stored in AWS Secrets Manager.

        :schema: SecretSource#SecretArn
        '''
        result = self._values.get("secret_arn")
        assert result is not None, "Required property 'secret_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_key(self) -> builtins.str:
        '''Reference for the SecretKey.

        The actual password is stored in AWS Secret Manager.

        :schema: SecretSource#SecretKey
        '''
        result = self._values.get("secret_key")
        assert result is not None, "Required property 'secret_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-exportpolicy.Svm",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uuid": "uuid"},
)
class Svm:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the SVM.
        :param uuid: The UUID of the SVM.

        :schema: SVM
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5a8082cf14b0c71d9fd4b22eb013207ae49d45e378fc0ac4916eec404ad56a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if uuid is not None:
            self._values["uuid"] = uuid

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the SVM.

        :schema: SVM#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''The UUID of the SVM.

        :schema: SVM#UUID
        '''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Svm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnExportPolicy",
    "CfnExportPolicyProps",
    "PasswordSource",
    "Rule",
    "RuleChownMode",
    "RuleClients",
    "RuleNtfsUnixSecurity",
    "RuleProtocols",
    "RuleRoRule",
    "RuleRwRule",
    "RuleSuperuser",
    "SecretSource",
    "Svm",
]

publication.publish()

def _typecheckingstub__d5036e6a2101ae44b91e0723c721a9480aad118820ad067a0b125a65cea93bf7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    name: builtins.str,
    svm: typing.Union[Svm, typing.Dict[builtins.str, typing.Any]],
    rules: typing.Optional[typing.Sequence[typing.Union[Rule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbcd7770cf37e96eaaca1100d2ad70bca32ccb00f9f9594c252bf8afa506150(
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    name: builtins.str,
    svm: typing.Union[Svm, typing.Dict[builtins.str, typing.Any]],
    rules: typing.Optional[typing.Sequence[typing.Union[Rule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983b5f685776359c32a76e90b6b818b923c465bb6bdec295e65fd87b027b066a(
    *,
    secret: typing.Union[SecretSource, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8bb3bca01c8732d5dc3e40047c752c84ddb9c5f9f4722a6b52e87078088fd3(
    *,
    allow_device_creation: typing.Optional[builtins.bool] = None,
    allow_suid: typing.Optional[builtins.bool] = None,
    anonymous_user: typing.Optional[builtins.str] = None,
    chown_mode: typing.Optional[RuleChownMode] = None,
    clients: typing.Optional[typing.Sequence[typing.Union[RuleClients, typing.Dict[builtins.str, typing.Any]]]] = None,
    index: typing.Optional[jsii.Number] = None,
    ntfs_unix_security: typing.Optional[RuleNtfsUnixSecurity] = None,
    protocols: typing.Optional[typing.Sequence[RuleProtocols]] = None,
    ro_rule: typing.Optional[typing.Sequence[RuleRoRule]] = None,
    rw_rule: typing.Optional[typing.Sequence[RuleRwRule]] = None,
    superuser: typing.Optional[typing.Sequence[RuleSuperuser]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7d7ec697a5054c33572c8eda8a1e453b93df61d8514c2a40d2273e4a5029cf(
    *,
    match: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1032e4d2df19bafa9cada47415c6ace5bf31853726f90ef33431e08a6b3ea4b(
    *,
    secret_arn: builtins.str,
    secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5a8082cf14b0c71d9fd4b22eb013207ae49d45e378fc0ac4916eec404ad56a(
    *,
    name: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
