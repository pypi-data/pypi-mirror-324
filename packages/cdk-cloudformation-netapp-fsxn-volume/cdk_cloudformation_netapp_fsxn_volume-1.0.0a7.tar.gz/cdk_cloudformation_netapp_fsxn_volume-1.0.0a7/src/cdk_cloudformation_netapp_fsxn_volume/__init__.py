r'''
# netapp-fsxn-volume

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NetApp::FSxN::Volume` v1.0.0.

## Description

A volume is a logical storage unit which provides flexible space for data files, snapshots, and block devices. The NetApp:FSxN custom resource allows you to configure and manage FSX for ONTAP volumes by specifying parameters such as volume name, size, storage efficiency, export policies, and other attributes. To use this resource, you must create the Link module. Once activated, you will need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key.

## References

* [Source](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NetApp::FSxN::Volume \
  --publisher-id a25d267c2b9b86b8d408fce3c7a4d94d34c90946 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/a25d267c2b9b86b8d408fce3c7a4d94d34c90946/NetApp-FSxN-Volume \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NetApp::FSxN::Volume`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnetapp-fsxn-volume+v1.0.0).
* Issues related to `NetApp::FSxN::Volume` should be reported to the [publisher](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider).

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


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.Autosize",
    jsii_struct_bases=[],
    name_mapping={
        "grow_threshold": "growThreshold",
        "maximum": "maximum",
        "minimum": "minimum",
        "mode": "mode",
        "shrink_threshold": "shrinkThreshold",
    },
)
class Autosize:
    def __init__(
        self,
        *,
        grow_threshold: typing.Optional[jsii.Number] = None,
        maximum: typing.Optional[jsii.Number] = None,
        minimum: typing.Optional[jsii.Number] = None,
        mode: typing.Optional["AutosizeMode"] = None,
        shrink_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param grow_threshold: The used space threshold percentage for automatic growth of the volume.
        :param maximum: Maximum size in bytes up to which a volume grows automatically. This size cannot be less than the current volume size, or less than or equal to the minimum size of volume.
        :param minimum: Minimum size in bytes up to which the volume shrinks automatically. This size cannot be greater than or equal to the maximum size of volume.
        :param mode: The autosize mode of the volume.
        :param shrink_threshold: The used space threshold percentage for automatic shrinkage of the volume.

        :schema: Autosize
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eafd31d3ac511b88152be9605aac6fb5d590871608d76cc45c2de443231e202)
            check_type(argname="argument grow_threshold", value=grow_threshold, expected_type=type_hints["grow_threshold"])
            check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument shrink_threshold", value=shrink_threshold, expected_type=type_hints["shrink_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grow_threshold is not None:
            self._values["grow_threshold"] = grow_threshold
        if maximum is not None:
            self._values["maximum"] = maximum
        if minimum is not None:
            self._values["minimum"] = minimum
        if mode is not None:
            self._values["mode"] = mode
        if shrink_threshold is not None:
            self._values["shrink_threshold"] = shrink_threshold

    @builtins.property
    def grow_threshold(self) -> typing.Optional[jsii.Number]:
        '''The used space threshold percentage for automatic growth of the volume.

        :schema: Autosize#GrowThreshold
        '''
        result = self._values.get("grow_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum(self) -> typing.Optional[jsii.Number]:
        '''Maximum size in bytes up to which a volume grows automatically.

        This size cannot be less than the current volume size, or less than or equal to the minimum size of volume.

        :schema: Autosize#Maximum
        '''
        result = self._values.get("maximum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum(self) -> typing.Optional[jsii.Number]:
        '''Minimum size in bytes up to which the volume shrinks automatically.

        This size cannot be greater than or equal to the maximum size of volume.

        :schema: Autosize#Minimum
        '''
        result = self._values.get("minimum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mode(self) -> typing.Optional["AutosizeMode"]:
        '''The autosize mode of the volume.

        :schema: Autosize#Mode
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional["AutosizeMode"], result)

    @builtins.property
    def shrink_threshold(self) -> typing.Optional[jsii.Number]:
        '''The used space threshold percentage for automatic shrinkage of the volume.

        :schema: Autosize#ShrinkThreshold
        '''
        result = self._values.get("shrink_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Autosize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.AutosizeMode")
class AutosizeMode(enum.Enum):
    '''The autosize mode of the volume.

    :schema: AutosizeMode
    '''

    GROW = "GROW"
    '''grow.'''
    GROW_UNDERSCORE_SHRINK = "GROW_UNDERSCORE_SHRINK"
    '''grow_shrink.'''
    OFF = "OFF"
    '''off.'''


class CfnVolume(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.CfnVolume",
):
    '''A CloudFormation ``NetApp::FSxN::Volume``.

    :cloudformationResource: NetApp::FSxN::Volume
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
        svm: typing.Union["NameWithUuidRef", typing.Dict[builtins.str, typing.Any]],
        aggregates: typing.Optional[typing.Sequence[builtins.str]] = None,
        anti_ransomware_state: typing.Optional["CfnVolumePropsAntiRansomwareState"] = None,
        autosize: typing.Optional[typing.Union[Autosize, typing.Dict[builtins.str, typing.Any]]] = None,
        clone: typing.Optional[typing.Union["Clone", typing.Dict[builtins.str, typing.Any]]] = None,
        constituents_per_aggregate: typing.Optional[jsii.Number] = None,
        efficiency: typing.Optional[typing.Union["Efficiency", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption: typing.Optional[builtins.bool] = None,
        nas: typing.Optional[typing.Union["Nas", typing.Dict[builtins.str, typing.Any]]] = None,
        ontap_tags: typing.Optional[typing.Sequence[typing.Union["OntapTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        size: typing.Optional[jsii.Number] = None,
        snaplock: typing.Optional[typing.Union["Snaplock", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_policy: typing.Optional[builtins.str] = None,
        state: typing.Optional["CfnVolumePropsState"] = None,
        style: typing.Optional["CfnVolumePropsStyle"] = None,
        tiering: typing.Optional[typing.Union["Tiering", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional["CfnVolumePropsType"] = None,
    ) -> None:
        '''Create a new ``NetApp::FSxN::Volume``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param name: Volume name. The name of volume must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 197 or fewer characters in length for FlexGroups, and 203 or fewer characters in length for all other types of volumes. Volume names must be unique within an SVM.
        :param svm: The SVM that contains the volume.
        :param aggregates: List of aggregate names that host the volume.
        :param anti_ransomware_state: The anti-ransomware state of the volume.
        :param autosize: The autosize settings of the volume.
        :param clone: The clone settings of the volume.
        :param constituents_per_aggregate: Specifies the number of times to iterate constituents over the aggregates when creating or expanding a FlexGroup volume.
        :param efficiency: The storage efficiency settings for the volume.
        :param encryption: Indicates if the volume is encrypted.
        :param nas: The NAS settings of the volume.
        :param ontap_tags: Tags associated with the ONTAP volume.
        :param size: Physical size of the volume, in bytes. The minimum size for a FlexVol volume is 20MB and the minimum size for a FlexGroup volume is 200MB per constituent. The recommended size for a FlexGroup volume is a minimum of 100GB per constituent. For all volumes, the default size is equal to the minimum size.
        :param snaplock: The SnapLock settings of the volume.
        :param snapshot_policy: Snapshot policy name.
        :param state: The state of the volume (e.g., online, offline, restricted). Client access is supported only when volume is online and connected to its junction path. Taking volume to offline or restricted state removes its junction path and blocks client access.
        :param style: The style of the volume (e.g., FlexVol or FlexGroup).
        :param tiering: The tiering settings of the volume.
        :param type: The type of volume (e.g., read-write or data protection).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7807739269ec53ee2d3e5f59703fde795ad4642df968ba8d306b23cbde5690)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVolumeProps(
            file_system_id=file_system_id,
            fsx_admin_password_source=fsx_admin_password_source,
            link_arn=link_arn,
            name=name,
            svm=svm,
            aggregates=aggregates,
            anti_ransomware_state=anti_ransomware_state,
            autosize=autosize,
            clone=clone,
            constituents_per_aggregate=constituents_per_aggregate,
            efficiency=efficiency,
            encryption=encryption,
            nas=nas,
            ontap_tags=ontap_tags,
            size=size,
            snaplock=snaplock,
            snapshot_policy=snapshot_policy,
            state=state,
            style=style,
            tiering=tiering,
            type=type,
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
        '''Attribute ``NetApp::FSxN::Volume.UUID``.

        :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUuid"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnVolumeProps":
        '''Resource props.'''
        return typing.cast("CfnVolumeProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.CfnVolumeProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "fsx_admin_password_source": "fsxAdminPasswordSource",
        "link_arn": "linkArn",
        "name": "name",
        "svm": "svm",
        "aggregates": "aggregates",
        "anti_ransomware_state": "antiRansomwareState",
        "autosize": "autosize",
        "clone": "clone",
        "constituents_per_aggregate": "constituentsPerAggregate",
        "efficiency": "efficiency",
        "encryption": "encryption",
        "nas": "nas",
        "ontap_tags": "ontapTags",
        "size": "size",
        "snaplock": "snaplock",
        "snapshot_policy": "snapshotPolicy",
        "state": "state",
        "style": "style",
        "tiering": "tiering",
        "type": "type",
    },
)
class CfnVolumeProps:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
        name: builtins.str,
        svm: typing.Union["NameWithUuidRef", typing.Dict[builtins.str, typing.Any]],
        aggregates: typing.Optional[typing.Sequence[builtins.str]] = None,
        anti_ransomware_state: typing.Optional["CfnVolumePropsAntiRansomwareState"] = None,
        autosize: typing.Optional[typing.Union[Autosize, typing.Dict[builtins.str, typing.Any]]] = None,
        clone: typing.Optional[typing.Union["Clone", typing.Dict[builtins.str, typing.Any]]] = None,
        constituents_per_aggregate: typing.Optional[jsii.Number] = None,
        efficiency: typing.Optional[typing.Union["Efficiency", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption: typing.Optional[builtins.bool] = None,
        nas: typing.Optional[typing.Union["Nas", typing.Dict[builtins.str, typing.Any]]] = None,
        ontap_tags: typing.Optional[typing.Sequence[typing.Union["OntapTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        size: typing.Optional[jsii.Number] = None,
        snaplock: typing.Optional[typing.Union["Snaplock", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_policy: typing.Optional[builtins.str] = None,
        state: typing.Optional["CfnVolumePropsState"] = None,
        style: typing.Optional["CfnVolumePropsStyle"] = None,
        tiering: typing.Optional[typing.Union["Tiering", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional["CfnVolumePropsType"] = None,
    ) -> None:
        '''A volume is a logical storage unit which provides flexible space for data files, snapshots, and block devices.

        The NetApp:FSxN custom resource allows you to configure and manage FSX for ONTAP volumes by specifying parameters such as volume name, size, storage efficiency, export policies, and other attributes. To use this resource, you must create the Link module. Once activated, you will need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key.

        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param name: Volume name. The name of volume must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 197 or fewer characters in length for FlexGroups, and 203 or fewer characters in length for all other types of volumes. Volume names must be unique within an SVM.
        :param svm: The SVM that contains the volume.
        :param aggregates: List of aggregate names that host the volume.
        :param anti_ransomware_state: The anti-ransomware state of the volume.
        :param autosize: The autosize settings of the volume.
        :param clone: The clone settings of the volume.
        :param constituents_per_aggregate: Specifies the number of times to iterate constituents over the aggregates when creating or expanding a FlexGroup volume.
        :param efficiency: The storage efficiency settings for the volume.
        :param encryption: Indicates if the volume is encrypted.
        :param nas: The NAS settings of the volume.
        :param ontap_tags: Tags associated with the ONTAP volume.
        :param size: Physical size of the volume, in bytes. The minimum size for a FlexVol volume is 20MB and the minimum size for a FlexGroup volume is 200MB per constituent. The recommended size for a FlexGroup volume is a minimum of 100GB per constituent. For all volumes, the default size is equal to the minimum size.
        :param snaplock: The SnapLock settings of the volume.
        :param snapshot_policy: Snapshot policy name.
        :param state: The state of the volume (e.g., online, offline, restricted). Client access is supported only when volume is online and connected to its junction path. Taking volume to offline or restricted state removes its junction path and blocks client access.
        :param style: The style of the volume (e.g., FlexVol or FlexGroup).
        :param tiering: The tiering settings of the volume.
        :param type: The type of volume (e.g., read-write or data protection).

        :schema: CfnVolumeProps
        '''
        if isinstance(fsx_admin_password_source, dict):
            fsx_admin_password_source = PasswordSource(**fsx_admin_password_source)
        if isinstance(svm, dict):
            svm = NameWithUuidRef(**svm)
        if isinstance(autosize, dict):
            autosize = Autosize(**autosize)
        if isinstance(clone, dict):
            clone = Clone(**clone)
        if isinstance(efficiency, dict):
            efficiency = Efficiency(**efficiency)
        if isinstance(nas, dict):
            nas = Nas(**nas)
        if isinstance(snaplock, dict):
            snaplock = Snaplock(**snaplock)
        if isinstance(tiering, dict):
            tiering = Tiering(**tiering)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e5f166fc7fcfd76c3d97f547dbade9303d259ebfa09c598fb8ff16ab076d07)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument fsx_admin_password_source", value=fsx_admin_password_source, expected_type=type_hints["fsx_admin_password_source"])
            check_type(argname="argument link_arn", value=link_arn, expected_type=type_hints["link_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument svm", value=svm, expected_type=type_hints["svm"])
            check_type(argname="argument aggregates", value=aggregates, expected_type=type_hints["aggregates"])
            check_type(argname="argument anti_ransomware_state", value=anti_ransomware_state, expected_type=type_hints["anti_ransomware_state"])
            check_type(argname="argument autosize", value=autosize, expected_type=type_hints["autosize"])
            check_type(argname="argument clone", value=clone, expected_type=type_hints["clone"])
            check_type(argname="argument constituents_per_aggregate", value=constituents_per_aggregate, expected_type=type_hints["constituents_per_aggregate"])
            check_type(argname="argument efficiency", value=efficiency, expected_type=type_hints["efficiency"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument nas", value=nas, expected_type=type_hints["nas"])
            check_type(argname="argument ontap_tags", value=ontap_tags, expected_type=type_hints["ontap_tags"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument snaplock", value=snaplock, expected_type=type_hints["snaplock"])
            check_type(argname="argument snapshot_policy", value=snapshot_policy, expected_type=type_hints["snapshot_policy"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument style", value=style, expected_type=type_hints["style"])
            check_type(argname="argument tiering", value=tiering, expected_type=type_hints["tiering"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_system_id": file_system_id,
            "fsx_admin_password_source": fsx_admin_password_source,
            "link_arn": link_arn,
            "name": name,
            "svm": svm,
        }
        if aggregates is not None:
            self._values["aggregates"] = aggregates
        if anti_ransomware_state is not None:
            self._values["anti_ransomware_state"] = anti_ransomware_state
        if autosize is not None:
            self._values["autosize"] = autosize
        if clone is not None:
            self._values["clone"] = clone
        if constituents_per_aggregate is not None:
            self._values["constituents_per_aggregate"] = constituents_per_aggregate
        if efficiency is not None:
            self._values["efficiency"] = efficiency
        if encryption is not None:
            self._values["encryption"] = encryption
        if nas is not None:
            self._values["nas"] = nas
        if ontap_tags is not None:
            self._values["ontap_tags"] = ontap_tags
        if size is not None:
            self._values["size"] = size
        if snaplock is not None:
            self._values["snaplock"] = snaplock
        if snapshot_policy is not None:
            self._values["snapshot_policy"] = snapshot_policy
        if state is not None:
            self._values["state"] = state
        if style is not None:
            self._values["style"] = style
        if tiering is not None:
            self._values["tiering"] = tiering
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.

        :schema: CfnVolumeProps#FileSystemId
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fsx_admin_password_source(self) -> "PasswordSource":
        '''The password source for the FSx admin user.

        :schema: CfnVolumeProps#FsxAdminPasswordSource
        '''
        result = self._values.get("fsx_admin_password_source")
        assert result is not None, "Required property 'fsx_admin_password_source' is missing"
        return typing.cast("PasswordSource", result)

    @builtins.property
    def link_arn(self) -> builtins.str:
        '''The ARN of the AWS Lambda function that will be invoked to manage the resource.

        :schema: CfnVolumeProps#LinkArn
        '''
        result = self._values.get("link_arn")
        assert result is not None, "Required property 'link_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Volume name.

        The name of volume must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 197 or fewer characters in length for FlexGroups, and 203 or fewer characters in length for all other types of volumes. Volume names must be unique within an SVM.

        :schema: CfnVolumeProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def svm(self) -> "NameWithUuidRef":
        '''The SVM that contains the volume.

        :schema: CfnVolumeProps#SVM
        '''
        result = self._values.get("svm")
        assert result is not None, "Required property 'svm' is missing"
        return typing.cast("NameWithUuidRef", result)

    @builtins.property
    def aggregates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of aggregate names that host the volume.

        :schema: CfnVolumeProps#Aggregates
        '''
        result = self._values.get("aggregates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def anti_ransomware_state(
        self,
    ) -> typing.Optional["CfnVolumePropsAntiRansomwareState"]:
        '''The anti-ransomware state of the volume.

        :schema: CfnVolumeProps#AntiRansomwareState
        '''
        result = self._values.get("anti_ransomware_state")
        return typing.cast(typing.Optional["CfnVolumePropsAntiRansomwareState"], result)

    @builtins.property
    def autosize(self) -> typing.Optional[Autosize]:
        '''The autosize settings of the volume.

        :schema: CfnVolumeProps#Autosize
        '''
        result = self._values.get("autosize")
        return typing.cast(typing.Optional[Autosize], result)

    @builtins.property
    def clone(self) -> typing.Optional["Clone"]:
        '''The clone settings of the volume.

        :schema: CfnVolumeProps#Clone
        '''
        result = self._values.get("clone")
        return typing.cast(typing.Optional["Clone"], result)

    @builtins.property
    def constituents_per_aggregate(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of times to iterate constituents over the aggregates when creating or expanding a FlexGroup volume.

        :schema: CfnVolumeProps#ConstituentsPerAggregate
        '''
        result = self._values.get("constituents_per_aggregate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def efficiency(self) -> typing.Optional["Efficiency"]:
        '''The storage efficiency settings for the volume.

        :schema: CfnVolumeProps#Efficiency
        '''
        result = self._values.get("efficiency")
        return typing.cast(typing.Optional["Efficiency"], result)

    @builtins.property
    def encryption(self) -> typing.Optional[builtins.bool]:
        '''Indicates if the volume is encrypted.

        :schema: CfnVolumeProps#Encryption
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nas(self) -> typing.Optional["Nas"]:
        '''The NAS settings of the volume.

        :schema: CfnVolumeProps#NAS
        '''
        result = self._values.get("nas")
        return typing.cast(typing.Optional["Nas"], result)

    @builtins.property
    def ontap_tags(self) -> typing.Optional[typing.List["OntapTag"]]:
        '''Tags associated with the ONTAP volume.

        :schema: CfnVolumeProps#ONTAPTags
        '''
        result = self._values.get("ontap_tags")
        return typing.cast(typing.Optional[typing.List["OntapTag"]], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Physical size of the volume, in bytes.

        The minimum size for a FlexVol volume is 20MB and the minimum size for a FlexGroup volume is 200MB per constituent. The recommended size for a FlexGroup volume is a minimum of 100GB per constituent. For all volumes, the default size is equal to the minimum size.

        :schema: CfnVolumeProps#Size
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snaplock(self) -> typing.Optional["Snaplock"]:
        '''The SnapLock settings of the volume.

        :schema: CfnVolumeProps#Snaplock
        '''
        result = self._values.get("snaplock")
        return typing.cast(typing.Optional["Snaplock"], result)

    @builtins.property
    def snapshot_policy(self) -> typing.Optional[builtins.str]:
        '''Snapshot policy name.

        :schema: CfnVolumeProps#SnapshotPolicy
        '''
        result = self._values.get("snapshot_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional["CfnVolumePropsState"]:
        '''The state of the volume (e.g., online, offline, restricted). Client access is supported only when volume is online and connected to its junction path. Taking volume to offline or restricted state removes its junction path and blocks client access.

        :schema: CfnVolumeProps#State
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional["CfnVolumePropsState"], result)

    @builtins.property
    def style(self) -> typing.Optional["CfnVolumePropsStyle"]:
        '''The style of the volume (e.g., FlexVol or FlexGroup).

        :schema: CfnVolumeProps#Style
        '''
        result = self._values.get("style")
        return typing.cast(typing.Optional["CfnVolumePropsStyle"], result)

    @builtins.property
    def tiering(self) -> typing.Optional["Tiering"]:
        '''The tiering settings of the volume.

        :schema: CfnVolumeProps#Tiering
        '''
        result = self._values.get("tiering")
        return typing.cast(typing.Optional["Tiering"], result)

    @builtins.property
    def type(self) -> typing.Optional["CfnVolumePropsType"]:
        '''The type of volume (e.g., read-write or data protection).

        :schema: CfnVolumeProps#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["CfnVolumePropsType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVolumeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.CfnVolumePropsAntiRansomwareState"
)
class CfnVolumePropsAntiRansomwareState(enum.Enum):
    '''The anti-ransomware state of the volume.

    :schema: CfnVolumePropsAntiRansomwareState
    '''

    DISABLED = "DISABLED"
    '''disabled.'''
    DRY_UNDERSCORE_RUN = "DRY_UNDERSCORE_RUN"
    '''dry_run.'''
    ENABLED = "ENABLED"
    '''enabled.'''
    PAUSED = "PAUSED"
    '''paused.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.CfnVolumePropsState")
class CfnVolumePropsState(enum.Enum):
    '''The state of the volume (e.g., online, offline, restricted). Client access is supported only when volume is online and connected to its junction path. Taking volume to offline or restricted state removes its junction path and blocks client access.

    :schema: CfnVolumePropsState
    '''

    OFFLINE = "OFFLINE"
    '''offline.'''
    ONLINE = "ONLINE"
    '''online.'''
    RESTRICTED = "RESTRICTED"
    '''restricted.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.CfnVolumePropsStyle")
class CfnVolumePropsStyle(enum.Enum):
    '''The style of the volume (e.g., FlexVol or FlexGroup).

    :schema: CfnVolumePropsStyle
    '''

    FLEXVOL = "FLEXVOL"
    '''flexvol.'''
    FLEXGROUP = "FLEXGROUP"
    '''flexgroup.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.CfnVolumePropsType")
class CfnVolumePropsType(enum.Enum):
    '''The type of volume (e.g., read-write or data protection).

    :schema: CfnVolumePropsType
    '''

    RW = "RW"
    '''rw.'''
    DP = "DP"
    '''dp.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.Clone",
    jsii_struct_bases=[],
    name_mapping={
        "parent_svm": "parentSvm",
        "parent_volume": "parentVolume",
        "is_cloned": "isCloned",
        "parent_snapshot": "parentSnapshot",
    },
)
class Clone:
    def __init__(
        self,
        *,
        parent_svm: typing.Union["NameWithUuidRef", typing.Dict[builtins.str, typing.Any]],
        parent_volume: typing.Union["NameWithUuidRef", typing.Dict[builtins.str, typing.Any]],
        is_cloned: typing.Optional[builtins.bool] = None,
        parent_snapshot: typing.Optional[typing.Union["NameWithUuidRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param parent_svm: SVM containing the parent volume.
        :param parent_volume: The parent volume of the clone.
        :param is_cloned: Setting 'IsCloned' attribute to false splits the clone from its parent volume.
        :param parent_snapshot: The snapshot of the parent volume from which the clone is created.

        :schema: Clone
        '''
        if isinstance(parent_svm, dict):
            parent_svm = NameWithUuidRef(**parent_svm)
        if isinstance(parent_volume, dict):
            parent_volume = NameWithUuidRef(**parent_volume)
        if isinstance(parent_snapshot, dict):
            parent_snapshot = NameWithUuidRef(**parent_snapshot)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ca653fa1fb2699547c2f1e3d189431bf9e1efec2748d591e29f5a9952ef26a)
            check_type(argname="argument parent_svm", value=parent_svm, expected_type=type_hints["parent_svm"])
            check_type(argname="argument parent_volume", value=parent_volume, expected_type=type_hints["parent_volume"])
            check_type(argname="argument is_cloned", value=is_cloned, expected_type=type_hints["is_cloned"])
            check_type(argname="argument parent_snapshot", value=parent_snapshot, expected_type=type_hints["parent_snapshot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parent_svm": parent_svm,
            "parent_volume": parent_volume,
        }
        if is_cloned is not None:
            self._values["is_cloned"] = is_cloned
        if parent_snapshot is not None:
            self._values["parent_snapshot"] = parent_snapshot

    @builtins.property
    def parent_svm(self) -> "NameWithUuidRef":
        '''SVM containing the parent volume.

        :schema: Clone#ParentSVM
        '''
        result = self._values.get("parent_svm")
        assert result is not None, "Required property 'parent_svm' is missing"
        return typing.cast("NameWithUuidRef", result)

    @builtins.property
    def parent_volume(self) -> "NameWithUuidRef":
        '''The parent volume of the clone.

        :schema: Clone#ParentVolume
        '''
        result = self._values.get("parent_volume")
        assert result is not None, "Required property 'parent_volume' is missing"
        return typing.cast("NameWithUuidRef", result)

    @builtins.property
    def is_cloned(self) -> typing.Optional[builtins.bool]:
        '''Setting 'IsCloned' attribute to false splits the clone from its parent volume.

        :schema: Clone#IsCloned
        '''
        result = self._values.get("is_cloned")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parent_snapshot(self) -> typing.Optional["NameWithUuidRef"]:
        '''The snapshot of the parent volume from which the clone is created.

        :schema: Clone#ParentSnapshot
        '''
        result = self._values.get("parent_snapshot")
        return typing.cast(typing.Optional["NameWithUuidRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Clone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.Efficiency",
    jsii_struct_bases=[],
    name_mapping={
        "compaction": "compaction",
        "compression": "compression",
        "cross_volume_dedupe": "crossVolumeDedupe",
        "dedupe": "dedupe",
    },
)
class Efficiency:
    def __init__(
        self,
        *,
        compaction: typing.Optional["EfficiencyCompaction"] = None,
        compression: typing.Optional["EfficiencyCompression"] = None,
        cross_volume_dedupe: typing.Optional["EfficiencyCrossVolumeDedupe"] = None,
        dedupe: typing.Optional["EfficiencyDedupe"] = None,
    ) -> None:
        '''
        :param compaction: The compaction setting of the volume.
        :param compression: The compression setting of the volume.
        :param cross_volume_dedupe: The cross-volume deduplication setting of the volume.
        :param dedupe: The deduplication setting of the volume.

        :schema: Efficiency
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb2ec2444fcae48fb646df9ccceb5aa519cd20996005728f29d47e77d847f45)
            check_type(argname="argument compaction", value=compaction, expected_type=type_hints["compaction"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument cross_volume_dedupe", value=cross_volume_dedupe, expected_type=type_hints["cross_volume_dedupe"])
            check_type(argname="argument dedupe", value=dedupe, expected_type=type_hints["dedupe"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compaction is not None:
            self._values["compaction"] = compaction
        if compression is not None:
            self._values["compression"] = compression
        if cross_volume_dedupe is not None:
            self._values["cross_volume_dedupe"] = cross_volume_dedupe
        if dedupe is not None:
            self._values["dedupe"] = dedupe

    @builtins.property
    def compaction(self) -> typing.Optional["EfficiencyCompaction"]:
        '''The compaction setting of the volume.

        :schema: Efficiency#Compaction
        '''
        result = self._values.get("compaction")
        return typing.cast(typing.Optional["EfficiencyCompaction"], result)

    @builtins.property
    def compression(self) -> typing.Optional["EfficiencyCompression"]:
        '''The compression setting of the volume.

        :schema: Efficiency#Compression
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional["EfficiencyCompression"], result)

    @builtins.property
    def cross_volume_dedupe(self) -> typing.Optional["EfficiencyCrossVolumeDedupe"]:
        '''The cross-volume deduplication setting of the volume.

        :schema: Efficiency#CrossVolumeDedupe
        '''
        result = self._values.get("cross_volume_dedupe")
        return typing.cast(typing.Optional["EfficiencyCrossVolumeDedupe"], result)

    @builtins.property
    def dedupe(self) -> typing.Optional["EfficiencyDedupe"]:
        '''The deduplication setting of the volume.

        :schema: Efficiency#Dedupe
        '''
        result = self._values.get("dedupe")
        return typing.cast(typing.Optional["EfficiencyDedupe"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Efficiency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.EfficiencyCompaction")
class EfficiencyCompaction(enum.Enum):
    '''The compaction setting of the volume.

    :schema: EfficiencyCompaction
    '''

    INLINE = "INLINE"
    '''inline.'''
    NONE = "NONE"
    '''none.'''
    MIXED = "MIXED"
    '''mixed.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.EfficiencyCompression")
class EfficiencyCompression(enum.Enum):
    '''The compression setting of the volume.

    :schema: EfficiencyCompression
    '''

    INLINE = "INLINE"
    '''inline.'''
    BACKGROUND = "BACKGROUND"
    '''background.'''
    BOTH = "BOTH"
    '''both.'''
    NONE = "NONE"
    '''none.'''
    MIXED = "MIXED"
    '''mixed.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.EfficiencyCrossVolumeDedupe"
)
class EfficiencyCrossVolumeDedupe(enum.Enum):
    '''The cross-volume deduplication setting of the volume.

    :schema: EfficiencyCrossVolumeDedupe
    '''

    INLINE = "INLINE"
    '''inline.'''
    BACKGROUND = "BACKGROUND"
    '''background.'''
    BOTH = "BOTH"
    '''both.'''
    NONE = "NONE"
    '''none.'''
    MIXED = "MIXED"
    '''mixed.'''


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.EfficiencyDedupe")
class EfficiencyDedupe(enum.Enum):
    '''The deduplication setting of the volume.

    :schema: EfficiencyDedupe
    '''

    INLINE = "INLINE"
    '''inline.'''
    BACKGROUND = "BACKGROUND"
    '''background.'''
    BOTH = "BOTH"
    '''both.'''
    NONE = "NONE"
    '''none.'''
    MIXED = "MIXED"
    '''mixed.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.NameWithUuidRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uuid": "uuid"},
)
class NameWithUuidRef:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name part of the reference, which can be used to identify resources such as SVM, volume or snapshot.
        :param uuid: The UUID part of the reference, which can be used to identify resources such as SVM, volume or snapshot.

        :schema: NameWithUuidRef
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2104ab1a6d47ece4db45e93d253fc69be460d3d4751e2f1317d9a06a3bdcb2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if uuid is not None:
            self._values["uuid"] = uuid

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name part of the reference, which can be used to identify resources such as SVM, volume or snapshot.

        :schema: NameWithUuidRef#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''The UUID part of the reference, which can be used to identify resources such as SVM, volume or snapshot.

        :schema: NameWithUuidRef#UUID
        '''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NameWithUuidRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.Nas",
    jsii_struct_bases=[],
    name_mapping={
        "export_policy": "exportPolicy",
        "junction_path": "junctionPath",
        "security_style": "securityStyle",
    },
)
class Nas:
    def __init__(
        self,
        *,
        export_policy: typing.Optional[builtins.str] = None,
        junction_path: typing.Optional[builtins.str] = None,
        security_style: typing.Optional["NasSecurityStyle"] = None,
    ) -> None:
        '''
        :param export_policy: The export policy associated with the volume.
        :param junction_path: The fully-qualified path in the hosting SVM's namespace at which the volume is mounted.
        :param security_style: Security style associated with the volume.

        :schema: NAS
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a614936ac5249a54ae4a76658502f7acbb0ae9ad126716611fd350b5da16cbb0)
            check_type(argname="argument export_policy", value=export_policy, expected_type=type_hints["export_policy"])
            check_type(argname="argument junction_path", value=junction_path, expected_type=type_hints["junction_path"])
            check_type(argname="argument security_style", value=security_style, expected_type=type_hints["security_style"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if export_policy is not None:
            self._values["export_policy"] = export_policy
        if junction_path is not None:
            self._values["junction_path"] = junction_path
        if security_style is not None:
            self._values["security_style"] = security_style

    @builtins.property
    def export_policy(self) -> typing.Optional[builtins.str]:
        '''The export policy associated with the volume.

        :schema: NAS#ExportPolicy
        '''
        result = self._values.get("export_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def junction_path(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified path in the hosting SVM's namespace at which the volume is mounted.

        :schema: NAS#JunctionPath
        '''
        result = self._values.get("junction_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_style(self) -> typing.Optional["NasSecurityStyle"]:
        '''Security style associated with the volume.

        :schema: NAS#SecurityStyle
        '''
        result = self._values.get("security_style")
        return typing.cast(typing.Optional["NasSecurityStyle"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Nas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.NasSecurityStyle")
class NasSecurityStyle(enum.Enum):
    '''Security style associated with the volume.

    :schema: NasSecurityStyle
    '''

    MIXED = "MIXED"
    '''mixed.'''
    NTFS = "NTFS"
    '''ntfs.'''
    UNIX = "UNIX"
    '''unix.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.OntapTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class OntapTag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: The key of the tag.
        :param value: The value of the tag.

        :schema: ONTAPTag
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3e576eca07c3184f415caf761c184635c9513d714bf51037204091c94ee646)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the tag.

        :schema: ONTAPTag#Key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the tag.

        :schema: ONTAPTag#Value
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OntapTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.PasswordSource",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9db357e22185b084e370631d5cbcf6123291ee646d8f3b8af10c5aae642591d)
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
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.SecretSource",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7589ccb89a8dd1c879cf0272e269003e1328953f64e03c0b71db5192466eaa8)
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
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.Snaplock",
    jsii_struct_bases=[],
    name_mapping={
        "default_retention": "defaultRetention",
        "maximum_retention": "maximumRetention",
        "minimum_retention": "minimumRetention",
        "snaplock_type": "snaplockType",
    },
)
class Snaplock:
    def __init__(
        self,
        *,
        default_retention: typing.Optional[builtins.str] = None,
        maximum_retention: typing.Optional[builtins.str] = None,
        minimum_retention: typing.Optional[builtins.str] = None,
        snaplock_type: typing.Optional["SnaplockSnaplockType"] = None,
    ) -> None:
        '''
        :param default_retention: The default retention period for new files in the SnapLock volume.
        :param maximum_retention: The maximum retention period for the SnapLock volume.
        :param minimum_retention: The minimum retention period for the SnapLock volume.
        :param snaplock_type: The SnapLock type of the volume.

        :schema: Snaplock
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22580f9c82f86b694febdc1c7781260ae543f065ca84b91e1e50908773ae505b)
            check_type(argname="argument default_retention", value=default_retention, expected_type=type_hints["default_retention"])
            check_type(argname="argument maximum_retention", value=maximum_retention, expected_type=type_hints["maximum_retention"])
            check_type(argname="argument minimum_retention", value=minimum_retention, expected_type=type_hints["minimum_retention"])
            check_type(argname="argument snaplock_type", value=snaplock_type, expected_type=type_hints["snaplock_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_retention is not None:
            self._values["default_retention"] = default_retention
        if maximum_retention is not None:
            self._values["maximum_retention"] = maximum_retention
        if minimum_retention is not None:
            self._values["minimum_retention"] = minimum_retention
        if snaplock_type is not None:
            self._values["snaplock_type"] = snaplock_type

    @builtins.property
    def default_retention(self) -> typing.Optional[builtins.str]:
        '''The default retention period for new files in the SnapLock volume.

        :schema: Snaplock#DefaultRetention
        '''
        result = self._values.get("default_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_retention(self) -> typing.Optional[builtins.str]:
        '''The maximum retention period for the SnapLock volume.

        :schema: Snaplock#MaximumRetention
        '''
        result = self._values.get("maximum_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_retention(self) -> typing.Optional[builtins.str]:
        '''The minimum retention period for the SnapLock volume.

        :schema: Snaplock#MinimumRetention
        '''
        result = self._values.get("minimum_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snaplock_type(self) -> typing.Optional["SnaplockSnaplockType"]:
        '''The SnapLock type of the volume.

        :schema: Snaplock#SnaplockType
        '''
        result = self._values.get("snaplock_type")
        return typing.cast(typing.Optional["SnaplockSnaplockType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Snaplock(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.SnaplockSnaplockType")
class SnaplockSnaplockType(enum.Enum):
    '''The SnapLock type of the volume.

    :schema: SnaplockSnaplockType
    '''

    COMPLIANCE = "COMPLIANCE"
    '''compliance.'''
    ENTERPRISE = "ENTERPRISE"
    '''enterprise.'''
    NON_UNDERSCORE_SNAPLOCK = "NON_UNDERSCORE_SNAPLOCK"
    '''non_snaplock.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-volume.Tiering",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "min_cooling_days": "minCoolingDays"},
)
class Tiering:
    def __init__(
        self,
        *,
        policy: "TieringPolicy",
        min_cooling_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param policy: Policy that determines whether the user data blocks of a volume in a FabricPool will be tiered to the capacity pool storage tier when they become cold.
        :param min_cooling_days: This parameter specifies the minimum number of days that user data blocks of the volume must be cooled before they can be considered cold and tiered out to the capacity pool storage tier.

        :schema: Tiering
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71025f0bd9ad0231a6137bebe501256ff6678de4824312326b2f55d66efec804)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument min_cooling_days", value=min_cooling_days, expected_type=type_hints["min_cooling_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
        }
        if min_cooling_days is not None:
            self._values["min_cooling_days"] = min_cooling_days

    @builtins.property
    def policy(self) -> "TieringPolicy":
        '''Policy that determines whether the user data blocks of a volume in a FabricPool will be tiered to the capacity pool storage tier when they become cold.

        :schema: Tiering#Policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast("TieringPolicy", result)

    @builtins.property
    def min_cooling_days(self) -> typing.Optional[jsii.Number]:
        '''This parameter specifies the minimum number of days that user data blocks of the volume must be cooled before they can be considered cold and tiered out to the capacity pool storage tier.

        :schema: Tiering#MinCoolingDays
        '''
        result = self._values.get("min_cooling_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tiering(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/netapp-fsxn-volume.TieringPolicy")
class TieringPolicy(enum.Enum):
    '''Policy that determines whether the user data blocks of a volume in a FabricPool will be tiered to the capacity pool storage tier when they become cold.

    :schema: TieringPolicy
    '''

    ALL = "ALL"
    '''all.'''
    AUTO = "AUTO"
    '''auto.'''
    NONE = "NONE"
    '''none.'''
    SNAPSHOT_UNDERSCORE_ONLY = "SNAPSHOT_UNDERSCORE_ONLY"
    '''snapshot_only.'''


__all__ = [
    "Autosize",
    "AutosizeMode",
    "CfnVolume",
    "CfnVolumeProps",
    "CfnVolumePropsAntiRansomwareState",
    "CfnVolumePropsState",
    "CfnVolumePropsStyle",
    "CfnVolumePropsType",
    "Clone",
    "Efficiency",
    "EfficiencyCompaction",
    "EfficiencyCompression",
    "EfficiencyCrossVolumeDedupe",
    "EfficiencyDedupe",
    "NameWithUuidRef",
    "Nas",
    "NasSecurityStyle",
    "OntapTag",
    "PasswordSource",
    "SecretSource",
    "Snaplock",
    "SnaplockSnaplockType",
    "Tiering",
    "TieringPolicy",
]

publication.publish()

def _typecheckingstub__1eafd31d3ac511b88152be9605aac6fb5d590871608d76cc45c2de443231e202(
    *,
    grow_threshold: typing.Optional[jsii.Number] = None,
    maximum: typing.Optional[jsii.Number] = None,
    minimum: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[AutosizeMode] = None,
    shrink_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7807739269ec53ee2d3e5f59703fde795ad4642df968ba8d306b23cbde5690(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    name: builtins.str,
    svm: typing.Union[NameWithUuidRef, typing.Dict[builtins.str, typing.Any]],
    aggregates: typing.Optional[typing.Sequence[builtins.str]] = None,
    anti_ransomware_state: typing.Optional[CfnVolumePropsAntiRansomwareState] = None,
    autosize: typing.Optional[typing.Union[Autosize, typing.Dict[builtins.str, typing.Any]]] = None,
    clone: typing.Optional[typing.Union[Clone, typing.Dict[builtins.str, typing.Any]]] = None,
    constituents_per_aggregate: typing.Optional[jsii.Number] = None,
    efficiency: typing.Optional[typing.Union[Efficiency, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption: typing.Optional[builtins.bool] = None,
    nas: typing.Optional[typing.Union[Nas, typing.Dict[builtins.str, typing.Any]]] = None,
    ontap_tags: typing.Optional[typing.Sequence[typing.Union[OntapTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    size: typing.Optional[jsii.Number] = None,
    snaplock: typing.Optional[typing.Union[Snaplock, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshot_policy: typing.Optional[builtins.str] = None,
    state: typing.Optional[CfnVolumePropsState] = None,
    style: typing.Optional[CfnVolumePropsStyle] = None,
    tiering: typing.Optional[typing.Union[Tiering, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[CfnVolumePropsType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e5f166fc7fcfd76c3d97f547dbade9303d259ebfa09c598fb8ff16ab076d07(
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    name: builtins.str,
    svm: typing.Union[NameWithUuidRef, typing.Dict[builtins.str, typing.Any]],
    aggregates: typing.Optional[typing.Sequence[builtins.str]] = None,
    anti_ransomware_state: typing.Optional[CfnVolumePropsAntiRansomwareState] = None,
    autosize: typing.Optional[typing.Union[Autosize, typing.Dict[builtins.str, typing.Any]]] = None,
    clone: typing.Optional[typing.Union[Clone, typing.Dict[builtins.str, typing.Any]]] = None,
    constituents_per_aggregate: typing.Optional[jsii.Number] = None,
    efficiency: typing.Optional[typing.Union[Efficiency, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption: typing.Optional[builtins.bool] = None,
    nas: typing.Optional[typing.Union[Nas, typing.Dict[builtins.str, typing.Any]]] = None,
    ontap_tags: typing.Optional[typing.Sequence[typing.Union[OntapTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    size: typing.Optional[jsii.Number] = None,
    snaplock: typing.Optional[typing.Union[Snaplock, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshot_policy: typing.Optional[builtins.str] = None,
    state: typing.Optional[CfnVolumePropsState] = None,
    style: typing.Optional[CfnVolumePropsStyle] = None,
    tiering: typing.Optional[typing.Union[Tiering, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[CfnVolumePropsType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ca653fa1fb2699547c2f1e3d189431bf9e1efec2748d591e29f5a9952ef26a(
    *,
    parent_svm: typing.Union[NameWithUuidRef, typing.Dict[builtins.str, typing.Any]],
    parent_volume: typing.Union[NameWithUuidRef, typing.Dict[builtins.str, typing.Any]],
    is_cloned: typing.Optional[builtins.bool] = None,
    parent_snapshot: typing.Optional[typing.Union[NameWithUuidRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb2ec2444fcae48fb646df9ccceb5aa519cd20996005728f29d47e77d847f45(
    *,
    compaction: typing.Optional[EfficiencyCompaction] = None,
    compression: typing.Optional[EfficiencyCompression] = None,
    cross_volume_dedupe: typing.Optional[EfficiencyCrossVolumeDedupe] = None,
    dedupe: typing.Optional[EfficiencyDedupe] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2104ab1a6d47ece4db45e93d253fc69be460d3d4751e2f1317d9a06a3bdcb2(
    *,
    name: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a614936ac5249a54ae4a76658502f7acbb0ae9ad126716611fd350b5da16cbb0(
    *,
    export_policy: typing.Optional[builtins.str] = None,
    junction_path: typing.Optional[builtins.str] = None,
    security_style: typing.Optional[NasSecurityStyle] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3e576eca07c3184f415caf761c184635c9513d714bf51037204091c94ee646(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9db357e22185b084e370631d5cbcf6123291ee646d8f3b8af10c5aae642591d(
    *,
    secret: typing.Union[SecretSource, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7589ccb89a8dd1c879cf0272e269003e1328953f64e03c0b71db5192466eaa8(
    *,
    secret_arn: builtins.str,
    secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22580f9c82f86b694febdc1c7781260ae543f065ca84b91e1e50908773ae505b(
    *,
    default_retention: typing.Optional[builtins.str] = None,
    maximum_retention: typing.Optional[builtins.str] = None,
    minimum_retention: typing.Optional[builtins.str] = None,
    snaplock_type: typing.Optional[SnaplockSnaplockType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71025f0bd9ad0231a6137bebe501256ff6678de4824312326b2f55d66efec804(
    *,
    policy: TieringPolicy,
    min_cooling_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
