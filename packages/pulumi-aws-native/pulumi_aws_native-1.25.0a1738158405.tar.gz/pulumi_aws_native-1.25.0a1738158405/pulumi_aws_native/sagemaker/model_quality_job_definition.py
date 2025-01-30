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

__all__ = ['ModelQualityJobDefinitionArgs', 'ModelQualityJobDefinition']

@pulumi.input_type
class ModelQualityJobDefinitionArgs:
    def __init__(__self__, *,
                 job_resources: pulumi.Input['ModelQualityJobDefinitionMonitoringResourcesArgs'],
                 model_quality_app_specification: pulumi.Input['ModelQualityJobDefinitionModelQualityAppSpecificationArgs'],
                 model_quality_job_input: pulumi.Input['ModelQualityJobDefinitionModelQualityJobInputArgs'],
                 model_quality_job_output_config: pulumi.Input['ModelQualityJobDefinitionMonitoringOutputConfigArgs'],
                 role_arn: pulumi.Input[str],
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 job_definition_name: Optional[pulumi.Input[str]] = None,
                 model_quality_baseline_config: Optional[pulumi.Input['ModelQualityJobDefinitionModelQualityBaselineConfigArgs']] = None,
                 network_config: Optional[pulumi.Input['ModelQualityJobDefinitionNetworkConfigArgs']] = None,
                 stopping_condition: Optional[pulumi.Input['ModelQualityJobDefinitionStoppingConditionArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.CreateOnlyTagArgs']]]] = None):
        """
        The set of arguments for constructing a ModelQualityJobDefinition resource.
        :param pulumi.Input['ModelQualityJobDefinitionMonitoringResourcesArgs'] job_resources: Identifies the resources to deploy for a monitoring job.
        :param pulumi.Input['ModelQualityJobDefinitionModelQualityAppSpecificationArgs'] model_quality_app_specification: Container image configuration object for the monitoring job.
        :param pulumi.Input['ModelQualityJobDefinitionModelQualityJobInputArgs'] model_quality_job_input: A list of the inputs that are monitored. Currently endpoints are supported.
        :param pulumi.Input['ModelQualityJobDefinitionMonitoringOutputConfigArgs'] model_quality_job_output_config: The output configuration for monitoring jobs.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can assume to perform tasks on your behalf.
        :param pulumi.Input[str] job_definition_name: The name of the monitoring job definition.
        :param pulumi.Input['ModelQualityJobDefinitionModelQualityBaselineConfigArgs'] model_quality_baseline_config: Specifies the constraints and baselines for the monitoring job.
        :param pulumi.Input['ModelQualityJobDefinitionNetworkConfigArgs'] network_config: Specifies the network configuration for the monitoring job.
        :param pulumi.Input['ModelQualityJobDefinitionStoppingConditionArgs'] stopping_condition: A time limit for how long the monitoring job is allowed to run before stopping.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.CreateOnlyTagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "job_resources", job_resources)
        pulumi.set(__self__, "model_quality_app_specification", model_quality_app_specification)
        pulumi.set(__self__, "model_quality_job_input", model_quality_job_input)
        pulumi.set(__self__, "model_quality_job_output_config", model_quality_job_output_config)
        pulumi.set(__self__, "role_arn", role_arn)
        if endpoint_name is not None:
            pulumi.set(__self__, "endpoint_name", endpoint_name)
        if job_definition_name is not None:
            pulumi.set(__self__, "job_definition_name", job_definition_name)
        if model_quality_baseline_config is not None:
            pulumi.set(__self__, "model_quality_baseline_config", model_quality_baseline_config)
        if network_config is not None:
            pulumi.set(__self__, "network_config", network_config)
        if stopping_condition is not None:
            pulumi.set(__self__, "stopping_condition", stopping_condition)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="jobResources")
    def job_resources(self) -> pulumi.Input['ModelQualityJobDefinitionMonitoringResourcesArgs']:
        """
        Identifies the resources to deploy for a monitoring job.
        """
        return pulumi.get(self, "job_resources")

    @job_resources.setter
    def job_resources(self, value: pulumi.Input['ModelQualityJobDefinitionMonitoringResourcesArgs']):
        pulumi.set(self, "job_resources", value)

    @property
    @pulumi.getter(name="modelQualityAppSpecification")
    def model_quality_app_specification(self) -> pulumi.Input['ModelQualityJobDefinitionModelQualityAppSpecificationArgs']:
        """
        Container image configuration object for the monitoring job.
        """
        return pulumi.get(self, "model_quality_app_specification")

    @model_quality_app_specification.setter
    def model_quality_app_specification(self, value: pulumi.Input['ModelQualityJobDefinitionModelQualityAppSpecificationArgs']):
        pulumi.set(self, "model_quality_app_specification", value)

    @property
    @pulumi.getter(name="modelQualityJobInput")
    def model_quality_job_input(self) -> pulumi.Input['ModelQualityJobDefinitionModelQualityJobInputArgs']:
        """
        A list of the inputs that are monitored. Currently endpoints are supported.
        """
        return pulumi.get(self, "model_quality_job_input")

    @model_quality_job_input.setter
    def model_quality_job_input(self, value: pulumi.Input['ModelQualityJobDefinitionModelQualityJobInputArgs']):
        pulumi.set(self, "model_quality_job_input", value)

    @property
    @pulumi.getter(name="modelQualityJobOutputConfig")
    def model_quality_job_output_config(self) -> pulumi.Input['ModelQualityJobDefinitionMonitoringOutputConfigArgs']:
        """
        The output configuration for monitoring jobs.
        """
        return pulumi.get(self, "model_quality_job_output_config")

    @model_quality_job_output_config.setter
    def model_quality_job_output_config(self, value: pulumi.Input['ModelQualityJobDefinitionMonitoringOutputConfigArgs']):
        pulumi.set(self, "model_quality_job_output_config", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can assume to perform tasks on your behalf.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="endpointName")
    def endpoint_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "endpoint_name")

    @endpoint_name.setter
    def endpoint_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_name", value)

    @property
    @pulumi.getter(name="jobDefinitionName")
    def job_definition_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the monitoring job definition.
        """
        return pulumi.get(self, "job_definition_name")

    @job_definition_name.setter
    def job_definition_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "job_definition_name", value)

    @property
    @pulumi.getter(name="modelQualityBaselineConfig")
    def model_quality_baseline_config(self) -> Optional[pulumi.Input['ModelQualityJobDefinitionModelQualityBaselineConfigArgs']]:
        """
        Specifies the constraints and baselines for the monitoring job.
        """
        return pulumi.get(self, "model_quality_baseline_config")

    @model_quality_baseline_config.setter
    def model_quality_baseline_config(self, value: Optional[pulumi.Input['ModelQualityJobDefinitionModelQualityBaselineConfigArgs']]):
        pulumi.set(self, "model_quality_baseline_config", value)

    @property
    @pulumi.getter(name="networkConfig")
    def network_config(self) -> Optional[pulumi.Input['ModelQualityJobDefinitionNetworkConfigArgs']]:
        """
        Specifies the network configuration for the monitoring job.
        """
        return pulumi.get(self, "network_config")

    @network_config.setter
    def network_config(self, value: Optional[pulumi.Input['ModelQualityJobDefinitionNetworkConfigArgs']]):
        pulumi.set(self, "network_config", value)

    @property
    @pulumi.getter(name="stoppingCondition")
    def stopping_condition(self) -> Optional[pulumi.Input['ModelQualityJobDefinitionStoppingConditionArgs']]:
        """
        A time limit for how long the monitoring job is allowed to run before stopping.
        """
        return pulumi.get(self, "stopping_condition")

    @stopping_condition.setter
    def stopping_condition(self, value: Optional[pulumi.Input['ModelQualityJobDefinitionStoppingConditionArgs']]):
        pulumi.set(self, "stopping_condition", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.CreateOnlyTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.CreateOnlyTagArgs']]]]):
        pulumi.set(self, "tags", value)


class ModelQualityJobDefinition(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 job_definition_name: Optional[pulumi.Input[str]] = None,
                 job_resources: Optional[pulumi.Input[Union['ModelQualityJobDefinitionMonitoringResourcesArgs', 'ModelQualityJobDefinitionMonitoringResourcesArgsDict']]] = None,
                 model_quality_app_specification: Optional[pulumi.Input[Union['ModelQualityJobDefinitionModelQualityAppSpecificationArgs', 'ModelQualityJobDefinitionModelQualityAppSpecificationArgsDict']]] = None,
                 model_quality_baseline_config: Optional[pulumi.Input[Union['ModelQualityJobDefinitionModelQualityBaselineConfigArgs', 'ModelQualityJobDefinitionModelQualityBaselineConfigArgsDict']]] = None,
                 model_quality_job_input: Optional[pulumi.Input[Union['ModelQualityJobDefinitionModelQualityJobInputArgs', 'ModelQualityJobDefinitionModelQualityJobInputArgsDict']]] = None,
                 model_quality_job_output_config: Optional[pulumi.Input[Union['ModelQualityJobDefinitionMonitoringOutputConfigArgs', 'ModelQualityJobDefinitionMonitoringOutputConfigArgsDict']]] = None,
                 network_config: Optional[pulumi.Input[Union['ModelQualityJobDefinitionNetworkConfigArgs', 'ModelQualityJobDefinitionNetworkConfigArgsDict']]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 stopping_condition: Optional[pulumi.Input[Union['ModelQualityJobDefinitionStoppingConditionArgs', 'ModelQualityJobDefinitionStoppingConditionArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.CreateOnlyTagArgs', '_root_inputs.CreateOnlyTagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::SageMaker::ModelQualityJobDefinition

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] job_definition_name: The name of the monitoring job definition.
        :param pulumi.Input[Union['ModelQualityJobDefinitionMonitoringResourcesArgs', 'ModelQualityJobDefinitionMonitoringResourcesArgsDict']] job_resources: Identifies the resources to deploy for a monitoring job.
        :param pulumi.Input[Union['ModelQualityJobDefinitionModelQualityAppSpecificationArgs', 'ModelQualityJobDefinitionModelQualityAppSpecificationArgsDict']] model_quality_app_specification: Container image configuration object for the monitoring job.
        :param pulumi.Input[Union['ModelQualityJobDefinitionModelQualityBaselineConfigArgs', 'ModelQualityJobDefinitionModelQualityBaselineConfigArgsDict']] model_quality_baseline_config: Specifies the constraints and baselines for the monitoring job.
        :param pulumi.Input[Union['ModelQualityJobDefinitionModelQualityJobInputArgs', 'ModelQualityJobDefinitionModelQualityJobInputArgsDict']] model_quality_job_input: A list of the inputs that are monitored. Currently endpoints are supported.
        :param pulumi.Input[Union['ModelQualityJobDefinitionMonitoringOutputConfigArgs', 'ModelQualityJobDefinitionMonitoringOutputConfigArgsDict']] model_quality_job_output_config: The output configuration for monitoring jobs.
        :param pulumi.Input[Union['ModelQualityJobDefinitionNetworkConfigArgs', 'ModelQualityJobDefinitionNetworkConfigArgsDict']] network_config: Specifies the network configuration for the monitoring job.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can assume to perform tasks on your behalf.
        :param pulumi.Input[Union['ModelQualityJobDefinitionStoppingConditionArgs', 'ModelQualityJobDefinitionStoppingConditionArgsDict']] stopping_condition: A time limit for how long the monitoring job is allowed to run before stopping.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.CreateOnlyTagArgs', '_root_inputs.CreateOnlyTagArgsDict']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ModelQualityJobDefinitionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::SageMaker::ModelQualityJobDefinition

        :param str resource_name: The name of the resource.
        :param ModelQualityJobDefinitionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ModelQualityJobDefinitionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 job_definition_name: Optional[pulumi.Input[str]] = None,
                 job_resources: Optional[pulumi.Input[Union['ModelQualityJobDefinitionMonitoringResourcesArgs', 'ModelQualityJobDefinitionMonitoringResourcesArgsDict']]] = None,
                 model_quality_app_specification: Optional[pulumi.Input[Union['ModelQualityJobDefinitionModelQualityAppSpecificationArgs', 'ModelQualityJobDefinitionModelQualityAppSpecificationArgsDict']]] = None,
                 model_quality_baseline_config: Optional[pulumi.Input[Union['ModelQualityJobDefinitionModelQualityBaselineConfigArgs', 'ModelQualityJobDefinitionModelQualityBaselineConfigArgsDict']]] = None,
                 model_quality_job_input: Optional[pulumi.Input[Union['ModelQualityJobDefinitionModelQualityJobInputArgs', 'ModelQualityJobDefinitionModelQualityJobInputArgsDict']]] = None,
                 model_quality_job_output_config: Optional[pulumi.Input[Union['ModelQualityJobDefinitionMonitoringOutputConfigArgs', 'ModelQualityJobDefinitionMonitoringOutputConfigArgsDict']]] = None,
                 network_config: Optional[pulumi.Input[Union['ModelQualityJobDefinitionNetworkConfigArgs', 'ModelQualityJobDefinitionNetworkConfigArgsDict']]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 stopping_condition: Optional[pulumi.Input[Union['ModelQualityJobDefinitionStoppingConditionArgs', 'ModelQualityJobDefinitionStoppingConditionArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.CreateOnlyTagArgs', '_root_inputs.CreateOnlyTagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ModelQualityJobDefinitionArgs.__new__(ModelQualityJobDefinitionArgs)

            __props__.__dict__["endpoint_name"] = endpoint_name
            __props__.__dict__["job_definition_name"] = job_definition_name
            if job_resources is None and not opts.urn:
                raise TypeError("Missing required property 'job_resources'")
            __props__.__dict__["job_resources"] = job_resources
            if model_quality_app_specification is None and not opts.urn:
                raise TypeError("Missing required property 'model_quality_app_specification'")
            __props__.__dict__["model_quality_app_specification"] = model_quality_app_specification
            __props__.__dict__["model_quality_baseline_config"] = model_quality_baseline_config
            if model_quality_job_input is None and not opts.urn:
                raise TypeError("Missing required property 'model_quality_job_input'")
            __props__.__dict__["model_quality_job_input"] = model_quality_job_input
            if model_quality_job_output_config is None and not opts.urn:
                raise TypeError("Missing required property 'model_quality_job_output_config'")
            __props__.__dict__["model_quality_job_output_config"] = model_quality_job_output_config
            __props__.__dict__["network_config"] = network_config
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["stopping_condition"] = stopping_condition
            __props__.__dict__["tags"] = tags
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["job_definition_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["endpointName", "jobDefinitionName", "jobResources", "modelQualityAppSpecification", "modelQualityBaselineConfig", "modelQualityJobInput", "modelQualityJobOutputConfig", "networkConfig", "roleArn", "stoppingCondition", "tags[*]"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ModelQualityJobDefinition, __self__).__init__(
            'aws-native:sagemaker:ModelQualityJobDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ModelQualityJobDefinition':
        """
        Get an existing ModelQualityJobDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ModelQualityJobDefinitionArgs.__new__(ModelQualityJobDefinitionArgs)

        __props__.__dict__["creation_time"] = None
        __props__.__dict__["endpoint_name"] = None
        __props__.__dict__["job_definition_arn"] = None
        __props__.__dict__["job_definition_name"] = None
        __props__.__dict__["job_resources"] = None
        __props__.__dict__["model_quality_app_specification"] = None
        __props__.__dict__["model_quality_baseline_config"] = None
        __props__.__dict__["model_quality_job_input"] = None
        __props__.__dict__["model_quality_job_output_config"] = None
        __props__.__dict__["network_config"] = None
        __props__.__dict__["role_arn"] = None
        __props__.__dict__["stopping_condition"] = None
        __props__.__dict__["tags"] = None
        return ModelQualityJobDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        The time at which the job definition was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="endpointName")
    def endpoint_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "endpoint_name")

    @property
    @pulumi.getter(name="jobDefinitionArn")
    def job_definition_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of job definition.
        """
        return pulumi.get(self, "job_definition_arn")

    @property
    @pulumi.getter(name="jobDefinitionName")
    def job_definition_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the monitoring job definition.
        """
        return pulumi.get(self, "job_definition_name")

    @property
    @pulumi.getter(name="jobResources")
    def job_resources(self) -> pulumi.Output['outputs.ModelQualityJobDefinitionMonitoringResources']:
        """
        Identifies the resources to deploy for a monitoring job.
        """
        return pulumi.get(self, "job_resources")

    @property
    @pulumi.getter(name="modelQualityAppSpecification")
    def model_quality_app_specification(self) -> pulumi.Output['outputs.ModelQualityJobDefinitionModelQualityAppSpecification']:
        """
        Container image configuration object for the monitoring job.
        """
        return pulumi.get(self, "model_quality_app_specification")

    @property
    @pulumi.getter(name="modelQualityBaselineConfig")
    def model_quality_baseline_config(self) -> pulumi.Output[Optional['outputs.ModelQualityJobDefinitionModelQualityBaselineConfig']]:
        """
        Specifies the constraints and baselines for the monitoring job.
        """
        return pulumi.get(self, "model_quality_baseline_config")

    @property
    @pulumi.getter(name="modelQualityJobInput")
    def model_quality_job_input(self) -> pulumi.Output['outputs.ModelQualityJobDefinitionModelQualityJobInput']:
        """
        A list of the inputs that are monitored. Currently endpoints are supported.
        """
        return pulumi.get(self, "model_quality_job_input")

    @property
    @pulumi.getter(name="modelQualityJobOutputConfig")
    def model_quality_job_output_config(self) -> pulumi.Output['outputs.ModelQualityJobDefinitionMonitoringOutputConfig']:
        """
        The output configuration for monitoring jobs.
        """
        return pulumi.get(self, "model_quality_job_output_config")

    @property
    @pulumi.getter(name="networkConfig")
    def network_config(self) -> pulumi.Output[Optional['outputs.ModelQualityJobDefinitionNetworkConfig']]:
        """
        Specifies the network configuration for the monitoring job.
        """
        return pulumi.get(self, "network_config")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can assume to perform tasks on your behalf.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="stoppingCondition")
    def stopping_condition(self) -> pulumi.Output[Optional['outputs.ModelQualityJobDefinitionStoppingCondition']]:
        """
        A time limit for how long the monitoring job is allowed to run before stopping.
        """
        return pulumi.get(self, "stopping_condition")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.CreateOnlyTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

