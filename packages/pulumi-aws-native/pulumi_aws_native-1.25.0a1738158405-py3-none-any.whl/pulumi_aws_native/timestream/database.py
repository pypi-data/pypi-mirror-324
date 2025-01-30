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

__all__ = ['DatabaseArgs', 'Database']

@pulumi.input_type
class DatabaseArgs:
    def __init__(__self__, *,
                 database_name: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Database resource.
        :param pulumi.Input[str] database_name: The name for the database. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the database name.
        :param pulumi.Input[str] kms_key_id: The KMS key for the database. If the KMS key is not specified, the database will be encrypted with a Timestream managed KMS key located in your account.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        if database_name is not None:
            pulumi.set(__self__, "database_name", database_name)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the database. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the database name.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The KMS key for the database. If the KMS key is not specified, the database will be encrypted with a Timestream managed KMS key located in your account.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Database(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        The AWS::Timestream::Database resource creates a Timestream database.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_name: The name for the database. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the database name.
        :param pulumi.Input[str] kms_key_id: The KMS key for the database. If the KMS key is not specified, the database will be encrypted with a Timestream managed KMS key located in your account.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[DatabaseArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::Timestream::Database resource creates a Timestream database.

        :param str resource_name: The name of the resource.
        :param DatabaseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatabaseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DatabaseArgs.__new__(DatabaseArgs)

            __props__.__dict__["database_name"] = database_name
            __props__.__dict__["kms_key_id"] = kms_key_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["databaseName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Database, __self__).__init__(
            'aws-native:timestream:Database',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Database':
        """
        Get an existing Database resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DatabaseArgs.__new__(DatabaseArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["database_name"] = None
        __props__.__dict__["kms_key_id"] = None
        __props__.__dict__["tags"] = None
        return Database(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The `arn` of the database.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name for the database. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the database name.
        """
        return pulumi.get(self, "database_name")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[Optional[str]]:
        """
        The KMS key for the database. If the KMS key is not specified, the database will be encrypted with a Timestream managed KMS key located in your account.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

