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

__all__ = ['ConfigurationArgs', 'Configuration']

@pulumi.input_type
class ConfigurationArgs:
    def __init__(__self__, *,
                 engine_type: pulumi.Input[str],
                 authentication_strategy: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 engine_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Configuration resource.
        :param pulumi.Input[str] engine_type: The type of broker engine. Note: Currently, Amazon MQ only supports ACTIVEMQ for creating and editing broker configurations.
        :param pulumi.Input[str] authentication_strategy: The authentication strategy associated with the configuration. The default is SIMPLE.
        :param pulumi.Input[str] data: The base64-encoded XML configuration.
        :param pulumi.Input[str] description: The description of the configuration.
        :param pulumi.Input[str] engine_version: The version of the broker engine.
        :param pulumi.Input[str] name: The name of the configuration.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: Create tags when creating the configuration.
        """
        pulumi.set(__self__, "engine_type", engine_type)
        if authentication_strategy is not None:
            pulumi.set(__self__, "authentication_strategy", authentication_strategy)
        if data is not None:
            pulumi.set(__self__, "data", data)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if engine_version is not None:
            pulumi.set(__self__, "engine_version", engine_version)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="engineType")
    def engine_type(self) -> pulumi.Input[str]:
        """
        The type of broker engine. Note: Currently, Amazon MQ only supports ACTIVEMQ for creating and editing broker configurations.
        """
        return pulumi.get(self, "engine_type")

    @engine_type.setter
    def engine_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "engine_type", value)

    @property
    @pulumi.getter(name="authenticationStrategy")
    def authentication_strategy(self) -> Optional[pulumi.Input[str]]:
        """
        The authentication strategy associated with the configuration. The default is SIMPLE.
        """
        return pulumi.get(self, "authentication_strategy")

    @authentication_strategy.setter
    def authentication_strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication_strategy", value)

    @property
    @pulumi.getter
    def data(self) -> Optional[pulumi.Input[str]]:
        """
        The base64-encoded XML configuration.
        """
        return pulumi.get(self, "data")

    @data.setter
    def data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the configuration.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the broker engine.
        """
        return pulumi.get(self, "engine_version")

    @engine_version.setter
    def engine_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "engine_version", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        Create tags when creating the configuration.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Configuration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_strategy: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 engine_type: Optional[pulumi.Input[str]] = None,
                 engine_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::AmazonMQ::Configuration

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import base64
        import pulumi_aws_native as aws_native

        configuration = aws_native.amazonmq.Configuration("configuration",
            data=base64.b64encode(\"\"\"<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <broker xmlns="http://activemq.apache.org/schema/core" start="false">
          <destinationPolicy>
            <policyMap>
              <policyEntries>
                <policyEntry topic=">">
                  <pendingMessageLimitStrategy>
                    <constantPendingMessageLimitStrategy limit="3000"/>
                  </pendingMessageLimitStrategy>
                </policyEntry>
              </policyEntries>
            </policyMap>
          </destinationPolicy>
          <plugins>
          </plugins>
        </broker>
        \"\"\".encode()).decode(),
            engine_type="ACTIVEMQ",
            engine_version="5.15.0",
            name="my-configuration-1")

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication_strategy: The authentication strategy associated with the configuration. The default is SIMPLE.
        :param pulumi.Input[str] data: The base64-encoded XML configuration.
        :param pulumi.Input[str] description: The description of the configuration.
        :param pulumi.Input[str] engine_type: The type of broker engine. Note: Currently, Amazon MQ only supports ACTIVEMQ for creating and editing broker configurations.
        :param pulumi.Input[str] engine_version: The version of the broker engine.
        :param pulumi.Input[str] name: The name of the configuration.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: Create tags when creating the configuration.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::AmazonMQ::Configuration

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import base64
        import pulumi_aws_native as aws_native

        configuration = aws_native.amazonmq.Configuration("configuration",
            data=base64.b64encode(\"\"\"<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <broker xmlns="http://activemq.apache.org/schema/core" start="false">
          <destinationPolicy>
            <policyMap>
              <policyEntries>
                <policyEntry topic=">">
                  <pendingMessageLimitStrategy>
                    <constantPendingMessageLimitStrategy limit="3000"/>
                  </pendingMessageLimitStrategy>
                </policyEntry>
              </policyEntries>
            </policyMap>
          </destinationPolicy>
          <plugins>
          </plugins>
        </broker>
        \"\"\".encode()).decode(),
            engine_type="ACTIVEMQ",
            engine_version="5.15.0",
            name="my-configuration-1")

        ```

        :param str resource_name: The name of the resource.
        :param ConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_strategy: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 engine_type: Optional[pulumi.Input[str]] = None,
                 engine_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConfigurationArgs.__new__(ConfigurationArgs)

            __props__.__dict__["authentication_strategy"] = authentication_strategy
            __props__.__dict__["data"] = data
            __props__.__dict__["description"] = description
            if engine_type is None and not opts.urn:
                raise TypeError("Missing required property 'engine_type'")
            __props__.__dict__["engine_type"] = engine_type
            __props__.__dict__["engine_version"] = engine_version
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["aws_id"] = None
            __props__.__dict__["revision"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["authenticationStrategy", "engineType", "engineVersion", "name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Configuration, __self__).__init__(
            'aws-native:amazonmq:Configuration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Configuration':
        """
        Get an existing Configuration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConfigurationArgs.__new__(ConfigurationArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["authentication_strategy"] = None
        __props__.__dict__["aws_id"] = None
        __props__.__dict__["data"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["engine_type"] = None
        __props__.__dict__["engine_version"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["revision"] = None
        __props__.__dict__["tags"] = None
        return Configuration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the Amazon MQ configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="authenticationStrategy")
    def authentication_strategy(self) -> pulumi.Output[Optional[str]]:
        """
        The authentication strategy associated with the configuration. The default is SIMPLE.
        """
        return pulumi.get(self, "authentication_strategy")

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The ID of the Amazon MQ configuration.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter
    def data(self) -> pulumi.Output[Optional[str]]:
        """
        The base64-encoded XML configuration.
        """
        return pulumi.get(self, "data")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the configuration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="engineType")
    def engine_type(self) -> pulumi.Output[str]:
        """
        The type of broker engine. Note: Currently, Amazon MQ only supports ACTIVEMQ for creating and editing broker configurations.
        """
        return pulumi.get(self, "engine_type")

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> pulumi.Output[Optional[str]]:
        """
        The version of the broker engine.
        """
        return pulumi.get(self, "engine_version")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def revision(self) -> pulumi.Output[str]:
        """
        The revision number of the configuration.
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        Create tags when creating the configuration.
        """
        return pulumi.get(self, "tags")

