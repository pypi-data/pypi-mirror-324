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

__all__ = ['WorkerConfigurationArgs', 'WorkerConfiguration']

@pulumi.input_type
class WorkerConfigurationArgs:
    def __init__(__self__, *,
                 properties_file_content: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a WorkerConfiguration resource.
        :param pulumi.Input[str] properties_file_content: Base64 encoded contents of connect-distributed.properties file.
        :param pulumi.Input[str] description: A summary description of the worker configuration.
        :param pulumi.Input[str] name: The name of the worker configuration.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: A collection of tags associated with a resource
        """
        pulumi.set(__self__, "properties_file_content", properties_file_content)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="propertiesFileContent")
    def properties_file_content(self) -> pulumi.Input[str]:
        """
        Base64 encoded contents of connect-distributed.properties file.
        """
        return pulumi.get(self, "properties_file_content")

    @properties_file_content.setter
    def properties_file_content(self, value: pulumi.Input[str]):
        pulumi.set(self, "properties_file_content", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A summary description of the worker configuration.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the worker configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        A collection of tags associated with a resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class WorkerConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties_file_content: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        The configuration of the workers, which are the processes that run the connector logic.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A summary description of the worker configuration.
        :param pulumi.Input[str] name: The name of the worker configuration.
        :param pulumi.Input[str] properties_file_content: Base64 encoded contents of connect-distributed.properties file.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: A collection of tags associated with a resource
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WorkerConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The configuration of the workers, which are the processes that run the connector logic.

        :param str resource_name: The name of the resource.
        :param WorkerConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkerConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties_file_content: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WorkerConfigurationArgs.__new__(WorkerConfigurationArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            if properties_file_content is None and not opts.urn:
                raise TypeError("Missing required property 'properties_file_content'")
            __props__.__dict__["properties_file_content"] = properties_file_content
            __props__.__dict__["tags"] = tags
            __props__.__dict__["revision"] = None
            __props__.__dict__["worker_configuration_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["description", "name", "propertiesFileContent"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(WorkerConfiguration, __self__).__init__(
            'aws-native:kafkaconnect:WorkerConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WorkerConfiguration':
        """
        Get an existing WorkerConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WorkerConfigurationArgs.__new__(WorkerConfigurationArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties_file_content"] = None
        __props__.__dict__["revision"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["worker_configuration_arn"] = None
        return WorkerConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A summary description of the worker configuration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the worker configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="propertiesFileContent")
    def properties_file_content(self) -> pulumi.Output[str]:
        """
        Base64 encoded contents of connect-distributed.properties file.
        """
        return pulumi.get(self, "properties_file_content")

    @property
    @pulumi.getter
    def revision(self) -> pulumi.Output[int]:
        """
        The description of a revision of the worker configuration.
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        A collection of tags associated with a resource
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="workerConfigurationArn")
    def worker_configuration_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the custom configuration.
        """
        return pulumi.get(self, "worker_configuration_arn")

