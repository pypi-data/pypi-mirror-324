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
    'GetAliasResult',
    'AwaitableGetAliasResult',
    'get_alias',
    'get_alias_output',
]

@pulumi.output_type
class GetAliasResult:
    def __init__(__self__, alias_id=None, description=None, name=None, routing_strategy=None):
        if alias_id and not isinstance(alias_id, str):
            raise TypeError("Expected argument 'alias_id' to be a str")
        pulumi.set(__self__, "alias_id", alias_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if routing_strategy and not isinstance(routing_strategy, dict):
            raise TypeError("Expected argument 'routing_strategy' to be a dict")
        pulumi.set(__self__, "routing_strategy", routing_strategy)

    @property
    @pulumi.getter(name="aliasId")
    def alias_id(self) -> Optional[str]:
        """
        Unique alias ID
        """
        return pulumi.get(self, "alias_id")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A human-readable description of the alias.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A descriptive label that is associated with an alias. Alias names do not need to be unique.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="routingStrategy")
    def routing_strategy(self) -> Optional['outputs.AliasRoutingStrategy']:
        """
        A routing configuration that specifies where traffic is directed for this alias, such as to a fleet or to a message.
        """
        return pulumi.get(self, "routing_strategy")


class AwaitableGetAliasResult(GetAliasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAliasResult(
            alias_id=self.alias_id,
            description=self.description,
            name=self.name,
            routing_strategy=self.routing_strategy)


def get_alias(alias_id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAliasResult:
    """
    The AWS::GameLift::Alias resource creates an alias for an Amazon GameLift (GameLift) fleet destination.


    :param str alias_id: Unique alias ID
    """
    __args__ = dict()
    __args__['aliasId'] = alias_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:gamelift:getAlias', __args__, opts=opts, typ=GetAliasResult).value

    return AwaitableGetAliasResult(
        alias_id=pulumi.get(__ret__, 'alias_id'),
        description=pulumi.get(__ret__, 'description'),
        name=pulumi.get(__ret__, 'name'),
        routing_strategy=pulumi.get(__ret__, 'routing_strategy'))
def get_alias_output(alias_id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetAliasResult]:
    """
    The AWS::GameLift::Alias resource creates an alias for an Amazon GameLift (GameLift) fleet destination.


    :param str alias_id: Unique alias ID
    """
    __args__ = dict()
    __args__['aliasId'] = alias_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:gamelift:getAlias', __args__, opts=opts, typ=GetAliasResult)
    return __ret__.apply(lambda __response__: GetAliasResult(
        alias_id=pulumi.get(__response__, 'alias_id'),
        description=pulumi.get(__response__, 'description'),
        name=pulumi.get(__response__, 'name'),
        routing_strategy=pulumi.get(__response__, 'routing_strategy')))
