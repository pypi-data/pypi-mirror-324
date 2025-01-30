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
from ._enums import *

__all__ = [
    'GetMultiplexResult',
    'AwaitableGetMultiplexResult',
    'get_multiplex',
    'get_multiplex_output',
]

@pulumi.output_type
class GetMultiplexResult:
    def __init__(__self__, arn=None, destinations=None, id=None, multiplex_settings=None, name=None, pipelines_running_count=None, program_count=None, state=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if destinations and not isinstance(destinations, list):
            raise TypeError("Expected argument 'destinations' to be a list")
        pulumi.set(__self__, "destinations", destinations)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if multiplex_settings and not isinstance(multiplex_settings, dict):
            raise TypeError("Expected argument 'multiplex_settings' to be a dict")
        pulumi.set(__self__, "multiplex_settings", multiplex_settings)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if pipelines_running_count and not isinstance(pipelines_running_count, int):
            raise TypeError("Expected argument 'pipelines_running_count' to be a int")
        pulumi.set(__self__, "pipelines_running_count", pipelines_running_count)
        if program_count and not isinstance(program_count, int):
            raise TypeError("Expected argument 'program_count' to be a int")
        pulumi.set(__self__, "program_count", program_count)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The unique arn of the multiplex.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def destinations(self) -> Optional[Sequence['outputs.MultiplexOutputDestination']]:
        """
        A list of the multiplex output destinations.
        """
        return pulumi.get(self, "destinations")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The unique id of the multiplex.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="multiplexSettings")
    def multiplex_settings(self) -> Optional['outputs.MultiplexSettings']:
        """
        Configuration for a multiplex event.
        """
        return pulumi.get(self, "multiplex_settings")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of multiplex.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pipelinesRunningCount")
    def pipelines_running_count(self) -> Optional[int]:
        """
        The number of currently healthy pipelines.
        """
        return pulumi.get(self, "pipelines_running_count")

    @property
    @pulumi.getter(name="programCount")
    def program_count(self) -> Optional[int]:
        """
        The number of programs in the multiplex.
        """
        return pulumi.get(self, "program_count")

    @property
    @pulumi.getter
    def state(self) -> Optional['MultiplexState']:
        """
        The current state of the multiplex.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A collection of key-value pairs.
        """
        return pulumi.get(self, "tags")


class AwaitableGetMultiplexResult(GetMultiplexResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMultiplexResult(
            arn=self.arn,
            destinations=self.destinations,
            id=self.id,
            multiplex_settings=self.multiplex_settings,
            name=self.name,
            pipelines_running_count=self.pipelines_running_count,
            program_count=self.program_count,
            state=self.state,
            tags=self.tags)


def get_multiplex(id: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMultiplexResult:
    """
    Resource schema for AWS::MediaLive::Multiplex


    :param str id: The unique id of the multiplex.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:medialive:getMultiplex', __args__, opts=opts, typ=GetMultiplexResult).value

    return AwaitableGetMultiplexResult(
        arn=pulumi.get(__ret__, 'arn'),
        destinations=pulumi.get(__ret__, 'destinations'),
        id=pulumi.get(__ret__, 'id'),
        multiplex_settings=pulumi.get(__ret__, 'multiplex_settings'),
        name=pulumi.get(__ret__, 'name'),
        pipelines_running_count=pulumi.get(__ret__, 'pipelines_running_count'),
        program_count=pulumi.get(__ret__, 'program_count'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'))
def get_multiplex_output(id: Optional[pulumi.Input[str]] = None,
                         opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetMultiplexResult]:
    """
    Resource schema for AWS::MediaLive::Multiplex


    :param str id: The unique id of the multiplex.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:medialive:getMultiplex', __args__, opts=opts, typ=GetMultiplexResult)
    return __ret__.apply(lambda __response__: GetMultiplexResult(
        arn=pulumi.get(__response__, 'arn'),
        destinations=pulumi.get(__response__, 'destinations'),
        id=pulumi.get(__response__, 'id'),
        multiplex_settings=pulumi.get(__response__, 'multiplex_settings'),
        name=pulumi.get(__response__, 'name'),
        pipelines_running_count=pulumi.get(__response__, 'pipelines_running_count'),
        program_count=pulumi.get(__response__, 'program_count'),
        state=pulumi.get(__response__, 'state'),
        tags=pulumi.get(__response__, 'tags')))
