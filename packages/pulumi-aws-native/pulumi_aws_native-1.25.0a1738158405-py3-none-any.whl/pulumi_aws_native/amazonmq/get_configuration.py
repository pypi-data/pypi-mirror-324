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
    'GetConfigurationResult',
    'AwaitableGetConfigurationResult',
    'get_configuration',
    'get_configuration_output',
]

@pulumi.output_type
class GetConfigurationResult:
    def __init__(__self__, arn=None, description=None, id=None, revision=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if revision and not isinstance(revision, str):
            raise TypeError("Expected argument 'revision' to be a str")
        pulumi.set(__self__, "revision", revision)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the Amazon MQ configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the configuration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the Amazon MQ configuration.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def revision(self) -> Optional[str]:
        """
        The revision number of the configuration.
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Create tags when creating the configuration.
        """
        return pulumi.get(self, "tags")


class AwaitableGetConfigurationResult(GetConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConfigurationResult(
            arn=self.arn,
            description=self.description,
            id=self.id,
            revision=self.revision,
            tags=self.tags)


def get_configuration(id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConfigurationResult:
    """
    Resource Type definition for AWS::AmazonMQ::Configuration


    :param str id: The ID of the Amazon MQ configuration.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:amazonmq:getConfiguration', __args__, opts=opts, typ=GetConfigurationResult).value

    return AwaitableGetConfigurationResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        revision=pulumi.get(__ret__, 'revision'),
        tags=pulumi.get(__ret__, 'tags'))
def get_configuration_output(id: Optional[pulumi.Input[str]] = None,
                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetConfigurationResult]:
    """
    Resource Type definition for AWS::AmazonMQ::Configuration


    :param str id: The ID of the Amazon MQ configuration.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:amazonmq:getConfiguration', __args__, opts=opts, typ=GetConfigurationResult)
    return __ret__.apply(lambda __response__: GetConfigurationResult(
        arn=pulumi.get(__response__, 'arn'),
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        revision=pulumi.get(__response__, 'revision'),
        tags=pulumi.get(__response__, 'tags')))
