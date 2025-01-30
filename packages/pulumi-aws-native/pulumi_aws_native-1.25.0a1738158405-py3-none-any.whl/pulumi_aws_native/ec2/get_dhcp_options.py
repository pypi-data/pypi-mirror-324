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
    'GetDhcpOptionsResult',
    'AwaitableGetDhcpOptionsResult',
    'get_dhcp_options',
    'get_dhcp_options_output',
]

@pulumi.output_type
class GetDhcpOptionsResult:
    def __init__(__self__, dhcp_options_id=None, tags=None):
        if dhcp_options_id and not isinstance(dhcp_options_id, str):
            raise TypeError("Expected argument 'dhcp_options_id' to be a str")
        pulumi.set(__self__, "dhcp_options_id", dhcp_options_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="dhcpOptionsId")
    def dhcp_options_id(self) -> Optional[str]:
        """
        The ID of the DHCP options set.
        """
        return pulumi.get(self, "dhcp_options_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Any tags assigned to the DHCP options set.
        """
        return pulumi.get(self, "tags")


class AwaitableGetDhcpOptionsResult(GetDhcpOptionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDhcpOptionsResult(
            dhcp_options_id=self.dhcp_options_id,
            tags=self.tags)


def get_dhcp_options(dhcp_options_id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDhcpOptionsResult:
    """
    Resource Type definition for AWS::EC2::DHCPOptions


    :param str dhcp_options_id: The ID of the DHCP options set.
    """
    __args__ = dict()
    __args__['dhcpOptionsId'] = dhcp_options_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getDhcpOptions', __args__, opts=opts, typ=GetDhcpOptionsResult).value

    return AwaitableGetDhcpOptionsResult(
        dhcp_options_id=pulumi.get(__ret__, 'dhcp_options_id'),
        tags=pulumi.get(__ret__, 'tags'))
def get_dhcp_options_output(dhcp_options_id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetDhcpOptionsResult]:
    """
    Resource Type definition for AWS::EC2::DHCPOptions


    :param str dhcp_options_id: The ID of the DHCP options set.
    """
    __args__ = dict()
    __args__['dhcpOptionsId'] = dhcp_options_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getDhcpOptions', __args__, opts=opts, typ=GetDhcpOptionsResult)
    return __ret__.apply(lambda __response__: GetDhcpOptionsResult(
        dhcp_options_id=pulumi.get(__response__, 'dhcp_options_id'),
        tags=pulumi.get(__response__, 'tags')))
