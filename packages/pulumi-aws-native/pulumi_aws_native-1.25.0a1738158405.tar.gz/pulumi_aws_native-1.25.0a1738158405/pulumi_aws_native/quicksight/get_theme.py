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
    'GetThemeResult',
    'AwaitableGetThemeResult',
    'get_theme',
    'get_theme_output',
]

@pulumi.output_type
class GetThemeResult:
    def __init__(__self__, arn=None, created_time=None, last_updated_time=None, name=None, permissions=None, tags=None, type=None, version=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_time and not isinstance(created_time, str):
            raise TypeError("Expected argument 'created_time' to be a str")
        pulumi.set(__self__, "created_time", created_time)
        if last_updated_time and not isinstance(last_updated_time, str):
            raise TypeError("Expected argument 'last_updated_time' to be a str")
        pulumi.set(__self__, "last_updated_time", last_updated_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if permissions and not isinstance(permissions, list):
            raise TypeError("Expected argument 'permissions' to be a list")
        pulumi.set(__self__, "permissions", permissions)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, dict):
            raise TypeError("Expected argument 'version' to be a dict")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        <p>The Amazon Resource Name (ARN) of the theme.</p>
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> Optional[str]:
        """
        <p>The date and time that the theme was created.</p>
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> Optional[str]:
        """
        <p>The date and time that the theme was last updated.</p>
        """
        return pulumi.get(self, "last_updated_time")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A display name for the theme.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def permissions(self) -> Optional[Sequence['outputs.ThemeResourcePermission']]:
        """
        A valid grouping of resource permissions to apply to the new theme.
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A map of the key-value pairs for the resource tag or tags that you want to add to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional['ThemeType']:
        """
        Theme type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> Optional['outputs.ThemeVersion']:
        return pulumi.get(self, "version")


class AwaitableGetThemeResult(GetThemeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetThemeResult(
            arn=self.arn,
            created_time=self.created_time,
            last_updated_time=self.last_updated_time,
            name=self.name,
            permissions=self.permissions,
            tags=self.tags,
            type=self.type,
            version=self.version)


def get_theme(aws_account_id: Optional[str] = None,
              theme_id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetThemeResult:
    """
    Definition of the AWS::QuickSight::Theme Resource Type.


    :param str aws_account_id: The ID of the AWS account where you want to store the new theme.
    :param str theme_id: An ID for the theme that you want to create. The theme ID is unique per AWS Region in each AWS account.
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    __args__['themeId'] = theme_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:quicksight:getTheme', __args__, opts=opts, typ=GetThemeResult).value

    return AwaitableGetThemeResult(
        arn=pulumi.get(__ret__, 'arn'),
        created_time=pulumi.get(__ret__, 'created_time'),
        last_updated_time=pulumi.get(__ret__, 'last_updated_time'),
        name=pulumi.get(__ret__, 'name'),
        permissions=pulumi.get(__ret__, 'permissions'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'),
        version=pulumi.get(__ret__, 'version'))
def get_theme_output(aws_account_id: Optional[pulumi.Input[str]] = None,
                     theme_id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetThemeResult]:
    """
    Definition of the AWS::QuickSight::Theme Resource Type.


    :param str aws_account_id: The ID of the AWS account where you want to store the new theme.
    :param str theme_id: An ID for the theme that you want to create. The theme ID is unique per AWS Region in each AWS account.
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    __args__['themeId'] = theme_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:quicksight:getTheme', __args__, opts=opts, typ=GetThemeResult)
    return __ret__.apply(lambda __response__: GetThemeResult(
        arn=pulumi.get(__response__, 'arn'),
        created_time=pulumi.get(__response__, 'created_time'),
        last_updated_time=pulumi.get(__response__, 'last_updated_time'),
        name=pulumi.get(__response__, 'name'),
        permissions=pulumi.get(__response__, 'permissions'),
        tags=pulumi.get(__response__, 'tags'),
        type=pulumi.get(__response__, 'type'),
        version=pulumi.get(__response__, 'version')))
