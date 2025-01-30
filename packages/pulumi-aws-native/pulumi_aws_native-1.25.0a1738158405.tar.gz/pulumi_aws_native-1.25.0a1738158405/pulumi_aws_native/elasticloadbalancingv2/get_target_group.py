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

__all__ = [
    'GetTargetGroupResult',
    'AwaitableGetTargetGroupResult',
    'get_target_group',
    'get_target_group_output',
]

@pulumi.output_type
class GetTargetGroupResult:
    def __init__(__self__, health_check_enabled=None, health_check_interval_seconds=None, health_check_path=None, health_check_port=None, health_check_protocol=None, health_check_timeout_seconds=None, healthy_threshold_count=None, load_balancer_arns=None, matcher=None, tags=None, target_group_arn=None, target_group_attributes=None, target_group_full_name=None, target_group_name=None, targets=None, unhealthy_threshold_count=None):
        if health_check_enabled and not isinstance(health_check_enabled, bool):
            raise TypeError("Expected argument 'health_check_enabled' to be a bool")
        pulumi.set(__self__, "health_check_enabled", health_check_enabled)
        if health_check_interval_seconds and not isinstance(health_check_interval_seconds, int):
            raise TypeError("Expected argument 'health_check_interval_seconds' to be a int")
        pulumi.set(__self__, "health_check_interval_seconds", health_check_interval_seconds)
        if health_check_path and not isinstance(health_check_path, str):
            raise TypeError("Expected argument 'health_check_path' to be a str")
        pulumi.set(__self__, "health_check_path", health_check_path)
        if health_check_port and not isinstance(health_check_port, str):
            raise TypeError("Expected argument 'health_check_port' to be a str")
        pulumi.set(__self__, "health_check_port", health_check_port)
        if health_check_protocol and not isinstance(health_check_protocol, str):
            raise TypeError("Expected argument 'health_check_protocol' to be a str")
        pulumi.set(__self__, "health_check_protocol", health_check_protocol)
        if health_check_timeout_seconds and not isinstance(health_check_timeout_seconds, int):
            raise TypeError("Expected argument 'health_check_timeout_seconds' to be a int")
        pulumi.set(__self__, "health_check_timeout_seconds", health_check_timeout_seconds)
        if healthy_threshold_count and not isinstance(healthy_threshold_count, int):
            raise TypeError("Expected argument 'healthy_threshold_count' to be a int")
        pulumi.set(__self__, "healthy_threshold_count", healthy_threshold_count)
        if load_balancer_arns and not isinstance(load_balancer_arns, list):
            raise TypeError("Expected argument 'load_balancer_arns' to be a list")
        pulumi.set(__self__, "load_balancer_arns", load_balancer_arns)
        if matcher and not isinstance(matcher, dict):
            raise TypeError("Expected argument 'matcher' to be a dict")
        pulumi.set(__self__, "matcher", matcher)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if target_group_arn and not isinstance(target_group_arn, str):
            raise TypeError("Expected argument 'target_group_arn' to be a str")
        pulumi.set(__self__, "target_group_arn", target_group_arn)
        if target_group_attributes and not isinstance(target_group_attributes, list):
            raise TypeError("Expected argument 'target_group_attributes' to be a list")
        pulumi.set(__self__, "target_group_attributes", target_group_attributes)
        if target_group_full_name and not isinstance(target_group_full_name, str):
            raise TypeError("Expected argument 'target_group_full_name' to be a str")
        pulumi.set(__self__, "target_group_full_name", target_group_full_name)
        if target_group_name and not isinstance(target_group_name, str):
            raise TypeError("Expected argument 'target_group_name' to be a str")
        pulumi.set(__self__, "target_group_name", target_group_name)
        if targets and not isinstance(targets, list):
            raise TypeError("Expected argument 'targets' to be a list")
        pulumi.set(__self__, "targets", targets)
        if unhealthy_threshold_count and not isinstance(unhealthy_threshold_count, int):
            raise TypeError("Expected argument 'unhealthy_threshold_count' to be a int")
        pulumi.set(__self__, "unhealthy_threshold_count", unhealthy_threshold_count)

    @property
    @pulumi.getter(name="healthCheckEnabled")
    def health_check_enabled(self) -> Optional[bool]:
        """
        Indicates whether health checks are enabled. If the target type is lambda, health checks are disabled by default but can be enabled. If the target type is instance, ip, or alb, health checks are always enabled and cannot be disabled.
        """
        return pulumi.get(self, "health_check_enabled")

    @property
    @pulumi.getter(name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> Optional[int]:
        """
        The approximate amount of time, in seconds, between health checks of an individual target.
        """
        return pulumi.get(self, "health_check_interval_seconds")

    @property
    @pulumi.getter(name="healthCheckPath")
    def health_check_path(self) -> Optional[str]:
        """
        [HTTP/HTTPS health checks] The destination for health checks on the targets. [HTTP1 or HTTP2 protocol version] The ping path. The default is /. [GRPC protocol version] The path of a custom health check method with the format /package.service/method. The default is /AWS.ALB/healthcheck.
        """
        return pulumi.get(self, "health_check_path")

    @property
    @pulumi.getter(name="healthCheckPort")
    def health_check_port(self) -> Optional[str]:
        """
        The port the load balancer uses when performing health checks on targets. 
        """
        return pulumi.get(self, "health_check_port")

    @property
    @pulumi.getter(name="healthCheckProtocol")
    def health_check_protocol(self) -> Optional[str]:
        """
        The protocol the load balancer uses when performing health checks on targets. 
        """
        return pulumi.get(self, "health_check_protocol")

    @property
    @pulumi.getter(name="healthCheckTimeoutSeconds")
    def health_check_timeout_seconds(self) -> Optional[int]:
        """
        The amount of time, in seconds, during which no response from a target means a failed health check.
        """
        return pulumi.get(self, "health_check_timeout_seconds")

    @property
    @pulumi.getter(name="healthyThresholdCount")
    def healthy_threshold_count(self) -> Optional[int]:
        """
        The number of consecutive health checks successes required before considering an unhealthy target healthy. 
        """
        return pulumi.get(self, "healthy_threshold_count")

    @property
    @pulumi.getter(name="loadBalancerArns")
    def load_balancer_arns(self) -> Optional[Sequence[str]]:
        """
        The Amazon Resource Names (ARNs) of the load balancers that route traffic to this target group.
        """
        return pulumi.get(self, "load_balancer_arns")

    @property
    @pulumi.getter
    def matcher(self) -> Optional['outputs.TargetGroupMatcher']:
        """
        [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking for a successful response from a target.
        """
        return pulumi.get(self, "matcher")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetGroupArn")
    def target_group_arn(self) -> Optional[str]:
        """
        The ARN of the Target Group
        """
        return pulumi.get(self, "target_group_arn")

    @property
    @pulumi.getter(name="targetGroupAttributes")
    def target_group_attributes(self) -> Optional[Sequence['outputs.TargetGroupAttribute']]:
        """
        The attributes.
        """
        return pulumi.get(self, "target_group_attributes")

    @property
    @pulumi.getter(name="targetGroupFullName")
    def target_group_full_name(self) -> Optional[str]:
        """
        The full name of the target group.
        """
        return pulumi.get(self, "target_group_full_name")

    @property
    @pulumi.getter(name="targetGroupName")
    def target_group_name(self) -> Optional[str]:
        """
        The name of the target group.
        """
        return pulumi.get(self, "target_group_name")

    @property
    @pulumi.getter
    def targets(self) -> Optional[Sequence['outputs.TargetGroupTargetDescription']]:
        """
        The targets.
        """
        return pulumi.get(self, "targets")

    @property
    @pulumi.getter(name="unhealthyThresholdCount")
    def unhealthy_threshold_count(self) -> Optional[int]:
        """
        The number of consecutive health check failures required before considering a target unhealthy.
        """
        return pulumi.get(self, "unhealthy_threshold_count")


class AwaitableGetTargetGroupResult(GetTargetGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTargetGroupResult(
            health_check_enabled=self.health_check_enabled,
            health_check_interval_seconds=self.health_check_interval_seconds,
            health_check_path=self.health_check_path,
            health_check_port=self.health_check_port,
            health_check_protocol=self.health_check_protocol,
            health_check_timeout_seconds=self.health_check_timeout_seconds,
            healthy_threshold_count=self.healthy_threshold_count,
            load_balancer_arns=self.load_balancer_arns,
            matcher=self.matcher,
            tags=self.tags,
            target_group_arn=self.target_group_arn,
            target_group_attributes=self.target_group_attributes,
            target_group_full_name=self.target_group_full_name,
            target_group_name=self.target_group_name,
            targets=self.targets,
            unhealthy_threshold_count=self.unhealthy_threshold_count)


def get_target_group(target_group_arn: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTargetGroupResult:
    """
    Resource Type definition for AWS::ElasticLoadBalancingV2::TargetGroup


    :param str target_group_arn: The ARN of the Target Group
    """
    __args__ = dict()
    __args__['targetGroupArn'] = target_group_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:elasticloadbalancingv2:getTargetGroup', __args__, opts=opts, typ=GetTargetGroupResult).value

    return AwaitableGetTargetGroupResult(
        health_check_enabled=pulumi.get(__ret__, 'health_check_enabled'),
        health_check_interval_seconds=pulumi.get(__ret__, 'health_check_interval_seconds'),
        health_check_path=pulumi.get(__ret__, 'health_check_path'),
        health_check_port=pulumi.get(__ret__, 'health_check_port'),
        health_check_protocol=pulumi.get(__ret__, 'health_check_protocol'),
        health_check_timeout_seconds=pulumi.get(__ret__, 'health_check_timeout_seconds'),
        healthy_threshold_count=pulumi.get(__ret__, 'healthy_threshold_count'),
        load_balancer_arns=pulumi.get(__ret__, 'load_balancer_arns'),
        matcher=pulumi.get(__ret__, 'matcher'),
        tags=pulumi.get(__ret__, 'tags'),
        target_group_arn=pulumi.get(__ret__, 'target_group_arn'),
        target_group_attributes=pulumi.get(__ret__, 'target_group_attributes'),
        target_group_full_name=pulumi.get(__ret__, 'target_group_full_name'),
        target_group_name=pulumi.get(__ret__, 'target_group_name'),
        targets=pulumi.get(__ret__, 'targets'),
        unhealthy_threshold_count=pulumi.get(__ret__, 'unhealthy_threshold_count'))
def get_target_group_output(target_group_arn: Optional[pulumi.Input[str]] = None,
                            opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetTargetGroupResult]:
    """
    Resource Type definition for AWS::ElasticLoadBalancingV2::TargetGroup


    :param str target_group_arn: The ARN of the Target Group
    """
    __args__ = dict()
    __args__['targetGroupArn'] = target_group_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:elasticloadbalancingv2:getTargetGroup', __args__, opts=opts, typ=GetTargetGroupResult)
    return __ret__.apply(lambda __response__: GetTargetGroupResult(
        health_check_enabled=pulumi.get(__response__, 'health_check_enabled'),
        health_check_interval_seconds=pulumi.get(__response__, 'health_check_interval_seconds'),
        health_check_path=pulumi.get(__response__, 'health_check_path'),
        health_check_port=pulumi.get(__response__, 'health_check_port'),
        health_check_protocol=pulumi.get(__response__, 'health_check_protocol'),
        health_check_timeout_seconds=pulumi.get(__response__, 'health_check_timeout_seconds'),
        healthy_threshold_count=pulumi.get(__response__, 'healthy_threshold_count'),
        load_balancer_arns=pulumi.get(__response__, 'load_balancer_arns'),
        matcher=pulumi.get(__response__, 'matcher'),
        tags=pulumi.get(__response__, 'tags'),
        target_group_arn=pulumi.get(__response__, 'target_group_arn'),
        target_group_attributes=pulumi.get(__response__, 'target_group_attributes'),
        target_group_full_name=pulumi.get(__response__, 'target_group_full_name'),
        target_group_name=pulumi.get(__response__, 'target_group_name'),
        targets=pulumi.get(__response__, 'targets'),
        unhealthy_threshold_count=pulumi.get(__response__, 'unhealthy_threshold_count')))
