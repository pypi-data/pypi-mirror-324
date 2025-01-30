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
    'GetServiceActionResult',
    'AwaitableGetServiceActionResult',
    'get_service_action',
    'get_service_action_output',
]

@pulumi.output_type
class GetServiceActionResult:
    def __init__(__self__, definition=None, definition_type=None, description=None, id=None, name=None):
        if definition and not isinstance(definition, list):
            raise TypeError("Expected argument 'definition' to be a list")
        pulumi.set(__self__, "definition", definition)
        if definition_type and not isinstance(definition_type, str):
            raise TypeError("Expected argument 'definition_type' to be a str")
        pulumi.set(__self__, "definition_type", definition_type)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def definition(self) -> Optional[Sequence['outputs.ServiceActionDefinitionParameter']]:
        """
        A map that defines the self-service action.
        """
        return pulumi.get(self, "definition")

    @property
    @pulumi.getter(name="definitionType")
    def definition_type(self) -> Optional['ServiceActionDefinitionType']:
        """
        The self-service action definition type. For example, `SSM_AUTOMATION` .
        """
        return pulumi.get(self, "definition_type")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The self-service action description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The self-service action identifier. For example, `act-fs7abcd89wxyz` .
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The self-service action name.
        """
        return pulumi.get(self, "name")


class AwaitableGetServiceActionResult(GetServiceActionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceActionResult(
            definition=self.definition,
            definition_type=self.definition_type,
            description=self.description,
            id=self.id,
            name=self.name)


def get_service_action(id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceActionResult:
    """
    Resource Schema for AWS::ServiceCatalog::ServiceAction


    :param str id: The self-service action identifier. For example, `act-fs7abcd89wxyz` .
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:servicecatalog:getServiceAction', __args__, opts=opts, typ=GetServiceActionResult).value

    return AwaitableGetServiceActionResult(
        definition=pulumi.get(__ret__, 'definition'),
        definition_type=pulumi.get(__ret__, 'definition_type'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'))
def get_service_action_output(id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetServiceActionResult]:
    """
    Resource Schema for AWS::ServiceCatalog::ServiceAction


    :param str id: The self-service action identifier. For example, `act-fs7abcd89wxyz` .
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:servicecatalog:getServiceAction', __args__, opts=opts, typ=GetServiceActionResult)
    return __ret__.apply(lambda __response__: GetServiceActionResult(
        definition=pulumi.get(__response__, 'definition'),
        definition_type=pulumi.get(__response__, 'definition_type'),
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name')))
