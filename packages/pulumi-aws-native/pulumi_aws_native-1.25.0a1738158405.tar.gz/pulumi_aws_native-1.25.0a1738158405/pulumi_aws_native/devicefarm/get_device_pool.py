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
from . import outputs
from .. import outputs as _root_outputs
from ._enums import *

__all__ = [
    'GetDevicePoolResult',
    'AwaitableGetDevicePoolResult',
    'get_device_pool',
    'get_device_pool_output',
]

@pulumi.output_type
class GetDevicePoolResult:
    def __init__(__self__, arn=None, description=None, max_devices=None, name=None, rules=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if max_devices and not isinstance(max_devices, int):
            raise TypeError("Expected argument 'max_devices' to be a int")
        pulumi.set(__self__, "max_devices", max_devices)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if rules and not isinstance(rules, list):
            raise TypeError("Expected argument 'rules' to be a list")
        pulumi.set(__self__, "rules", rules)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the device pool. See [Amazon resource names](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) in the *General Reference guide* .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The device pool's description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="maxDevices")
    def max_devices(self) -> Optional[int]:
        """
        The number of devices that Device Farm can add to your device pool. Device Farm adds devices that are available and meet the criteria that you assign for the `rules` parameter. Depending on how many devices meet these constraints, your device pool might contain fewer devices than the value for this parameter.

        By specifying the maximum number of devices, you can control the costs that you incur by running tests.
        """
        return pulumi.get(self, "max_devices")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The device pool's name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.DevicePoolRule']]:
        """
        The device pool's rules.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.

        For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) in the *guide* .
        """
        return pulumi.get(self, "tags")


class AwaitableGetDevicePoolResult(GetDevicePoolResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDevicePoolResult(
            arn=self.arn,
            description=self.description,
            max_devices=self.max_devices,
            name=self.name,
            rules=self.rules,
            tags=self.tags)


def get_device_pool(arn: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDevicePoolResult:
    """
    AWS::DeviceFarm::DevicePool creates a new Device Pool for a given DF Project


    :param str arn: The Amazon Resource Name (ARN) of the device pool. See [Amazon resource names](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) in the *General Reference guide* .
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:devicefarm:getDevicePool', __args__, opts=opts, typ=GetDevicePoolResult).value

    return AwaitableGetDevicePoolResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        max_devices=pulumi.get(__ret__, 'max_devices'),
        name=pulumi.get(__ret__, 'name'),
        rules=pulumi.get(__ret__, 'rules'),
        tags=pulumi.get(__ret__, 'tags'))
def get_device_pool_output(arn: Optional[pulumi.Input[str]] = None,
                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetDevicePoolResult]:
    """
    AWS::DeviceFarm::DevicePool creates a new Device Pool for a given DF Project


    :param str arn: The Amazon Resource Name (ARN) of the device pool. See [Amazon resource names](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) in the *General Reference guide* .
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:devicefarm:getDevicePool', __args__, opts=opts, typ=GetDevicePoolResult)
    return __ret__.apply(lambda __response__: GetDevicePoolResult(
        arn=pulumi.get(__response__, 'arn'),
        description=pulumi.get(__response__, 'description'),
        max_devices=pulumi.get(__response__, 'max_devices'),
        name=pulumi.get(__response__, 'name'),
        rules=pulumi.get(__response__, 'rules'),
        tags=pulumi.get(__response__, 'tags')))
