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
    'GetSubnetResult',
    'AwaitableGetSubnetResult',
    'get_subnet',
    'get_subnet_output',
]

@pulumi.output_type
class GetSubnetResult:
    def __init__(__self__, assign_ipv6_address_on_creation=None, enable_dns64=None, ipv6_cidr_block=None, ipv6_cidr_blocks=None, map_public_ip_on_launch=None, network_acl_association_id=None, private_dns_name_options_on_launch=None, subnet_id=None, tags=None):
        if assign_ipv6_address_on_creation and not isinstance(assign_ipv6_address_on_creation, bool):
            raise TypeError("Expected argument 'assign_ipv6_address_on_creation' to be a bool")
        pulumi.set(__self__, "assign_ipv6_address_on_creation", assign_ipv6_address_on_creation)
        if enable_dns64 and not isinstance(enable_dns64, bool):
            raise TypeError("Expected argument 'enable_dns64' to be a bool")
        pulumi.set(__self__, "enable_dns64", enable_dns64)
        if ipv6_cidr_block and not isinstance(ipv6_cidr_block, str):
            raise TypeError("Expected argument 'ipv6_cidr_block' to be a str")
        pulumi.set(__self__, "ipv6_cidr_block", ipv6_cidr_block)
        if ipv6_cidr_blocks and not isinstance(ipv6_cidr_blocks, list):
            raise TypeError("Expected argument 'ipv6_cidr_blocks' to be a list")
        pulumi.set(__self__, "ipv6_cidr_blocks", ipv6_cidr_blocks)
        if map_public_ip_on_launch and not isinstance(map_public_ip_on_launch, bool):
            raise TypeError("Expected argument 'map_public_ip_on_launch' to be a bool")
        pulumi.set(__self__, "map_public_ip_on_launch", map_public_ip_on_launch)
        if network_acl_association_id and not isinstance(network_acl_association_id, str):
            raise TypeError("Expected argument 'network_acl_association_id' to be a str")
        pulumi.set(__self__, "network_acl_association_id", network_acl_association_id)
        if private_dns_name_options_on_launch and not isinstance(private_dns_name_options_on_launch, dict):
            raise TypeError("Expected argument 'private_dns_name_options_on_launch' to be a dict")
        pulumi.set(__self__, "private_dns_name_options_on_launch", private_dns_name_options_on_launch)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="assignIpv6AddressOnCreation")
    def assign_ipv6_address_on_creation(self) -> Optional[bool]:
        """
        Indicates whether a network interface created in this subnet receives an IPv6 address. The default value is ``false``.
         If you specify ``AssignIpv6AddressOnCreation``, you must also specify an IPv6 CIDR block.
        """
        return pulumi.get(self, "assign_ipv6_address_on_creation")

    @property
    @pulumi.getter(name="enableDns64")
    def enable_dns64(self) -> Optional[bool]:
        """
        Indicates whether DNS queries made to the Amazon-provided DNS Resolver in this subnet should return synthetic IPv6 addresses for IPv4-only destinations.
          You must first configure a NAT gateway in a public subnet (separate from the subnet containing the IPv6-only workloads). For example, the subnet containing the NAT gateway should have a ``0.0.0.0/0`` route pointing to the internet gateway. For more information, see [Configure DNS64 and NAT64](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-nat64-dns64.html#nat-gateway-nat64-dns64-walkthrough) in the *User Guide*.
        """
        return pulumi.get(self, "enable_dns64")

    @property
    @pulumi.getter(name="ipv6CidrBlock")
    def ipv6_cidr_block(self) -> Optional[str]:
        """
        The IPv6 CIDR block.
         If you specify ``AssignIpv6AddressOnCreation``, you must also specify an IPv6 CIDR block.
        """
        return pulumi.get(self, "ipv6_cidr_block")

    @property
    @pulumi.getter(name="ipv6CidrBlocks")
    def ipv6_cidr_blocks(self) -> Optional[Sequence[str]]:
        """
        The IPv6 CIDR blocks that are associated with the subnet.
        """
        return pulumi.get(self, "ipv6_cidr_blocks")

    @property
    @pulumi.getter(name="mapPublicIpOnLaunch")
    def map_public_ip_on_launch(self) -> Optional[bool]:
        """
        Indicates whether instances launched in this subnet receive a public IPv4 address. The default value is ``false``.
          AWS charges for all public IPv4 addresses, including public IPv4 addresses associated with running instances and Elastic IP addresses. For more information, see the *Public IPv4 Address* tab on the [VPC pricing page](https://docs.aws.amazon.com/vpc/pricing/).
        """
        return pulumi.get(self, "map_public_ip_on_launch")

    @property
    @pulumi.getter(name="networkAclAssociationId")
    def network_acl_association_id(self) -> Optional[str]:
        """
        The ID of the network ACL that is associated with the subnet's VPC, such as `acl-5fb85d36` .
        """
        return pulumi.get(self, "network_acl_association_id")

    @property
    @pulumi.getter(name="privateDnsNameOptionsOnLaunch")
    def private_dns_name_options_on_launch(self) -> Optional['outputs.PrivateDnsNameOptionsOnLaunchProperties']:
        """
        The hostname type for EC2 instances launched into this subnet and how DNS A and AAAA record queries to the instances should be handled. For more information, see [Amazon EC2 instance hostname types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-naming.html) in the *User Guide*.
         Available options:
          +  EnableResourceNameDnsAAAARecord (true | false)
          +  EnableResourceNameDnsARecord (true | false)
          +  HostnameType (ip-name | resource-name)
        """
        return pulumi.get(self, "private_dns_name_options_on_launch")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[str]:
        """
        The ID of the subnet.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Any tags assigned to the subnet.
        """
        return pulumi.get(self, "tags")


class AwaitableGetSubnetResult(GetSubnetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubnetResult(
            assign_ipv6_address_on_creation=self.assign_ipv6_address_on_creation,
            enable_dns64=self.enable_dns64,
            ipv6_cidr_block=self.ipv6_cidr_block,
            ipv6_cidr_blocks=self.ipv6_cidr_blocks,
            map_public_ip_on_launch=self.map_public_ip_on_launch,
            network_acl_association_id=self.network_acl_association_id,
            private_dns_name_options_on_launch=self.private_dns_name_options_on_launch,
            subnet_id=self.subnet_id,
            tags=self.tags)


def get_subnet(subnet_id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubnetResult:
    """
    Specifies a subnet for the specified VPC.
     For an IPv4 only subnet, specify an IPv4 CIDR block. If the VPC has an IPv6 CIDR block, you can create an IPv6 only subnet or a dual stack subnet instead. For an IPv6 only subnet, specify an IPv6 CIDR block. For a dual stack subnet, specify both an IPv4 CIDR block and an IPv6 CIDR block.
     For more information, see [Subnets for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html) in the *Amazon VPC User Guide*.


    :param str subnet_id: The ID of the subnet.
    """
    __args__ = dict()
    __args__['subnetId'] = subnet_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getSubnet', __args__, opts=opts, typ=GetSubnetResult).value

    return AwaitableGetSubnetResult(
        assign_ipv6_address_on_creation=pulumi.get(__ret__, 'assign_ipv6_address_on_creation'),
        enable_dns64=pulumi.get(__ret__, 'enable_dns64'),
        ipv6_cidr_block=pulumi.get(__ret__, 'ipv6_cidr_block'),
        ipv6_cidr_blocks=pulumi.get(__ret__, 'ipv6_cidr_blocks'),
        map_public_ip_on_launch=pulumi.get(__ret__, 'map_public_ip_on_launch'),
        network_acl_association_id=pulumi.get(__ret__, 'network_acl_association_id'),
        private_dns_name_options_on_launch=pulumi.get(__ret__, 'private_dns_name_options_on_launch'),
        subnet_id=pulumi.get(__ret__, 'subnet_id'),
        tags=pulumi.get(__ret__, 'tags'))
def get_subnet_output(subnet_id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSubnetResult]:
    """
    Specifies a subnet for the specified VPC.
     For an IPv4 only subnet, specify an IPv4 CIDR block. If the VPC has an IPv6 CIDR block, you can create an IPv6 only subnet or a dual stack subnet instead. For an IPv6 only subnet, specify an IPv6 CIDR block. For a dual stack subnet, specify both an IPv4 CIDR block and an IPv6 CIDR block.
     For more information, see [Subnets for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html) in the *Amazon VPC User Guide*.


    :param str subnet_id: The ID of the subnet.
    """
    __args__ = dict()
    __args__['subnetId'] = subnet_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getSubnet', __args__, opts=opts, typ=GetSubnetResult)
    return __ret__.apply(lambda __response__: GetSubnetResult(
        assign_ipv6_address_on_creation=pulumi.get(__response__, 'assign_ipv6_address_on_creation'),
        enable_dns64=pulumi.get(__response__, 'enable_dns64'),
        ipv6_cidr_block=pulumi.get(__response__, 'ipv6_cidr_block'),
        ipv6_cidr_blocks=pulumi.get(__response__, 'ipv6_cidr_blocks'),
        map_public_ip_on_launch=pulumi.get(__response__, 'map_public_ip_on_launch'),
        network_acl_association_id=pulumi.get(__response__, 'network_acl_association_id'),
        private_dns_name_options_on_launch=pulumi.get(__response__, 'private_dns_name_options_on_launch'),
        subnet_id=pulumi.get(__response__, 'subnet_id'),
        tags=pulumi.get(__response__, 'tags')))
