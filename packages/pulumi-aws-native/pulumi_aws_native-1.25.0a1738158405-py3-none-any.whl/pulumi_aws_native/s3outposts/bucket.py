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

__all__ = ['BucketArgs', 'Bucket']

@pulumi.input_type
class BucketArgs:
    def __init__(__self__, *,
                 outpost_id: pulumi.Input[str],
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 lifecycle_configuration: Optional[pulumi.Input['BucketLifecycleConfigurationArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Bucket resource.
        :param pulumi.Input[str] outpost_id: The id of the customer outpost on which the bucket resides.
        :param pulumi.Input[str] bucket_name: A name for the bucket.
        :param pulumi.Input['BucketLifecycleConfigurationArgs'] lifecycle_configuration: Rules that define how Amazon S3Outposts manages objects during their lifetime.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: An arbitrary set of tags (key-value pairs) for this S3Outposts bucket.
        """
        pulumi.set(__self__, "outpost_id", outpost_id)
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if lifecycle_configuration is not None:
            pulumi.set(__self__, "lifecycle_configuration", lifecycle_configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="outpostId")
    def outpost_id(self) -> pulumi.Input[str]:
        """
        The id of the customer outpost on which the bucket resides.
        """
        return pulumi.get(self, "outpost_id")

    @outpost_id.setter
    def outpost_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "outpost_id", value)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the bucket.
        """
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter(name="lifecycleConfiguration")
    def lifecycle_configuration(self) -> Optional[pulumi.Input['BucketLifecycleConfigurationArgs']]:
        """
        Rules that define how Amazon S3Outposts manages objects during their lifetime.
        """
        return pulumi.get(self, "lifecycle_configuration")

    @lifecycle_configuration.setter
    def lifecycle_configuration(self, value: Optional[pulumi.Input['BucketLifecycleConfigurationArgs']]):
        pulumi.set(self, "lifecycle_configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        An arbitrary set of tags (key-value pairs) for this S3Outposts bucket.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Bucket(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 lifecycle_configuration: Optional[pulumi.Input[Union['BucketLifecycleConfigurationArgs', 'BucketLifecycleConfigurationArgsDict']]] = None,
                 outpost_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource Type Definition for AWS::S3Outposts::Bucket

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket_name: A name for the bucket.
        :param pulumi.Input[Union['BucketLifecycleConfigurationArgs', 'BucketLifecycleConfigurationArgsDict']] lifecycle_configuration: Rules that define how Amazon S3Outposts manages objects during their lifetime.
        :param pulumi.Input[str] outpost_id: The id of the customer outpost on which the bucket resides.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: An arbitrary set of tags (key-value pairs) for this S3Outposts bucket.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type Definition for AWS::S3Outposts::Bucket

        :param str resource_name: The name of the resource.
        :param BucketArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 lifecycle_configuration: Optional[pulumi.Input[Union['BucketLifecycleConfigurationArgs', 'BucketLifecycleConfigurationArgsDict']]] = None,
                 outpost_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketArgs.__new__(BucketArgs)

            __props__.__dict__["bucket_name"] = bucket_name
            __props__.__dict__["lifecycle_configuration"] = lifecycle_configuration
            if outpost_id is None and not opts.urn:
                raise TypeError("Missing required property 'outpost_id'")
            __props__.__dict__["outpost_id"] = outpost_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["bucketName", "outpostId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Bucket, __self__).__init__(
            'aws-native:s3outposts:Bucket',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Bucket':
        """
        Get an existing Bucket resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BucketArgs.__new__(BucketArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["bucket_name"] = None
        __props__.__dict__["lifecycle_configuration"] = None
        __props__.__dict__["outpost_id"] = None
        __props__.__dict__["tags"] = None
        return Bucket(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the specified bucket.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Output[str]:
        """
        A name for the bucket.
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter(name="lifecycleConfiguration")
    def lifecycle_configuration(self) -> pulumi.Output[Optional['outputs.BucketLifecycleConfiguration']]:
        """
        Rules that define how Amazon S3Outposts manages objects during their lifetime.
        """
        return pulumi.get(self, "lifecycle_configuration")

    @property
    @pulumi.getter(name="outpostId")
    def outpost_id(self) -> pulumi.Output[str]:
        """
        The id of the customer outpost on which the bucket resides.
        """
        return pulumi.get(self, "outpost_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        An arbitrary set of tags (key-value pairs) for this S3Outposts bucket.
        """
        return pulumi.get(self, "tags")

