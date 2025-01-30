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

__all__ = ['SlackChannelConfigurationArgs', 'SlackChannelConfiguration']

@pulumi.input_type
class SlackChannelConfigurationArgs:
    def __init__(__self__, *,
                 iam_role_arn: pulumi.Input[str],
                 slack_channel_id: pulumi.Input[str],
                 slack_workspace_id: pulumi.Input[str],
                 configuration_name: Optional[pulumi.Input[str]] = None,
                 customization_resource_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 guardrail_policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 logging_level: Optional[pulumi.Input[str]] = None,
                 sns_topic_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 user_role_required: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a SlackChannelConfiguration resource.
        :param pulumi.Input[str] iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot
        :param pulumi.Input[str] slack_channel_id: The id of the Slack channel
        :param pulumi.Input[str] slack_workspace_id: The id of the Slack workspace
        :param pulumi.Input[str] configuration_name: The name of the configuration
        :param pulumi.Input[Sequence[pulumi.Input[str]]] customization_resource_arns: ARNs of Custom Actions to associate with notifications in the provided chat channel.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param pulumi.Input[str] logging_level: Specifies the logging level for this configuration:ERROR,INFO or NONE. This property affects the log entries pushed to Amazon CloudWatch logs
        :param pulumi.Input[Sequence[pulumi.Input[str]]] sns_topic_arns: ARNs of SNS topics which delivers notifications to AWS Chatbot, for example CloudWatch alarm notifications.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags to add to the configuration
        :param pulumi.Input[bool] user_role_required: Enables use of a user role requirement in your chat configuration
        """
        pulumi.set(__self__, "iam_role_arn", iam_role_arn)
        pulumi.set(__self__, "slack_channel_id", slack_channel_id)
        pulumi.set(__self__, "slack_workspace_id", slack_workspace_id)
        if configuration_name is not None:
            pulumi.set(__self__, "configuration_name", configuration_name)
        if customization_resource_arns is not None:
            pulumi.set(__self__, "customization_resource_arns", customization_resource_arns)
        if guardrail_policies is not None:
            pulumi.set(__self__, "guardrail_policies", guardrail_policies)
        if logging_level is not None:
            pulumi.set(__self__, "logging_level", logging_level)
        if sns_topic_arns is not None:
            pulumi.set(__self__, "sns_topic_arns", sns_topic_arns)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if user_role_required is not None:
            pulumi.set(__self__, "user_role_required", user_role_required)

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the IAM role that defines the permissions for AWS Chatbot
        """
        return pulumi.get(self, "iam_role_arn")

    @iam_role_arn.setter
    def iam_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "iam_role_arn", value)

    @property
    @pulumi.getter(name="slackChannelId")
    def slack_channel_id(self) -> pulumi.Input[str]:
        """
        The id of the Slack channel
        """
        return pulumi.get(self, "slack_channel_id")

    @slack_channel_id.setter
    def slack_channel_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "slack_channel_id", value)

    @property
    @pulumi.getter(name="slackWorkspaceId")
    def slack_workspace_id(self) -> pulumi.Input[str]:
        """
        The id of the Slack workspace
        """
        return pulumi.get(self, "slack_workspace_id")

    @slack_workspace_id.setter
    def slack_workspace_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "slack_workspace_id", value)

    @property
    @pulumi.getter(name="configurationName")
    def configuration_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the configuration
        """
        return pulumi.get(self, "configuration_name")

    @configuration_name.setter
    def configuration_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configuration_name", value)

    @property
    @pulumi.getter(name="customizationResourceArns")
    def customization_resource_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        ARNs of Custom Actions to associate with notifications in the provided chat channel.
        """
        return pulumi.get(self, "customization_resource_arns")

    @customization_resource_arns.setter
    def customization_resource_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "customization_resource_arns", value)

    @property
    @pulumi.getter(name="guardrailPolicies")
    def guardrail_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        """
        return pulumi.get(self, "guardrail_policies")

    @guardrail_policies.setter
    def guardrail_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "guardrail_policies", value)

    @property
    @pulumi.getter(name="loggingLevel")
    def logging_level(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the logging level for this configuration:ERROR,INFO or NONE. This property affects the log entries pushed to Amazon CloudWatch logs
        """
        return pulumi.get(self, "logging_level")

    @logging_level.setter
    def logging_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "logging_level", value)

    @property
    @pulumi.getter(name="snsTopicArns")
    def sns_topic_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        ARNs of SNS topics which delivers notifications to AWS Chatbot, for example CloudWatch alarm notifications.
        """
        return pulumi.get(self, "sns_topic_arns")

    @sns_topic_arns.setter
    def sns_topic_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "sns_topic_arns", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags to add to the configuration
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="userRoleRequired")
    def user_role_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables use of a user role requirement in your chat configuration
        """
        return pulumi.get(self, "user_role_required")

    @user_role_required.setter
    def user_role_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "user_role_required", value)


class SlackChannelConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_name: Optional[pulumi.Input[str]] = None,
                 customization_resource_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 guardrail_policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 iam_role_arn: Optional[pulumi.Input[str]] = None,
                 logging_level: Optional[pulumi.Input[str]] = None,
                 slack_channel_id: Optional[pulumi.Input[str]] = None,
                 slack_workspace_id: Optional[pulumi.Input[str]] = None,
                 sns_topic_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 user_role_required: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Resource schema for AWS::Chatbot::SlackChannelConfiguration.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configuration_name: The name of the configuration
        :param pulumi.Input[Sequence[pulumi.Input[str]]] customization_resource_arns: ARNs of Custom Actions to associate with notifications in the provided chat channel.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param pulumi.Input[str] iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot
        :param pulumi.Input[str] logging_level: Specifies the logging level for this configuration:ERROR,INFO or NONE. This property affects the log entries pushed to Amazon CloudWatch logs
        :param pulumi.Input[str] slack_channel_id: The id of the Slack channel
        :param pulumi.Input[str] slack_workspace_id: The id of the Slack workspace
        :param pulumi.Input[Sequence[pulumi.Input[str]]] sns_topic_arns: ARNs of SNS topics which delivers notifications to AWS Chatbot, for example CloudWatch alarm notifications.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags to add to the configuration
        :param pulumi.Input[bool] user_role_required: Enables use of a user role requirement in your chat configuration
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SlackChannelConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::Chatbot::SlackChannelConfiguration.

        :param str resource_name: The name of the resource.
        :param SlackChannelConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SlackChannelConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_name: Optional[pulumi.Input[str]] = None,
                 customization_resource_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 guardrail_policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 iam_role_arn: Optional[pulumi.Input[str]] = None,
                 logging_level: Optional[pulumi.Input[str]] = None,
                 slack_channel_id: Optional[pulumi.Input[str]] = None,
                 slack_workspace_id: Optional[pulumi.Input[str]] = None,
                 sns_topic_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 user_role_required: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SlackChannelConfigurationArgs.__new__(SlackChannelConfigurationArgs)

            __props__.__dict__["configuration_name"] = configuration_name
            __props__.__dict__["customization_resource_arns"] = customization_resource_arns
            __props__.__dict__["guardrail_policies"] = guardrail_policies
            if iam_role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'iam_role_arn'")
            __props__.__dict__["iam_role_arn"] = iam_role_arn
            __props__.__dict__["logging_level"] = logging_level
            if slack_channel_id is None and not opts.urn:
                raise TypeError("Missing required property 'slack_channel_id'")
            __props__.__dict__["slack_channel_id"] = slack_channel_id
            if slack_workspace_id is None and not opts.urn:
                raise TypeError("Missing required property 'slack_workspace_id'")
            __props__.__dict__["slack_workspace_id"] = slack_workspace_id
            __props__.__dict__["sns_topic_arns"] = sns_topic_arns
            __props__.__dict__["tags"] = tags
            __props__.__dict__["user_role_required"] = user_role_required
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["configurationName", "slackWorkspaceId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(SlackChannelConfiguration, __self__).__init__(
            'aws-native:chatbot:SlackChannelConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SlackChannelConfiguration':
        """
        Get an existing SlackChannelConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SlackChannelConfigurationArgs.__new__(SlackChannelConfigurationArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["configuration_name"] = None
        __props__.__dict__["customization_resource_arns"] = None
        __props__.__dict__["guardrail_policies"] = None
        __props__.__dict__["iam_role_arn"] = None
        __props__.__dict__["logging_level"] = None
        __props__.__dict__["slack_channel_id"] = None
        __props__.__dict__["slack_workspace_id"] = None
        __props__.__dict__["sns_topic_arns"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["user_role_required"] = None
        return SlackChannelConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the configuration
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="configurationName")
    def configuration_name(self) -> pulumi.Output[str]:
        """
        The name of the configuration
        """
        return pulumi.get(self, "configuration_name")

    @property
    @pulumi.getter(name="customizationResourceArns")
    def customization_resource_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        ARNs of Custom Actions to associate with notifications in the provided chat channel.
        """
        return pulumi.get(self, "customization_resource_arns")

    @property
    @pulumi.getter(name="guardrailPolicies")
    def guardrail_policies(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        """
        return pulumi.get(self, "guardrail_policies")

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the IAM role that defines the permissions for AWS Chatbot
        """
        return pulumi.get(self, "iam_role_arn")

    @property
    @pulumi.getter(name="loggingLevel")
    def logging_level(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the logging level for this configuration:ERROR,INFO or NONE. This property affects the log entries pushed to Amazon CloudWatch logs
        """
        return pulumi.get(self, "logging_level")

    @property
    @pulumi.getter(name="slackChannelId")
    def slack_channel_id(self) -> pulumi.Output[str]:
        """
        The id of the Slack channel
        """
        return pulumi.get(self, "slack_channel_id")

    @property
    @pulumi.getter(name="slackWorkspaceId")
    def slack_workspace_id(self) -> pulumi.Output[str]:
        """
        The id of the Slack workspace
        """
        return pulumi.get(self, "slack_workspace_id")

    @property
    @pulumi.getter(name="snsTopicArns")
    def sns_topic_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        ARNs of SNS topics which delivers notifications to AWS Chatbot, for example CloudWatch alarm notifications.
        """
        return pulumi.get(self, "sns_topic_arns")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags to add to the configuration
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="userRoleRequired")
    def user_role_required(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables use of a user role requirement in your chat configuration
        """
        return pulumi.get(self, "user_role_required")

