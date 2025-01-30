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
from ._inputs import *

__all__ = ['ConfigurationArgs', 'Configuration']

@pulumi.input_type
class ConfigurationArgs:
    def __init__(__self__, *,
                 server_properties: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_versions_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 latest_revision: Optional[pulumi.Input['ConfigurationLatestRevisionArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Configuration resource.
        """
        pulumi.set(__self__, "server_properties", server_properties)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if kafka_versions_list is not None:
            pulumi.set(__self__, "kafka_versions_list", kafka_versions_list)
        if latest_revision is not None:
            pulumi.set(__self__, "latest_revision", latest_revision)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="serverProperties")
    def server_properties(self) -> pulumi.Input[str]:
        return pulumi.get(self, "server_properties")

    @server_properties.setter
    def server_properties(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_properties", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="kafkaVersionsList")
    def kafka_versions_list(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "kafka_versions_list")

    @kafka_versions_list.setter
    def kafka_versions_list(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "kafka_versions_list", value)

    @property
    @pulumi.getter(name="latestRevision")
    def latest_revision(self) -> Optional[pulumi.Input['ConfigurationLatestRevisionArgs']]:
        return pulumi.get(self, "latest_revision")

    @latest_revision.setter
    def latest_revision(self, value: Optional[pulumi.Input['ConfigurationLatestRevisionArgs']]):
        pulumi.set(self, "latest_revision", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class Configuration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_versions_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 latest_revision: Optional[pulumi.Input[Union['ConfigurationLatestRevisionArgs', 'ConfigurationLatestRevisionArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_properties: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::MSK::Configuration

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::MSK::Configuration

        :param str resource_name: The name of the resource.
        :param ConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_versions_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 latest_revision: Optional[pulumi.Input[Union['ConfigurationLatestRevisionArgs', 'ConfigurationLatestRevisionArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_properties: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConfigurationArgs.__new__(ConfigurationArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["kafka_versions_list"] = kafka_versions_list
            __props__.__dict__["latest_revision"] = latest_revision
            __props__.__dict__["name"] = name
            if server_properties is None and not opts.urn:
                raise TypeError("Missing required property 'server_properties'")
            __props__.__dict__["server_properties"] = server_properties
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["kafkaVersionsList[*]", "name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Configuration, __self__).__init__(
            'aws-native:msk:Configuration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Configuration':
        """
        Get an existing Configuration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConfigurationArgs.__new__(ConfigurationArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["kafka_versions_list"] = None
        __props__.__dict__["latest_revision"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["server_properties"] = None
        return Configuration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="kafkaVersionsList")
    def kafka_versions_list(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "kafka_versions_list")

    @property
    @pulumi.getter(name="latestRevision")
    def latest_revision(self) -> pulumi.Output[Optional['outputs.ConfigurationLatestRevision']]:
        return pulumi.get(self, "latest_revision")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serverProperties")
    def server_properties(self) -> pulumi.Output[str]:
        return pulumi.get(self, "server_properties")

