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

__all__ = ['MessageTemplateVersionArgs', 'MessageTemplateVersion']

@pulumi.input_type
class MessageTemplateVersionArgs:
    def __init__(__self__, *,
                 message_template_arn: pulumi.Input[str],
                 message_template_content_sha256: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MessageTemplateVersion resource.
        :param pulumi.Input[str] message_template_arn: The unqualified Amazon Resource Name (ARN) of the message template.
        :param pulumi.Input[str] message_template_content_sha256: The content SHA256 of the message template.
        """
        pulumi.set(__self__, "message_template_arn", message_template_arn)
        if message_template_content_sha256 is not None:
            pulumi.set(__self__, "message_template_content_sha256", message_template_content_sha256)

    @property
    @pulumi.getter(name="messageTemplateArn")
    def message_template_arn(self) -> pulumi.Input[str]:
        """
        The unqualified Amazon Resource Name (ARN) of the message template.
        """
        return pulumi.get(self, "message_template_arn")

    @message_template_arn.setter
    def message_template_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "message_template_arn", value)

    @property
    @pulumi.getter(name="messageTemplateContentSha256")
    def message_template_content_sha256(self) -> Optional[pulumi.Input[str]]:
        """
        The content SHA256 of the message template.
        """
        return pulumi.get(self, "message_template_content_sha256")

    @message_template_content_sha256.setter
    def message_template_content_sha256(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message_template_content_sha256", value)


class MessageTemplateVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 message_template_arn: Optional[pulumi.Input[str]] = None,
                 message_template_content_sha256: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A version for the specified customer-managed message template within the specified knowledge base.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] message_template_arn: The unqualified Amazon Resource Name (ARN) of the message template.
        :param pulumi.Input[str] message_template_content_sha256: The content SHA256 of the message template.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MessageTemplateVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A version for the specified customer-managed message template within the specified knowledge base.

        :param str resource_name: The name of the resource.
        :param MessageTemplateVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MessageTemplateVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 message_template_arn: Optional[pulumi.Input[str]] = None,
                 message_template_content_sha256: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MessageTemplateVersionArgs.__new__(MessageTemplateVersionArgs)

            if message_template_arn is None and not opts.urn:
                raise TypeError("Missing required property 'message_template_arn'")
            __props__.__dict__["message_template_arn"] = message_template_arn
            __props__.__dict__["message_template_content_sha256"] = message_template_content_sha256
            __props__.__dict__["message_template_version_arn"] = None
            __props__.__dict__["message_template_version_number"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["messageTemplateArn"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(MessageTemplateVersion, __self__).__init__(
            'aws-native:wisdom:MessageTemplateVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MessageTemplateVersion':
        """
        Get an existing MessageTemplateVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MessageTemplateVersionArgs.__new__(MessageTemplateVersionArgs)

        __props__.__dict__["message_template_arn"] = None
        __props__.__dict__["message_template_content_sha256"] = None
        __props__.__dict__["message_template_version_arn"] = None
        __props__.__dict__["message_template_version_number"] = None
        return MessageTemplateVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="messageTemplateArn")
    def message_template_arn(self) -> pulumi.Output[str]:
        """
        The unqualified Amazon Resource Name (ARN) of the message template.
        """
        return pulumi.get(self, "message_template_arn")

    @property
    @pulumi.getter(name="messageTemplateContentSha256")
    def message_template_content_sha256(self) -> pulumi.Output[Optional[str]]:
        """
        The content SHA256 of the message template.
        """
        return pulumi.get(self, "message_template_content_sha256")

    @property
    @pulumi.getter(name="messageTemplateVersionArn")
    def message_template_version_arn(self) -> pulumi.Output[str]:
        """
        The unqualified Amazon Resource Name (ARN) of the message template version.
        """
        return pulumi.get(self, "message_template_version_arn")

    @property
    @pulumi.getter(name="messageTemplateVersionNumber")
    def message_template_version_number(self) -> pulumi.Output[float]:
        """
        Current version number of the message template.
        """
        return pulumi.get(self, "message_template_version_number")

