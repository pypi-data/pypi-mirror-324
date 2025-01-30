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
    'GetEndpointResult',
    'AwaitableGetEndpointResult',
    'get_endpoint',
    'get_endpoint_output',
]

@pulumi.output_type
class GetEndpointResult:
    def __init__(__self__, arn=None, cidr_block=None, creation_time=None, failed_reason=None, id=None, network_interfaces=None, status=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if cidr_block and not isinstance(cidr_block, str):
            raise TypeError("Expected argument 'cidr_block' to be a str")
        pulumi.set(__self__, "cidr_block", cidr_block)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if failed_reason and not isinstance(failed_reason, dict):
            raise TypeError("Expected argument 'failed_reason' to be a dict")
        pulumi.set(__self__, "failed_reason", failed_reason)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError("Expected argument 'network_interfaces' to be a list")
        pulumi.set(__self__, "network_interfaces", network_interfaces)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the endpoint.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> Optional[str]:
        """
        The VPC CIDR committed by this endpoint.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        The time the endpoint was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="failedReason")
    def failed_reason(self) -> Optional['outputs.EndpointFailedReason']:
        """
        The failure reason, if any, for a create or delete endpoint operation.
        """
        return pulumi.get(self, "failed_reason")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the endpoint.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[Sequence['outputs.EndpointNetworkInterface']]:
        """
        The network interfaces of the endpoint.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter
    def status(self) -> Optional['EndpointStatus']:
        """
        The status of the endpoint.
        """
        return pulumi.get(self, "status")


class AwaitableGetEndpointResult(GetEndpointResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEndpointResult(
            arn=self.arn,
            cidr_block=self.cidr_block,
            creation_time=self.creation_time,
            failed_reason=self.failed_reason,
            id=self.id,
            network_interfaces=self.network_interfaces,
            status=self.status)


def get_endpoint(arn: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEndpointResult:
    """
    Resource Type Definition for AWS::S3Outposts::Endpoint


    :param str arn: The Amazon Resource Name (ARN) of the endpoint.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:s3outposts:getEndpoint', __args__, opts=opts, typ=GetEndpointResult).value

    return AwaitableGetEndpointResult(
        arn=pulumi.get(__ret__, 'arn'),
        cidr_block=pulumi.get(__ret__, 'cidr_block'),
        creation_time=pulumi.get(__ret__, 'creation_time'),
        failed_reason=pulumi.get(__ret__, 'failed_reason'),
        id=pulumi.get(__ret__, 'id'),
        network_interfaces=pulumi.get(__ret__, 'network_interfaces'),
        status=pulumi.get(__ret__, 'status'))
def get_endpoint_output(arn: Optional[pulumi.Input[str]] = None,
                        opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetEndpointResult]:
    """
    Resource Type Definition for AWS::S3Outposts::Endpoint


    :param str arn: The Amazon Resource Name (ARN) of the endpoint.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:s3outposts:getEndpoint', __args__, opts=opts, typ=GetEndpointResult)
    return __ret__.apply(lambda __response__: GetEndpointResult(
        arn=pulumi.get(__response__, 'arn'),
        cidr_block=pulumi.get(__response__, 'cidr_block'),
        creation_time=pulumi.get(__response__, 'creation_time'),
        failed_reason=pulumi.get(__response__, 'failed_reason'),
        id=pulumi.get(__response__, 'id'),
        network_interfaces=pulumi.get(__response__, 'network_interfaces'),
        status=pulumi.get(__response__, 'status')))
