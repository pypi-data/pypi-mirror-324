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
    'GetIpamResourceDiscoveryAssociationResult',
    'AwaitableGetIpamResourceDiscoveryAssociationResult',
    'get_ipam_resource_discovery_association',
    'get_ipam_resource_discovery_association_output',
]

@pulumi.output_type
class GetIpamResourceDiscoveryAssociationResult:
    def __init__(__self__, ipam_arn=None, ipam_region=None, ipam_resource_discovery_association_arn=None, ipam_resource_discovery_association_id=None, is_default=None, owner_id=None, resource_discovery_status=None, state=None, tags=None):
        if ipam_arn and not isinstance(ipam_arn, str):
            raise TypeError("Expected argument 'ipam_arn' to be a str")
        pulumi.set(__self__, "ipam_arn", ipam_arn)
        if ipam_region and not isinstance(ipam_region, str):
            raise TypeError("Expected argument 'ipam_region' to be a str")
        pulumi.set(__self__, "ipam_region", ipam_region)
        if ipam_resource_discovery_association_arn and not isinstance(ipam_resource_discovery_association_arn, str):
            raise TypeError("Expected argument 'ipam_resource_discovery_association_arn' to be a str")
        pulumi.set(__self__, "ipam_resource_discovery_association_arn", ipam_resource_discovery_association_arn)
        if ipam_resource_discovery_association_id and not isinstance(ipam_resource_discovery_association_id, str):
            raise TypeError("Expected argument 'ipam_resource_discovery_association_id' to be a str")
        pulumi.set(__self__, "ipam_resource_discovery_association_id", ipam_resource_discovery_association_id)
        if is_default and not isinstance(is_default, bool):
            raise TypeError("Expected argument 'is_default' to be a bool")
        pulumi.set(__self__, "is_default", is_default)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if resource_discovery_status and not isinstance(resource_discovery_status, str):
            raise TypeError("Expected argument 'resource_discovery_status' to be a str")
        pulumi.set(__self__, "resource_discovery_status", resource_discovery_status)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="ipamArn")
    def ipam_arn(self) -> Optional[str]:
        """
        Arn of the IPAM.
        """
        return pulumi.get(self, "ipam_arn")

    @property
    @pulumi.getter(name="ipamRegion")
    def ipam_region(self) -> Optional[str]:
        """
        The home region of the IPAM.
        """
        return pulumi.get(self, "ipam_region")

    @property
    @pulumi.getter(name="ipamResourceDiscoveryAssociationArn")
    def ipam_resource_discovery_association_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the resource discovery association is a part of.
        """
        return pulumi.get(self, "ipam_resource_discovery_association_arn")

    @property
    @pulumi.getter(name="ipamResourceDiscoveryAssociationId")
    def ipam_resource_discovery_association_id(self) -> Optional[str]:
        """
        Id of the IPAM Resource Discovery Association.
        """
        return pulumi.get(self, "ipam_resource_discovery_association_id")

    @property
    @pulumi.getter(name="isDefault")
    def is_default(self) -> Optional[bool]:
        """
        If the Resource Discovery Association exists due as part of CreateIpam.
        """
        return pulumi.get(self, "is_default")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[str]:
        """
        The AWS Account ID for the account where the shared IPAM exists.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="resourceDiscoveryStatus")
    def resource_discovery_status(self) -> Optional[str]:
        """
        The status of the resource discovery.
        """
        return pulumi.get(self, "resource_discovery_status")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The operational state of the Resource Discovery Association. Related to Create/Delete activities.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetIpamResourceDiscoveryAssociationResult(GetIpamResourceDiscoveryAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIpamResourceDiscoveryAssociationResult(
            ipam_arn=self.ipam_arn,
            ipam_region=self.ipam_region,
            ipam_resource_discovery_association_arn=self.ipam_resource_discovery_association_arn,
            ipam_resource_discovery_association_id=self.ipam_resource_discovery_association_id,
            is_default=self.is_default,
            owner_id=self.owner_id,
            resource_discovery_status=self.resource_discovery_status,
            state=self.state,
            tags=self.tags)


def get_ipam_resource_discovery_association(ipam_resource_discovery_association_id: Optional[str] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIpamResourceDiscoveryAssociationResult:
    """
    Resource Schema of AWS::EC2::IPAMResourceDiscoveryAssociation Type


    :param str ipam_resource_discovery_association_id: Id of the IPAM Resource Discovery Association.
    """
    __args__ = dict()
    __args__['ipamResourceDiscoveryAssociationId'] = ipam_resource_discovery_association_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getIpamResourceDiscoveryAssociation', __args__, opts=opts, typ=GetIpamResourceDiscoveryAssociationResult).value

    return AwaitableGetIpamResourceDiscoveryAssociationResult(
        ipam_arn=pulumi.get(__ret__, 'ipam_arn'),
        ipam_region=pulumi.get(__ret__, 'ipam_region'),
        ipam_resource_discovery_association_arn=pulumi.get(__ret__, 'ipam_resource_discovery_association_arn'),
        ipam_resource_discovery_association_id=pulumi.get(__ret__, 'ipam_resource_discovery_association_id'),
        is_default=pulumi.get(__ret__, 'is_default'),
        owner_id=pulumi.get(__ret__, 'owner_id'),
        resource_discovery_status=pulumi.get(__ret__, 'resource_discovery_status'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'))
def get_ipam_resource_discovery_association_output(ipam_resource_discovery_association_id: Optional[pulumi.Input[str]] = None,
                                                   opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetIpamResourceDiscoveryAssociationResult]:
    """
    Resource Schema of AWS::EC2::IPAMResourceDiscoveryAssociation Type


    :param str ipam_resource_discovery_association_id: Id of the IPAM Resource Discovery Association.
    """
    __args__ = dict()
    __args__['ipamResourceDiscoveryAssociationId'] = ipam_resource_discovery_association_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getIpamResourceDiscoveryAssociation', __args__, opts=opts, typ=GetIpamResourceDiscoveryAssociationResult)
    return __ret__.apply(lambda __response__: GetIpamResourceDiscoveryAssociationResult(
        ipam_arn=pulumi.get(__response__, 'ipam_arn'),
        ipam_region=pulumi.get(__response__, 'ipam_region'),
        ipam_resource_discovery_association_arn=pulumi.get(__response__, 'ipam_resource_discovery_association_arn'),
        ipam_resource_discovery_association_id=pulumi.get(__response__, 'ipam_resource_discovery_association_id'),
        is_default=pulumi.get(__response__, 'is_default'),
        owner_id=pulumi.get(__response__, 'owner_id'),
        resource_discovery_status=pulumi.get(__response__, 'resource_discovery_status'),
        state=pulumi.get(__response__, 'state'),
        tags=pulumi.get(__response__, 'tags')))
