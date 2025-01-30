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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs
from ._inputs import *

__all__ = ['TargetGroupArgs', 'TargetGroup']

@pulumi.input_type
class TargetGroupArgs:
    def __init__(__self__, *,
                 health_check_enabled: Optional[pulumi.Input[bool]] = None,
                 health_check_interval_seconds: Optional[pulumi.Input[int]] = None,
                 health_check_path: Optional[pulumi.Input[str]] = None,
                 health_check_port: Optional[pulumi.Input[str]] = None,
                 health_check_protocol: Optional[pulumi.Input[str]] = None,
                 health_check_timeout_seconds: Optional[pulumi.Input[int]] = None,
                 healthy_threshold_count: Optional[pulumi.Input[int]] = None,
                 ip_address_type: Optional[pulumi.Input[str]] = None,
                 matcher: Optional[pulumi.Input['TargetGroupMatcherArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 protocol_version: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 target_group_attributes: Optional[pulumi.Input[Sequence[pulumi.Input['TargetGroupAttributeArgs']]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input['TargetGroupTargetDescriptionArgs']]]] = None,
                 unhealthy_threshold_count: Optional[pulumi.Input[int]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TargetGroup resource.
        :param pulumi.Input[bool] health_check_enabled: Indicates whether health checks are enabled. If the target type is lambda, health checks are disabled by default but can be enabled. If the target type is instance, ip, or alb, health checks are always enabled and cannot be disabled.
        :param pulumi.Input[int] health_check_interval_seconds: The approximate amount of time, in seconds, between health checks of an individual target.
        :param pulumi.Input[str] health_check_path: [HTTP/HTTPS health checks] The destination for health checks on the targets. [HTTP1 or HTTP2 protocol version] The ping path. The default is /. [GRPC protocol version] The path of a custom health check method with the format /package.service/method. The default is /AWS.ALB/healthcheck.
        :param pulumi.Input[str] health_check_port: The port the load balancer uses when performing health checks on targets. 
        :param pulumi.Input[str] health_check_protocol: The protocol the load balancer uses when performing health checks on targets. 
        :param pulumi.Input[int] health_check_timeout_seconds: The amount of time, in seconds, during which no response from a target means a failed health check.
        :param pulumi.Input[int] healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. 
        :param pulumi.Input[str] ip_address_type: The type of IP address used for this target group. The possible values are ipv4 and ipv6. 
        :param pulumi.Input['TargetGroupMatcherArgs'] matcher: [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking for a successful response from a target.
        :param pulumi.Input[str] name: The name of the target group.
        :param pulumi.Input[int] port: The port on which the targets receive traffic. This port is used unless you specify a port override when registering the target. If the target is a Lambda function, this parameter does not apply. If the protocol is GENEVE, the supported port is 6081.
        :param pulumi.Input[str] protocol: The protocol to use for routing traffic to the targets.
        :param pulumi.Input[str] protocol_version: [HTTP/HTTPS protocol] The protocol version. The possible values are GRPC, HTTP1, and HTTP2.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags.
        :param pulumi.Input[Sequence[pulumi.Input['TargetGroupAttributeArgs']]] target_group_attributes: The attributes.
        :param pulumi.Input[str] target_type: The type of target that you must specify when registering targets with this target group. You can't specify targets for a target group using more than one target type.
        :param pulumi.Input[Sequence[pulumi.Input['TargetGroupTargetDescriptionArgs']]] targets: The targets.
        :param pulumi.Input[int] unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy.
        :param pulumi.Input[str] vpc_id: The identifier of the virtual private cloud (VPC). If the target is a Lambda function, this parameter does not apply.
        """
        if health_check_enabled is not None:
            pulumi.set(__self__, "health_check_enabled", health_check_enabled)
        if health_check_interval_seconds is not None:
            pulumi.set(__self__, "health_check_interval_seconds", health_check_interval_seconds)
        if health_check_path is not None:
            pulumi.set(__self__, "health_check_path", health_check_path)
        if health_check_port is not None:
            pulumi.set(__self__, "health_check_port", health_check_port)
        if health_check_protocol is not None:
            pulumi.set(__self__, "health_check_protocol", health_check_protocol)
        if health_check_timeout_seconds is not None:
            pulumi.set(__self__, "health_check_timeout_seconds", health_check_timeout_seconds)
        if healthy_threshold_count is not None:
            pulumi.set(__self__, "healthy_threshold_count", healthy_threshold_count)
        if ip_address_type is not None:
            pulumi.set(__self__, "ip_address_type", ip_address_type)
        if matcher is not None:
            pulumi.set(__self__, "matcher", matcher)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if protocol_version is not None:
            pulumi.set(__self__, "protocol_version", protocol_version)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if target_group_attributes is not None:
            pulumi.set(__self__, "target_group_attributes", target_group_attributes)
        if target_type is not None:
            pulumi.set(__self__, "target_type", target_type)
        if targets is not None:
            pulumi.set(__self__, "targets", targets)
        if unhealthy_threshold_count is not None:
            pulumi.set(__self__, "unhealthy_threshold_count", unhealthy_threshold_count)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="healthCheckEnabled")
    def health_check_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether health checks are enabled. If the target type is lambda, health checks are disabled by default but can be enabled. If the target type is instance, ip, or alb, health checks are always enabled and cannot be disabled.
        """
        return pulumi.get(self, "health_check_enabled")

    @health_check_enabled.setter
    def health_check_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "health_check_enabled", value)

    @property
    @pulumi.getter(name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The approximate amount of time, in seconds, between health checks of an individual target.
        """
        return pulumi.get(self, "health_check_interval_seconds")

    @health_check_interval_seconds.setter
    def health_check_interval_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "health_check_interval_seconds", value)

    @property
    @pulumi.getter(name="healthCheckPath")
    def health_check_path(self) -> Optional[pulumi.Input[str]]:
        """
        [HTTP/HTTPS health checks] The destination for health checks on the targets. [HTTP1 or HTTP2 protocol version] The ping path. The default is /. [GRPC protocol version] The path of a custom health check method with the format /package.service/method. The default is /AWS.ALB/healthcheck.
        """
        return pulumi.get(self, "health_check_path")

    @health_check_path.setter
    def health_check_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "health_check_path", value)

    @property
    @pulumi.getter(name="healthCheckPort")
    def health_check_port(self) -> Optional[pulumi.Input[str]]:
        """
        The port the load balancer uses when performing health checks on targets. 
        """
        return pulumi.get(self, "health_check_port")

    @health_check_port.setter
    def health_check_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "health_check_port", value)

    @property
    @pulumi.getter(name="healthCheckProtocol")
    def health_check_protocol(self) -> Optional[pulumi.Input[str]]:
        """
        The protocol the load balancer uses when performing health checks on targets. 
        """
        return pulumi.get(self, "health_check_protocol")

    @health_check_protocol.setter
    def health_check_protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "health_check_protocol", value)

    @property
    @pulumi.getter(name="healthCheckTimeoutSeconds")
    def health_check_timeout_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The amount of time, in seconds, during which no response from a target means a failed health check.
        """
        return pulumi.get(self, "health_check_timeout_seconds")

    @health_check_timeout_seconds.setter
    def health_check_timeout_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "health_check_timeout_seconds", value)

    @property
    @pulumi.getter(name="healthyThresholdCount")
    def healthy_threshold_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of consecutive health checks successes required before considering an unhealthy target healthy. 
        """
        return pulumi.get(self, "healthy_threshold_count")

    @healthy_threshold_count.setter
    def healthy_threshold_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "healthy_threshold_count", value)

    @property
    @pulumi.getter(name="ipAddressType")
    def ip_address_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of IP address used for this target group. The possible values are ipv4 and ipv6. 
        """
        return pulumi.get(self, "ip_address_type")

    @ip_address_type.setter
    def ip_address_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address_type", value)

    @property
    @pulumi.getter
    def matcher(self) -> Optional[pulumi.Input['TargetGroupMatcherArgs']]:
        """
        [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking for a successful response from a target.
        """
        return pulumi.get(self, "matcher")

    @matcher.setter
    def matcher(self, value: Optional[pulumi.Input['TargetGroupMatcherArgs']]):
        pulumi.set(self, "matcher", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the target group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The port on which the targets receive traffic. This port is used unless you specify a port override when registering the target. If the target is a Lambda function, this parameter does not apply. If the protocol is GENEVE, the supported port is 6081.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[str]]:
        """
        The protocol to use for routing traffic to the targets.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="protocolVersion")
    def protocol_version(self) -> Optional[pulumi.Input[str]]:
        """
        [HTTP/HTTPS protocol] The protocol version. The possible values are GRPC, HTTP1, and HTTP2.
        """
        return pulumi.get(self, "protocol_version")

    @protocol_version.setter
    def protocol_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol_version", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="targetGroupAttributes")
    def target_group_attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TargetGroupAttributeArgs']]]]:
        """
        The attributes.
        """
        return pulumi.get(self, "target_group_attributes")

    @target_group_attributes.setter
    def target_group_attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TargetGroupAttributeArgs']]]]):
        pulumi.set(self, "target_group_attributes", value)

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of target that you must specify when registering targets with this target group. You can't specify targets for a target group using more than one target type.
        """
        return pulumi.get(self, "target_type")

    @target_type.setter
    def target_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_type", value)

    @property
    @pulumi.getter
    def targets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TargetGroupTargetDescriptionArgs']]]]:
        """
        The targets.
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TargetGroupTargetDescriptionArgs']]]]):
        pulumi.set(self, "targets", value)

    @property
    @pulumi.getter(name="unhealthyThresholdCount")
    def unhealthy_threshold_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of consecutive health check failures required before considering a target unhealthy.
        """
        return pulumi.get(self, "unhealthy_threshold_count")

    @unhealthy_threshold_count.setter
    def unhealthy_threshold_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "unhealthy_threshold_count", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the virtual private cloud (VPC). If the target is a Lambda function, this parameter does not apply.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class TargetGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 health_check_enabled: Optional[pulumi.Input[bool]] = None,
                 health_check_interval_seconds: Optional[pulumi.Input[int]] = None,
                 health_check_path: Optional[pulumi.Input[str]] = None,
                 health_check_port: Optional[pulumi.Input[str]] = None,
                 health_check_protocol: Optional[pulumi.Input[str]] = None,
                 health_check_timeout_seconds: Optional[pulumi.Input[int]] = None,
                 healthy_threshold_count: Optional[pulumi.Input[int]] = None,
                 ip_address_type: Optional[pulumi.Input[str]] = None,
                 matcher: Optional[pulumi.Input[Union['TargetGroupMatcherArgs', 'TargetGroupMatcherArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 protocol_version: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 target_group_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TargetGroupAttributeArgs', 'TargetGroupAttributeArgsDict']]]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TargetGroupTargetDescriptionArgs', 'TargetGroupTargetDescriptionArgsDict']]]]] = None,
                 unhealthy_threshold_count: Optional[pulumi.Input[int]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::ElasticLoadBalancingV2::TargetGroup

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] health_check_enabled: Indicates whether health checks are enabled. If the target type is lambda, health checks are disabled by default but can be enabled. If the target type is instance, ip, or alb, health checks are always enabled and cannot be disabled.
        :param pulumi.Input[int] health_check_interval_seconds: The approximate amount of time, in seconds, between health checks of an individual target.
        :param pulumi.Input[str] health_check_path: [HTTP/HTTPS health checks] The destination for health checks on the targets. [HTTP1 or HTTP2 protocol version] The ping path. The default is /. [GRPC protocol version] The path of a custom health check method with the format /package.service/method. The default is /AWS.ALB/healthcheck.
        :param pulumi.Input[str] health_check_port: The port the load balancer uses when performing health checks on targets. 
        :param pulumi.Input[str] health_check_protocol: The protocol the load balancer uses when performing health checks on targets. 
        :param pulumi.Input[int] health_check_timeout_seconds: The amount of time, in seconds, during which no response from a target means a failed health check.
        :param pulumi.Input[int] healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. 
        :param pulumi.Input[str] ip_address_type: The type of IP address used for this target group. The possible values are ipv4 and ipv6. 
        :param pulumi.Input[Union['TargetGroupMatcherArgs', 'TargetGroupMatcherArgsDict']] matcher: [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking for a successful response from a target.
        :param pulumi.Input[str] name: The name of the target group.
        :param pulumi.Input[int] port: The port on which the targets receive traffic. This port is used unless you specify a port override when registering the target. If the target is a Lambda function, this parameter does not apply. If the protocol is GENEVE, the supported port is 6081.
        :param pulumi.Input[str] protocol: The protocol to use for routing traffic to the targets.
        :param pulumi.Input[str] protocol_version: [HTTP/HTTPS protocol] The protocol version. The possible values are GRPC, HTTP1, and HTTP2.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags.
        :param pulumi.Input[Sequence[pulumi.Input[Union['TargetGroupAttributeArgs', 'TargetGroupAttributeArgsDict']]]] target_group_attributes: The attributes.
        :param pulumi.Input[str] target_type: The type of target that you must specify when registering targets with this target group. You can't specify targets for a target group using more than one target type.
        :param pulumi.Input[Sequence[pulumi.Input[Union['TargetGroupTargetDescriptionArgs', 'TargetGroupTargetDescriptionArgsDict']]]] targets: The targets.
        :param pulumi.Input[int] unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy.
        :param pulumi.Input[str] vpc_id: The identifier of the virtual private cloud (VPC). If the target is a Lambda function, this parameter does not apply.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[TargetGroupArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::ElasticLoadBalancingV2::TargetGroup

        :param str resource_name: The name of the resource.
        :param TargetGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TargetGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 health_check_enabled: Optional[pulumi.Input[bool]] = None,
                 health_check_interval_seconds: Optional[pulumi.Input[int]] = None,
                 health_check_path: Optional[pulumi.Input[str]] = None,
                 health_check_port: Optional[pulumi.Input[str]] = None,
                 health_check_protocol: Optional[pulumi.Input[str]] = None,
                 health_check_timeout_seconds: Optional[pulumi.Input[int]] = None,
                 healthy_threshold_count: Optional[pulumi.Input[int]] = None,
                 ip_address_type: Optional[pulumi.Input[str]] = None,
                 matcher: Optional[pulumi.Input[Union['TargetGroupMatcherArgs', 'TargetGroupMatcherArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 protocol_version: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 target_group_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TargetGroupAttributeArgs', 'TargetGroupAttributeArgsDict']]]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TargetGroupTargetDescriptionArgs', 'TargetGroupTargetDescriptionArgsDict']]]]] = None,
                 unhealthy_threshold_count: Optional[pulumi.Input[int]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TargetGroupArgs.__new__(TargetGroupArgs)

            __props__.__dict__["health_check_enabled"] = health_check_enabled
            __props__.__dict__["health_check_interval_seconds"] = health_check_interval_seconds
            __props__.__dict__["health_check_path"] = health_check_path
            __props__.__dict__["health_check_port"] = health_check_port
            __props__.__dict__["health_check_protocol"] = health_check_protocol
            __props__.__dict__["health_check_timeout_seconds"] = health_check_timeout_seconds
            __props__.__dict__["healthy_threshold_count"] = healthy_threshold_count
            __props__.__dict__["ip_address_type"] = ip_address_type
            __props__.__dict__["matcher"] = matcher
            __props__.__dict__["name"] = name
            __props__.__dict__["port"] = port
            __props__.__dict__["protocol"] = protocol
            __props__.__dict__["protocol_version"] = protocol_version
            __props__.__dict__["tags"] = tags
            __props__.__dict__["target_group_attributes"] = target_group_attributes
            __props__.__dict__["target_type"] = target_type
            __props__.__dict__["targets"] = targets
            __props__.__dict__["unhealthy_threshold_count"] = unhealthy_threshold_count
            __props__.__dict__["vpc_id"] = vpc_id
            __props__.__dict__["load_balancer_arns"] = None
            __props__.__dict__["target_group_arn"] = None
            __props__.__dict__["target_group_full_name"] = None
            __props__.__dict__["target_group_name"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["ipAddressType", "name", "port", "protocol", "protocolVersion", "targetType", "vpcId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(TargetGroup, __self__).__init__(
            'aws-native:elasticloadbalancingv2:TargetGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TargetGroup':
        """
        Get an existing TargetGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TargetGroupArgs.__new__(TargetGroupArgs)

        __props__.__dict__["health_check_enabled"] = None
        __props__.__dict__["health_check_interval_seconds"] = None
        __props__.__dict__["health_check_path"] = None
        __props__.__dict__["health_check_port"] = None
        __props__.__dict__["health_check_protocol"] = None
        __props__.__dict__["health_check_timeout_seconds"] = None
        __props__.__dict__["healthy_threshold_count"] = None
        __props__.__dict__["ip_address_type"] = None
        __props__.__dict__["load_balancer_arns"] = None
        __props__.__dict__["matcher"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["port"] = None
        __props__.__dict__["protocol"] = None
        __props__.__dict__["protocol_version"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["target_group_arn"] = None
        __props__.__dict__["target_group_attributes"] = None
        __props__.__dict__["target_group_full_name"] = None
        __props__.__dict__["target_group_name"] = None
        __props__.__dict__["target_type"] = None
        __props__.__dict__["targets"] = None
        __props__.__dict__["unhealthy_threshold_count"] = None
        __props__.__dict__["vpc_id"] = None
        return TargetGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="healthCheckEnabled")
    def health_check_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether health checks are enabled. If the target type is lambda, health checks are disabled by default but can be enabled. If the target type is instance, ip, or alb, health checks are always enabled and cannot be disabled.
        """
        return pulumi.get(self, "health_check_enabled")

    @property
    @pulumi.getter(name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        The approximate amount of time, in seconds, between health checks of an individual target.
        """
        return pulumi.get(self, "health_check_interval_seconds")

    @property
    @pulumi.getter(name="healthCheckPath")
    def health_check_path(self) -> pulumi.Output[Optional[str]]:
        """
        [HTTP/HTTPS health checks] The destination for health checks on the targets. [HTTP1 or HTTP2 protocol version] The ping path. The default is /. [GRPC protocol version] The path of a custom health check method with the format /package.service/method. The default is /AWS.ALB/healthcheck.
        """
        return pulumi.get(self, "health_check_path")

    @property
    @pulumi.getter(name="healthCheckPort")
    def health_check_port(self) -> pulumi.Output[Optional[str]]:
        """
        The port the load balancer uses when performing health checks on targets. 
        """
        return pulumi.get(self, "health_check_port")

    @property
    @pulumi.getter(name="healthCheckProtocol")
    def health_check_protocol(self) -> pulumi.Output[Optional[str]]:
        """
        The protocol the load balancer uses when performing health checks on targets. 
        """
        return pulumi.get(self, "health_check_protocol")

    @property
    @pulumi.getter(name="healthCheckTimeoutSeconds")
    def health_check_timeout_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        The amount of time, in seconds, during which no response from a target means a failed health check.
        """
        return pulumi.get(self, "health_check_timeout_seconds")

    @property
    @pulumi.getter(name="healthyThresholdCount")
    def healthy_threshold_count(self) -> pulumi.Output[Optional[int]]:
        """
        The number of consecutive health checks successes required before considering an unhealthy target healthy. 
        """
        return pulumi.get(self, "healthy_threshold_count")

    @property
    @pulumi.getter(name="ipAddressType")
    def ip_address_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of IP address used for this target group. The possible values are ipv4 and ipv6. 
        """
        return pulumi.get(self, "ip_address_type")

    @property
    @pulumi.getter(name="loadBalancerArns")
    def load_balancer_arns(self) -> pulumi.Output[Sequence[str]]:
        """
        The Amazon Resource Names (ARNs) of the load balancers that route traffic to this target group.
        """
        return pulumi.get(self, "load_balancer_arns")

    @property
    @pulumi.getter
    def matcher(self) -> pulumi.Output[Optional['outputs.TargetGroupMatcher']]:
        """
        [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking for a successful response from a target.
        """
        return pulumi.get(self, "matcher")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the target group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        """
        The port on which the targets receive traffic. This port is used unless you specify a port override when registering the target. If the target is a Lambda function, this parameter does not apply. If the protocol is GENEVE, the supported port is 6081.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[Optional[str]]:
        """
        The protocol to use for routing traffic to the targets.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="protocolVersion")
    def protocol_version(self) -> pulumi.Output[Optional[str]]:
        """
        [HTTP/HTTPS protocol] The protocol version. The possible values are GRPC, HTTP1, and HTTP2.
        """
        return pulumi.get(self, "protocol_version")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetGroupArn")
    def target_group_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Target Group
        """
        return pulumi.get(self, "target_group_arn")

    @property
    @pulumi.getter(name="targetGroupAttributes")
    def target_group_attributes(self) -> pulumi.Output[Optional[Sequence['outputs.TargetGroupAttribute']]]:
        """
        The attributes.
        """
        return pulumi.get(self, "target_group_attributes")

    @property
    @pulumi.getter(name="targetGroupFullName")
    def target_group_full_name(self) -> pulumi.Output[str]:
        """
        The full name of the target group.
        """
        return pulumi.get(self, "target_group_full_name")

    @property
    @pulumi.getter(name="targetGroupName")
    def target_group_name(self) -> pulumi.Output[str]:
        """
        The name of the target group.
        """
        return pulumi.get(self, "target_group_name")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of target that you must specify when registering targets with this target group. You can't specify targets for a target group using more than one target type.
        """
        return pulumi.get(self, "target_type")

    @property
    @pulumi.getter
    def targets(self) -> pulumi.Output[Optional[Sequence['outputs.TargetGroupTargetDescription']]]:
        """
        The targets.
        """
        return pulumi.get(self, "targets")

    @property
    @pulumi.getter(name="unhealthyThresholdCount")
    def unhealthy_threshold_count(self) -> pulumi.Output[Optional[int]]:
        """
        The number of consecutive health check failures required before considering a target unhealthy.
        """
        return pulumi.get(self, "unhealthy_threshold_count")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[Optional[str]]:
        """
        The identifier of the virtual private cloud (VPC). If the target is a Lambda function, this parameter does not apply.
        """
        return pulumi.get(self, "vpc_id")

