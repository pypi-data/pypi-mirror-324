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

__all__ = ['QueueArgs', 'Queue']

@pulumi.input_type
class QueueArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 farm_id: pulumi.Input[str],
                 allowed_storage_profile_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 default_budget_action: Optional[pulumi.Input['QueueDefaultQueueBudgetAction']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 job_attachment_settings: Optional[pulumi.Input['QueueJobAttachmentSettingsArgs']] = None,
                 job_run_as_user: Optional[pulumi.Input['QueueJobRunAsUserArgs']] = None,
                 required_file_system_location_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Queue resource.
        :param pulumi.Input[str] display_name: The display name of the queue summary to update.
               
               > This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        :param pulumi.Input[str] farm_id: The farm ID.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_storage_profile_ids: The identifiers of the storage profiles that this queue can use to share assets between workers using different operating systems.
        :param pulumi.Input['QueueDefaultQueueBudgetAction'] default_budget_action: The default action taken on a queue summary if a budget wasn't configured.
        :param pulumi.Input[str] description: A description of the queue that helps identify what the queue is used for.
        :param pulumi.Input['QueueJobAttachmentSettingsArgs'] job_attachment_settings: The job attachment settings. These are the Amazon S3 bucket name and the Amazon S3 prefix.
        :param pulumi.Input['QueueJobRunAsUserArgs'] job_run_as_user: Identifies the user for a job.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] required_file_system_location_names: The file system location that the queue uses.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role that workers use when running jobs in this queue.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "farm_id", farm_id)
        if allowed_storage_profile_ids is not None:
            pulumi.set(__self__, "allowed_storage_profile_ids", allowed_storage_profile_ids)
        if default_budget_action is not None:
            pulumi.set(__self__, "default_budget_action", default_budget_action)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if job_attachment_settings is not None:
            pulumi.set(__self__, "job_attachment_settings", job_attachment_settings)
        if job_run_as_user is not None:
            pulumi.set(__self__, "job_run_as_user", job_run_as_user)
        if required_file_system_location_names is not None:
            pulumi.set(__self__, "required_file_system_location_names", required_file_system_location_names)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The display name of the queue summary to update.

        > This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="farmId")
    def farm_id(self) -> pulumi.Input[str]:
        """
        The farm ID.
        """
        return pulumi.get(self, "farm_id")

    @farm_id.setter
    def farm_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "farm_id", value)

    @property
    @pulumi.getter(name="allowedStorageProfileIds")
    def allowed_storage_profile_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The identifiers of the storage profiles that this queue can use to share assets between workers using different operating systems.
        """
        return pulumi.get(self, "allowed_storage_profile_ids")

    @allowed_storage_profile_ids.setter
    def allowed_storage_profile_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_storage_profile_ids", value)

    @property
    @pulumi.getter(name="defaultBudgetAction")
    def default_budget_action(self) -> Optional[pulumi.Input['QueueDefaultQueueBudgetAction']]:
        """
        The default action taken on a queue summary if a budget wasn't configured.
        """
        return pulumi.get(self, "default_budget_action")

    @default_budget_action.setter
    def default_budget_action(self, value: Optional[pulumi.Input['QueueDefaultQueueBudgetAction']]):
        pulumi.set(self, "default_budget_action", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the queue that helps identify what the queue is used for.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="jobAttachmentSettings")
    def job_attachment_settings(self) -> Optional[pulumi.Input['QueueJobAttachmentSettingsArgs']]:
        """
        The job attachment settings. These are the Amazon S3 bucket name and the Amazon S3 prefix.
        """
        return pulumi.get(self, "job_attachment_settings")

    @job_attachment_settings.setter
    def job_attachment_settings(self, value: Optional[pulumi.Input['QueueJobAttachmentSettingsArgs']]):
        pulumi.set(self, "job_attachment_settings", value)

    @property
    @pulumi.getter(name="jobRunAsUser")
    def job_run_as_user(self) -> Optional[pulumi.Input['QueueJobRunAsUserArgs']]:
        """
        Identifies the user for a job.
        """
        return pulumi.get(self, "job_run_as_user")

    @job_run_as_user.setter
    def job_run_as_user(self, value: Optional[pulumi.Input['QueueJobRunAsUserArgs']]):
        pulumi.set(self, "job_run_as_user", value)

    @property
    @pulumi.getter(name="requiredFileSystemLocationNames")
    def required_file_system_location_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The file system location that the queue uses.
        """
        return pulumi.get(self, "required_file_system_location_names")

    @required_file_system_location_names.setter
    def required_file_system_location_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "required_file_system_location_names", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the IAM role that workers use when running jobs in this queue.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)

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


class Queue(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_storage_profile_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 default_budget_action: Optional[pulumi.Input['QueueDefaultQueueBudgetAction']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 farm_id: Optional[pulumi.Input[str]] = None,
                 job_attachment_settings: Optional[pulumi.Input[Union['QueueJobAttachmentSettingsArgs', 'QueueJobAttachmentSettingsArgsDict']]] = None,
                 job_run_as_user: Optional[pulumi.Input[Union['QueueJobRunAsUserArgs', 'QueueJobRunAsUserArgsDict']]] = None,
                 required_file_system_location_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Definition of AWS::Deadline::Queue Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_storage_profile_ids: The identifiers of the storage profiles that this queue can use to share assets between workers using different operating systems.
        :param pulumi.Input['QueueDefaultQueueBudgetAction'] default_budget_action: The default action taken on a queue summary if a budget wasn't configured.
        :param pulumi.Input[str] description: A description of the queue that helps identify what the queue is used for.
        :param pulumi.Input[str] display_name: The display name of the queue summary to update.
               
               > This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        :param pulumi.Input[str] farm_id: The farm ID.
        :param pulumi.Input[Union['QueueJobAttachmentSettingsArgs', 'QueueJobAttachmentSettingsArgsDict']] job_attachment_settings: The job attachment settings. These are the Amazon S3 bucket name and the Amazon S3 prefix.
        :param pulumi.Input[Union['QueueJobRunAsUserArgs', 'QueueJobRunAsUserArgsDict']] job_run_as_user: Identifies the user for a job.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] required_file_system_location_names: The file system location that the queue uses.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role that workers use when running jobs in this queue.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: QueueArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::Deadline::Queue Resource Type

        :param str resource_name: The name of the resource.
        :param QueueArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(QueueArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_storage_profile_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 default_budget_action: Optional[pulumi.Input['QueueDefaultQueueBudgetAction']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 farm_id: Optional[pulumi.Input[str]] = None,
                 job_attachment_settings: Optional[pulumi.Input[Union['QueueJobAttachmentSettingsArgs', 'QueueJobAttachmentSettingsArgsDict']]] = None,
                 job_run_as_user: Optional[pulumi.Input[Union['QueueJobRunAsUserArgs', 'QueueJobRunAsUserArgsDict']]] = None,
                 required_file_system_location_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = QueueArgs.__new__(QueueArgs)

            __props__.__dict__["allowed_storage_profile_ids"] = allowed_storage_profile_ids
            __props__.__dict__["default_budget_action"] = default_budget_action
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            if farm_id is None and not opts.urn:
                raise TypeError("Missing required property 'farm_id'")
            __props__.__dict__["farm_id"] = farm_id
            __props__.__dict__["job_attachment_settings"] = job_attachment_settings
            __props__.__dict__["job_run_as_user"] = job_run_as_user
            __props__.__dict__["required_file_system_location_names"] = required_file_system_location_names
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["queue_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["farmId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Queue, __self__).__init__(
            'aws-native:deadline:Queue',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Queue':
        """
        Get an existing Queue resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = QueueArgs.__new__(QueueArgs)

        __props__.__dict__["allowed_storage_profile_ids"] = None
        __props__.__dict__["arn"] = None
        __props__.__dict__["default_budget_action"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["farm_id"] = None
        __props__.__dict__["job_attachment_settings"] = None
        __props__.__dict__["job_run_as_user"] = None
        __props__.__dict__["queue_id"] = None
        __props__.__dict__["required_file_system_location_names"] = None
        __props__.__dict__["role_arn"] = None
        __props__.__dict__["tags"] = None
        return Queue(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowedStorageProfileIds")
    def allowed_storage_profile_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The identifiers of the storage profiles that this queue can use to share assets between workers using different operating systems.
        """
        return pulumi.get(self, "allowed_storage_profile_ids")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the queue.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="defaultBudgetAction")
    def default_budget_action(self) -> pulumi.Output[Optional['QueueDefaultQueueBudgetAction']]:
        """
        The default action taken on a queue summary if a budget wasn't configured.
        """
        return pulumi.get(self, "default_budget_action")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the queue that helps identify what the queue is used for.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name of the queue summary to update.

        > This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="farmId")
    def farm_id(self) -> pulumi.Output[str]:
        """
        The farm ID.
        """
        return pulumi.get(self, "farm_id")

    @property
    @pulumi.getter(name="jobAttachmentSettings")
    def job_attachment_settings(self) -> pulumi.Output[Optional['outputs.QueueJobAttachmentSettings']]:
        """
        The job attachment settings. These are the Amazon S3 bucket name and the Amazon S3 prefix.
        """
        return pulumi.get(self, "job_attachment_settings")

    @property
    @pulumi.getter(name="jobRunAsUser")
    def job_run_as_user(self) -> pulumi.Output[Optional['outputs.QueueJobRunAsUser']]:
        """
        Identifies the user for a job.
        """
        return pulumi.get(self, "job_run_as_user")

    @property
    @pulumi.getter(name="queueId")
    def queue_id(self) -> pulumi.Output[str]:
        """
        The queue ID.
        """
        return pulumi.get(self, "queue_id")

    @property
    @pulumi.getter(name="requiredFileSystemLocationNames")
    def required_file_system_location_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The file system location that the queue uses.
        """
        return pulumi.get(self, "required_file_system_location_names")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the IAM role that workers use when running jobs in this queue.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

