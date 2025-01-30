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
    'GetMonitorResult',
    'AwaitableGetMonitorResult',
    'get_monitor',
    'get_monitor_output',
]

@pulumi.output_type
class GetMonitorResult:
    def __init__(__self__, arn=None, display_name=None, identity_center_application_arn=None, monitor_id=None, role_arn=None, subdomain=None, url=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if identity_center_application_arn and not isinstance(identity_center_application_arn, str):
            raise TypeError("Expected argument 'identity_center_application_arn' to be a str")
        pulumi.set(__self__, "identity_center_application_arn", identity_center_application_arn)
        if monitor_id and not isinstance(monitor_id, str):
            raise TypeError("Expected argument 'monitor_id' to be a str")
        pulumi.set(__self__, "monitor_id", monitor_id)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if subdomain and not isinstance(subdomain, str):
            raise TypeError("Expected argument 'subdomain' to be a str")
        pulumi.set(__self__, "subdomain", subdomain)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the monitor.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The name of the monitor that displays on the Deadline Cloud console.

        > This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="identityCenterApplicationArn")
    def identity_center_application_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) that the IAM Identity Center assigned to the monitor when it was created.
        """
        return pulumi.get(self, "identity_center_application_arn")

    @property
    @pulumi.getter(name="monitorId")
    def monitor_id(self) -> Optional[str]:
        """
        The unique identifier for the monitor.
        """
        return pulumi.get(self, "monitor_id")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role for the monitor. Users of the monitor use this role to access Deadline Cloud resources.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def subdomain(self) -> Optional[str]:
        """
        The subdomain used for the monitor URL. The full URL of the monitor is subdomain.Region.deadlinecloud.amazonaws.com.
        """
        return pulumi.get(self, "subdomain")

    @property
    @pulumi.getter
    def url(self) -> Optional[str]:
        """
        The complete URL of the monitor. The full URL of the monitor is subdomain.Region.deadlinecloud.amazonaws.com.
        """
        return pulumi.get(self, "url")


class AwaitableGetMonitorResult(GetMonitorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMonitorResult(
            arn=self.arn,
            display_name=self.display_name,
            identity_center_application_arn=self.identity_center_application_arn,
            monitor_id=self.monitor_id,
            role_arn=self.role_arn,
            subdomain=self.subdomain,
            url=self.url)


def get_monitor(arn: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMonitorResult:
    """
    Definition of AWS::Deadline::Monitor Resource Type


    :param str arn: The Amazon Resource Name (ARN) of the monitor.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:deadline:getMonitor', __args__, opts=opts, typ=GetMonitorResult).value

    return AwaitableGetMonitorResult(
        arn=pulumi.get(__ret__, 'arn'),
        display_name=pulumi.get(__ret__, 'display_name'),
        identity_center_application_arn=pulumi.get(__ret__, 'identity_center_application_arn'),
        monitor_id=pulumi.get(__ret__, 'monitor_id'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        subdomain=pulumi.get(__ret__, 'subdomain'),
        url=pulumi.get(__ret__, 'url'))
def get_monitor_output(arn: Optional[pulumi.Input[str]] = None,
                       opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetMonitorResult]:
    """
    Definition of AWS::Deadline::Monitor Resource Type


    :param str arn: The Amazon Resource Name (ARN) of the monitor.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:deadline:getMonitor', __args__, opts=opts, typ=GetMonitorResult)
    return __ret__.apply(lambda __response__: GetMonitorResult(
        arn=pulumi.get(__response__, 'arn'),
        display_name=pulumi.get(__response__, 'display_name'),
        identity_center_application_arn=pulumi.get(__response__, 'identity_center_application_arn'),
        monitor_id=pulumi.get(__response__, 'monitor_id'),
        role_arn=pulumi.get(__response__, 'role_arn'),
        subdomain=pulumi.get(__response__, 'subdomain'),
        url=pulumi.get(__response__, 'url')))
