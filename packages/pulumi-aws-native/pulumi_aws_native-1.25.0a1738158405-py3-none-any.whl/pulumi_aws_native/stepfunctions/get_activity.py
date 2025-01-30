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
    'GetActivityResult',
    'AwaitableGetActivityResult',
    'get_activity',
    'get_activity_output',
]

@pulumi.output_type
class GetActivityResult:
    def __init__(__self__, arn=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Returns the ARN of the resource.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The list of tags to add to a resource.

        Tags may only contain Unicode letters, digits, white space, or these symbols: `_ . : / = + - @` .
        """
        return pulumi.get(self, "tags")


class AwaitableGetActivityResult(GetActivityResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetActivityResult(
            arn=self.arn,
            tags=self.tags)


def get_activity(arn: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetActivityResult:
    """
    Resource schema for Activity


    :param str arn: Returns the ARN of the resource.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:stepfunctions:getActivity', __args__, opts=opts, typ=GetActivityResult).value

    return AwaitableGetActivityResult(
        arn=pulumi.get(__ret__, 'arn'),
        tags=pulumi.get(__ret__, 'tags'))
def get_activity_output(arn: Optional[pulumi.Input[str]] = None,
                        opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetActivityResult]:
    """
    Resource schema for Activity


    :param str arn: Returns the ARN of the resource.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:stepfunctions:getActivity', __args__, opts=opts, typ=GetActivityResult)
    return __ret__.apply(lambda __response__: GetActivityResult(
        arn=pulumi.get(__response__, 'arn'),
        tags=pulumi.get(__response__, 'tags')))
