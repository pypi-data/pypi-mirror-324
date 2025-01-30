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

__all__ = [
    'GetFlowVpcInterfaceResult',
    'AwaitableGetFlowVpcInterfaceResult',
    'get_flow_vpc_interface',
    'get_flow_vpc_interface_output',
]

@pulumi.output_type
class GetFlowVpcInterfaceResult:
    def __init__(__self__, network_interface_ids=None, role_arn=None, security_group_ids=None, subnet_id=None):
        if network_interface_ids and not isinstance(network_interface_ids, list):
            raise TypeError("Expected argument 'network_interface_ids' to be a list")
        pulumi.set(__self__, "network_interface_ids", network_interface_ids)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="networkInterfaceIds")
    def network_interface_ids(self) -> Optional[Sequence[str]]:
        """
        IDs of the network interfaces created in customer's account by MediaConnect.
        """
        return pulumi.get(self, "network_interface_ids")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        Role Arn MediaConnect can assume to create ENIs in customer's account.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        """
        Security Group IDs to be used on ENI.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[str]:
        """
        Subnet must be in the AZ of the Flow
        """
        return pulumi.get(self, "subnet_id")


class AwaitableGetFlowVpcInterfaceResult(GetFlowVpcInterfaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFlowVpcInterfaceResult(
            network_interface_ids=self.network_interface_ids,
            role_arn=self.role_arn,
            security_group_ids=self.security_group_ids,
            subnet_id=self.subnet_id)


def get_flow_vpc_interface(flow_arn: Optional[str] = None,
                           name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFlowVpcInterfaceResult:
    """
    Resource schema for AWS::MediaConnect::FlowVpcInterface


    :param str flow_arn: The Amazon Resource Name (ARN), a unique identifier for any AWS resource, of the flow.
    :param str name: Immutable and has to be a unique against other VpcInterfaces in this Flow.
    """
    __args__ = dict()
    __args__['flowArn'] = flow_arn
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:mediaconnect:getFlowVpcInterface', __args__, opts=opts, typ=GetFlowVpcInterfaceResult).value

    return AwaitableGetFlowVpcInterfaceResult(
        network_interface_ids=pulumi.get(__ret__, 'network_interface_ids'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        security_group_ids=pulumi.get(__ret__, 'security_group_ids'),
        subnet_id=pulumi.get(__ret__, 'subnet_id'))
def get_flow_vpc_interface_output(flow_arn: Optional[pulumi.Input[str]] = None,
                                  name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetFlowVpcInterfaceResult]:
    """
    Resource schema for AWS::MediaConnect::FlowVpcInterface


    :param str flow_arn: The Amazon Resource Name (ARN), a unique identifier for any AWS resource, of the flow.
    :param str name: Immutable and has to be a unique against other VpcInterfaces in this Flow.
    """
    __args__ = dict()
    __args__['flowArn'] = flow_arn
    __args__['name'] = name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:mediaconnect:getFlowVpcInterface', __args__, opts=opts, typ=GetFlowVpcInterfaceResult)
    return __ret__.apply(lambda __response__: GetFlowVpcInterfaceResult(
        network_interface_ids=pulumi.get(__response__, 'network_interface_ids'),
        role_arn=pulumi.get(__response__, 'role_arn'),
        security_group_ids=pulumi.get(__response__, 'security_group_ids'),
        subnet_id=pulumi.get(__response__, 'subnet_id')))
