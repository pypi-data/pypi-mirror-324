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

__all__ = ['JobDefinitionArgs', 'JobDefinition']

@pulumi.input_type
class JobDefinitionArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 container_properties: Optional[pulumi.Input['JobDefinitionContainerPropertiesArgs']] = None,
                 ecs_properties: Optional[pulumi.Input['JobDefinitionEcsPropertiesArgs']] = None,
                 eks_properties: Optional[pulumi.Input['JobDefinitionEksPropertiesArgs']] = None,
                 job_definition_name: Optional[pulumi.Input[str]] = None,
                 node_properties: Optional[pulumi.Input['JobDefinitionNodePropertiesArgs']] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 platform_capabilities: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 propagate_tags: Optional[pulumi.Input[bool]] = None,
                 retry_strategy: Optional[pulumi.Input['JobDefinitionRetryStrategyArgs']] = None,
                 scheduling_priority: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout: Optional[pulumi.Input['JobDefinitionJobTimeoutArgs']] = None):
        """
        The set of arguments for constructing a JobDefinition resource.
        :param pulumi.Input[str] type: The type of job definition. For more information about multi-node parallel jobs, see [Creating a multi-node parallel job definition](https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html) in the *AWS Batch User Guide* .
               
               - If the value is `container` , then one of the following is required: `containerProperties` , `ecsProperties` , or `eksProperties` .
               - If the value is `multinode` , then `nodeProperties` is required.
               
               > If the job is run on Fargate resources, then `multinode` isn't supported.
        :param pulumi.Input['JobDefinitionContainerPropertiesArgs'] container_properties: An object with properties specific to Amazon ECS-based jobs. When `containerProperties` is used in the job definition, it can't be used in addition to `eksProperties` , `ecsProperties` , or `nodeProperties` .
        :param pulumi.Input['JobDefinitionEcsPropertiesArgs'] ecs_properties: An object that contains the properties for the Amazon ECS resources of a job.When `ecsProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `eksProperties` , or `nodeProperties` .
        :param pulumi.Input['JobDefinitionEksPropertiesArgs'] eks_properties: An object with properties that are specific to Amazon EKS-based jobs. When `eksProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `ecsProperties` , or `nodeProperties` .
        :param pulumi.Input[str] job_definition_name: The name of the job definition.
        :param pulumi.Input['JobDefinitionNodePropertiesArgs'] node_properties: An object with properties that are specific to multi-node parallel jobs. When `nodeProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `ecsProperties` , or `eksProperties` .
               
               > If the job runs on Fargate resources, don't specify `nodeProperties` . Use `containerProperties` instead.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] parameters: Default parameters or parameter substitution placeholders that are set in the job definition. Parameters are specified as a key-value pair mapping. Parameters in a `SubmitJob` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see [Job definition parameters](https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html) in the *AWS Batch User Guide* .
        :param pulumi.Input[Sequence[pulumi.Input[str]]] platform_capabilities: The platform capabilities required by the job definition. If no value is specified, it defaults to `EC2` . Jobs run on Fargate resources specify `FARGATE` .
        :param pulumi.Input[bool] propagate_tags: Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task. If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the `FAILED` state.
        :param pulumi.Input['JobDefinitionRetryStrategyArgs'] retry_strategy: The retry strategy to use for failed jobs that are submitted with this job definition.
        :param pulumi.Input[int] scheduling_priority: The scheduling priority of the job definition. This only affects jobs in job queues with a fair share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A key-value pair to associate with a resource.
        :param pulumi.Input['JobDefinitionJobTimeoutArgs'] timeout: The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.
        """
        pulumi.set(__self__, "type", type)
        if container_properties is not None:
            pulumi.set(__self__, "container_properties", container_properties)
        if ecs_properties is not None:
            pulumi.set(__self__, "ecs_properties", ecs_properties)
        if eks_properties is not None:
            pulumi.set(__self__, "eks_properties", eks_properties)
        if job_definition_name is not None:
            pulumi.set(__self__, "job_definition_name", job_definition_name)
        if node_properties is not None:
            pulumi.set(__self__, "node_properties", node_properties)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if platform_capabilities is not None:
            pulumi.set(__self__, "platform_capabilities", platform_capabilities)
        if propagate_tags is not None:
            pulumi.set(__self__, "propagate_tags", propagate_tags)
        if retry_strategy is not None:
            pulumi.set(__self__, "retry_strategy", retry_strategy)
        if scheduling_priority is not None:
            pulumi.set(__self__, "scheduling_priority", scheduling_priority)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of job definition. For more information about multi-node parallel jobs, see [Creating a multi-node parallel job definition](https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html) in the *AWS Batch User Guide* .

        - If the value is `container` , then one of the following is required: `containerProperties` , `ecsProperties` , or `eksProperties` .
        - If the value is `multinode` , then `nodeProperties` is required.

        > If the job is run on Fargate resources, then `multinode` isn't supported.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="containerProperties")
    def container_properties(self) -> Optional[pulumi.Input['JobDefinitionContainerPropertiesArgs']]:
        """
        An object with properties specific to Amazon ECS-based jobs. When `containerProperties` is used in the job definition, it can't be used in addition to `eksProperties` , `ecsProperties` , or `nodeProperties` .
        """
        return pulumi.get(self, "container_properties")

    @container_properties.setter
    def container_properties(self, value: Optional[pulumi.Input['JobDefinitionContainerPropertiesArgs']]):
        pulumi.set(self, "container_properties", value)

    @property
    @pulumi.getter(name="ecsProperties")
    def ecs_properties(self) -> Optional[pulumi.Input['JobDefinitionEcsPropertiesArgs']]:
        """
        An object that contains the properties for the Amazon ECS resources of a job.When `ecsProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `eksProperties` , or `nodeProperties` .
        """
        return pulumi.get(self, "ecs_properties")

    @ecs_properties.setter
    def ecs_properties(self, value: Optional[pulumi.Input['JobDefinitionEcsPropertiesArgs']]):
        pulumi.set(self, "ecs_properties", value)

    @property
    @pulumi.getter(name="eksProperties")
    def eks_properties(self) -> Optional[pulumi.Input['JobDefinitionEksPropertiesArgs']]:
        """
        An object with properties that are specific to Amazon EKS-based jobs. When `eksProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `ecsProperties` , or `nodeProperties` .
        """
        return pulumi.get(self, "eks_properties")

    @eks_properties.setter
    def eks_properties(self, value: Optional[pulumi.Input['JobDefinitionEksPropertiesArgs']]):
        pulumi.set(self, "eks_properties", value)

    @property
    @pulumi.getter(name="jobDefinitionName")
    def job_definition_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the job definition.
        """
        return pulumi.get(self, "job_definition_name")

    @job_definition_name.setter
    def job_definition_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "job_definition_name", value)

    @property
    @pulumi.getter(name="nodeProperties")
    def node_properties(self) -> Optional[pulumi.Input['JobDefinitionNodePropertiesArgs']]:
        """
        An object with properties that are specific to multi-node parallel jobs. When `nodeProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `ecsProperties` , or `eksProperties` .

        > If the job runs on Fargate resources, don't specify `nodeProperties` . Use `containerProperties` instead.
        """
        return pulumi.get(self, "node_properties")

    @node_properties.setter
    def node_properties(self, value: Optional[pulumi.Input['JobDefinitionNodePropertiesArgs']]):
        pulumi.set(self, "node_properties", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Default parameters or parameter substitution placeholders that are set in the job definition. Parameters are specified as a key-value pair mapping. Parameters in a `SubmitJob` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see [Job definition parameters](https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html) in the *AWS Batch User Guide* .
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="platformCapabilities")
    def platform_capabilities(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The platform capabilities required by the job definition. If no value is specified, it defaults to `EC2` . Jobs run on Fargate resources specify `FARGATE` .
        """
        return pulumi.get(self, "platform_capabilities")

    @platform_capabilities.setter
    def platform_capabilities(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "platform_capabilities", value)

    @property
    @pulumi.getter(name="propagateTags")
    def propagate_tags(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task. If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the `FAILED` state.
        """
        return pulumi.get(self, "propagate_tags")

    @propagate_tags.setter
    def propagate_tags(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "propagate_tags", value)

    @property
    @pulumi.getter(name="retryStrategy")
    def retry_strategy(self) -> Optional[pulumi.Input['JobDefinitionRetryStrategyArgs']]:
        """
        The retry strategy to use for failed jobs that are submitted with this job definition.
        """
        return pulumi.get(self, "retry_strategy")

    @retry_strategy.setter
    def retry_strategy(self, value: Optional[pulumi.Input['JobDefinitionRetryStrategyArgs']]):
        pulumi.set(self, "retry_strategy", value)

    @property
    @pulumi.getter(name="schedulingPriority")
    def scheduling_priority(self) -> Optional[pulumi.Input[int]]:
        """
        The scheduling priority of the job definition. This only affects jobs in job queues with a fair share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.
        """
        return pulumi.get(self, "scheduling_priority")

    @scheduling_priority.setter
    def scheduling_priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "scheduling_priority", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A key-value pair to associate with a resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input['JobDefinitionJobTimeoutArgs']]:
        """
        The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.
        """
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input['JobDefinitionJobTimeoutArgs']]):
        pulumi.set(self, "timeout", value)


class JobDefinition(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_properties: Optional[pulumi.Input[Union['JobDefinitionContainerPropertiesArgs', 'JobDefinitionContainerPropertiesArgsDict']]] = None,
                 ecs_properties: Optional[pulumi.Input[Union['JobDefinitionEcsPropertiesArgs', 'JobDefinitionEcsPropertiesArgsDict']]] = None,
                 eks_properties: Optional[pulumi.Input[Union['JobDefinitionEksPropertiesArgs', 'JobDefinitionEksPropertiesArgsDict']]] = None,
                 job_definition_name: Optional[pulumi.Input[str]] = None,
                 node_properties: Optional[pulumi.Input[Union['JobDefinitionNodePropertiesArgs', 'JobDefinitionNodePropertiesArgsDict']]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 platform_capabilities: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 propagate_tags: Optional[pulumi.Input[bool]] = None,
                 retry_strategy: Optional[pulumi.Input[Union['JobDefinitionRetryStrategyArgs', 'JobDefinitionRetryStrategyArgsDict']]] = None,
                 scheduling_priority: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout: Optional[pulumi.Input[Union['JobDefinitionJobTimeoutArgs', 'JobDefinitionJobTimeoutArgsDict']]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Batch::JobDefinition

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['JobDefinitionContainerPropertiesArgs', 'JobDefinitionContainerPropertiesArgsDict']] container_properties: An object with properties specific to Amazon ECS-based jobs. When `containerProperties` is used in the job definition, it can't be used in addition to `eksProperties` , `ecsProperties` , or `nodeProperties` .
        :param pulumi.Input[Union['JobDefinitionEcsPropertiesArgs', 'JobDefinitionEcsPropertiesArgsDict']] ecs_properties: An object that contains the properties for the Amazon ECS resources of a job.When `ecsProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `eksProperties` , or `nodeProperties` .
        :param pulumi.Input[Union['JobDefinitionEksPropertiesArgs', 'JobDefinitionEksPropertiesArgsDict']] eks_properties: An object with properties that are specific to Amazon EKS-based jobs. When `eksProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `ecsProperties` , or `nodeProperties` .
        :param pulumi.Input[str] job_definition_name: The name of the job definition.
        :param pulumi.Input[Union['JobDefinitionNodePropertiesArgs', 'JobDefinitionNodePropertiesArgsDict']] node_properties: An object with properties that are specific to multi-node parallel jobs. When `nodeProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `ecsProperties` , or `eksProperties` .
               
               > If the job runs on Fargate resources, don't specify `nodeProperties` . Use `containerProperties` instead.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] parameters: Default parameters or parameter substitution placeholders that are set in the job definition. Parameters are specified as a key-value pair mapping. Parameters in a `SubmitJob` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see [Job definition parameters](https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html) in the *AWS Batch User Guide* .
        :param pulumi.Input[Sequence[pulumi.Input[str]]] platform_capabilities: The platform capabilities required by the job definition. If no value is specified, it defaults to `EC2` . Jobs run on Fargate resources specify `FARGATE` .
        :param pulumi.Input[bool] propagate_tags: Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task. If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the `FAILED` state.
        :param pulumi.Input[Union['JobDefinitionRetryStrategyArgs', 'JobDefinitionRetryStrategyArgsDict']] retry_strategy: The retry strategy to use for failed jobs that are submitted with this job definition.
        :param pulumi.Input[int] scheduling_priority: The scheduling priority of the job definition. This only affects jobs in job queues with a fair share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A key-value pair to associate with a resource.
        :param pulumi.Input[Union['JobDefinitionJobTimeoutArgs', 'JobDefinitionJobTimeoutArgsDict']] timeout: The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.
        :param pulumi.Input[str] type: The type of job definition. For more information about multi-node parallel jobs, see [Creating a multi-node parallel job definition](https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html) in the *AWS Batch User Guide* .
               
               - If the value is `container` , then one of the following is required: `containerProperties` , `ecsProperties` , or `eksProperties` .
               - If the value is `multinode` , then `nodeProperties` is required.
               
               > If the job is run on Fargate resources, then `multinode` isn't supported.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: JobDefinitionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Batch::JobDefinition

        :param str resource_name: The name of the resource.
        :param JobDefinitionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JobDefinitionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_properties: Optional[pulumi.Input[Union['JobDefinitionContainerPropertiesArgs', 'JobDefinitionContainerPropertiesArgsDict']]] = None,
                 ecs_properties: Optional[pulumi.Input[Union['JobDefinitionEcsPropertiesArgs', 'JobDefinitionEcsPropertiesArgsDict']]] = None,
                 eks_properties: Optional[pulumi.Input[Union['JobDefinitionEksPropertiesArgs', 'JobDefinitionEksPropertiesArgsDict']]] = None,
                 job_definition_name: Optional[pulumi.Input[str]] = None,
                 node_properties: Optional[pulumi.Input[Union['JobDefinitionNodePropertiesArgs', 'JobDefinitionNodePropertiesArgsDict']]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 platform_capabilities: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 propagate_tags: Optional[pulumi.Input[bool]] = None,
                 retry_strategy: Optional[pulumi.Input[Union['JobDefinitionRetryStrategyArgs', 'JobDefinitionRetryStrategyArgsDict']]] = None,
                 scheduling_priority: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout: Optional[pulumi.Input[Union['JobDefinitionJobTimeoutArgs', 'JobDefinitionJobTimeoutArgsDict']]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = JobDefinitionArgs.__new__(JobDefinitionArgs)

            __props__.__dict__["container_properties"] = container_properties
            __props__.__dict__["ecs_properties"] = ecs_properties
            __props__.__dict__["eks_properties"] = eks_properties
            __props__.__dict__["job_definition_name"] = job_definition_name
            __props__.__dict__["node_properties"] = node_properties
            __props__.__dict__["parameters"] = parameters
            __props__.__dict__["platform_capabilities"] = platform_capabilities
            __props__.__dict__["propagate_tags"] = propagate_tags
            __props__.__dict__["retry_strategy"] = retry_strategy
            __props__.__dict__["scheduling_priority"] = scheduling_priority
            __props__.__dict__["tags"] = tags
            __props__.__dict__["timeout"] = timeout
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["jobDefinitionName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(JobDefinition, __self__).__init__(
            'aws-native:batch:JobDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'JobDefinition':
        """
        Get an existing JobDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = JobDefinitionArgs.__new__(JobDefinitionArgs)

        __props__.__dict__["container_properties"] = None
        __props__.__dict__["ecs_properties"] = None
        __props__.__dict__["eks_properties"] = None
        __props__.__dict__["job_definition_name"] = None
        __props__.__dict__["node_properties"] = None
        __props__.__dict__["parameters"] = None
        __props__.__dict__["platform_capabilities"] = None
        __props__.__dict__["propagate_tags"] = None
        __props__.__dict__["retry_strategy"] = None
        __props__.__dict__["scheduling_priority"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["timeout"] = None
        __props__.__dict__["type"] = None
        return JobDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="containerProperties")
    def container_properties(self) -> pulumi.Output[Optional['outputs.JobDefinitionContainerProperties']]:
        """
        An object with properties specific to Amazon ECS-based jobs. When `containerProperties` is used in the job definition, it can't be used in addition to `eksProperties` , `ecsProperties` , or `nodeProperties` .
        """
        return pulumi.get(self, "container_properties")

    @property
    @pulumi.getter(name="ecsProperties")
    def ecs_properties(self) -> pulumi.Output[Optional['outputs.JobDefinitionEcsProperties']]:
        """
        An object that contains the properties for the Amazon ECS resources of a job.When `ecsProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `eksProperties` , or `nodeProperties` .
        """
        return pulumi.get(self, "ecs_properties")

    @property
    @pulumi.getter(name="eksProperties")
    def eks_properties(self) -> pulumi.Output[Optional['outputs.JobDefinitionEksProperties']]:
        """
        An object with properties that are specific to Amazon EKS-based jobs. When `eksProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `ecsProperties` , or `nodeProperties` .
        """
        return pulumi.get(self, "eks_properties")

    @property
    @pulumi.getter(name="jobDefinitionName")
    def job_definition_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the job definition.
        """
        return pulumi.get(self, "job_definition_name")

    @property
    @pulumi.getter(name="nodeProperties")
    def node_properties(self) -> pulumi.Output[Optional['outputs.JobDefinitionNodeProperties']]:
        """
        An object with properties that are specific to multi-node parallel jobs. When `nodeProperties` is used in the job definition, it can't be used in addition to `containerProperties` , `ecsProperties` , or `eksProperties` .

        > If the job runs on Fargate resources, don't specify `nodeProperties` . Use `containerProperties` instead.
        """
        return pulumi.get(self, "node_properties")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Default parameters or parameter substitution placeholders that are set in the job definition. Parameters are specified as a key-value pair mapping. Parameters in a `SubmitJob` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see [Job definition parameters](https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html) in the *AWS Batch User Guide* .
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="platformCapabilities")
    def platform_capabilities(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The platform capabilities required by the job definition. If no value is specified, it defaults to `EC2` . Jobs run on Fargate resources specify `FARGATE` .
        """
        return pulumi.get(self, "platform_capabilities")

    @property
    @pulumi.getter(name="propagateTags")
    def propagate_tags(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task. If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the `FAILED` state.
        """
        return pulumi.get(self, "propagate_tags")

    @property
    @pulumi.getter(name="retryStrategy")
    def retry_strategy(self) -> pulumi.Output[Optional['outputs.JobDefinitionRetryStrategy']]:
        """
        The retry strategy to use for failed jobs that are submitted with this job definition.
        """
        return pulumi.get(self, "retry_strategy")

    @property
    @pulumi.getter(name="schedulingPriority")
    def scheduling_priority(self) -> pulumi.Output[Optional[int]]:
        """
        The scheduling priority of the job definition. This only affects jobs in job queues with a fair share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.
        """
        return pulumi.get(self, "scheduling_priority")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A key-value pair to associate with a resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def timeout(self) -> pulumi.Output[Optional['outputs.JobDefinitionJobTimeout']]:
        """
        The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of job definition. For more information about multi-node parallel jobs, see [Creating a multi-node parallel job definition](https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html) in the *AWS Batch User Guide* .

        - If the value is `container` , then one of the following is required: `containerProperties` , `ecsProperties` , or `eksProperties` .
        - If the value is `multinode` , then `nodeProperties` is required.

        > If the job is run on Fargate resources, then `multinode` isn't supported.
        """
        return pulumi.get(self, "type")

