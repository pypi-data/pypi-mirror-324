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
    'GetSyncJobResult',
    'AwaitableGetSyncJobResult',
    'get_sync_job',
    'get_sync_job_output',
]

@pulumi.output_type
class GetSyncJobResult:
    def __init__(__self__, arn=None, creation_date_time=None, state=None, update_date_time=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if creation_date_time and not isinstance(creation_date_time, str):
            raise TypeError("Expected argument 'creation_date_time' to be a str")
        pulumi.set(__self__, "creation_date_time", creation_date_time)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if update_date_time and not isinstance(update_date_time, str):
            raise TypeError("Expected argument 'update_date_time' to be a str")
        pulumi.set(__self__, "update_date_time", update_date_time)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the SyncJob.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="creationDateTime")
    def creation_date_time(self) -> Optional[str]:
        """
        The date and time when the sync job was created.
        """
        return pulumi.get(self, "creation_date_time")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of SyncJob.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="updateDateTime")
    def update_date_time(self) -> Optional[str]:
        """
        The date and time when the sync job was updated.
        """
        return pulumi.get(self, "update_date_time")


class AwaitableGetSyncJobResult(GetSyncJobResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSyncJobResult(
            arn=self.arn,
            creation_date_time=self.creation_date_time,
            state=self.state,
            update_date_time=self.update_date_time)


def get_sync_job(sync_source: Optional[str] = None,
                 workspace_id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSyncJobResult:
    """
    Resource schema for AWS::IoTTwinMaker::SyncJob


    :param str sync_source: The source of the SyncJob.
    :param str workspace_id: The ID of the workspace.
    """
    __args__ = dict()
    __args__['syncSource'] = sync_source
    __args__['workspaceId'] = workspace_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iottwinmaker:getSyncJob', __args__, opts=opts, typ=GetSyncJobResult).value

    return AwaitableGetSyncJobResult(
        arn=pulumi.get(__ret__, 'arn'),
        creation_date_time=pulumi.get(__ret__, 'creation_date_time'),
        state=pulumi.get(__ret__, 'state'),
        update_date_time=pulumi.get(__ret__, 'update_date_time'))
def get_sync_job_output(sync_source: Optional[pulumi.Input[str]] = None,
                        workspace_id: Optional[pulumi.Input[str]] = None,
                        opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSyncJobResult]:
    """
    Resource schema for AWS::IoTTwinMaker::SyncJob


    :param str sync_source: The source of the SyncJob.
    :param str workspace_id: The ID of the workspace.
    """
    __args__ = dict()
    __args__['syncSource'] = sync_source
    __args__['workspaceId'] = workspace_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iottwinmaker:getSyncJob', __args__, opts=opts, typ=GetSyncJobResult)
    return __ret__.apply(lambda __response__: GetSyncJobResult(
        arn=pulumi.get(__response__, 'arn'),
        creation_date_time=pulumi.get(__response__, 'creation_date_time'),
        state=pulumi.get(__response__, 'state'),
        update_date_time=pulumi.get(__response__, 'update_date_time')))
