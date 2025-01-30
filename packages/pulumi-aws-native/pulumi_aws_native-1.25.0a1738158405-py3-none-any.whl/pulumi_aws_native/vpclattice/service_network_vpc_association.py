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
from ._enums import *

__all__ = ['ServiceNetworkVpcAssociationArgs', 'ServiceNetworkVpcAssociation']

@pulumi.input_type
class ServiceNetworkVpcAssociationArgs:
    def __init__(__self__, *,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 service_network_identifier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 vpc_identifier: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ServiceNetworkVpcAssociation resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_ids: The IDs of the security groups. Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see [Control traffic to resources using security groups](https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html) in the *Amazon VPC User Guide* .
        :param pulumi.Input[str] service_network_identifier: The ID or ARN of the service network. You must use an ARN if the resources are in different accounts.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags for the association.
        :param pulumi.Input[str] vpc_identifier: The ID of the VPC.
        """
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if service_network_identifier is not None:
            pulumi.set(__self__, "service_network_identifier", service_network_identifier)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vpc_identifier is not None:
            pulumi.set(__self__, "vpc_identifier", vpc_identifier)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The IDs of the security groups. Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see [Control traffic to resources using security groups](https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html) in the *Amazon VPC User Guide* .
        """
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="serviceNetworkIdentifier")
    def service_network_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The ID or ARN of the service network. You must use an ARN if the resources are in different accounts.
        """
        return pulumi.get(self, "service_network_identifier")

    @service_network_identifier.setter
    def service_network_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_network_identifier", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags for the association.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vpcIdentifier")
    def vpc_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC.
        """
        return pulumi.get(self, "vpc_identifier")

    @vpc_identifier.setter
    def vpc_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_identifier", value)


class ServiceNetworkVpcAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 service_network_identifier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 vpc_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Associates a VPC with a service network.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_ids: The IDs of the security groups. Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see [Control traffic to resources using security groups](https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html) in the *Amazon VPC User Guide* .
        :param pulumi.Input[str] service_network_identifier: The ID or ARN of the service network. You must use an ARN if the resources are in different accounts.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags for the association.
        :param pulumi.Input[str] vpc_identifier: The ID of the VPC.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ServiceNetworkVpcAssociationArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Associates a VPC with a service network.

        :param str resource_name: The name of the resource.
        :param ServiceNetworkVpcAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceNetworkVpcAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 service_network_identifier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 vpc_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceNetworkVpcAssociationArgs.__new__(ServiceNetworkVpcAssociationArgs)

            __props__.__dict__["security_group_ids"] = security_group_ids
            __props__.__dict__["service_network_identifier"] = service_network_identifier
            __props__.__dict__["tags"] = tags
            __props__.__dict__["vpc_identifier"] = vpc_identifier
            __props__.__dict__["arn"] = None
            __props__.__dict__["aws_id"] = None
            __props__.__dict__["created_at"] = None
            __props__.__dict__["service_network_arn"] = None
            __props__.__dict__["service_network_id"] = None
            __props__.__dict__["service_network_name"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["vpc_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["serviceNetworkIdentifier", "vpcIdentifier"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ServiceNetworkVpcAssociation, __self__).__init__(
            'aws-native:vpclattice:ServiceNetworkVpcAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ServiceNetworkVpcAssociation':
        """
        Get an existing ServiceNetworkVpcAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ServiceNetworkVpcAssociationArgs.__new__(ServiceNetworkVpcAssociationArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["aws_id"] = None
        __props__.__dict__["created_at"] = None
        __props__.__dict__["security_group_ids"] = None
        __props__.__dict__["service_network_arn"] = None
        __props__.__dict__["service_network_id"] = None
        __props__.__dict__["service_network_identifier"] = None
        __props__.__dict__["service_network_name"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["vpc_id"] = None
        __props__.__dict__["vpc_identifier"] = None
        return ServiceNetworkVpcAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the association between the service network and the VPC.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The ID of the specified association between the service network and the VPC.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The date and time that the association was created, specified in ISO-8601 format.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The IDs of the security groups. Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see [Control traffic to resources using security groups](https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html) in the *Amazon VPC User Guide* .
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="serviceNetworkArn")
    def service_network_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the service network.
        """
        return pulumi.get(self, "service_network_arn")

    @property
    @pulumi.getter(name="serviceNetworkId")
    def service_network_id(self) -> pulumi.Output[str]:
        """
        The ID of the service network.
        """
        return pulumi.get(self, "service_network_id")

    @property
    @pulumi.getter(name="serviceNetworkIdentifier")
    def service_network_identifier(self) -> pulumi.Output[Optional[str]]:
        """
        The ID or ARN of the service network. You must use an ARN if the resources are in different accounts.
        """
        return pulumi.get(self, "service_network_identifier")

    @property
    @pulumi.getter(name="serviceNetworkName")
    def service_network_name(self) -> pulumi.Output[str]:
        """
        The name of the service network.
        """
        return pulumi.get(self, "service_network_name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['ServiceNetworkVpcAssociationStatus']:
        """
        The status of the association.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags for the association.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The ID of the VPC.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcIdentifier")
    def vpc_identifier(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the VPC.
        """
        return pulumi.get(self, "vpc_identifier")

