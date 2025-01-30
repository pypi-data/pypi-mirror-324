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

__all__ = ['RuleArgs', 'Rule']

@pulumi.input_type
class RuleArgs:
    def __init__(__self__, *,
                 actions: pulumi.Input['RuleActionsArgs'],
                 function: pulumi.Input[str],
                 instance_arn: pulumi.Input[str],
                 publish_status: pulumi.Input['RulePublishStatus'],
                 trigger_event_source: pulumi.Input['RuleTriggerEventSourceArgs'],
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Rule resource.
        :param pulumi.Input['RuleActionsArgs'] actions: A list of actions to be run when the rule is triggered.
        :param pulumi.Input[str] function: The conditions of the rule.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param pulumi.Input['RulePublishStatus'] publish_status: The publish status of the rule.
                 *Allowed values*: ``DRAFT`` | ``PUBLISHED``
        :param pulumi.Input['RuleTriggerEventSourceArgs'] trigger_event_source: The event source to trigger the rule.
        :param pulumi.Input[str] name: The name of the rule.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        pulumi.set(__self__, "actions", actions)
        pulumi.set(__self__, "function", function)
        pulumi.set(__self__, "instance_arn", instance_arn)
        pulumi.set(__self__, "publish_status", publish_status)
        pulumi.set(__self__, "trigger_event_source", trigger_event_source)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Input['RuleActionsArgs']:
        """
        A list of actions to be run when the rule is triggered.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: pulumi.Input['RuleActionsArgs']):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter
    def function(self) -> pulumi.Input[str]:
        """
        The conditions of the rule.
        """
        return pulumi.get(self, "function")

    @function.setter
    def function(self, value: pulumi.Input[str]):
        pulumi.set(self, "function", value)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the instance.
        """
        return pulumi.get(self, "instance_arn")

    @instance_arn.setter
    def instance_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_arn", value)

    @property
    @pulumi.getter(name="publishStatus")
    def publish_status(self) -> pulumi.Input['RulePublishStatus']:
        """
        The publish status of the rule.
          *Allowed values*: ``DRAFT`` | ``PUBLISHED``
        """
        return pulumi.get(self, "publish_status")

    @publish_status.setter
    def publish_status(self, value: pulumi.Input['RulePublishStatus']):
        pulumi.set(self, "publish_status", value)

    @property
    @pulumi.getter(name="triggerEventSource")
    def trigger_event_source(self) -> pulumi.Input['RuleTriggerEventSourceArgs']:
        """
        The event source to trigger the rule.
        """
        return pulumi.get(self, "trigger_event_source")

    @trigger_event_source.setter
    def trigger_event_source(self, value: pulumi.Input['RuleTriggerEventSourceArgs']):
        pulumi.set(self, "trigger_event_source", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the rule.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Rule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Union['RuleActionsArgs', 'RuleActionsArgsDict']]] = None,
                 function: Optional[pulumi.Input[str]] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 publish_status: Optional[pulumi.Input['RulePublishStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 trigger_event_source: Optional[pulumi.Input[Union['RuleTriggerEventSourceArgs', 'RuleTriggerEventSourceArgsDict']]] = None,
                 __props__=None):
        """
        Creates a rule for the specified CON instance.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['RuleActionsArgs', 'RuleActionsArgsDict']] actions: A list of actions to be run when the rule is triggered.
        :param pulumi.Input[str] function: The conditions of the rule.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param pulumi.Input[str] name: The name of the rule.
        :param pulumi.Input['RulePublishStatus'] publish_status: The publish status of the rule.
                 *Allowed values*: ``DRAFT`` | ``PUBLISHED``
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        :param pulumi.Input[Union['RuleTriggerEventSourceArgs', 'RuleTriggerEventSourceArgsDict']] trigger_event_source: The event source to trigger the rule.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a rule for the specified CON instance.

        :param str resource_name: The name of the resource.
        :param RuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Union['RuleActionsArgs', 'RuleActionsArgsDict']]] = None,
                 function: Optional[pulumi.Input[str]] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 publish_status: Optional[pulumi.Input['RulePublishStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 trigger_event_source: Optional[pulumi.Input[Union['RuleTriggerEventSourceArgs', 'RuleTriggerEventSourceArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RuleArgs.__new__(RuleArgs)

            if actions is None and not opts.urn:
                raise TypeError("Missing required property 'actions'")
            __props__.__dict__["actions"] = actions
            if function is None and not opts.urn:
                raise TypeError("Missing required property 'function'")
            __props__.__dict__["function"] = function
            if instance_arn is None and not opts.urn:
                raise TypeError("Missing required property 'instance_arn'")
            __props__.__dict__["instance_arn"] = instance_arn
            __props__.__dict__["name"] = name
            if publish_status is None and not opts.urn:
                raise TypeError("Missing required property 'publish_status'")
            __props__.__dict__["publish_status"] = publish_status
            __props__.__dict__["tags"] = tags
            if trigger_event_source is None and not opts.urn:
                raise TypeError("Missing required property 'trigger_event_source'")
            __props__.__dict__["trigger_event_source"] = trigger_event_source
            __props__.__dict__["rule_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["instanceArn", "triggerEventSource"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Rule, __self__).__init__(
            'aws-native:connect:Rule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Rule':
        """
        Get an existing Rule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RuleArgs.__new__(RuleArgs)

        __props__.__dict__["actions"] = None
        __props__.__dict__["function"] = None
        __props__.__dict__["instance_arn"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["publish_status"] = None
        __props__.__dict__["rule_arn"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["trigger_event_source"] = None
        return Rule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Output['outputs.RuleActions']:
        """
        A list of actions to be run when the rule is triggered.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter
    def function(self) -> pulumi.Output[str]:
        """
        The conditions of the rule.
        """
        return pulumi.get(self, "function")

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the instance.
        """
        return pulumi.get(self, "instance_arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the rule.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publishStatus")
    def publish_status(self) -> pulumi.Output['RulePublishStatus']:
        """
        The publish status of the rule.
          *Allowed values*: ``DRAFT`` | ``PUBLISHED``
        """
        return pulumi.get(self, "publish_status")

    @property
    @pulumi.getter(name="ruleArn")
    def rule_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the rule.
        """
        return pulumi.get(self, "rule_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="triggerEventSource")
    def trigger_event_source(self) -> pulumi.Output['outputs.RuleTriggerEventSource']:
        """
        The event source to trigger the rule.
        """
        return pulumi.get(self, "trigger_event_source")

