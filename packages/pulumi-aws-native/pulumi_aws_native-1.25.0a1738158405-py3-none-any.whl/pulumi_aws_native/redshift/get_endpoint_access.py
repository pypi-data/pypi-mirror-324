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

__all__ = [
    'GetEndpointAccessResult',
    'AwaitableGetEndpointAccessResult',
    'get_endpoint_access',
    'get_endpoint_access_output',
]

@pulumi.output_type
class GetEndpointAccessResult:
    def __init__(__self__, address=None, endpoint_create_time=None, endpoint_status=None, port=None, vpc_endpoint=None, vpc_security_group_ids=None, vpc_security_groups=None):
        if address and not isinstance(address, str):
            raise TypeError("Expected argument 'address' to be a str")
        pulumi.set(__self__, "address", address)
        if endpoint_create_time and not isinstance(endpoint_create_time, str):
            raise TypeError("Expected argument 'endpoint_create_time' to be a str")
        pulumi.set(__self__, "endpoint_create_time", endpoint_create_time)
        if endpoint_status and not isinstance(endpoint_status, str):
            raise TypeError("Expected argument 'endpoint_status' to be a str")
        pulumi.set(__self__, "endpoint_status", endpoint_status)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if vpc_endpoint and not isinstance(vpc_endpoint, dict):
            raise TypeError("Expected argument 'vpc_endpoint' to be a dict")
        pulumi.set(__self__, "vpc_endpoint", vpc_endpoint)
        if vpc_security_group_ids and not isinstance(vpc_security_group_ids, list):
            raise TypeError("Expected argument 'vpc_security_group_ids' to be a list")
        pulumi.set(__self__, "vpc_security_group_ids", vpc_security_group_ids)
        if vpc_security_groups and not isinstance(vpc_security_groups, list):
            raise TypeError("Expected argument 'vpc_security_groups' to be a list")
        pulumi.set(__self__, "vpc_security_groups", vpc_security_groups)

    @property
    @pulumi.getter
    def address(self) -> Optional[str]:
        """
        The DNS address of the endpoint.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="endpointCreateTime")
    def endpoint_create_time(self) -> Optional[str]:
        """
        The time (UTC) that the endpoint was created.
        """
        return pulumi.get(self, "endpoint_create_time")

    @property
    @pulumi.getter(name="endpointStatus")
    def endpoint_status(self) -> Optional[str]:
        """
        The status of the endpoint.
        """
        return pulumi.get(self, "endpoint_status")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        The port number on which the cluster accepts incoming connections.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="vpcEndpoint")
    def vpc_endpoint(self) -> Optional['outputs.VpcEndpointProperties']:
        """
        The connection endpoint for connecting to an Amazon Redshift cluster through the proxy.
        """
        return pulumi.get(self, "vpc_endpoint")

    @property
    @pulumi.getter(name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> Optional[Sequence[str]]:
        """
        A list of vpc security group ids to apply to the created endpoint access.
        """
        return pulumi.get(self, "vpc_security_group_ids")

    @property
    @pulumi.getter(name="vpcSecurityGroups")
    def vpc_security_groups(self) -> Optional[Sequence['outputs.EndpointAccessVpcSecurityGroup']]:
        """
        A list of Virtual Private Cloud (VPC) security groups to be associated with the endpoint.
        """
        return pulumi.get(self, "vpc_security_groups")


class AwaitableGetEndpointAccessResult(GetEndpointAccessResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEndpointAccessResult(
            address=self.address,
            endpoint_create_time=self.endpoint_create_time,
            endpoint_status=self.endpoint_status,
            port=self.port,
            vpc_endpoint=self.vpc_endpoint,
            vpc_security_group_ids=self.vpc_security_group_ids,
            vpc_security_groups=self.vpc_security_groups)


def get_endpoint_access(endpoint_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEndpointAccessResult:
    """
    Resource schema for a Redshift-managed VPC endpoint.


    :param str endpoint_name: The name of the endpoint.
    """
    __args__ = dict()
    __args__['endpointName'] = endpoint_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:redshift:getEndpointAccess', __args__, opts=opts, typ=GetEndpointAccessResult).value

    return AwaitableGetEndpointAccessResult(
        address=pulumi.get(__ret__, 'address'),
        endpoint_create_time=pulumi.get(__ret__, 'endpoint_create_time'),
        endpoint_status=pulumi.get(__ret__, 'endpoint_status'),
        port=pulumi.get(__ret__, 'port'),
        vpc_endpoint=pulumi.get(__ret__, 'vpc_endpoint'),
        vpc_security_group_ids=pulumi.get(__ret__, 'vpc_security_group_ids'),
        vpc_security_groups=pulumi.get(__ret__, 'vpc_security_groups'))
def get_endpoint_access_output(endpoint_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetEndpointAccessResult]:
    """
    Resource schema for a Redshift-managed VPC endpoint.


    :param str endpoint_name: The name of the endpoint.
    """
    __args__ = dict()
    __args__['endpointName'] = endpoint_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:redshift:getEndpointAccess', __args__, opts=opts, typ=GetEndpointAccessResult)
    return __ret__.apply(lambda __response__: GetEndpointAccessResult(
        address=pulumi.get(__response__, 'address'),
        endpoint_create_time=pulumi.get(__response__, 'endpoint_create_time'),
        endpoint_status=pulumi.get(__response__, 'endpoint_status'),
        port=pulumi.get(__response__, 'port'),
        vpc_endpoint=pulumi.get(__response__, 'vpc_endpoint'),
        vpc_security_group_ids=pulumi.get(__response__, 'vpc_security_group_ids'),
        vpc_security_groups=pulumi.get(__response__, 'vpc_security_groups')))
