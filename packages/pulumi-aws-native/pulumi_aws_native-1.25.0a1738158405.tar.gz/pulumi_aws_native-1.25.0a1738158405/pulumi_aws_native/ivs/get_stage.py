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
    'GetStageResult',
    'AwaitableGetStageResult',
    'get_stage',
    'get_stage_output',
]

@pulumi.output_type
class GetStageResult:
    def __init__(__self__, active_session_id=None, arn=None, auto_participant_recording_configuration=None, name=None, tags=None):
        if active_session_id and not isinstance(active_session_id, str):
            raise TypeError("Expected argument 'active_session_id' to be a str")
        pulumi.set(__self__, "active_session_id", active_session_id)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if auto_participant_recording_configuration and not isinstance(auto_participant_recording_configuration, dict):
            raise TypeError("Expected argument 'auto_participant_recording_configuration' to be a dict")
        pulumi.set(__self__, "auto_participant_recording_configuration", auto_participant_recording_configuration)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="activeSessionId")
    def active_session_id(self) -> Optional[str]:
        """
        ID of the active session within the stage.
        """
        return pulumi.get(self, "active_session_id")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Stage ARN is automatically generated on creation and assigned as the unique identifier.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoParticipantRecordingConfiguration")
    def auto_participant_recording_configuration(self) -> Optional['outputs.StageAutoParticipantRecordingConfiguration']:
        return pulumi.get(self, "auto_participant_recording_configuration")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Stage name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetStageResult(GetStageResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStageResult(
            active_session_id=self.active_session_id,
            arn=self.arn,
            auto_participant_recording_configuration=self.auto_participant_recording_configuration,
            name=self.name,
            tags=self.tags)


def get_stage(arn: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStageResult:
    """
    Resource Definition for type AWS::IVS::Stage.


    :param str arn: Stage ARN is automatically generated on creation and assigned as the unique identifier.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ivs:getStage', __args__, opts=opts, typ=GetStageResult).value

    return AwaitableGetStageResult(
        active_session_id=pulumi.get(__ret__, 'active_session_id'),
        arn=pulumi.get(__ret__, 'arn'),
        auto_participant_recording_configuration=pulumi.get(__ret__, 'auto_participant_recording_configuration'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_stage_output(arn: Optional[pulumi.Input[str]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetStageResult]:
    """
    Resource Definition for type AWS::IVS::Stage.


    :param str arn: Stage ARN is automatically generated on creation and assigned as the unique identifier.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ivs:getStage', __args__, opts=opts, typ=GetStageResult)
    return __ret__.apply(lambda __response__: GetStageResult(
        active_session_id=pulumi.get(__response__, 'active_session_id'),
        arn=pulumi.get(__response__, 'arn'),
        auto_participant_recording_configuration=pulumi.get(__response__, 'auto_participant_recording_configuration'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags')))
