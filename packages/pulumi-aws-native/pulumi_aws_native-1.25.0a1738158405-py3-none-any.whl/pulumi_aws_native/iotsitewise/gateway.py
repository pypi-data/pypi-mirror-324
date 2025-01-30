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

__all__ = ['GatewayArgs', 'Gateway']

@pulumi.input_type
class GatewayArgs:
    def __init__(__self__, *,
                 gateway_platform: pulumi.Input['GatewayPlatformArgs'],
                 gateway_capability_summaries: Optional[pulumi.Input[Sequence[pulumi.Input['GatewayCapabilitySummaryArgs']]]] = None,
                 gateway_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Gateway resource.
        :param pulumi.Input['GatewayPlatformArgs'] gateway_platform: The gateway's platform. You can only specify one platform in a gateway.
        :param pulumi.Input[Sequence[pulumi.Input['GatewayCapabilitySummaryArgs']]] gateway_capability_summaries: A list of gateway capability summaries that each contain a namespace and status.
        :param pulumi.Input[str] gateway_name: A unique, friendly name for the gateway.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: A list of key-value pairs that contain metadata for the gateway.
        """
        pulumi.set(__self__, "gateway_platform", gateway_platform)
        if gateway_capability_summaries is not None:
            pulumi.set(__self__, "gateway_capability_summaries", gateway_capability_summaries)
        if gateway_name is not None:
            pulumi.set(__self__, "gateway_name", gateway_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="gatewayPlatform")
    def gateway_platform(self) -> pulumi.Input['GatewayPlatformArgs']:
        """
        The gateway's platform. You can only specify one platform in a gateway.
        """
        return pulumi.get(self, "gateway_platform")

    @gateway_platform.setter
    def gateway_platform(self, value: pulumi.Input['GatewayPlatformArgs']):
        pulumi.set(self, "gateway_platform", value)

    @property
    @pulumi.getter(name="gatewayCapabilitySummaries")
    def gateway_capability_summaries(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GatewayCapabilitySummaryArgs']]]]:
        """
        A list of gateway capability summaries that each contain a namespace and status.
        """
        return pulumi.get(self, "gateway_capability_summaries")

    @gateway_capability_summaries.setter
    def gateway_capability_summaries(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GatewayCapabilitySummaryArgs']]]]):
        pulumi.set(self, "gateway_capability_summaries", value)

    @property
    @pulumi.getter(name="gatewayName")
    def gateway_name(self) -> Optional[pulumi.Input[str]]:
        """
        A unique, friendly name for the gateway.
        """
        return pulumi.get(self, "gateway_name")

    @gateway_name.setter
    def gateway_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gateway_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        A list of key-value pairs that contain metadata for the gateway.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Gateway(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 gateway_capability_summaries: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GatewayCapabilitySummaryArgs', 'GatewayCapabilitySummaryArgsDict']]]]] = None,
                 gateway_name: Optional[pulumi.Input[str]] = None,
                 gateway_platform: Optional[pulumi.Input[Union['GatewayPlatformArgs', 'GatewayPlatformArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource schema for AWS::IoTSiteWise::Gateway

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['GatewayCapabilitySummaryArgs', 'GatewayCapabilitySummaryArgsDict']]]] gateway_capability_summaries: A list of gateway capability summaries that each contain a namespace and status.
        :param pulumi.Input[str] gateway_name: A unique, friendly name for the gateway.
        :param pulumi.Input[Union['GatewayPlatformArgs', 'GatewayPlatformArgsDict']] gateway_platform: The gateway's platform. You can only specify one platform in a gateway.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: A list of key-value pairs that contain metadata for the gateway.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GatewayArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::IoTSiteWise::Gateway

        :param str resource_name: The name of the resource.
        :param GatewayArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GatewayArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 gateway_capability_summaries: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GatewayCapabilitySummaryArgs', 'GatewayCapabilitySummaryArgsDict']]]]] = None,
                 gateway_name: Optional[pulumi.Input[str]] = None,
                 gateway_platform: Optional[pulumi.Input[Union['GatewayPlatformArgs', 'GatewayPlatformArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GatewayArgs.__new__(GatewayArgs)

            __props__.__dict__["gateway_capability_summaries"] = gateway_capability_summaries
            __props__.__dict__["gateway_name"] = gateway_name
            if gateway_platform is None and not opts.urn:
                raise TypeError("Missing required property 'gateway_platform'")
            __props__.__dict__["gateway_platform"] = gateway_platform
            __props__.__dict__["tags"] = tags
            __props__.__dict__["gateway_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["gatewayPlatform"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Gateway, __self__).__init__(
            'aws-native:iotsitewise:Gateway',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Gateway':
        """
        Get an existing Gateway resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = GatewayArgs.__new__(GatewayArgs)

        __props__.__dict__["gateway_capability_summaries"] = None
        __props__.__dict__["gateway_id"] = None
        __props__.__dict__["gateway_name"] = None
        __props__.__dict__["gateway_platform"] = None
        __props__.__dict__["tags"] = None
        return Gateway(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="gatewayCapabilitySummaries")
    def gateway_capability_summaries(self) -> pulumi.Output[Optional[Sequence['outputs.GatewayCapabilitySummary']]]:
        """
        A list of gateway capability summaries that each contain a namespace and status.
        """
        return pulumi.get(self, "gateway_capability_summaries")

    @property
    @pulumi.getter(name="gatewayId")
    def gateway_id(self) -> pulumi.Output[str]:
        """
        The ID of the gateway device.
        """
        return pulumi.get(self, "gateway_id")

    @property
    @pulumi.getter(name="gatewayName")
    def gateway_name(self) -> pulumi.Output[str]:
        """
        A unique, friendly name for the gateway.
        """
        return pulumi.get(self, "gateway_name")

    @property
    @pulumi.getter(name="gatewayPlatform")
    def gateway_platform(self) -> pulumi.Output['outputs.GatewayPlatform']:
        """
        The gateway's platform. You can only specify one platform in a gateway.
        """
        return pulumi.get(self, "gateway_platform")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        A list of key-value pairs that contain metadata for the gateway.
        """
        return pulumi.get(self, "tags")

