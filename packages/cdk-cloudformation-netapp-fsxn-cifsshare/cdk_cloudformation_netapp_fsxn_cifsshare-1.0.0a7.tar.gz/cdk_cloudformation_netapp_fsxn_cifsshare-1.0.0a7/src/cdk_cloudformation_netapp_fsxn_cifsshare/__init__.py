r'''
# netapp-fsxn-cifsshare

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NetApp::FSxN::CifsShare` v1.0.0.

## Description

A CIFS share is a shared folder tied to an FSx for ONTAP volume. It allows Windows and other SMB-compatible clients to access files on the volume over the network. CIFS shares can be managed with access controls and permissions to ensure secure and efficient file sharing across users and applications. Once activated, you will need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you would need to first create the Link module.

## References

* [Source](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NetApp::FSxN::CifsShare \
  --publisher-id a25d267c2b9b86b8d408fce3c7a4d94d34c90946 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/a25d267c2b9b86b8d408fce3c7a4d94d34c90946/NetApp-FSxN-CifsShare \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NetApp::FSxN::CifsShare`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnetapp-fsxn-cifsshare+v1.0.0).
* Issues related to `NetApp::FSxN::CifsShare` should be reported to the [publisher](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider).

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


class CfnCifsShare(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/netapp-fsxn-cifsshare.CfnCifsShare",
):
    '''A CloudFormation ``NetApp::FSxN::CifsShare``.

    :cloudformationResource: NetApp::FSxN::CifsShare
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
        path: builtins.str,
        svm: typing.Union["Svm", typing.Dict[builtins.str, typing.Any]],
        ac_ls: typing.Optional[typing.Sequence[typing.Union["CifsShareAcl", typing.Dict[builtins.str, typing.Any]]]] = None,
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``NetApp::FSxN::CifsShare``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param name: Name of the CIFS share.
        :param path: Path in the host SVM namespace that is shared through this share.
        :param svm: Existing SVM in which to create the CIFS share.
        :param ac_ls: Share permissions that users and groups have on the CIFS share.
        :param comment: Text comment about the CIFS share.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1d6f519e2c554a636c47dea51f585ab1b91e6d3c5ad1f6f5d23db8a2759a62)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCifsShareProps(
            file_system_id=file_system_id,
            fsx_admin_password_source=fsx_admin_password_source,
            link_arn=link_arn,
            name=name,
            path=path,
            svm=svm,
            ac_ls=ac_ls,
            comment=comment,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrShareID")
    def attr_share_id(self) -> builtins.str:
        '''Attribute ``NetApp::FSxN::CifsShare.ShareID``.

        :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrShareID"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnCifsShareProps":
        '''Resource props.'''
        return typing.cast("CfnCifsShareProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-cifsshare.CfnCifsShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "fsx_admin_password_source": "fsxAdminPasswordSource",
        "link_arn": "linkArn",
        "name": "name",
        "path": "path",
        "svm": "svm",
        "ac_ls": "acLs",
        "comment": "comment",
    },
)
class CfnCifsShareProps:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
        name: builtins.str,
        path: builtins.str,
        svm: typing.Union["Svm", typing.Dict[builtins.str, typing.Any]],
        ac_ls: typing.Optional[typing.Sequence[typing.Union["CifsShareAcl", typing.Dict[builtins.str, typing.Any]]]] = None,
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''A CIFS share is a shared folder tied to an FSx for ONTAP volume.

        It allows Windows and other SMB-compatible clients to access files on the volume over the network. CIFS shares can be managed with access controls and permissions to ensure secure and efficient file sharing across users and applications. Once activated, you will need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you would need to first create the Link module.

        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param name: Name of the CIFS share.
        :param path: Path in the host SVM namespace that is shared through this share.
        :param svm: Existing SVM in which to create the CIFS share.
        :param ac_ls: Share permissions that users and groups have on the CIFS share.
        :param comment: Text comment about the CIFS share.

        :schema: CfnCifsShareProps
        '''
        if isinstance(fsx_admin_password_source, dict):
            fsx_admin_password_source = PasswordSource(**fsx_admin_password_source)
        if isinstance(svm, dict):
            svm = Svm(**svm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7dbf5a55527caf3c86d8706928ef345a488584d5461da41e18328906a84698)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument fsx_admin_password_source", value=fsx_admin_password_source, expected_type=type_hints["fsx_admin_password_source"])
            check_type(argname="argument link_arn", value=link_arn, expected_type=type_hints["link_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument svm", value=svm, expected_type=type_hints["svm"])
            check_type(argname="argument ac_ls", value=ac_ls, expected_type=type_hints["ac_ls"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_system_id": file_system_id,
            "fsx_admin_password_source": fsx_admin_password_source,
            "link_arn": link_arn,
            "name": name,
            "path": path,
            "svm": svm,
        }
        if ac_ls is not None:
            self._values["ac_ls"] = ac_ls
        if comment is not None:
            self._values["comment"] = comment

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.

        :schema: CfnCifsShareProps#FileSystemId
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fsx_admin_password_source(self) -> "PasswordSource":
        '''The password source for the FSx admin user.

        :schema: CfnCifsShareProps#FsxAdminPasswordSource
        '''
        result = self._values.get("fsx_admin_password_source")
        assert result is not None, "Required property 'fsx_admin_password_source' is missing"
        return typing.cast("PasswordSource", result)

    @builtins.property
    def link_arn(self) -> builtins.str:
        '''The ARN of the AWS Lambda function that will be invoked to manage the resource.

        :schema: CfnCifsShareProps#LinkArn
        '''
        result = self._values.get("link_arn")
        assert result is not None, "Required property 'link_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the CIFS share.

        :schema: CfnCifsShareProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Path in the host SVM namespace that is shared through this share.

        :schema: CfnCifsShareProps#Path
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def svm(self) -> "Svm":
        '''Existing SVM in which to create the CIFS share.

        :schema: CfnCifsShareProps#SVM
        '''
        result = self._values.get("svm")
        assert result is not None, "Required property 'svm' is missing"
        return typing.cast("Svm", result)

    @builtins.property
    def ac_ls(self) -> typing.Optional[typing.List["CifsShareAcl"]]:
        '''Share permissions that users and groups have on the CIFS share.

        :schema: CfnCifsShareProps#ACLs
        '''
        result = self._values.get("ac_ls")
        return typing.cast(typing.Optional[typing.List["CifsShareAcl"]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Text comment about the CIFS share.

        :schema: CfnCifsShareProps#Comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCifsShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-cifsshare.CifsShareAcl",
    jsii_struct_bases=[],
    name_mapping={
        "permission": "permission",
        "type": "type",
        "user_or_group": "userOrGroup",
    },
)
class CifsShareAcl:
    def __init__(
        self,
        *,
        permission: "CifsShareAclPermission",
        type: "CifsShareAclType",
        user_or_group: builtins.str,
    ) -> None:
        '''
        :param permission: Access rights that a user or group has on the defined CIFS Share.
        :param type: Type of the user or group to add to the access control list on the defined CIFS share.
        :param user_or_group: User or group name to add to the access control list on the defined CIFS share.

        :schema: CifsShareAcl
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c526829c1c59193708a2d69b556af41e851f44c2c88c0dd2835ac441eb00225)
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_or_group", value=user_or_group, expected_type=type_hints["user_or_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permission": permission,
            "type": type,
            "user_or_group": user_or_group,
        }

    @builtins.property
    def permission(self) -> "CifsShareAclPermission":
        '''Access rights that a user or group has on the defined CIFS Share.

        :schema: CifsShareAcl#Permission
        '''
        result = self._values.get("permission")
        assert result is not None, "Required property 'permission' is missing"
        return typing.cast("CifsShareAclPermission", result)

    @builtins.property
    def type(self) -> "CifsShareAclType":
        '''Type of the user or group to add to the access control list on the defined CIFS share.

        :schema: CifsShareAcl#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("CifsShareAclType", result)

    @builtins.property
    def user_or_group(self) -> builtins.str:
        '''User or group name to add to the access control list on the defined CIFS share.

        :schema: CifsShareAcl#UserOrGroup
        '''
        result = self._values.get("user_or_group")
        assert result is not None, "Required property 'user_or_group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CifsShareAcl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/netapp-fsxn-cifsshare.CifsShareAclPermission"
)
class CifsShareAclPermission(enum.Enum):
    '''Access rights that a user or group has on the defined CIFS Share.

    :schema: CifsShareAclPermission
    '''

    NO_UNDERSCORE_ACCESS = "NO_UNDERSCORE_ACCESS"
    '''no_access.'''
    READ = "READ"
    '''read.'''
    CHANGE = "CHANGE"
    '''change.'''
    FULL_UNDERSCORE_CONTROL = "FULL_UNDERSCORE_CONTROL"
    '''full_control.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-cifsshare.CifsShareAclType")
class CifsShareAclType(enum.Enum):
    '''Type of the user or group to add to the access control list on the defined CIFS share.

    :schema: CifsShareAclType
    '''

    WINDOWS = "WINDOWS"
    '''windows.'''
    UNIX_UNDERSCORE_USER = "UNIX_UNDERSCORE_USER"
    '''unix_user.'''
    UNIX_UNDERSCORE_GROUP = "UNIX_UNDERSCORE_GROUP"
    '''unix_group.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-cifsshare.PasswordSource",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbd278c2a79f5f5f2c8dec41ff834bb53ef08a0fa2d69db9c1500489ab85abbb)
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
    jsii_type="@cdk-cloudformation/netapp-fsxn-cifsshare.SecretSource",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d68a304ebe3038b607dec508bfc7a8fdca56be932d311c28571649d0935eea)
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
    jsii_type="@cdk-cloudformation/netapp-fsxn-cifsshare.Svm",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cf5f4cb4e9e267cbf8d67c72d09c6a8bed1de0c0fdac2638d39a7db5bcabd22)
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
    "CfnCifsShare",
    "CfnCifsShareProps",
    "CifsShareAcl",
    "CifsShareAclPermission",
    "CifsShareAclType",
    "PasswordSource",
    "SecretSource",
    "Svm",
]

publication.publish()

def _typecheckingstub__0e1d6f519e2c554a636c47dea51f585ab1b91e6d3c5ad1f6f5d23db8a2759a62(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    name: builtins.str,
    path: builtins.str,
    svm: typing.Union[Svm, typing.Dict[builtins.str, typing.Any]],
    ac_ls: typing.Optional[typing.Sequence[typing.Union[CifsShareAcl, typing.Dict[builtins.str, typing.Any]]]] = None,
    comment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7dbf5a55527caf3c86d8706928ef345a488584d5461da41e18328906a84698(
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    name: builtins.str,
    path: builtins.str,
    svm: typing.Union[Svm, typing.Dict[builtins.str, typing.Any]],
    ac_ls: typing.Optional[typing.Sequence[typing.Union[CifsShareAcl, typing.Dict[builtins.str, typing.Any]]]] = None,
    comment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c526829c1c59193708a2d69b556af41e851f44c2c88c0dd2835ac441eb00225(
    *,
    permission: CifsShareAclPermission,
    type: CifsShareAclType,
    user_or_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd278c2a79f5f5f2c8dec41ff834bb53ef08a0fa2d69db9c1500489ab85abbb(
    *,
    secret: typing.Union[SecretSource, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d68a304ebe3038b607dec508bfc7a8fdca56be932d311c28571649d0935eea(
    *,
    secret_arn: builtins.str,
    secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf5f4cb4e9e267cbf8d67c72d09c6a8bed1de0c0fdac2638d39a7db5bcabd22(
    *,
    name: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
