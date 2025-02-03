r'''
# netapp-fsxn-svmpeer

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NetApp::FSxN::SvmPeer` v1.0.0.

## Description

A storage VM (SVM) peer is a relationship established between two SVMs from different FSX for ONTAP file systems, enabling the sharing of resources and data across file systems. Once activated, you will need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you would need to first create the Link module.

## References

* [Source](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NetApp::FSxN::SvmPeer \
  --publisher-id a25d267c2b9b86b8d408fce3c7a4d94d34c90946 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/a25d267c2b9b86b8d408fce3c7a4d94d34c90946/NetApp-FSxN-SvmPeer \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NetApp::FSxN::SvmPeer`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnetapp-fsxn-svmpeer+v1.0.0).
* Issues related to `NetApp::FSxN::SvmPeer` should be reported to the [publisher](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider).

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


class CfnSvmPeer(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/netapp-fsxn-svmpeer.CfnSvmPeer",
):
    '''A CloudFormation ``NetApp::FSxN::SvmPeer``.

    :cloudformationResource: NetApp::FSxN::SvmPeer
    :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        applications: typing.Sequence["CfnSvmPeerPropsApplications"],
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        fsxn_destination_info: typing.Union["FsxnDestination", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
        peer_svm_name: builtins.str,
        svm: typing.Union["Svm", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Create a new ``NetApp::FSxN::SvmPeer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param applications: A list of applications that will use the SVM peer relationship.
        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param fsxn_destination_info: The destination information for the Cluster Peer relationship.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param peer_svm_name: The name of the destination peer SVM.
        :param svm: The SVM information of the local SVM to peer with the destination SVM.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b01cda3bacf2ff5a3654f90bd4ed989f1d85f7cb05f3b531a806705b0b30629)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSvmPeerProps(
            applications=applications,
            file_system_id=file_system_id,
            fsx_admin_password_source=fsx_admin_password_source,
            fsxn_destination_info=fsxn_destination_info,
            link_arn=link_arn,
            peer_svm_name=peer_svm_name,
            svm=svm,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrUuid")
    def attr_uuid(self) -> builtins.str:
        '''Attribute ``NetApp::FSxN::SvmPeer.UUID``.

        :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUuid"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnSvmPeerProps":
        '''Resource props.'''
        return typing.cast("CfnSvmPeerProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-svmpeer.CfnSvmPeerProps",
    jsii_struct_bases=[],
    name_mapping={
        "applications": "applications",
        "file_system_id": "fileSystemId",
        "fsx_admin_password_source": "fsxAdminPasswordSource",
        "fsxn_destination_info": "fsxnDestinationInfo",
        "link_arn": "linkArn",
        "peer_svm_name": "peerSvmName",
        "svm": "svm",
    },
)
class CfnSvmPeerProps:
    def __init__(
        self,
        *,
        applications: typing.Sequence["CfnSvmPeerPropsApplications"],
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        fsxn_destination_info: typing.Union["FsxnDestination", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
        peer_svm_name: builtins.str,
        svm: typing.Union["Svm", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''A storage VM (SVM) peer is a relationship established between two SVMs from different FSX for ONTAP file systems, enabling the sharing of resources and data across file systems.

        Once activated, you will need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you would need to first create the Link module.

        :param applications: A list of applications that will use the SVM peer relationship.
        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param fsxn_destination_info: The destination information for the Cluster Peer relationship.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param peer_svm_name: The name of the destination peer SVM.
        :param svm: The SVM information of the local SVM to peer with the destination SVM.

        :schema: CfnSvmPeerProps
        '''
        if isinstance(fsx_admin_password_source, dict):
            fsx_admin_password_source = PasswordSource(**fsx_admin_password_source)
        if isinstance(fsxn_destination_info, dict):
            fsxn_destination_info = FsxnDestination(**fsxn_destination_info)
        if isinstance(svm, dict):
            svm = Svm(**svm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305f3651a07da99e953189ca1149904fe3f8ad9ffffe7465f8e495a4747b4da4)
            check_type(argname="argument applications", value=applications, expected_type=type_hints["applications"])
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument fsx_admin_password_source", value=fsx_admin_password_source, expected_type=type_hints["fsx_admin_password_source"])
            check_type(argname="argument fsxn_destination_info", value=fsxn_destination_info, expected_type=type_hints["fsxn_destination_info"])
            check_type(argname="argument link_arn", value=link_arn, expected_type=type_hints["link_arn"])
            check_type(argname="argument peer_svm_name", value=peer_svm_name, expected_type=type_hints["peer_svm_name"])
            check_type(argname="argument svm", value=svm, expected_type=type_hints["svm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "applications": applications,
            "file_system_id": file_system_id,
            "fsx_admin_password_source": fsx_admin_password_source,
            "fsxn_destination_info": fsxn_destination_info,
            "link_arn": link_arn,
            "peer_svm_name": peer_svm_name,
            "svm": svm,
        }

    @builtins.property
    def applications(self) -> typing.List["CfnSvmPeerPropsApplications"]:
        '''A list of applications that will use the SVM peer relationship.

        :schema: CfnSvmPeerProps#Applications
        '''
        result = self._values.get("applications")
        assert result is not None, "Required property 'applications' is missing"
        return typing.cast(typing.List["CfnSvmPeerPropsApplications"], result)

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.

        :schema: CfnSvmPeerProps#FileSystemId
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fsx_admin_password_source(self) -> "PasswordSource":
        '''The password source for the FSx admin user.

        :schema: CfnSvmPeerProps#FsxAdminPasswordSource
        '''
        result = self._values.get("fsx_admin_password_source")
        assert result is not None, "Required property 'fsx_admin_password_source' is missing"
        return typing.cast("PasswordSource", result)

    @builtins.property
    def fsxn_destination_info(self) -> "FsxnDestination":
        '''The destination information for the Cluster Peer relationship.

        :schema: CfnSvmPeerProps#FsxnDestinationInfo
        '''
        result = self._values.get("fsxn_destination_info")
        assert result is not None, "Required property 'fsxn_destination_info' is missing"
        return typing.cast("FsxnDestination", result)

    @builtins.property
    def link_arn(self) -> builtins.str:
        '''The ARN of the AWS Lambda function that will be invoked to manage the resource.

        :schema: CfnSvmPeerProps#LinkArn
        '''
        result = self._values.get("link_arn")
        assert result is not None, "Required property 'link_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_svm_name(self) -> builtins.str:
        '''The name of the destination peer SVM.

        :schema: CfnSvmPeerProps#PeerSvmName
        '''
        result = self._values.get("peer_svm_name")
        assert result is not None, "Required property 'peer_svm_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def svm(self) -> "Svm":
        '''The SVM information of the local SVM to peer with the destination SVM.

        :schema: CfnSvmPeerProps#SVM
        '''
        result = self._values.get("svm")
        assert result is not None, "Required property 'svm' is missing"
        return typing.cast("Svm", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSvmPeerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/netapp-fsxn-svmpeer.CfnSvmPeerPropsApplications"
)
class CfnSvmPeerPropsApplications(enum.Enum):
    '''
    :schema: CfnSvmPeerPropsApplications
    '''

    SNAPMIRROR = "SNAPMIRROR"
    '''snapmirror.'''
    FLEXCACHE = "FLEXCACHE"
    '''flexcache.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-svmpeer.FsxnDestination",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "fsx_admin_password_source": "fsxAdminPasswordSource",
        "link_arn": "linkArn",
    },
)
class FsxnDestination:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
    ) -> None:
        '''
        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.

        :schema: FsxnDestination
        '''
        if isinstance(fsx_admin_password_source, dict):
            fsx_admin_password_source = PasswordSource(**fsx_admin_password_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1188645d146ea6eb725031781105812dddcd5db4bd8bbec460a2b59c12f7cade)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument fsx_admin_password_source", value=fsx_admin_password_source, expected_type=type_hints["fsx_admin_password_source"])
            check_type(argname="argument link_arn", value=link_arn, expected_type=type_hints["link_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_system_id": file_system_id,
            "fsx_admin_password_source": fsx_admin_password_source,
            "link_arn": link_arn,
        }

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.

        :schema: FsxnDestination#FileSystemId
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fsx_admin_password_source(self) -> "PasswordSource":
        '''The password source for the FSx admin user.

        :schema: FsxnDestination#FsxAdminPasswordSource
        '''
        result = self._values.get("fsx_admin_password_source")
        assert result is not None, "Required property 'fsx_admin_password_source' is missing"
        return typing.cast("PasswordSource", result)

    @builtins.property
    def link_arn(self) -> builtins.str:
        '''The ARN of the AWS Lambda function that will be invoked to manage the resource.

        :schema: FsxnDestination#LinkArn
        '''
        result = self._values.get("link_arn")
        assert result is not None, "Required property 'link_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxnDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-svmpeer.PasswordSource",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73f11864652803dc40ddfd6d44c899660ab7408077dac58207c1e520b56b6e4e)
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
    jsii_type="@cdk-cloudformation/netapp-fsxn-svmpeer.SecretSource",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e42647b348cc516833be57b1518bae74d92b488fc55327f4c4ec79621e88a154)
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
    jsii_type="@cdk-cloudformation/netapp-fsxn-svmpeer.Svm",
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

        :schema: Svm
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600d28f0c2adb8514a48a5e438ebe0f3888563ade1bb5d5168879a06898bbd6a)
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

        :schema: Svm#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''The UUID of the SVM.

        :schema: Svm#UUID
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
    "CfnSvmPeer",
    "CfnSvmPeerProps",
    "CfnSvmPeerPropsApplications",
    "FsxnDestination",
    "PasswordSource",
    "SecretSource",
    "Svm",
]

publication.publish()

def _typecheckingstub__0b01cda3bacf2ff5a3654f90bd4ed989f1d85f7cb05f3b531a806705b0b30629(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    applications: typing.Sequence[CfnSvmPeerPropsApplications],
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    fsxn_destination_info: typing.Union[FsxnDestination, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    peer_svm_name: builtins.str,
    svm: typing.Union[Svm, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305f3651a07da99e953189ca1149904fe3f8ad9ffffe7465f8e495a4747b4da4(
    *,
    applications: typing.Sequence[CfnSvmPeerPropsApplications],
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    fsxn_destination_info: typing.Union[FsxnDestination, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    peer_svm_name: builtins.str,
    svm: typing.Union[Svm, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1188645d146ea6eb725031781105812dddcd5db4bd8bbec460a2b59c12f7cade(
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f11864652803dc40ddfd6d44c899660ab7408077dac58207c1e520b56b6e4e(
    *,
    secret: typing.Union[SecretSource, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42647b348cc516833be57b1518bae74d92b488fc55327f4c4ec79621e88a154(
    *,
    secret_arn: builtins.str,
    secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600d28f0c2adb8514a48a5e438ebe0f3888563ade1bb5d5168879a06898bbd6a(
    *,
    name: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
