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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs

__all__ = ['LocalGatewayRouteTableArgs', 'LocalGatewayRouteTable']

@pulumi.input_type
class LocalGatewayRouteTableArgs:
    def __init__(__self__, *,
                 local_gateway_id: pulumi.Input[str],
                 mode: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a LocalGatewayRouteTable resource.
        :param pulumi.Input[str] local_gateway_id: The ID of the local gateway.
        :param pulumi.Input[str] mode: The mode of the local gateway route table.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags for the local gateway route table.
        """
        pulumi.set(__self__, "local_gateway_id", local_gateway_id)
        if mode is not None:
            pulumi.set(__self__, "mode", mode)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="localGatewayId")
    def local_gateway_id(self) -> pulumi.Input[str]:
        """
        The ID of the local gateway.
        """
        return pulumi.get(self, "local_gateway_id")

    @local_gateway_id.setter
    def local_gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "local_gateway_id", value)

    @property
    @pulumi.getter
    def mode(self) -> Optional[pulumi.Input[str]]:
        """
        The mode of the local gateway route table.
        """
        return pulumi.get(self, "mode")

    @mode.setter
    def mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mode", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags for the local gateway route table.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class LocalGatewayRouteTable(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 local_gateway_id: Optional[pulumi.Input[str]] = None,
                 mode: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Describes a route table for a local gateway.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] local_gateway_id: The ID of the local gateway.
        :param pulumi.Input[str] mode: The mode of the local gateway route table.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags for the local gateway route table.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LocalGatewayRouteTableArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Describes a route table for a local gateway.

        :param str resource_name: The name of the resource.
        :param LocalGatewayRouteTableArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LocalGatewayRouteTableArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 local_gateway_id: Optional[pulumi.Input[str]] = None,
                 mode: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LocalGatewayRouteTableArgs.__new__(LocalGatewayRouteTableArgs)

            if local_gateway_id is None and not opts.urn:
                raise TypeError("Missing required property 'local_gateway_id'")
            __props__.__dict__["local_gateway_id"] = local_gateway_id
            __props__.__dict__["mode"] = mode
            __props__.__dict__["tags"] = tags
            __props__.__dict__["local_gateway_route_table_arn"] = None
            __props__.__dict__["local_gateway_route_table_id"] = None
            __props__.__dict__["outpost_arn"] = None
            __props__.__dict__["owner_id"] = None
            __props__.__dict__["state"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["localGatewayId", "mode"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(LocalGatewayRouteTable, __self__).__init__(
            'aws-native:ec2:LocalGatewayRouteTable',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'LocalGatewayRouteTable':
        """
        Get an existing LocalGatewayRouteTable resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = LocalGatewayRouteTableArgs.__new__(LocalGatewayRouteTableArgs)

        __props__.__dict__["local_gateway_id"] = None
        __props__.__dict__["local_gateway_route_table_arn"] = None
        __props__.__dict__["local_gateway_route_table_id"] = None
        __props__.__dict__["mode"] = None
        __props__.__dict__["outpost_arn"] = None
        __props__.__dict__["owner_id"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["tags"] = None
        return LocalGatewayRouteTable(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="localGatewayId")
    def local_gateway_id(self) -> pulumi.Output[str]:
        """
        The ID of the local gateway.
        """
        return pulumi.get(self, "local_gateway_id")

    @property
    @pulumi.getter(name="localGatewayRouteTableArn")
    def local_gateway_route_table_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the local gateway route table.
        """
        return pulumi.get(self, "local_gateway_route_table_arn")

    @property
    @pulumi.getter(name="localGatewayRouteTableId")
    def local_gateway_route_table_id(self) -> pulumi.Output[str]:
        """
        The ID of the local gateway route table.
        """
        return pulumi.get(self, "local_gateway_route_table_id")

    @property
    @pulumi.getter
    def mode(self) -> pulumi.Output[Optional[str]]:
        """
        The mode of the local gateway route table.
        """
        return pulumi.get(self, "mode")

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the outpost.
        """
        return pulumi.get(self, "outpost_arn")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        The owner of the local gateway route table.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the local gateway route table.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags for the local gateway route table.
        """
        return pulumi.get(self, "tags")

