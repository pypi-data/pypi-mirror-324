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

__all__ = [
    'GetWirelessGatewayResult',
    'AwaitableGetWirelessGatewayResult',
    'get_wireless_gateway',
    'get_wireless_gateway_output',
]

@pulumi.output_type
class GetWirelessGatewayResult:
    def __init__(__self__, arn=None, description=None, id=None, last_uplink_received_at=None, lo_ra_wan=None, name=None, tags=None, thing_arn=None, thing_name=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_uplink_received_at and not isinstance(last_uplink_received_at, str):
            raise TypeError("Expected argument 'last_uplink_received_at' to be a str")
        pulumi.set(__self__, "last_uplink_received_at", last_uplink_received_at)
        if lo_ra_wan and not isinstance(lo_ra_wan, dict):
            raise TypeError("Expected argument 'lo_ra_wan' to be a dict")
        pulumi.set(__self__, "lo_ra_wan", lo_ra_wan)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if thing_arn and not isinstance(thing_arn, str):
            raise TypeError("Expected argument 'thing_arn' to be a str")
        pulumi.set(__self__, "thing_arn", thing_arn)
        if thing_name and not isinstance(thing_name, str):
            raise TypeError("Expected argument 'thing_name' to be a str")
        pulumi.set(__self__, "thing_name", thing_name)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Arn for Wireless Gateway. Returned upon successful create.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of Wireless Gateway.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Id for Wireless Gateway. Returned upon successful create.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastUplinkReceivedAt")
    def last_uplink_received_at(self) -> Optional[str]:
        """
        The date and time when the most recent uplink was received.
        """
        return pulumi.get(self, "last_uplink_received_at")

    @property
    @pulumi.getter(name="loRaWan")
    def lo_ra_wan(self) -> Optional['outputs.WirelessGatewayLoRaWanGateway']:
        """
        The combination of Package, Station and Model which represents the version of the LoRaWAN Wireless Gateway.
        """
        return pulumi.get(self, "lo_ra_wan")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of Wireless Gateway.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of key-value pairs that contain metadata for the gateway.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="thingArn")
    def thing_arn(self) -> Optional[str]:
        """
        Thing Arn. Passed into Update to associate a Thing with the Wireless Gateway.
        """
        return pulumi.get(self, "thing_arn")

    @property
    @pulumi.getter(name="thingName")
    def thing_name(self) -> Optional[str]:
        """
        Thing Name. If there is a Thing created, this can be returned with a Get call.
        """
        return pulumi.get(self, "thing_name")


class AwaitableGetWirelessGatewayResult(GetWirelessGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWirelessGatewayResult(
            arn=self.arn,
            description=self.description,
            id=self.id,
            last_uplink_received_at=self.last_uplink_received_at,
            lo_ra_wan=self.lo_ra_wan,
            name=self.name,
            tags=self.tags,
            thing_arn=self.thing_arn,
            thing_name=self.thing_name)


def get_wireless_gateway(id: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWirelessGatewayResult:
    """
    Create and manage wireless gateways, including LoRa gateways.


    :param str id: Id for Wireless Gateway. Returned upon successful create.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iotwireless:getWirelessGateway', __args__, opts=opts, typ=GetWirelessGatewayResult).value

    return AwaitableGetWirelessGatewayResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        last_uplink_received_at=pulumi.get(__ret__, 'last_uplink_received_at'),
        lo_ra_wan=pulumi.get(__ret__, 'lo_ra_wan'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'),
        thing_arn=pulumi.get(__ret__, 'thing_arn'),
        thing_name=pulumi.get(__ret__, 'thing_name'))
def get_wireless_gateway_output(id: Optional[pulumi.Input[str]] = None,
                                opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetWirelessGatewayResult]:
    """
    Create and manage wireless gateways, including LoRa gateways.


    :param str id: Id for Wireless Gateway. Returned upon successful create.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iotwireless:getWirelessGateway', __args__, opts=opts, typ=GetWirelessGatewayResult)
    return __ret__.apply(lambda __response__: GetWirelessGatewayResult(
        arn=pulumi.get(__response__, 'arn'),
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        last_uplink_received_at=pulumi.get(__response__, 'last_uplink_received_at'),
        lo_ra_wan=pulumi.get(__response__, 'lo_ra_wan'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags'),
        thing_arn=pulumi.get(__response__, 'thing_arn'),
        thing_name=pulumi.get(__response__, 'thing_name')))
