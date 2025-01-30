# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities
from .. import outputs as _root_outputs
from ._enums import *

__all__ = [
    'GetLocationEfsResult',
    'AwaitableGetLocationEfsResult',
    'get_location_efs',
    'get_location_efs_output',
]

@pulumi.output_type
class GetLocationEfsResult:
    def __init__(__self__, access_point_arn=None, file_system_access_role_arn=None, in_transit_encryption=None, location_arn=None, location_uri=None, tags=None):
        if access_point_arn and not isinstance(access_point_arn, str):
            raise TypeError("Expected argument 'access_point_arn' to be a str")
        pulumi.set(__self__, "access_point_arn", access_point_arn)
        if file_system_access_role_arn and not isinstance(file_system_access_role_arn, str):
            raise TypeError("Expected argument 'file_system_access_role_arn' to be a str")
        pulumi.set(__self__, "file_system_access_role_arn", file_system_access_role_arn)
        if in_transit_encryption and not isinstance(in_transit_encryption, str):
            raise TypeError("Expected argument 'in_transit_encryption' to be a str")
        pulumi.set(__self__, "in_transit_encryption", in_transit_encryption)
        if location_arn and not isinstance(location_arn, str):
            raise TypeError("Expected argument 'location_arn' to be a str")
        pulumi.set(__self__, "location_arn", location_arn)
        if location_uri and not isinstance(location_uri, str):
            raise TypeError("Expected argument 'location_uri' to be a str")
        pulumi.set(__self__, "location_uri", location_uri)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="accessPointArn")
    def access_point_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for the Amazon EFS Access point that DataSync uses when accessing the EFS file system.
        """
        return pulumi.get(self, "access_point_arn")

    @property
    @pulumi.getter(name="fileSystemAccessRoleArn")
    def file_system_access_role_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the AWS IAM role that the DataSync will assume when mounting the EFS file system.
        """
        return pulumi.get(self, "file_system_access_role_arn")

    @property
    @pulumi.getter(name="inTransitEncryption")
    def in_transit_encryption(self) -> Optional['LocationEfsInTransitEncryption']:
        """
        Protocol that is used for encrypting the traffic exchanged between the DataSync Agent and the EFS file system.
        """
        return pulumi.get(self, "in_transit_encryption")

    @property
    @pulumi.getter(name="locationArn")
    def location_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the Amazon EFS file system location that is created.
        """
        return pulumi.get(self, "location_arn")

    @property
    @pulumi.getter(name="locationUri")
    def location_uri(self) -> Optional[str]:
        """
        The URL of the EFS location that was described.
        """
        return pulumi.get(self, "location_uri")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetLocationEfsResult(GetLocationEfsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLocationEfsResult(
            access_point_arn=self.access_point_arn,
            file_system_access_role_arn=self.file_system_access_role_arn,
            in_transit_encryption=self.in_transit_encryption,
            location_arn=self.location_arn,
            location_uri=self.location_uri,
            tags=self.tags)


def get_location_efs(location_arn: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLocationEfsResult:
    """
    Resource schema for AWS::DataSync::LocationEFS.


    :param str location_arn: The Amazon Resource Name (ARN) of the Amazon EFS file system location that is created.
    """
    __args__ = dict()
    __args__['locationArn'] = location_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:datasync:getLocationEfs', __args__, opts=opts, typ=GetLocationEfsResult).value

    return AwaitableGetLocationEfsResult(
        access_point_arn=pulumi.get(__ret__, 'access_point_arn'),
        file_system_access_role_arn=pulumi.get(__ret__, 'file_system_access_role_arn'),
        in_transit_encryption=pulumi.get(__ret__, 'in_transit_encryption'),
        location_arn=pulumi.get(__ret__, 'location_arn'),
        location_uri=pulumi.get(__ret__, 'location_uri'),
        tags=pulumi.get(__ret__, 'tags'))
def get_location_efs_output(location_arn: Optional[pulumi.Input[str]] = None,
                            opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetLocationEfsResult]:
    """
    Resource schema for AWS::DataSync::LocationEFS.


    :param str location_arn: The Amazon Resource Name (ARN) of the Amazon EFS file system location that is created.
    """
    __args__ = dict()
    __args__['locationArn'] = location_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:datasync:getLocationEfs', __args__, opts=opts, typ=GetLocationEfsResult)
    return __ret__.apply(lambda __response__: GetLocationEfsResult(
        access_point_arn=pulumi.get(__response__, 'access_point_arn'),
        file_system_access_role_arn=pulumi.get(__response__, 'file_system_access_role_arn'),
        in_transit_encryption=pulumi.get(__response__, 'in_transit_encryption'),
        location_arn=pulumi.get(__response__, 'location_arn'),
        location_uri=pulumi.get(__response__, 'location_uri'),
        tags=pulumi.get(__response__, 'tags')))
