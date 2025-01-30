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

__all__ = ['MailManagerArchiveArgs', 'MailManagerArchive']

@pulumi.input_type
class MailManagerArchiveArgs:
    def __init__(__self__, *,
                 archive_name: Optional[pulumi.Input[str]] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 retention: Optional[pulumi.Input['MailManagerArchiveArchiveRetentionPropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a MailManagerArchive resource.
        :param pulumi.Input[str] archive_name: A unique name for the new archive.
        :param pulumi.Input[str] kms_key_arn: The Amazon Resource Name (ARN) of the KMS key for encrypting emails in the archive.
        :param pulumi.Input['MailManagerArchiveArchiveRetentionPropertiesArgs'] retention: The period for retaining emails in the archive before automatic deletion.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        if archive_name is not None:
            pulumi.set(__self__, "archive_name", archive_name)
        if kms_key_arn is not None:
            pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if retention is not None:
            pulumi.set(__self__, "retention", retention)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="archiveName")
    def archive_name(self) -> Optional[pulumi.Input[str]]:
        """
        A unique name for the new archive.
        """
        return pulumi.get(self, "archive_name")

    @archive_name.setter
    def archive_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "archive_name", value)

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the KMS key for encrypting emails in the archive.
        """
        return pulumi.get(self, "kms_key_arn")

    @kms_key_arn.setter
    def kms_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_arn", value)

    @property
    @pulumi.getter
    def retention(self) -> Optional[pulumi.Input['MailManagerArchiveArchiveRetentionPropertiesArgs']]:
        """
        The period for retaining emails in the archive before automatic deletion.
        """
        return pulumi.get(self, "retention")

    @retention.setter
    def retention(self, value: Optional[pulumi.Input['MailManagerArchiveArchiveRetentionPropertiesArgs']]):
        pulumi.set(self, "retention", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class MailManagerArchive(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 archive_name: Optional[pulumi.Input[str]] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 retention: Optional[pulumi.Input[Union['MailManagerArchiveArchiveRetentionPropertiesArgs', 'MailManagerArchiveArchiveRetentionPropertiesArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Definition of AWS::SES::MailManagerArchive Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] archive_name: A unique name for the new archive.
        :param pulumi.Input[str] kms_key_arn: The Amazon Resource Name (ARN) of the KMS key for encrypting emails in the archive.
        :param pulumi.Input[Union['MailManagerArchiveArchiveRetentionPropertiesArgs', 'MailManagerArchiveArchiveRetentionPropertiesArgsDict']] retention: The period for retaining emails in the archive before automatic deletion.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[MailManagerArchiveArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::SES::MailManagerArchive Resource Type

        :param str resource_name: The name of the resource.
        :param MailManagerArchiveArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MailManagerArchiveArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 archive_name: Optional[pulumi.Input[str]] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 retention: Optional[pulumi.Input[Union['MailManagerArchiveArchiveRetentionPropertiesArgs', 'MailManagerArchiveArchiveRetentionPropertiesArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MailManagerArchiveArgs.__new__(MailManagerArchiveArgs)

            __props__.__dict__["archive_name"] = archive_name
            __props__.__dict__["kms_key_arn"] = kms_key_arn
            __props__.__dict__["retention"] = retention
            __props__.__dict__["tags"] = tags
            __props__.__dict__["archive_arn"] = None
            __props__.__dict__["archive_id"] = None
            __props__.__dict__["archive_state"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["kmsKeyArn"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(MailManagerArchive, __self__).__init__(
            'aws-native:ses:MailManagerArchive',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MailManagerArchive':
        """
        Get an existing MailManagerArchive resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MailManagerArchiveArgs.__new__(MailManagerArchiveArgs)

        __props__.__dict__["archive_arn"] = None
        __props__.__dict__["archive_id"] = None
        __props__.__dict__["archive_name"] = None
        __props__.__dict__["archive_state"] = None
        __props__.__dict__["kms_key_arn"] = None
        __props__.__dict__["retention"] = None
        __props__.__dict__["tags"] = None
        return MailManagerArchive(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="archiveArn")
    def archive_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the archive.
        """
        return pulumi.get(self, "archive_arn")

    @property
    @pulumi.getter(name="archiveId")
    def archive_id(self) -> pulumi.Output[str]:
        """
        The unique identifier of the archive.
        """
        return pulumi.get(self, "archive_id")

    @property
    @pulumi.getter(name="archiveName")
    def archive_name(self) -> pulumi.Output[Optional[str]]:
        """
        A unique name for the new archive.
        """
        return pulumi.get(self, "archive_name")

    @property
    @pulumi.getter(name="archiveState")
    def archive_state(self) -> pulumi.Output['MailManagerArchiveArchiveState']:
        """
        The current state of the archive:

        - `ACTIVE` – The archive is ready and available for use.
        - `PENDING_DELETION` – The archive has been marked for deletion and will be permanently deleted in 30 days. No further modifications can be made in this state.
        """
        return pulumi.get(self, "archive_state")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the KMS key for encrypting emails in the archive.
        """
        return pulumi.get(self, "kms_key_arn")

    @property
    @pulumi.getter
    def retention(self) -> pulumi.Output[Optional['outputs.MailManagerArchiveArchiveRetentionProperties']]:
        """
        The period for retaining emails in the archive before automatic deletion.
        """
        return pulumi.get(self, "retention")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        return pulumi.get(self, "tags")

