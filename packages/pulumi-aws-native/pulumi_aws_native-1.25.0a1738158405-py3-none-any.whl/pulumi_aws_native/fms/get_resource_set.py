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
    'GetResourceSetResult',
    'AwaitableGetResourceSetResult',
    'get_resource_set',
    'get_resource_set_output',
]

@pulumi.output_type
class GetResourceSetResult:
    def __init__(__self__, description=None, id=None, name=None, resource_type_list=None, resources=None, tags=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_type_list and not isinstance(resource_type_list, list):
            raise TypeError("Expected argument 'resource_type_list' to be a list")
        pulumi.set(__self__, "resource_type_list", resource_type_list)
        if resources and not isinstance(resources, list):
            raise TypeError("Expected argument 'resources' to be a list")
        pulumi.set(__self__, "resources", resources)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the resource set.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        A unique identifier for the resource set. This ID is returned in the responses to create and list commands. You provide it to operations like update and delete.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The descriptive name of the resource set. You can't change the name of a resource set after you create it.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceTypeList")
    def resource_type_list(self) -> Optional[Sequence[str]]:
        """
        Determines the resources that can be associated to the resource set. Depending on your setting for max results and the number of resource sets, a single call might not return the full list.
        """
        return pulumi.get(self, "resource_type_list")

    @property
    @pulumi.getter
    def resources(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "resources")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        return pulumi.get(self, "tags")


class AwaitableGetResourceSetResult(GetResourceSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourceSetResult(
            description=self.description,
            id=self.id,
            name=self.name,
            resource_type_list=self.resource_type_list,
            resources=self.resources,
            tags=self.tags)


def get_resource_set(id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourceSetResult:
    """
    Creates an AWS Firewall Manager resource set.


    :param str id: A unique identifier for the resource set. This ID is returned in the responses to create and list commands. You provide it to operations like update and delete.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:fms:getResourceSet', __args__, opts=opts, typ=GetResourceSetResult).value

    return AwaitableGetResourceSetResult(
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        resource_type_list=pulumi.get(__ret__, 'resource_type_list'),
        resources=pulumi.get(__ret__, 'resources'),
        tags=pulumi.get(__ret__, 'tags'))
def get_resource_set_output(id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetResourceSetResult]:
    """
    Creates an AWS Firewall Manager resource set.


    :param str id: A unique identifier for the resource set. This ID is returned in the responses to create and list commands. You provide it to operations like update and delete.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:fms:getResourceSet', __args__, opts=opts, typ=GetResourceSetResult)
    return __ret__.apply(lambda __response__: GetResourceSetResult(
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        resource_type_list=pulumi.get(__response__, 'resource_type_list'),
        resources=pulumi.get(__response__, 'resources'),
        tags=pulumi.get(__response__, 'tags')))
