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

__all__ = ['ClusterArgs', 'Cluster']

@pulumi.input_type
class ClusterArgs:
    def __init__(__self__, *,
                 instance_groups: pulumi.Input[Sequence[pulumi.Input['ClusterInstanceGroupArgs']]],
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 node_recovery: Optional[pulumi.Input['ClusterNodeRecovery']] = None,
                 orchestrator: Optional[pulumi.Input['ClusterOrchestratorArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 vpc_config: Optional[pulumi.Input['ClusterVpcConfigArgs']] = None):
        """
        The set of arguments for constructing a Cluster resource.
        :param pulumi.Input[Sequence[pulumi.Input['ClusterInstanceGroupArgs']]] instance_groups: The instance groups of the SageMaker HyperPod cluster.
        :param pulumi.Input[str] cluster_name: The name of the HyperPod Cluster.
        :param pulumi.Input['ClusterNodeRecovery'] node_recovery: If node auto-recovery is set to true, faulty nodes will be replaced or rebooted when a failure is detected. If set to false, nodes will be labelled when a fault is detected.
        :param pulumi.Input['ClusterOrchestratorArgs'] orchestrator: The orchestrator type for the SageMaker HyperPod cluster. Currently, `'eks'` is the only available option.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: Custom tags for managing the SageMaker HyperPod cluster as an AWS resource. You can add tags to your cluster in the same way you add them in other AWS services that support tagging.
        :param pulumi.Input['ClusterVpcConfigArgs'] vpc_config: Specifies an Amazon Virtual Private Cloud (VPC) that your SageMaker jobs, hosted models, and compute resources have access to. You can control access to and from your resources by configuring a VPC. For more information, see [Give SageMaker Access to Resources in your Amazon VPC](https://docs.aws.amazon.com/sagemaker/latest/dg/infrastructure-give-access.html) .
        """
        pulumi.set(__self__, "instance_groups", instance_groups)
        if cluster_name is not None:
            pulumi.set(__self__, "cluster_name", cluster_name)
        if node_recovery is not None:
            pulumi.set(__self__, "node_recovery", node_recovery)
        if orchestrator is not None:
            pulumi.set(__self__, "orchestrator", orchestrator)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vpc_config is not None:
            pulumi.set(__self__, "vpc_config", vpc_config)

    @property
    @pulumi.getter(name="instanceGroups")
    def instance_groups(self) -> pulumi.Input[Sequence[pulumi.Input['ClusterInstanceGroupArgs']]]:
        """
        The instance groups of the SageMaker HyperPod cluster.
        """
        return pulumi.get(self, "instance_groups")

    @instance_groups.setter
    def instance_groups(self, value: pulumi.Input[Sequence[pulumi.Input['ClusterInstanceGroupArgs']]]):
        pulumi.set(self, "instance_groups", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the HyperPod Cluster.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter(name="nodeRecovery")
    def node_recovery(self) -> Optional[pulumi.Input['ClusterNodeRecovery']]:
        """
        If node auto-recovery is set to true, faulty nodes will be replaced or rebooted when a failure is detected. If set to false, nodes will be labelled when a fault is detected.
        """
        return pulumi.get(self, "node_recovery")

    @node_recovery.setter
    def node_recovery(self, value: Optional[pulumi.Input['ClusterNodeRecovery']]):
        pulumi.set(self, "node_recovery", value)

    @property
    @pulumi.getter
    def orchestrator(self) -> Optional[pulumi.Input['ClusterOrchestratorArgs']]:
        """
        The orchestrator type for the SageMaker HyperPod cluster. Currently, `'eks'` is the only available option.
        """
        return pulumi.get(self, "orchestrator")

    @orchestrator.setter
    def orchestrator(self, value: Optional[pulumi.Input['ClusterOrchestratorArgs']]):
        pulumi.set(self, "orchestrator", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        Custom tags for managing the SageMaker HyperPod cluster as an AWS resource. You can add tags to your cluster in the same way you add them in other AWS services that support tagging.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> Optional[pulumi.Input['ClusterVpcConfigArgs']]:
        """
        Specifies an Amazon Virtual Private Cloud (VPC) that your SageMaker jobs, hosted models, and compute resources have access to. You can control access to and from your resources by configuring a VPC. For more information, see [Give SageMaker Access to Resources in your Amazon VPC](https://docs.aws.amazon.com/sagemaker/latest/dg/infrastructure-give-access.html) .
        """
        return pulumi.get(self, "vpc_config")

    @vpc_config.setter
    def vpc_config(self, value: Optional[pulumi.Input['ClusterVpcConfigArgs']]):
        pulumi.set(self, "vpc_config", value)


class Cluster(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 instance_groups: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ClusterInstanceGroupArgs', 'ClusterInstanceGroupArgsDict']]]]] = None,
                 node_recovery: Optional[pulumi.Input['ClusterNodeRecovery']] = None,
                 orchestrator: Optional[pulumi.Input[Union['ClusterOrchestratorArgs', 'ClusterOrchestratorArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 vpc_config: Optional[pulumi.Input[Union['ClusterVpcConfigArgs', 'ClusterVpcConfigArgsDict']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::SageMaker::Cluster

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_name: The name of the HyperPod Cluster.
        :param pulumi.Input[Sequence[pulumi.Input[Union['ClusterInstanceGroupArgs', 'ClusterInstanceGroupArgsDict']]]] instance_groups: The instance groups of the SageMaker HyperPod cluster.
        :param pulumi.Input['ClusterNodeRecovery'] node_recovery: If node auto-recovery is set to true, faulty nodes will be replaced or rebooted when a failure is detected. If set to false, nodes will be labelled when a fault is detected.
        :param pulumi.Input[Union['ClusterOrchestratorArgs', 'ClusterOrchestratorArgsDict']] orchestrator: The orchestrator type for the SageMaker HyperPod cluster. Currently, `'eks'` is the only available option.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: Custom tags for managing the SageMaker HyperPod cluster as an AWS resource. You can add tags to your cluster in the same way you add them in other AWS services that support tagging.
        :param pulumi.Input[Union['ClusterVpcConfigArgs', 'ClusterVpcConfigArgsDict']] vpc_config: Specifies an Amazon Virtual Private Cloud (VPC) that your SageMaker jobs, hosted models, and compute resources have access to. You can control access to and from your resources by configuring a VPC. For more information, see [Give SageMaker Access to Resources in your Amazon VPC](https://docs.aws.amazon.com/sagemaker/latest/dg/infrastructure-give-access.html) .
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::SageMaker::Cluster

        :param str resource_name: The name of the resource.
        :param ClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 instance_groups: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ClusterInstanceGroupArgs', 'ClusterInstanceGroupArgsDict']]]]] = None,
                 node_recovery: Optional[pulumi.Input['ClusterNodeRecovery']] = None,
                 orchestrator: Optional[pulumi.Input[Union['ClusterOrchestratorArgs', 'ClusterOrchestratorArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 vpc_config: Optional[pulumi.Input[Union['ClusterVpcConfigArgs', 'ClusterVpcConfigArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterArgs.__new__(ClusterArgs)

            __props__.__dict__["cluster_name"] = cluster_name
            if instance_groups is None and not opts.urn:
                raise TypeError("Missing required property 'instance_groups'")
            __props__.__dict__["instance_groups"] = instance_groups
            __props__.__dict__["node_recovery"] = node_recovery
            __props__.__dict__["orchestrator"] = orchestrator
            __props__.__dict__["tags"] = tags
            __props__.__dict__["vpc_config"] = vpc_config
            __props__.__dict__["cluster_arn"] = None
            __props__.__dict__["cluster_status"] = None
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["failure_message"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["clusterName", "instanceGroups[*].executionRole", "instanceGroups[*].instanceGroupName", "instanceGroups[*].instanceType", "instanceGroups[*].overrideVpcConfig", "instanceGroups[*].threadsPerCore", "orchestrator", "vpcConfig"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Cluster, __self__).__init__(
            'aws-native:sagemaker:Cluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Cluster':
        """
        Get an existing Cluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ClusterArgs.__new__(ClusterArgs)

        __props__.__dict__["cluster_arn"] = None
        __props__.__dict__["cluster_name"] = None
        __props__.__dict__["cluster_status"] = None
        __props__.__dict__["creation_time"] = None
        __props__.__dict__["failure_message"] = None
        __props__.__dict__["instance_groups"] = None
        __props__.__dict__["node_recovery"] = None
        __props__.__dict__["orchestrator"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["vpc_config"] = None
        return Cluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterArn")
    def cluster_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the HyperPod Cluster.
        """
        return pulumi.get(self, "cluster_arn")

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the HyperPod Cluster.
        """
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter(name="clusterStatus")
    def cluster_status(self) -> pulumi.Output['ClusterStatus']:
        """
        The status of the HyperPod Cluster.
        """
        return pulumi.get(self, "cluster_status")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        The time at which the HyperPod cluster was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="failureMessage")
    def failure_message(self) -> pulumi.Output[str]:
        """
        The failure message of the HyperPod Cluster.
        """
        return pulumi.get(self, "failure_message")

    @property
    @pulumi.getter(name="instanceGroups")
    def instance_groups(self) -> pulumi.Output[Sequence['outputs.ClusterInstanceGroup']]:
        """
        The instance groups of the SageMaker HyperPod cluster.
        """
        return pulumi.get(self, "instance_groups")

    @property
    @pulumi.getter(name="nodeRecovery")
    def node_recovery(self) -> pulumi.Output[Optional['ClusterNodeRecovery']]:
        """
        If node auto-recovery is set to true, faulty nodes will be replaced or rebooted when a failure is detected. If set to false, nodes will be labelled when a fault is detected.
        """
        return pulumi.get(self, "node_recovery")

    @property
    @pulumi.getter
    def orchestrator(self) -> pulumi.Output[Optional['outputs.ClusterOrchestrator']]:
        """
        The orchestrator type for the SageMaker HyperPod cluster. Currently, `'eks'` is the only available option.
        """
        return pulumi.get(self, "orchestrator")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        Custom tags for managing the SageMaker HyperPod cluster as an AWS resource. You can add tags to your cluster in the same way you add them in other AWS services that support tagging.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> pulumi.Output[Optional['outputs.ClusterVpcConfig']]:
        """
        Specifies an Amazon Virtual Private Cloud (VPC) that your SageMaker jobs, hosted models, and compute resources have access to. You can control access to and from your resources by configuring a VPC. For more information, see [Give SageMaker Access to Resources in your Amazon VPC](https://docs.aws.amazon.com/sagemaker/latest/dg/infrastructure-give-access.html) .
        """
        return pulumi.get(self, "vpc_config")

