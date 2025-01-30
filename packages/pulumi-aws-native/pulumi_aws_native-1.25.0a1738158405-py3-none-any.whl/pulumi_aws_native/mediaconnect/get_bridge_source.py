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
from ._enums import *

__all__ = [
    'GetBridgeSourceResult',
    'AwaitableGetBridgeSourceResult',
    'get_bridge_source',
    'get_bridge_source_output',
]

@pulumi.output_type
class GetBridgeSourceResult:
    def __init__(__self__, flow_source=None, network_source=None):
        if flow_source and not isinstance(flow_source, dict):
            raise TypeError("Expected argument 'flow_source' to be a dict")
        pulumi.set(__self__, "flow_source", flow_source)
        if network_source and not isinstance(network_source, dict):
            raise TypeError("Expected argument 'network_source' to be a dict")
        pulumi.set(__self__, "network_source", network_source)

    @property
    @pulumi.getter(name="flowSource")
    def flow_source(self) -> Optional['outputs.BridgeSourceBridgeFlowSource']:
        """
        Add a flow source to an existing bridge.
        """
        return pulumi.get(self, "flow_source")

    @property
    @pulumi.getter(name="networkSource")
    def network_source(self) -> Optional['outputs.BridgeSourceBridgeNetworkSource']:
        """
        Add a network source to an existing bridge.
        """
        return pulumi.get(self, "network_source")


class AwaitableGetBridgeSourceResult(GetBridgeSourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBridgeSourceResult(
            flow_source=self.flow_source,
            network_source=self.network_source)


def get_bridge_source(bridge_arn: Optional[str] = None,
                      name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBridgeSourceResult:
    """
    Resource schema for AWS::MediaConnect::BridgeSource


    :param str bridge_arn: The Amazon Resource Number (ARN) of the bridge.
    :param str name: The name of the source.
    """
    __args__ = dict()
    __args__['bridgeArn'] = bridge_arn
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:mediaconnect:getBridgeSource', __args__, opts=opts, typ=GetBridgeSourceResult).value

    return AwaitableGetBridgeSourceResult(
        flow_source=pulumi.get(__ret__, 'flow_source'),
        network_source=pulumi.get(__ret__, 'network_source'))
def get_bridge_source_output(bridge_arn: Optional[pulumi.Input[str]] = None,
                             name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetBridgeSourceResult]:
    """
    Resource schema for AWS::MediaConnect::BridgeSource


    :param str bridge_arn: The Amazon Resource Number (ARN) of the bridge.
    :param str name: The name of the source.
    """
    __args__ = dict()
    __args__['bridgeArn'] = bridge_arn
    __args__['name'] = name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:mediaconnect:getBridgeSource', __args__, opts=opts, typ=GetBridgeSourceResult)
    return __ret__.apply(lambda __response__: GetBridgeSourceResult(
        flow_source=pulumi.get(__response__, 'flow_source'),
        network_source=pulumi.get(__response__, 'network_source')))
