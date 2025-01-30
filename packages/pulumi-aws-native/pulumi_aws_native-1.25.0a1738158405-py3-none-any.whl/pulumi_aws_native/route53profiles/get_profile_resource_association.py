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
    'GetProfileResourceAssociationResult',
    'AwaitableGetProfileResourceAssociationResult',
    'get_profile_resource_association',
    'get_profile_resource_association_output',
]

@pulumi.output_type
class GetProfileResourceAssociationResult:
    def __init__(__self__, id=None, resource_properties=None, resource_type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if resource_properties and not isinstance(resource_properties, str):
            raise TypeError("Expected argument 'resource_properties' to be a str")
        pulumi.set(__self__, "resource_properties", resource_properties)
        if resource_type and not isinstance(resource_type, str):
            raise TypeError("Expected argument 'resource_type' to be a str")
        pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Primary Identifier for  Profile Resource Association
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="resourceProperties")
    def resource_properties(self) -> Optional[str]:
        """
        A JSON-formatted string with key-value pairs specifying the properties of the associated resource.
        """
        return pulumi.get(self, "resource_properties")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[str]:
        """
        The type of the resource associated to the  Profile.
        """
        return pulumi.get(self, "resource_type")


class AwaitableGetProfileResourceAssociationResult(GetProfileResourceAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProfileResourceAssociationResult(
            id=self.id,
            resource_properties=self.resource_properties,
            resource_type=self.resource_type)


def get_profile_resource_association(id: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProfileResourceAssociationResult:
    """
    Resource Type definition for AWS::Route53Profiles::ProfileResourceAssociation


    :param str id: Primary Identifier for  Profile Resource Association
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:route53profiles:getProfileResourceAssociation', __args__, opts=opts, typ=GetProfileResourceAssociationResult).value

    return AwaitableGetProfileResourceAssociationResult(
        id=pulumi.get(__ret__, 'id'),
        resource_properties=pulumi.get(__ret__, 'resource_properties'),
        resource_type=pulumi.get(__ret__, 'resource_type'))
def get_profile_resource_association_output(id: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetProfileResourceAssociationResult]:
    """
    Resource Type definition for AWS::Route53Profiles::ProfileResourceAssociation


    :param str id: Primary Identifier for  Profile Resource Association
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:route53profiles:getProfileResourceAssociation', __args__, opts=opts, typ=GetProfileResourceAssociationResult)
    return __ret__.apply(lambda __response__: GetProfileResourceAssociationResult(
        id=pulumi.get(__response__, 'id'),
        resource_properties=pulumi.get(__response__, 'resource_properties'),
        resource_type=pulumi.get(__response__, 'resource_type')))
