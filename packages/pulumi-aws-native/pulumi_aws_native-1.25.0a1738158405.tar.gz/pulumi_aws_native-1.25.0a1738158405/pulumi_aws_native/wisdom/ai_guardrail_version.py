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

__all__ = ['AiGuardrailVersionArgs', 'AiGuardrailVersion']

@pulumi.input_type
class AiGuardrailVersionArgs:
    def __init__(__self__, *,
                 ai_guardrail_id: pulumi.Input[str],
                 assistant_id: pulumi.Input[str],
                 modified_time_seconds: Optional[pulumi.Input[float]] = None):
        """
        The set of arguments for constructing a AiGuardrailVersion resource.
        :param pulumi.Input[str] ai_guardrail_id: The ID of the AI guardrail version.
        :param pulumi.Input[str] assistant_id: The ID of the AI guardrail version assistant.
        :param pulumi.Input[float] modified_time_seconds: The modified time of the AI guardrail version in seconds.
        """
        pulumi.set(__self__, "ai_guardrail_id", ai_guardrail_id)
        pulumi.set(__self__, "assistant_id", assistant_id)
        if modified_time_seconds is not None:
            pulumi.set(__self__, "modified_time_seconds", modified_time_seconds)

    @property
    @pulumi.getter(name="aiGuardrailId")
    def ai_guardrail_id(self) -> pulumi.Input[str]:
        """
        The ID of the AI guardrail version.
        """
        return pulumi.get(self, "ai_guardrail_id")

    @ai_guardrail_id.setter
    def ai_guardrail_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "ai_guardrail_id", value)

    @property
    @pulumi.getter(name="assistantId")
    def assistant_id(self) -> pulumi.Input[str]:
        """
        The ID of the AI guardrail version assistant.
        """
        return pulumi.get(self, "assistant_id")

    @assistant_id.setter
    def assistant_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "assistant_id", value)

    @property
    @pulumi.getter(name="modifiedTimeSeconds")
    def modified_time_seconds(self) -> Optional[pulumi.Input[float]]:
        """
        The modified time of the AI guardrail version in seconds.
        """
        return pulumi.get(self, "modified_time_seconds")

    @modified_time_seconds.setter
    def modified_time_seconds(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "modified_time_seconds", value)


class AiGuardrailVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ai_guardrail_id: Optional[pulumi.Input[str]] = None,
                 assistant_id: Optional[pulumi.Input[str]] = None,
                 modified_time_seconds: Optional[pulumi.Input[float]] = None,
                 __props__=None):
        """
        Definition of AWS::Wisdom::AIGuardrailVersion Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ai_guardrail_id: The ID of the AI guardrail version.
        :param pulumi.Input[str] assistant_id: The ID of the AI guardrail version assistant.
        :param pulumi.Input[float] modified_time_seconds: The modified time of the AI guardrail version in seconds.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AiGuardrailVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::Wisdom::AIGuardrailVersion Resource Type

        :param str resource_name: The name of the resource.
        :param AiGuardrailVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AiGuardrailVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ai_guardrail_id: Optional[pulumi.Input[str]] = None,
                 assistant_id: Optional[pulumi.Input[str]] = None,
                 modified_time_seconds: Optional[pulumi.Input[float]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AiGuardrailVersionArgs.__new__(AiGuardrailVersionArgs)

            if ai_guardrail_id is None and not opts.urn:
                raise TypeError("Missing required property 'ai_guardrail_id'")
            __props__.__dict__["ai_guardrail_id"] = ai_guardrail_id
            if assistant_id is None and not opts.urn:
                raise TypeError("Missing required property 'assistant_id'")
            __props__.__dict__["assistant_id"] = assistant_id
            __props__.__dict__["modified_time_seconds"] = modified_time_seconds
            __props__.__dict__["ai_guardrail_arn"] = None
            __props__.__dict__["ai_guardrail_version_id"] = None
            __props__.__dict__["assistant_arn"] = None
            __props__.__dict__["version_number"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["aiGuardrailId", "assistantId", "modifiedTimeSeconds"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(AiGuardrailVersion, __self__).__init__(
            'aws-native:wisdom:AiGuardrailVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AiGuardrailVersion':
        """
        Get an existing AiGuardrailVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AiGuardrailVersionArgs.__new__(AiGuardrailVersionArgs)

        __props__.__dict__["ai_guardrail_arn"] = None
        __props__.__dict__["ai_guardrail_id"] = None
        __props__.__dict__["ai_guardrail_version_id"] = None
        __props__.__dict__["assistant_arn"] = None
        __props__.__dict__["assistant_id"] = None
        __props__.__dict__["modified_time_seconds"] = None
        __props__.__dict__["version_number"] = None
        return AiGuardrailVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="aiGuardrailArn")
    def ai_guardrail_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the AI guardrail version.
        """
        return pulumi.get(self, "ai_guardrail_arn")

    @property
    @pulumi.getter(name="aiGuardrailId")
    def ai_guardrail_id(self) -> pulumi.Output[str]:
        """
        The ID of the AI guardrail version.
        """
        return pulumi.get(self, "ai_guardrail_id")

    @property
    @pulumi.getter(name="aiGuardrailVersionId")
    def ai_guardrail_version_id(self) -> pulumi.Output[str]:
        """
        The ID of the AI guardrail version.
        """
        return pulumi.get(self, "ai_guardrail_version_id")

    @property
    @pulumi.getter(name="assistantArn")
    def assistant_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the AI guardrail version assistant.
        """
        return pulumi.get(self, "assistant_arn")

    @property
    @pulumi.getter(name="assistantId")
    def assistant_id(self) -> pulumi.Output[str]:
        """
        The ID of the AI guardrail version assistant.
        """
        return pulumi.get(self, "assistant_id")

    @property
    @pulumi.getter(name="modifiedTimeSeconds")
    def modified_time_seconds(self) -> pulumi.Output[Optional[float]]:
        """
        The modified time of the AI guardrail version in seconds.
        """
        return pulumi.get(self, "modified_time_seconds")

    @property
    @pulumi.getter(name="versionNumber")
    def version_number(self) -> pulumi.Output[float]:
        """
        The version number for this AI Guardrail version.
        """
        return pulumi.get(self, "version_number")

