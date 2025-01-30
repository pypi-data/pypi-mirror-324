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
from ._inputs import *

__all__ = ['TriggerArgs', 'Trigger']

@pulumi.input_type
class TriggerArgs:
    def __init__(__self__, *,
                 actions: pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]],
                 type: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 event_batching_condition: Optional[pulumi.Input['TriggerEventBatchingConditionArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 predicate: Optional[pulumi.Input['TriggerPredicateArgs']] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 start_on_creation: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[Any] = None,
                 workflow_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Trigger resource.
        :param pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]] actions: The actions initiated by this trigger.
        :param pulumi.Input[str] type: The type of trigger that this is.
        :param pulumi.Input[str] description: A description of this trigger.
        :param pulumi.Input['TriggerEventBatchingConditionArgs'] event_batching_condition: Batch condition that must be met (specified number of events received or batch time window expired) before EventBridge event trigger fires.
        :param pulumi.Input[str] name: The name of the trigger.
        :param pulumi.Input['TriggerPredicateArgs'] predicate: The predicate of this trigger, which defines when it will fire.
        :param pulumi.Input[str] schedule: A cron expression used to specify the schedule.
        :param pulumi.Input[bool] start_on_creation: Set to true to start SCHEDULED and CONDITIONAL triggers when created. True is not supported for ON_DEMAND triggers.
        :param Any tags: The tags to use with this trigger.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Glue::Trigger` for more information about the expected schema for this property.
        :param pulumi.Input[str] workflow_name: The name of the workflow associated with the trigger.
        """
        pulumi.set(__self__, "actions", actions)
        pulumi.set(__self__, "type", type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if event_batching_condition is not None:
            pulumi.set(__self__, "event_batching_condition", event_batching_condition)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if predicate is not None:
            pulumi.set(__self__, "predicate", predicate)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if start_on_creation is not None:
            pulumi.set(__self__, "start_on_creation", start_on_creation)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if workflow_name is not None:
            pulumi.set(__self__, "workflow_name", workflow_name)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]]:
        """
        The actions initiated by this trigger.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of trigger that this is.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this trigger.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="eventBatchingCondition")
    def event_batching_condition(self) -> Optional[pulumi.Input['TriggerEventBatchingConditionArgs']]:
        """
        Batch condition that must be met (specified number of events received or batch time window expired) before EventBridge event trigger fires.
        """
        return pulumi.get(self, "event_batching_condition")

    @event_batching_condition.setter
    def event_batching_condition(self, value: Optional[pulumi.Input['TriggerEventBatchingConditionArgs']]):
        pulumi.set(self, "event_batching_condition", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the trigger.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def predicate(self) -> Optional[pulumi.Input['TriggerPredicateArgs']]:
        """
        The predicate of this trigger, which defines when it will fire.
        """
        return pulumi.get(self, "predicate")

    @predicate.setter
    def predicate(self, value: Optional[pulumi.Input['TriggerPredicateArgs']]):
        pulumi.set(self, "predicate", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input[str]]:
        """
        A cron expression used to specify the schedule.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="startOnCreation")
    def start_on_creation(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to true to start SCHEDULED and CONDITIONAL triggers when created. True is not supported for ON_DEMAND triggers.
        """
        return pulumi.get(self, "start_on_creation")

    @start_on_creation.setter
    def start_on_creation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "start_on_creation", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        """
        The tags to use with this trigger.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Glue::Trigger` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[Any]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="workflowName")
    def workflow_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the workflow associated with the trigger.
        """
        return pulumi.get(self, "workflow_name")

    @workflow_name.setter
    def workflow_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workflow_name", value)


class Trigger(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TriggerActionArgs', 'TriggerActionArgsDict']]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 event_batching_condition: Optional[pulumi.Input[Union['TriggerEventBatchingConditionArgs', 'TriggerEventBatchingConditionArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 predicate: Optional[pulumi.Input[Union['TriggerPredicateArgs', 'TriggerPredicateArgsDict']]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 start_on_creation: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[Any] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 workflow_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Glue::Trigger

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        on_demand_job_trigger = aws_native.glue.Trigger("onDemandJobTrigger",
            type="ON_DEMAND",
            description="DESCRIPTION_ON_DEMAND",
            actions=[{
                "job_name": "prod-job2",
            }],
            name="prod-trigger1-ondemand")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        on_demand_job_trigger = aws_native.glue.Trigger("onDemandJobTrigger",
            type="ON_DEMAND",
            description="DESCRIPTION_ON_DEMAND",
            actions=[{
                "job_name": "prod-job2",
            }],
            name="prod-trigger1-ondemand")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        scheduled_job_trigger = aws_native.glue.Trigger("scheduledJobTrigger",
            type="SCHEDULED",
            description="DESCRIPTION_SCHEDULED",
            schedule="cron(0 */2 * * ? *)",
            actions=[
                {
                    "job_name": "prod-job2",
                },
                {
                    "job_name": "prod-job3",
                    "arguments": {
                        "--job-bookmark-option": "job-bookmark-enable",
                    },
                },
            ],
            name="prod-trigger1-scheduled")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        scheduled_job_trigger = aws_native.glue.Trigger("scheduledJobTrigger",
            type="SCHEDULED",
            description="DESCRIPTION_SCHEDULED",
            schedule="cron(0 */2 * * ? *)",
            actions=[
                {
                    "job_name": "prod-job2",
                },
                {
                    "job_name": "prod-job3",
                    "arguments": {
                        "--job-bookmark-option": "job-bookmark-enable",
                    },
                },
            ],
            name="prod-trigger1-scheduled")

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['TriggerActionArgs', 'TriggerActionArgsDict']]]] actions: The actions initiated by this trigger.
        :param pulumi.Input[str] description: A description of this trigger.
        :param pulumi.Input[Union['TriggerEventBatchingConditionArgs', 'TriggerEventBatchingConditionArgsDict']] event_batching_condition: Batch condition that must be met (specified number of events received or batch time window expired) before EventBridge event trigger fires.
        :param pulumi.Input[str] name: The name of the trigger.
        :param pulumi.Input[Union['TriggerPredicateArgs', 'TriggerPredicateArgsDict']] predicate: The predicate of this trigger, which defines when it will fire.
        :param pulumi.Input[str] schedule: A cron expression used to specify the schedule.
        :param pulumi.Input[bool] start_on_creation: Set to true to start SCHEDULED and CONDITIONAL triggers when created. True is not supported for ON_DEMAND triggers.
        :param Any tags: The tags to use with this trigger.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Glue::Trigger` for more information about the expected schema for this property.
        :param pulumi.Input[str] type: The type of trigger that this is.
        :param pulumi.Input[str] workflow_name: The name of the workflow associated with the trigger.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TriggerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Glue::Trigger

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        on_demand_job_trigger = aws_native.glue.Trigger("onDemandJobTrigger",
            type="ON_DEMAND",
            description="DESCRIPTION_ON_DEMAND",
            actions=[{
                "job_name": "prod-job2",
            }],
            name="prod-trigger1-ondemand")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        on_demand_job_trigger = aws_native.glue.Trigger("onDemandJobTrigger",
            type="ON_DEMAND",
            description="DESCRIPTION_ON_DEMAND",
            actions=[{
                "job_name": "prod-job2",
            }],
            name="prod-trigger1-ondemand")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        scheduled_job_trigger = aws_native.glue.Trigger("scheduledJobTrigger",
            type="SCHEDULED",
            description="DESCRIPTION_SCHEDULED",
            schedule="cron(0 */2 * * ? *)",
            actions=[
                {
                    "job_name": "prod-job2",
                },
                {
                    "job_name": "prod-job3",
                    "arguments": {
                        "--job-bookmark-option": "job-bookmark-enable",
                    },
                },
            ],
            name="prod-trigger1-scheduled")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        scheduled_job_trigger = aws_native.glue.Trigger("scheduledJobTrigger",
            type="SCHEDULED",
            description="DESCRIPTION_SCHEDULED",
            schedule="cron(0 */2 * * ? *)",
            actions=[
                {
                    "job_name": "prod-job2",
                },
                {
                    "job_name": "prod-job3",
                    "arguments": {
                        "--job-bookmark-option": "job-bookmark-enable",
                    },
                },
            ],
            name="prod-trigger1-scheduled")

        ```

        :param str resource_name: The name of the resource.
        :param TriggerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TriggerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TriggerActionArgs', 'TriggerActionArgsDict']]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 event_batching_condition: Optional[pulumi.Input[Union['TriggerEventBatchingConditionArgs', 'TriggerEventBatchingConditionArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 predicate: Optional[pulumi.Input[Union['TriggerPredicateArgs', 'TriggerPredicateArgsDict']]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 start_on_creation: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[Any] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 workflow_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TriggerArgs.__new__(TriggerArgs)

            if actions is None and not opts.urn:
                raise TypeError("Missing required property 'actions'")
            __props__.__dict__["actions"] = actions
            __props__.__dict__["description"] = description
            __props__.__dict__["event_batching_condition"] = event_batching_condition
            __props__.__dict__["name"] = name
            __props__.__dict__["predicate"] = predicate
            __props__.__dict__["schedule"] = schedule
            __props__.__dict__["start_on_creation"] = start_on_creation
            __props__.__dict__["tags"] = tags
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["workflow_name"] = workflow_name
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name", "type", "workflowName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Trigger, __self__).__init__(
            'aws-native:glue:Trigger',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Trigger':
        """
        Get an existing Trigger resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TriggerArgs.__new__(TriggerArgs)

        __props__.__dict__["actions"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["event_batching_condition"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["predicate"] = None
        __props__.__dict__["schedule"] = None
        __props__.__dict__["start_on_creation"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["workflow_name"] = None
        return Trigger(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Output[Sequence['outputs.TriggerAction']]:
        """
        The actions initiated by this trigger.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of this trigger.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="eventBatchingCondition")
    def event_batching_condition(self) -> pulumi.Output[Optional['outputs.TriggerEventBatchingCondition']]:
        """
        Batch condition that must be met (specified number of events received or batch time window expired) before EventBridge event trigger fires.
        """
        return pulumi.get(self, "event_batching_condition")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the trigger.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def predicate(self) -> pulumi.Output[Optional['outputs.TriggerPredicate']]:
        """
        The predicate of this trigger, which defines when it will fire.
        """
        return pulumi.get(self, "predicate")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output[Optional[str]]:
        """
        A cron expression used to specify the schedule.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter(name="startOnCreation")
    def start_on_creation(self) -> pulumi.Output[Optional[bool]]:
        """
        Set to true to start SCHEDULED and CONDITIONAL triggers when created. True is not supported for ON_DEMAND triggers.
        """
        return pulumi.get(self, "start_on_creation")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Any]]:
        """
        The tags to use with this trigger.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Glue::Trigger` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of trigger that this is.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workflowName")
    def workflow_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the workflow associated with the trigger.
        """
        return pulumi.get(self, "workflow_name")

