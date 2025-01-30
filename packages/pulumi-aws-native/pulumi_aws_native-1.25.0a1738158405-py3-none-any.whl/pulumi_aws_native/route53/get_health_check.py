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
    'GetHealthCheckResult',
    'AwaitableGetHealthCheckResult',
    'get_health_check',
    'get_health_check_output',
]

@pulumi.output_type
class GetHealthCheckResult:
    def __init__(__self__, health_check_config=None, health_check_id=None, health_check_tags=None):
        if health_check_config and not isinstance(health_check_config, dict):
            raise TypeError("Expected argument 'health_check_config' to be a dict")
        pulumi.set(__self__, "health_check_config", health_check_config)
        if health_check_id and not isinstance(health_check_id, str):
            raise TypeError("Expected argument 'health_check_id' to be a str")
        pulumi.set(__self__, "health_check_id", health_check_id)
        if health_check_tags and not isinstance(health_check_tags, list):
            raise TypeError("Expected argument 'health_check_tags' to be a list")
        pulumi.set(__self__, "health_check_tags", health_check_tags)

    @property
    @pulumi.getter(name="healthCheckConfig")
    def health_check_config(self) -> Optional['outputs.HealthCheckConfigProperties']:
        """
        A complex type that contains information about the health check.
        """
        return pulumi.get(self, "health_check_config")

    @property
    @pulumi.getter(name="healthCheckId")
    def health_check_id(self) -> Optional[str]:
        """
        The identifier that Amazon Route 53 assigned to the health check when you created it. When you add or update a resource record set, you use this value to specify which health check to use. The value can be up to 64 characters long.
        """
        return pulumi.get(self, "health_check_id")

    @property
    @pulumi.getter(name="healthCheckTags")
    def health_check_tags(self) -> Optional[Sequence['outputs.HealthCheckTag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "health_check_tags")


class AwaitableGetHealthCheckResult(GetHealthCheckResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHealthCheckResult(
            health_check_config=self.health_check_config,
            health_check_id=self.health_check_id,
            health_check_tags=self.health_check_tags)


def get_health_check(health_check_id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHealthCheckResult:
    """
    Resource schema for AWS::Route53::HealthCheck.


    :param str health_check_id: The identifier that Amazon Route 53 assigned to the health check when you created it. When you add or update a resource record set, you use this value to specify which health check to use. The value can be up to 64 characters long.
    """
    __args__ = dict()
    __args__['healthCheckId'] = health_check_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:route53:getHealthCheck', __args__, opts=opts, typ=GetHealthCheckResult).value

    return AwaitableGetHealthCheckResult(
        health_check_config=pulumi.get(__ret__, 'health_check_config'),
        health_check_id=pulumi.get(__ret__, 'health_check_id'),
        health_check_tags=pulumi.get(__ret__, 'health_check_tags'))
def get_health_check_output(health_check_id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetHealthCheckResult]:
    """
    Resource schema for AWS::Route53::HealthCheck.


    :param str health_check_id: The identifier that Amazon Route 53 assigned to the health check when you created it. When you add or update a resource record set, you use this value to specify which health check to use. The value can be up to 64 characters long.
    """
    __args__ = dict()
    __args__['healthCheckId'] = health_check_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:route53:getHealthCheck', __args__, opts=opts, typ=GetHealthCheckResult)
    return __ret__.apply(lambda __response__: GetHealthCheckResult(
        health_check_config=pulumi.get(__response__, 'health_check_config'),
        health_check_id=pulumi.get(__response__, 'health_check_id'),
        health_check_tags=pulumi.get(__response__, 'health_check_tags')))
