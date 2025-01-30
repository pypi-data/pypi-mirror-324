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
    'GetTestGridProjectResult',
    'AwaitableGetTestGridProjectResult',
    'get_test_grid_project',
    'get_test_grid_project_output',
]

@pulumi.output_type
class GetTestGridProjectResult:
    def __init__(__self__, arn=None, description=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the `TestGrid` project. See [Amazon resource names](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) in the *General Reference guide* .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A human-readable description for the project.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A human-readable name for the project.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.

        For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) in the *guide* .
        """
        return pulumi.get(self, "tags")


class AwaitableGetTestGridProjectResult(GetTestGridProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTestGridProjectResult(
            arn=self.arn,
            description=self.description,
            name=self.name,
            tags=self.tags)


def get_test_grid_project(arn: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTestGridProjectResult:
    """
    AWS::DeviceFarm::TestGridProject creates a new TestGrid Project


    :param str arn: The Amazon Resource Name (ARN) of the `TestGrid` project. See [Amazon resource names](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) in the *General Reference guide* .
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:devicefarm:getTestGridProject', __args__, opts=opts, typ=GetTestGridProjectResult).value

    return AwaitableGetTestGridProjectResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_test_grid_project_output(arn: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetTestGridProjectResult]:
    """
    AWS::DeviceFarm::TestGridProject creates a new TestGrid Project


    :param str arn: The Amazon Resource Name (ARN) of the `TestGrid` project. See [Amazon resource names](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) in the *General Reference guide* .
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:devicefarm:getTestGridProject', __args__, opts=opts, typ=GetTestGridProjectResult)
    return __ret__.apply(lambda __response__: GetTestGridProjectResult(
        arn=pulumi.get(__response__, 'arn'),
        description=pulumi.get(__response__, 'description'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags')))
