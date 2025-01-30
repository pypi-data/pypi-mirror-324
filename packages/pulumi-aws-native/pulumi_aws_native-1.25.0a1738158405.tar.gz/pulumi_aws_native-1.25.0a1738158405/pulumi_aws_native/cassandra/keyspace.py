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

__all__ = ['KeyspaceArgs', 'Keyspace']

@pulumi.input_type
class KeyspaceArgs:
    def __init__(__self__, *,
                 client_side_timestamps_enabled: Optional[pulumi.Input[bool]] = None,
                 keyspace_name: Optional[pulumi.Input[str]] = None,
                 replication_specification: Optional[pulumi.Input['KeyspaceReplicationSpecificationArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Keyspace resource.
        :param pulumi.Input[bool] client_side_timestamps_enabled: Indicates whether client-side timestamps are enabled (true) or disabled (false) for all tables in the keyspace. To add a Region to a single-Region keyspace with at least one table, the value must be set to true. After you enabled client-side timestamps for a table, you can’t disable it again.
        :param pulumi.Input[str] keyspace_name: Name for Cassandra keyspace
        :param pulumi.Input['KeyspaceReplicationSpecificationArgs'] replication_specification: Specifies the `ReplicationStrategy` of a keyspace. The options are:
               
               - `SINGLE_REGION` for a single Region keyspace (optional) or
               - `MULTI_REGION` for a multi-Region keyspace
               
               If no `ReplicationStrategy` is provided, the default is `SINGLE_REGION` . If you choose `MULTI_REGION` , you must also provide a `RegionList` with the AWS Regions that the keyspace is replicated in.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: An array of key-value pairs to apply to this resource.
               
               For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        if client_side_timestamps_enabled is not None:
            pulumi.set(__self__, "client_side_timestamps_enabled", client_side_timestamps_enabled)
        if keyspace_name is not None:
            pulumi.set(__self__, "keyspace_name", keyspace_name)
        if replication_specification is not None:
            pulumi.set(__self__, "replication_specification", replication_specification)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="clientSideTimestampsEnabled")
    def client_side_timestamps_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether client-side timestamps are enabled (true) or disabled (false) for all tables in the keyspace. To add a Region to a single-Region keyspace with at least one table, the value must be set to true. After you enabled client-side timestamps for a table, you can’t disable it again.
        """
        return pulumi.get(self, "client_side_timestamps_enabled")

    @client_side_timestamps_enabled.setter
    def client_side_timestamps_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "client_side_timestamps_enabled", value)

    @property
    @pulumi.getter(name="keyspaceName")
    def keyspace_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name for Cassandra keyspace
        """
        return pulumi.get(self, "keyspace_name")

    @keyspace_name.setter
    def keyspace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "keyspace_name", value)

    @property
    @pulumi.getter(name="replicationSpecification")
    def replication_specification(self) -> Optional[pulumi.Input['KeyspaceReplicationSpecificationArgs']]:
        """
        Specifies the `ReplicationStrategy` of a keyspace. The options are:

        - `SINGLE_REGION` for a single Region keyspace (optional) or
        - `MULTI_REGION` for a multi-Region keyspace

        If no `ReplicationStrategy` is provided, the default is `SINGLE_REGION` . If you choose `MULTI_REGION` , you must also provide a `RegionList` with the AWS Regions that the keyspace is replicated in.
        """
        return pulumi.get(self, "replication_specification")

    @replication_specification.setter
    def replication_specification(self, value: Optional[pulumi.Input['KeyspaceReplicationSpecificationArgs']]):
        pulumi.set(self, "replication_specification", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.

        For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Keyspace(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_side_timestamps_enabled: Optional[pulumi.Input[bool]] = None,
                 keyspace_name: Optional[pulumi.Input[str]] = None,
                 replication_specification: Optional[pulumi.Input[Union['KeyspaceReplicationSpecificationArgs', 'KeyspaceReplicationSpecificationArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource schema for AWS::Cassandra::Keyspace

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        my_new_keyspace = aws_native.cassandra.Keyspace("myNewKeyspace",
            keyspace_name="MyNewKeyspace",
            tags=[
                {
                    "key": "tag1",
                    "value": "val1",
                },
                {
                    "key": "tag2",
                    "value": "val2",
                },
            ])

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        multi_region_keyspace = aws_native.cassandra.Keyspace("multiRegionKeyspace",
            keyspace_name="MultiRegionKeyspace",
            replication_specification={
                "replication_strategy": aws_native.cassandra.KeyspaceReplicationSpecificationReplicationStrategy.MULTI_REGION,
                "region_list": [
                    aws_native.cassandra.KeyspaceRegionListItem.US_EAST1,
                    aws_native.cassandra.KeyspaceRegionListItem.US_WEST2,
                    aws_native.cassandra.KeyspaceRegionListItem.EU_WEST1,
                ],
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        multi_region_keyspace = aws_native.cassandra.Keyspace("multiRegionKeyspace",
            keyspace_name="MultiRegionKeyspace",
            replication_specification={
                "replication_strategy": aws_native.cassandra.KeyspaceReplicationSpecificationReplicationStrategy.MULTI_REGION,
                "region_list": [
                    aws_native.cassandra.KeyspaceRegionListItem.US_EAST1,
                    aws_native.cassandra.KeyspaceRegionListItem.US_WEST2,
                    aws_native.cassandra.KeyspaceRegionListItem.EU_WEST1,
                ],
            })

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] client_side_timestamps_enabled: Indicates whether client-side timestamps are enabled (true) or disabled (false) for all tables in the keyspace. To add a Region to a single-Region keyspace with at least one table, the value must be set to true. After you enabled client-side timestamps for a table, you can’t disable it again.
        :param pulumi.Input[str] keyspace_name: Name for Cassandra keyspace
        :param pulumi.Input[Union['KeyspaceReplicationSpecificationArgs', 'KeyspaceReplicationSpecificationArgsDict']] replication_specification: Specifies the `ReplicationStrategy` of a keyspace. The options are:
               
               - `SINGLE_REGION` for a single Region keyspace (optional) or
               - `MULTI_REGION` for a multi-Region keyspace
               
               If no `ReplicationStrategy` is provided, the default is `SINGLE_REGION` . If you choose `MULTI_REGION` , you must also provide a `RegionList` with the AWS Regions that the keyspace is replicated in.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: An array of key-value pairs to apply to this resource.
               
               For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[KeyspaceArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::Cassandra::Keyspace

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        my_new_keyspace = aws_native.cassandra.Keyspace("myNewKeyspace",
            keyspace_name="MyNewKeyspace",
            tags=[
                {
                    "key": "tag1",
                    "value": "val1",
                },
                {
                    "key": "tag2",
                    "value": "val2",
                },
            ])

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        multi_region_keyspace = aws_native.cassandra.Keyspace("multiRegionKeyspace",
            keyspace_name="MultiRegionKeyspace",
            replication_specification={
                "replication_strategy": aws_native.cassandra.KeyspaceReplicationSpecificationReplicationStrategy.MULTI_REGION,
                "region_list": [
                    aws_native.cassandra.KeyspaceRegionListItem.US_EAST1,
                    aws_native.cassandra.KeyspaceRegionListItem.US_WEST2,
                    aws_native.cassandra.KeyspaceRegionListItem.EU_WEST1,
                ],
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        multi_region_keyspace = aws_native.cassandra.Keyspace("multiRegionKeyspace",
            keyspace_name="MultiRegionKeyspace",
            replication_specification={
                "replication_strategy": aws_native.cassandra.KeyspaceReplicationSpecificationReplicationStrategy.MULTI_REGION,
                "region_list": [
                    aws_native.cassandra.KeyspaceRegionListItem.US_EAST1,
                    aws_native.cassandra.KeyspaceRegionListItem.US_WEST2,
                    aws_native.cassandra.KeyspaceRegionListItem.EU_WEST1,
                ],
            })

        ```

        :param str resource_name: The name of the resource.
        :param KeyspaceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KeyspaceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_side_timestamps_enabled: Optional[pulumi.Input[bool]] = None,
                 keyspace_name: Optional[pulumi.Input[str]] = None,
                 replication_specification: Optional[pulumi.Input[Union['KeyspaceReplicationSpecificationArgs', 'KeyspaceReplicationSpecificationArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KeyspaceArgs.__new__(KeyspaceArgs)

            __props__.__dict__["client_side_timestamps_enabled"] = client_side_timestamps_enabled
            __props__.__dict__["keyspace_name"] = keyspace_name
            __props__.__dict__["replication_specification"] = replication_specification
            __props__.__dict__["tags"] = tags
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["keyspaceName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Keyspace, __self__).__init__(
            'aws-native:cassandra:Keyspace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Keyspace':
        """
        Get an existing Keyspace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = KeyspaceArgs.__new__(KeyspaceArgs)

        __props__.__dict__["client_side_timestamps_enabled"] = None
        __props__.__dict__["keyspace_name"] = None
        __props__.__dict__["replication_specification"] = None
        __props__.__dict__["tags"] = None
        return Keyspace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clientSideTimestampsEnabled")
    def client_side_timestamps_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether client-side timestamps are enabled (true) or disabled (false) for all tables in the keyspace. To add a Region to a single-Region keyspace with at least one table, the value must be set to true. After you enabled client-side timestamps for a table, you can’t disable it again.
        """
        return pulumi.get(self, "client_side_timestamps_enabled")

    @property
    @pulumi.getter(name="keyspaceName")
    def keyspace_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name for Cassandra keyspace
        """
        return pulumi.get(self, "keyspace_name")

    @property
    @pulumi.getter(name="replicationSpecification")
    def replication_specification(self) -> pulumi.Output[Optional['outputs.KeyspaceReplicationSpecification']]:
        """
        Specifies the `ReplicationStrategy` of a keyspace. The options are:

        - `SINGLE_REGION` for a single Region keyspace (optional) or
        - `MULTI_REGION` for a multi-Region keyspace

        If no `ReplicationStrategy` is provided, the default is `SINGLE_REGION` . If you choose `MULTI_REGION` , you must also provide a `RegionList` with the AWS Regions that the keyspace is replicated in.
        """
        return pulumi.get(self, "replication_specification")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        An array of key-value pairs to apply to this resource.

        For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        return pulumi.get(self, "tags")

