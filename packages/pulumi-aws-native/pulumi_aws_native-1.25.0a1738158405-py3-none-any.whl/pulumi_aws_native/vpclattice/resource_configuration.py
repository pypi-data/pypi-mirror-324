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

__all__ = ['ResourceConfigurationArgs', 'ResourceConfiguration']

@pulumi.input_type
class ResourceConfigurationArgs:
    def __init__(__self__, *,
                 allow_association_to_sharable_service_network: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 protocol_type: Optional[pulumi.Input['ResourceConfigurationProtocolType']] = None,
                 resource_configuration_auth_type: Optional[pulumi.Input['ResourceConfigurationAuthType']] = None,
                 resource_configuration_definition: Optional[pulumi.Input[Union['ResourceConfigurationDefinition0PropertiesArgs', 'ResourceConfigurationDefinition1PropertiesArgs', 'ResourceConfigurationDefinition2PropertiesArgs']]] = None,
                 resource_configuration_group_id: Optional[pulumi.Input[str]] = None,
                 resource_configuration_type: Optional[pulumi.Input['ResourceConfigurationType']] = None,
                 resource_gateway_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a ResourceConfiguration resource.
        :param pulumi.Input[bool] allow_association_to_sharable_service_network: Specifies whether the resource configuration can be associated with a sharable service network.
        :param pulumi.Input[str] name: The name of the resource configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] port_ranges: (SINGLE, GROUP, CHILD) The TCP port ranges that a consumer can use to access a resource configuration (for example: 1-65535). You can separate port ranges using commas (for example: 1,2,22-30).
        :param pulumi.Input['ResourceConfigurationProtocolType'] protocol_type: (SINGLE, GROUP) The protocol accepted by the resource configuration.
        :param pulumi.Input['ResourceConfigurationAuthType'] resource_configuration_auth_type: The auth type for the resource configuration.
        :param pulumi.Input[Union['ResourceConfigurationDefinition0PropertiesArgs', 'ResourceConfigurationDefinition1PropertiesArgs', 'ResourceConfigurationDefinition2PropertiesArgs']] resource_configuration_definition: Identifies the resource configuration in one of the following ways:
               
               - *Amazon Resource Name (ARN)* - Supported resource-types that are provisioned by AWS services, such as RDS databases, can be identified by their ARN.
               - *Domain name* - Any domain name that is publicly resolvable.
               - *IP address* - For IPv4 and IPv6, only IP addresses in the VPC are supported.
        :param pulumi.Input[str] resource_configuration_group_id: The ID of the group resource configuration.
        :param pulumi.Input['ResourceConfigurationType'] resource_configuration_type: The type of resource configuration. A resource configuration can be one of the following types:
               
               - *SINGLE* - A single resource.
               - *GROUP* - A group of resources. You must create a group resource configuration before you create a child resource configuration.
               - *CHILD* - A single resource that is part of a group resource configuration.
               - *ARN* - An AWS resource.
        :param pulumi.Input[str] resource_gateway_id: The ID of the resource gateway.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags for the resource configuration.
        """
        if allow_association_to_sharable_service_network is not None:
            pulumi.set(__self__, "allow_association_to_sharable_service_network", allow_association_to_sharable_service_network)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if port_ranges is not None:
            pulumi.set(__self__, "port_ranges", port_ranges)
        if protocol_type is not None:
            pulumi.set(__self__, "protocol_type", protocol_type)
        if resource_configuration_auth_type is not None:
            pulumi.set(__self__, "resource_configuration_auth_type", resource_configuration_auth_type)
        if resource_configuration_definition is not None:
            pulumi.set(__self__, "resource_configuration_definition", resource_configuration_definition)
        if resource_configuration_group_id is not None:
            pulumi.set(__self__, "resource_configuration_group_id", resource_configuration_group_id)
        if resource_configuration_type is not None:
            pulumi.set(__self__, "resource_configuration_type", resource_configuration_type)
        if resource_gateway_id is not None:
            pulumi.set(__self__, "resource_gateway_id", resource_gateway_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="allowAssociationToSharableServiceNetwork")
    def allow_association_to_sharable_service_network(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the resource configuration can be associated with a sharable service network.
        """
        return pulumi.get(self, "allow_association_to_sharable_service_network")

    @allow_association_to_sharable_service_network.setter
    def allow_association_to_sharable_service_network(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_association_to_sharable_service_network", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="portRanges")
    def port_ranges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        (SINGLE, GROUP, CHILD) The TCP port ranges that a consumer can use to access a resource configuration (for example: 1-65535). You can separate port ranges using commas (for example: 1,2,22-30).
        """
        return pulumi.get(self, "port_ranges")

    @port_ranges.setter
    def port_ranges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "port_ranges", value)

    @property
    @pulumi.getter(name="protocolType")
    def protocol_type(self) -> Optional[pulumi.Input['ResourceConfigurationProtocolType']]:
        """
        (SINGLE, GROUP) The protocol accepted by the resource configuration.
        """
        return pulumi.get(self, "protocol_type")

    @protocol_type.setter
    def protocol_type(self, value: Optional[pulumi.Input['ResourceConfigurationProtocolType']]):
        pulumi.set(self, "protocol_type", value)

    @property
    @pulumi.getter(name="resourceConfigurationAuthType")
    def resource_configuration_auth_type(self) -> Optional[pulumi.Input['ResourceConfigurationAuthType']]:
        """
        The auth type for the resource configuration.
        """
        return pulumi.get(self, "resource_configuration_auth_type")

    @resource_configuration_auth_type.setter
    def resource_configuration_auth_type(self, value: Optional[pulumi.Input['ResourceConfigurationAuthType']]):
        pulumi.set(self, "resource_configuration_auth_type", value)

    @property
    @pulumi.getter(name="resourceConfigurationDefinition")
    def resource_configuration_definition(self) -> Optional[pulumi.Input[Union['ResourceConfigurationDefinition0PropertiesArgs', 'ResourceConfigurationDefinition1PropertiesArgs', 'ResourceConfigurationDefinition2PropertiesArgs']]]:
        """
        Identifies the resource configuration in one of the following ways:

        - *Amazon Resource Name (ARN)* - Supported resource-types that are provisioned by AWS services, such as RDS databases, can be identified by their ARN.
        - *Domain name* - Any domain name that is publicly resolvable.
        - *IP address* - For IPv4 and IPv6, only IP addresses in the VPC are supported.
        """
        return pulumi.get(self, "resource_configuration_definition")

    @resource_configuration_definition.setter
    def resource_configuration_definition(self, value: Optional[pulumi.Input[Union['ResourceConfigurationDefinition0PropertiesArgs', 'ResourceConfigurationDefinition1PropertiesArgs', 'ResourceConfigurationDefinition2PropertiesArgs']]]):
        pulumi.set(self, "resource_configuration_definition", value)

    @property
    @pulumi.getter(name="resourceConfigurationGroupId")
    def resource_configuration_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the group resource configuration.
        """
        return pulumi.get(self, "resource_configuration_group_id")

    @resource_configuration_group_id.setter
    def resource_configuration_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_configuration_group_id", value)

    @property
    @pulumi.getter(name="resourceConfigurationType")
    def resource_configuration_type(self) -> Optional[pulumi.Input['ResourceConfigurationType']]:
        """
        The type of resource configuration. A resource configuration can be one of the following types:

        - *SINGLE* - A single resource.
        - *GROUP* - A group of resources. You must create a group resource configuration before you create a child resource configuration.
        - *CHILD* - A single resource that is part of a group resource configuration.
        - *ARN* - An AWS resource.
        """
        return pulumi.get(self, "resource_configuration_type")

    @resource_configuration_type.setter
    def resource_configuration_type(self, value: Optional[pulumi.Input['ResourceConfigurationType']]):
        pulumi.set(self, "resource_configuration_type", value)

    @property
    @pulumi.getter(name="resourceGatewayId")
    def resource_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource gateway.
        """
        return pulumi.get(self, "resource_gateway_id")

    @resource_gateway_id.setter
    def resource_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_gateway_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags for the resource configuration.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class ResourceConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_association_to_sharable_service_network: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 protocol_type: Optional[pulumi.Input['ResourceConfigurationProtocolType']] = None,
                 resource_configuration_auth_type: Optional[pulumi.Input['ResourceConfigurationAuthType']] = None,
                 resource_configuration_definition: Optional[pulumi.Input[Union[Union['ResourceConfigurationDefinition0PropertiesArgs', 'ResourceConfigurationDefinition0PropertiesArgsDict'], Union['ResourceConfigurationDefinition1PropertiesArgs', 'ResourceConfigurationDefinition1PropertiesArgsDict'], Union['ResourceConfigurationDefinition2PropertiesArgs', 'ResourceConfigurationDefinition2PropertiesArgsDict']]]] = None,
                 resource_configuration_group_id: Optional[pulumi.Input[str]] = None,
                 resource_configuration_type: Optional[pulumi.Input['ResourceConfigurationType']] = None,
                 resource_gateway_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        VpcLattice ResourceConfiguration CFN resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_association_to_sharable_service_network: Specifies whether the resource configuration can be associated with a sharable service network.
        :param pulumi.Input[str] name: The name of the resource configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] port_ranges: (SINGLE, GROUP, CHILD) The TCP port ranges that a consumer can use to access a resource configuration (for example: 1-65535). You can separate port ranges using commas (for example: 1,2,22-30).
        :param pulumi.Input['ResourceConfigurationProtocolType'] protocol_type: (SINGLE, GROUP) The protocol accepted by the resource configuration.
        :param pulumi.Input['ResourceConfigurationAuthType'] resource_configuration_auth_type: The auth type for the resource configuration.
        :param pulumi.Input[Union[Union['ResourceConfigurationDefinition0PropertiesArgs', 'ResourceConfigurationDefinition0PropertiesArgsDict'], Union['ResourceConfigurationDefinition1PropertiesArgs', 'ResourceConfigurationDefinition1PropertiesArgsDict'], Union['ResourceConfigurationDefinition2PropertiesArgs', 'ResourceConfigurationDefinition2PropertiesArgsDict']]] resource_configuration_definition: Identifies the resource configuration in one of the following ways:
               
               - *Amazon Resource Name (ARN)* - Supported resource-types that are provisioned by AWS services, such as RDS databases, can be identified by their ARN.
               - *Domain name* - Any domain name that is publicly resolvable.
               - *IP address* - For IPv4 and IPv6, only IP addresses in the VPC are supported.
        :param pulumi.Input[str] resource_configuration_group_id: The ID of the group resource configuration.
        :param pulumi.Input['ResourceConfigurationType'] resource_configuration_type: The type of resource configuration. A resource configuration can be one of the following types:
               
               - *SINGLE* - A single resource.
               - *GROUP* - A group of resources. You must create a group resource configuration before you create a child resource configuration.
               - *CHILD* - A single resource that is part of a group resource configuration.
               - *ARN* - An AWS resource.
        :param pulumi.Input[str] resource_gateway_id: The ID of the resource gateway.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags for the resource configuration.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ResourceConfigurationArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        VpcLattice ResourceConfiguration CFN resource

        :param str resource_name: The name of the resource.
        :param ResourceConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_association_to_sharable_service_network: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 protocol_type: Optional[pulumi.Input['ResourceConfigurationProtocolType']] = None,
                 resource_configuration_auth_type: Optional[pulumi.Input['ResourceConfigurationAuthType']] = None,
                 resource_configuration_definition: Optional[pulumi.Input[Union[Union['ResourceConfigurationDefinition0PropertiesArgs', 'ResourceConfigurationDefinition0PropertiesArgsDict'], Union['ResourceConfigurationDefinition1PropertiesArgs', 'ResourceConfigurationDefinition1PropertiesArgsDict'], Union['ResourceConfigurationDefinition2PropertiesArgs', 'ResourceConfigurationDefinition2PropertiesArgsDict']]]] = None,
                 resource_configuration_group_id: Optional[pulumi.Input[str]] = None,
                 resource_configuration_type: Optional[pulumi.Input['ResourceConfigurationType']] = None,
                 resource_gateway_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceConfigurationArgs.__new__(ResourceConfigurationArgs)

            __props__.__dict__["allow_association_to_sharable_service_network"] = allow_association_to_sharable_service_network
            __props__.__dict__["name"] = name
            __props__.__dict__["port_ranges"] = port_ranges
            __props__.__dict__["protocol_type"] = protocol_type
            __props__.__dict__["resource_configuration_auth_type"] = resource_configuration_auth_type
            __props__.__dict__["resource_configuration_definition"] = resource_configuration_definition
            __props__.__dict__["resource_configuration_group_id"] = resource_configuration_group_id
            __props__.__dict__["resource_configuration_type"] = resource_configuration_type
            __props__.__dict__["resource_gateway_id"] = resource_gateway_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["aws_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["protocolType", "resourceConfigurationAuthType", "resourceConfigurationType", "resourceGatewayId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ResourceConfiguration, __self__).__init__(
            'aws-native:vpclattice:ResourceConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ResourceConfiguration':
        """
        Get an existing ResourceConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ResourceConfigurationArgs.__new__(ResourceConfigurationArgs)

        __props__.__dict__["allow_association_to_sharable_service_network"] = None
        __props__.__dict__["arn"] = None
        __props__.__dict__["aws_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["port_ranges"] = None
        __props__.__dict__["protocol_type"] = None
        __props__.__dict__["resource_configuration_auth_type"] = None
        __props__.__dict__["resource_configuration_definition"] = None
        __props__.__dict__["resource_configuration_group_id"] = None
        __props__.__dict__["resource_configuration_type"] = None
        __props__.__dict__["resource_gateway_id"] = None
        __props__.__dict__["tags"] = None
        return ResourceConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowAssociationToSharableServiceNetwork")
    def allow_association_to_sharable_service_network(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the resource configuration can be associated with a sharable service network.
        """
        return pulumi.get(self, "allow_association_to_sharable_service_network")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the resource configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The ID of the resource configuration.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="portRanges")
    def port_ranges(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        (SINGLE, GROUP, CHILD) The TCP port ranges that a consumer can use to access a resource configuration (for example: 1-65535). You can separate port ranges using commas (for example: 1,2,22-30).
        """
        return pulumi.get(self, "port_ranges")

    @property
    @pulumi.getter(name="protocolType")
    def protocol_type(self) -> pulumi.Output[Optional['ResourceConfigurationProtocolType']]:
        """
        (SINGLE, GROUP) The protocol accepted by the resource configuration.
        """
        return pulumi.get(self, "protocol_type")

    @property
    @pulumi.getter(name="resourceConfigurationAuthType")
    def resource_configuration_auth_type(self) -> pulumi.Output[Optional['ResourceConfigurationAuthType']]:
        """
        The auth type for the resource configuration.
        """
        return pulumi.get(self, "resource_configuration_auth_type")

    @property
    @pulumi.getter(name="resourceConfigurationDefinition")
    def resource_configuration_definition(self) -> pulumi.Output[Optional[Any]]:
        """
        Identifies the resource configuration in one of the following ways:

        - *Amazon Resource Name (ARN)* - Supported resource-types that are provisioned by AWS services, such as RDS databases, can be identified by their ARN.
        - *Domain name* - Any domain name that is publicly resolvable.
        - *IP address* - For IPv4 and IPv6, only IP addresses in the VPC are supported.
        """
        return pulumi.get(self, "resource_configuration_definition")

    @property
    @pulumi.getter(name="resourceConfigurationGroupId")
    def resource_configuration_group_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the group resource configuration.
        """
        return pulumi.get(self, "resource_configuration_group_id")

    @property
    @pulumi.getter(name="resourceConfigurationType")
    def resource_configuration_type(self) -> pulumi.Output[Optional['ResourceConfigurationType']]:
        """
        The type of resource configuration. A resource configuration can be one of the following types:

        - *SINGLE* - A single resource.
        - *GROUP* - A group of resources. You must create a group resource configuration before you create a child resource configuration.
        - *CHILD* - A single resource that is part of a group resource configuration.
        - *ARN* - An AWS resource.
        """
        return pulumi.get(self, "resource_configuration_type")

    @property
    @pulumi.getter(name="resourceGatewayId")
    def resource_gateway_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the resource gateway.
        """
        return pulumi.get(self, "resource_gateway_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags for the resource configuration.
        """
        return pulumi.get(self, "tags")

