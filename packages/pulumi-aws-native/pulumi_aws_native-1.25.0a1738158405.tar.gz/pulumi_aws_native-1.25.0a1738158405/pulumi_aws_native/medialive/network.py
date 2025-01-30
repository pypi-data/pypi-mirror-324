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
from ._enums import *
from ._inputs import *

__all__ = ['NetworkArgs', 'Network']

@pulumi.input_type
class NetworkArgs:
    def __init__(__self__, *,
                 ip_pools: pulumi.Input[Sequence[pulumi.Input['NetworkIpPoolArgs']]],
                 name: Optional[pulumi.Input[str]] = None,
                 routes: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkRouteArgs']]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Network resource.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkIpPoolArgs']]] ip_pools: The list of IP address cidr pools for the network
        :param pulumi.Input[str] name: The user-specified name of the Network to be created.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkRouteArgs']]] routes: The routes for the network
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: A collection of key-value pairs.
        """
        pulumi.set(__self__, "ip_pools", ip_pools)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if routes is not None:
            pulumi.set(__self__, "routes", routes)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="ipPools")
    def ip_pools(self) -> pulumi.Input[Sequence[pulumi.Input['NetworkIpPoolArgs']]]:
        """
        The list of IP address cidr pools for the network
        """
        return pulumi.get(self, "ip_pools")

    @ip_pools.setter
    def ip_pools(self, value: pulumi.Input[Sequence[pulumi.Input['NetworkIpPoolArgs']]]):
        pulumi.set(self, "ip_pools", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The user-specified name of the Network to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def routes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkRouteArgs']]]]:
        """
        The routes for the network
        """
        return pulumi.get(self, "routes")

    @routes.setter
    def routes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkRouteArgs']]]]):
        pulumi.set(self, "routes", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        A collection of key-value pairs.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Network(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ip_pools: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkIpPoolArgs', 'NetworkIpPoolArgsDict']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 routes: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkRouteArgs', 'NetworkRouteArgsDict']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource schema for AWS::MediaLive::Network.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['NetworkIpPoolArgs', 'NetworkIpPoolArgsDict']]]] ip_pools: The list of IP address cidr pools for the network
        :param pulumi.Input[str] name: The user-specified name of the Network to be created.
        :param pulumi.Input[Sequence[pulumi.Input[Union['NetworkRouteArgs', 'NetworkRouteArgsDict']]]] routes: The routes for the network
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: A collection of key-value pairs.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::MediaLive::Network.

        :param str resource_name: The name of the resource.
        :param NetworkArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ip_pools: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkIpPoolArgs', 'NetworkIpPoolArgsDict']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 routes: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkRouteArgs', 'NetworkRouteArgsDict']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkArgs.__new__(NetworkArgs)

            if ip_pools is None and not opts.urn:
                raise TypeError("Missing required property 'ip_pools'")
            __props__.__dict__["ip_pools"] = ip_pools
            __props__.__dict__["name"] = name
            __props__.__dict__["routes"] = routes
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["associated_cluster_ids"] = None
            __props__.__dict__["aws_id"] = None
            __props__.__dict__["state"] = None
        super(Network, __self__).__init__(
            'aws-native:medialive:Network',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Network':
        """
        Get an existing Network resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NetworkArgs.__new__(NetworkArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["associated_cluster_ids"] = None
        __props__.__dict__["aws_id"] = None
        __props__.__dict__["ip_pools"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["routes"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["tags"] = None
        return Network(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Network.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="associatedClusterIds")
    def associated_cluster_ids(self) -> pulumi.Output[Sequence[str]]:
        return pulumi.get(self, "associated_cluster_ids")

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The unique ID of the Network.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter(name="ipPools")
    def ip_pools(self) -> pulumi.Output[Sequence['outputs.NetworkIpPool']]:
        """
        The list of IP address cidr pools for the network
        """
        return pulumi.get(self, "ip_pools")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The user-specified name of the Network to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def routes(self) -> pulumi.Output[Optional[Sequence['outputs.NetworkRoute']]]:
        """
        The routes for the network
        """
        return pulumi.get(self, "routes")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output['NetworkState']:
        """
        The current state of the Network.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        A collection of key-value pairs.
        """
        return pulumi.get(self, "tags")

