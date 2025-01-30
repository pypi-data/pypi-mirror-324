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
    'GetQuickConnectResult',
    'AwaitableGetQuickConnectResult',
    'get_quick_connect',
    'get_quick_connect_output',
]

@pulumi.output_type
class GetQuickConnectResult:
    def __init__(__self__, description=None, instance_arn=None, name=None, quick_connect_arn=None, quick_connect_config=None, quick_connect_type=None, tags=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if instance_arn and not isinstance(instance_arn, str):
            raise TypeError("Expected argument 'instance_arn' to be a str")
        pulumi.set(__self__, "instance_arn", instance_arn)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if quick_connect_arn and not isinstance(quick_connect_arn, str):
            raise TypeError("Expected argument 'quick_connect_arn' to be a str")
        pulumi.set(__self__, "quick_connect_arn", quick_connect_arn)
        if quick_connect_config and not isinstance(quick_connect_config, dict):
            raise TypeError("Expected argument 'quick_connect_config' to be a dict")
        pulumi.set(__self__, "quick_connect_config", quick_connect_config)
        if quick_connect_type and not isinstance(quick_connect_type, str):
            raise TypeError("Expected argument 'quick_connect_type' to be a str")
        pulumi.set(__self__, "quick_connect_type", quick_connect_type)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the quick connect.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> Optional[str]:
        """
        The identifier of the Amazon Connect instance.
        """
        return pulumi.get(self, "instance_arn")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the quick connect.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="quickConnectArn")
    def quick_connect_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for the quick connect.
        """
        return pulumi.get(self, "quick_connect_arn")

    @property
    @pulumi.getter(name="quickConnectConfig")
    def quick_connect_config(self) -> Optional['outputs.QuickConnectConfig']:
        """
        Configuration settings for the quick connect.
        """
        return pulumi.get(self, "quick_connect_config")

    @property
    @pulumi.getter(name="quickConnectType")
    def quick_connect_type(self) -> Optional['QuickConnectType']:
        """
        The type of quick connect. In the Amazon Connect console, when you create a quick connect, you are prompted to assign one of the following types: Agent (USER), External (PHONE_NUMBER), or Queue (QUEUE).
        """
        return pulumi.get(self, "quick_connect_type")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        One or more tags.
        """
        return pulumi.get(self, "tags")


class AwaitableGetQuickConnectResult(GetQuickConnectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetQuickConnectResult(
            description=self.description,
            instance_arn=self.instance_arn,
            name=self.name,
            quick_connect_arn=self.quick_connect_arn,
            quick_connect_config=self.quick_connect_config,
            quick_connect_type=self.quick_connect_type,
            tags=self.tags)


def get_quick_connect(quick_connect_arn: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetQuickConnectResult:
    """
    Resource Type definition for AWS::Connect::QuickConnect


    :param str quick_connect_arn: The Amazon Resource Name (ARN) for the quick connect.
    """
    __args__ = dict()
    __args__['quickConnectArn'] = quick_connect_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:connect:getQuickConnect', __args__, opts=opts, typ=GetQuickConnectResult).value

    return AwaitableGetQuickConnectResult(
        description=pulumi.get(__ret__, 'description'),
        instance_arn=pulumi.get(__ret__, 'instance_arn'),
        name=pulumi.get(__ret__, 'name'),
        quick_connect_arn=pulumi.get(__ret__, 'quick_connect_arn'),
        quick_connect_config=pulumi.get(__ret__, 'quick_connect_config'),
        quick_connect_type=pulumi.get(__ret__, 'quick_connect_type'),
        tags=pulumi.get(__ret__, 'tags'))
def get_quick_connect_output(quick_connect_arn: Optional[pulumi.Input[str]] = None,
                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetQuickConnectResult]:
    """
    Resource Type definition for AWS::Connect::QuickConnect


    :param str quick_connect_arn: The Amazon Resource Name (ARN) for the quick connect.
    """
    __args__ = dict()
    __args__['quickConnectArn'] = quick_connect_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:connect:getQuickConnect', __args__, opts=opts, typ=GetQuickConnectResult)
    return __ret__.apply(lambda __response__: GetQuickConnectResult(
        description=pulumi.get(__response__, 'description'),
        instance_arn=pulumi.get(__response__, 'instance_arn'),
        name=pulumi.get(__response__, 'name'),
        quick_connect_arn=pulumi.get(__response__, 'quick_connect_arn'),
        quick_connect_config=pulumi.get(__response__, 'quick_connect_config'),
        quick_connect_type=pulumi.get(__response__, 'quick_connect_type'),
        tags=pulumi.get(__response__, 'tags')))
