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
    'GetSubnetRouteTableAssociationResult',
    'AwaitableGetSubnetRouteTableAssociationResult',
    'get_subnet_route_table_association',
    'get_subnet_route_table_association_output',
]

@pulumi.output_type
class GetSubnetRouteTableAssociationResult:
    def __init__(__self__, id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the subnet route table association.
        """
        return pulumi.get(self, "id")


class AwaitableGetSubnetRouteTableAssociationResult(GetSubnetRouteTableAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubnetRouteTableAssociationResult(
            id=self.id)


def get_subnet_route_table_association(id: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubnetRouteTableAssociationResult:
    """
    Associates a subnet with a route table. The subnet and route table must be in the same VPC. This association causes traffic originating from the subnet to be routed according to the routes in the route table. A route table can be associated with multiple subnets. To create a route table, see [AWS::EC2::RouteTable](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-routetable.html).


    :param str id: The ID of the subnet route table association.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getSubnetRouteTableAssociation', __args__, opts=opts, typ=GetSubnetRouteTableAssociationResult).value

    return AwaitableGetSubnetRouteTableAssociationResult(
        id=pulumi.get(__ret__, 'id'))
def get_subnet_route_table_association_output(id: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSubnetRouteTableAssociationResult]:
    """
    Associates a subnet with a route table. The subnet and route table must be in the same VPC. This association causes traffic originating from the subnet to be routed according to the routes in the route table. A route table can be associated with multiple subnets. To create a route table, see [AWS::EC2::RouteTable](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-routetable.html).


    :param str id: The ID of the subnet route table association.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getSubnetRouteTableAssociation', __args__, opts=opts, typ=GetSubnetRouteTableAssociationResult)
    return __ret__.apply(lambda __response__: GetSubnetRouteTableAssociationResult(
        id=pulumi.get(__response__, 'id')))
