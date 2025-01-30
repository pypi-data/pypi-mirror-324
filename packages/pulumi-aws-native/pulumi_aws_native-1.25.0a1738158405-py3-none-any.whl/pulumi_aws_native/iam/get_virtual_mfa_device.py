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

__all__ = [
    'GetVirtualMfaDeviceResult',
    'AwaitableGetVirtualMfaDeviceResult',
    'get_virtual_mfa_device',
    'get_virtual_mfa_device_output',
]

@pulumi.output_type
class GetVirtualMfaDeviceResult:
    def __init__(__self__, serial_number=None, tags=None, users=None):
        if serial_number and not isinstance(serial_number, str):
            raise TypeError("Expected argument 'serial_number' to be a str")
        pulumi.set(__self__, "serial_number", serial_number)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> Optional[str]:
        """
        Returns the serial number for the specified `AWS::IAM::VirtualMFADevice` resource.
        """
        return pulumi.get(self, "serial_number")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of tags that you want to attach to the new IAM virtual MFA device. Each tag consists of a key name and an associated value. For more information about tagging, see [Tagging IAM resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide* .

        > If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def users(self) -> Optional[Sequence[str]]:
        """
        The IAM user associated with this virtual MFA device.
        """
        return pulumi.get(self, "users")


class AwaitableGetVirtualMfaDeviceResult(GetVirtualMfaDeviceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualMfaDeviceResult(
            serial_number=self.serial_number,
            tags=self.tags,
            users=self.users)


def get_virtual_mfa_device(serial_number: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualMfaDeviceResult:
    """
    Resource Type definition for AWS::IAM::VirtualMFADevice


    :param str serial_number: Returns the serial number for the specified `AWS::IAM::VirtualMFADevice` resource.
    """
    __args__ = dict()
    __args__['serialNumber'] = serial_number
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iam:getVirtualMfaDevice', __args__, opts=opts, typ=GetVirtualMfaDeviceResult).value

    return AwaitableGetVirtualMfaDeviceResult(
        serial_number=pulumi.get(__ret__, 'serial_number'),
        tags=pulumi.get(__ret__, 'tags'),
        users=pulumi.get(__ret__, 'users'))
def get_virtual_mfa_device_output(serial_number: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetVirtualMfaDeviceResult]:
    """
    Resource Type definition for AWS::IAM::VirtualMFADevice


    :param str serial_number: Returns the serial number for the specified `AWS::IAM::VirtualMFADevice` resource.
    """
    __args__ = dict()
    __args__['serialNumber'] = serial_number
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iam:getVirtualMfaDevice', __args__, opts=opts, typ=GetVirtualMfaDeviceResult)
    return __ret__.apply(lambda __response__: GetVirtualMfaDeviceResult(
        serial_number=pulumi.get(__response__, 'serial_number'),
        tags=pulumi.get(__response__, 'tags'),
        users=pulumi.get(__response__, 'users')))
