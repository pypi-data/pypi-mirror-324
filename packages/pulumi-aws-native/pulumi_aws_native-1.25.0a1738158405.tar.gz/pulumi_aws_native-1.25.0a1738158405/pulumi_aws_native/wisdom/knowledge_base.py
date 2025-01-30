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

__all__ = ['KnowledgeBaseArgs', 'KnowledgeBase']

@pulumi.input_type
class KnowledgeBaseArgs:
    def __init__(__self__, *,
                 knowledge_base_type: pulumi.Input['KnowledgeBaseType'],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rendering_configuration: Optional[pulumi.Input['KnowledgeBaseRenderingConfigurationArgs']] = None,
                 server_side_encryption_configuration: Optional[pulumi.Input['KnowledgeBaseServerSideEncryptionConfigurationArgs']] = None,
                 source_configuration: Optional[pulumi.Input[Union['KnowledgeBaseSourceConfiguration0PropertiesArgs', 'KnowledgeBaseSourceConfiguration1PropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.CreateOnlyTagArgs']]]] = None,
                 vector_ingestion_configuration: Optional[pulumi.Input['KnowledgeBaseVectorIngestionConfigurationArgs']] = None):
        """
        The set of arguments for constructing a KnowledgeBase resource.
        :param pulumi.Input['KnowledgeBaseType'] knowledge_base_type: The type of knowledge base. Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.
        :param pulumi.Input[str] description: The description.
        :param pulumi.Input[str] name: The name of the knowledge base.
        :param pulumi.Input['KnowledgeBaseRenderingConfigurationArgs'] rendering_configuration: Information about how to render the content.
        :param pulumi.Input['KnowledgeBaseServerSideEncryptionConfigurationArgs'] server_side_encryption_configuration: This customer managed key must have a policy that allows `kms:CreateGrant` and `kms:DescribeKey` permissions to the IAM identity using the key to invoke Wisdom. For more information about setting up a customer managed key for Wisdom, see [Enable Amazon Connect Wisdom for your instance](https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html) . For information about valid ID values, see [Key identifiers (KeyId)](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id) in the *AWS Key Management Service Developer Guide* .
        :param pulumi.Input[Union['KnowledgeBaseSourceConfiguration0PropertiesArgs', 'KnowledgeBaseSourceConfiguration1PropertiesArgs']] source_configuration: The source of the knowledge base content. Only set this argument for EXTERNAL or Managed knowledge bases.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.CreateOnlyTagArgs']]] tags: The tags used to organize, track, or control access for this resource.
        :param pulumi.Input['KnowledgeBaseVectorIngestionConfigurationArgs'] vector_ingestion_configuration: Contains details about how to ingest the documents in a data source.
        """
        pulumi.set(__self__, "knowledge_base_type", knowledge_base_type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if rendering_configuration is not None:
            pulumi.set(__self__, "rendering_configuration", rendering_configuration)
        if server_side_encryption_configuration is not None:
            pulumi.set(__self__, "server_side_encryption_configuration", server_side_encryption_configuration)
        if source_configuration is not None:
            pulumi.set(__self__, "source_configuration", source_configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vector_ingestion_configuration is not None:
            pulumi.set(__self__, "vector_ingestion_configuration", vector_ingestion_configuration)

    @property
    @pulumi.getter(name="knowledgeBaseType")
    def knowledge_base_type(self) -> pulumi.Input['KnowledgeBaseType']:
        """
        The type of knowledge base. Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.
        """
        return pulumi.get(self, "knowledge_base_type")

    @knowledge_base_type.setter
    def knowledge_base_type(self, value: pulumi.Input['KnowledgeBaseType']):
        pulumi.set(self, "knowledge_base_type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the knowledge base.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="renderingConfiguration")
    def rendering_configuration(self) -> Optional[pulumi.Input['KnowledgeBaseRenderingConfigurationArgs']]:
        """
        Information about how to render the content.
        """
        return pulumi.get(self, "rendering_configuration")

    @rendering_configuration.setter
    def rendering_configuration(self, value: Optional[pulumi.Input['KnowledgeBaseRenderingConfigurationArgs']]):
        pulumi.set(self, "rendering_configuration", value)

    @property
    @pulumi.getter(name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(self) -> Optional[pulumi.Input['KnowledgeBaseServerSideEncryptionConfigurationArgs']]:
        """
        This customer managed key must have a policy that allows `kms:CreateGrant` and `kms:DescribeKey` permissions to the IAM identity using the key to invoke Wisdom. For more information about setting up a customer managed key for Wisdom, see [Enable Amazon Connect Wisdom for your instance](https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html) . For information about valid ID values, see [Key identifiers (KeyId)](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id) in the *AWS Key Management Service Developer Guide* .
        """
        return pulumi.get(self, "server_side_encryption_configuration")

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(self, value: Optional[pulumi.Input['KnowledgeBaseServerSideEncryptionConfigurationArgs']]):
        pulumi.set(self, "server_side_encryption_configuration", value)

    @property
    @pulumi.getter(name="sourceConfiguration")
    def source_configuration(self) -> Optional[pulumi.Input[Union['KnowledgeBaseSourceConfiguration0PropertiesArgs', 'KnowledgeBaseSourceConfiguration1PropertiesArgs']]]:
        """
        The source of the knowledge base content. Only set this argument for EXTERNAL or Managed knowledge bases.
        """
        return pulumi.get(self, "source_configuration")

    @source_configuration.setter
    def source_configuration(self, value: Optional[pulumi.Input[Union['KnowledgeBaseSourceConfiguration0PropertiesArgs', 'KnowledgeBaseSourceConfiguration1PropertiesArgs']]]):
        pulumi.set(self, "source_configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.CreateOnlyTagArgs']]]]:
        """
        The tags used to organize, track, or control access for this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.CreateOnlyTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vectorIngestionConfiguration")
    def vector_ingestion_configuration(self) -> Optional[pulumi.Input['KnowledgeBaseVectorIngestionConfigurationArgs']]:
        """
        Contains details about how to ingest the documents in a data source.
        """
        return pulumi.get(self, "vector_ingestion_configuration")

    @vector_ingestion_configuration.setter
    def vector_ingestion_configuration(self, value: Optional[pulumi.Input['KnowledgeBaseVectorIngestionConfigurationArgs']]):
        pulumi.set(self, "vector_ingestion_configuration", value)


class KnowledgeBase(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 knowledge_base_type: Optional[pulumi.Input['KnowledgeBaseType']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rendering_configuration: Optional[pulumi.Input[Union['KnowledgeBaseRenderingConfigurationArgs', 'KnowledgeBaseRenderingConfigurationArgsDict']]] = None,
                 server_side_encryption_configuration: Optional[pulumi.Input[Union['KnowledgeBaseServerSideEncryptionConfigurationArgs', 'KnowledgeBaseServerSideEncryptionConfigurationArgsDict']]] = None,
                 source_configuration: Optional[pulumi.Input[Union[Union['KnowledgeBaseSourceConfiguration0PropertiesArgs', 'KnowledgeBaseSourceConfiguration0PropertiesArgsDict'], Union['KnowledgeBaseSourceConfiguration1PropertiesArgs', 'KnowledgeBaseSourceConfiguration1PropertiesArgsDict']]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.CreateOnlyTagArgs', '_root_inputs.CreateOnlyTagArgsDict']]]]] = None,
                 vector_ingestion_configuration: Optional[pulumi.Input[Union['KnowledgeBaseVectorIngestionConfigurationArgs', 'KnowledgeBaseVectorIngestionConfigurationArgsDict']]] = None,
                 __props__=None):
        """
        Definition of AWS::Wisdom::KnowledgeBase Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description.
        :param pulumi.Input['KnowledgeBaseType'] knowledge_base_type: The type of knowledge base. Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.
        :param pulumi.Input[str] name: The name of the knowledge base.
        :param pulumi.Input[Union['KnowledgeBaseRenderingConfigurationArgs', 'KnowledgeBaseRenderingConfigurationArgsDict']] rendering_configuration: Information about how to render the content.
        :param pulumi.Input[Union['KnowledgeBaseServerSideEncryptionConfigurationArgs', 'KnowledgeBaseServerSideEncryptionConfigurationArgsDict']] server_side_encryption_configuration: This customer managed key must have a policy that allows `kms:CreateGrant` and `kms:DescribeKey` permissions to the IAM identity using the key to invoke Wisdom. For more information about setting up a customer managed key for Wisdom, see [Enable Amazon Connect Wisdom for your instance](https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html) . For information about valid ID values, see [Key identifiers (KeyId)](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id) in the *AWS Key Management Service Developer Guide* .
        :param pulumi.Input[Union[Union['KnowledgeBaseSourceConfiguration0PropertiesArgs', 'KnowledgeBaseSourceConfiguration0PropertiesArgsDict'], Union['KnowledgeBaseSourceConfiguration1PropertiesArgs', 'KnowledgeBaseSourceConfiguration1PropertiesArgsDict']]] source_configuration: The source of the knowledge base content. Only set this argument for EXTERNAL or Managed knowledge bases.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.CreateOnlyTagArgs', '_root_inputs.CreateOnlyTagArgsDict']]]] tags: The tags used to organize, track, or control access for this resource.
        :param pulumi.Input[Union['KnowledgeBaseVectorIngestionConfigurationArgs', 'KnowledgeBaseVectorIngestionConfigurationArgsDict']] vector_ingestion_configuration: Contains details about how to ingest the documents in a data source.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KnowledgeBaseArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::Wisdom::KnowledgeBase Resource Type

        :param str resource_name: The name of the resource.
        :param KnowledgeBaseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KnowledgeBaseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 knowledge_base_type: Optional[pulumi.Input['KnowledgeBaseType']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rendering_configuration: Optional[pulumi.Input[Union['KnowledgeBaseRenderingConfigurationArgs', 'KnowledgeBaseRenderingConfigurationArgsDict']]] = None,
                 server_side_encryption_configuration: Optional[pulumi.Input[Union['KnowledgeBaseServerSideEncryptionConfigurationArgs', 'KnowledgeBaseServerSideEncryptionConfigurationArgsDict']]] = None,
                 source_configuration: Optional[pulumi.Input[Union[Union['KnowledgeBaseSourceConfiguration0PropertiesArgs', 'KnowledgeBaseSourceConfiguration0PropertiesArgsDict'], Union['KnowledgeBaseSourceConfiguration1PropertiesArgs', 'KnowledgeBaseSourceConfiguration1PropertiesArgsDict']]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.CreateOnlyTagArgs', '_root_inputs.CreateOnlyTagArgsDict']]]]] = None,
                 vector_ingestion_configuration: Optional[pulumi.Input[Union['KnowledgeBaseVectorIngestionConfigurationArgs', 'KnowledgeBaseVectorIngestionConfigurationArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KnowledgeBaseArgs.__new__(KnowledgeBaseArgs)

            __props__.__dict__["description"] = description
            if knowledge_base_type is None and not opts.urn:
                raise TypeError("Missing required property 'knowledge_base_type'")
            __props__.__dict__["knowledge_base_type"] = knowledge_base_type
            __props__.__dict__["name"] = name
            __props__.__dict__["rendering_configuration"] = rendering_configuration
            __props__.__dict__["server_side_encryption_configuration"] = server_side_encryption_configuration
            __props__.__dict__["source_configuration"] = source_configuration
            __props__.__dict__["tags"] = tags
            __props__.__dict__["vector_ingestion_configuration"] = vector_ingestion_configuration
            __props__.__dict__["knowledge_base_arn"] = None
            __props__.__dict__["knowledge_base_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["description", "knowledgeBaseType", "name", "serverSideEncryptionConfiguration", "sourceConfiguration", "tags[*]"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(KnowledgeBase, __self__).__init__(
            'aws-native:wisdom:KnowledgeBase',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'KnowledgeBase':
        """
        Get an existing KnowledgeBase resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = KnowledgeBaseArgs.__new__(KnowledgeBaseArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["knowledge_base_arn"] = None
        __props__.__dict__["knowledge_base_id"] = None
        __props__.__dict__["knowledge_base_type"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["rendering_configuration"] = None
        __props__.__dict__["server_side_encryption_configuration"] = None
        __props__.__dict__["source_configuration"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["vector_ingestion_configuration"] = None
        return KnowledgeBase(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the knowledge base.
        """
        return pulumi.get(self, "knowledge_base_arn")

    @property
    @pulumi.getter(name="knowledgeBaseId")
    def knowledge_base_id(self) -> pulumi.Output[str]:
        """
        The ID of the knowledge base.
        """
        return pulumi.get(self, "knowledge_base_id")

    @property
    @pulumi.getter(name="knowledgeBaseType")
    def knowledge_base_type(self) -> pulumi.Output['KnowledgeBaseType']:
        """
        The type of knowledge base. Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.
        """
        return pulumi.get(self, "knowledge_base_type")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the knowledge base.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="renderingConfiguration")
    def rendering_configuration(self) -> pulumi.Output[Optional['outputs.KnowledgeBaseRenderingConfiguration']]:
        """
        Information about how to render the content.
        """
        return pulumi.get(self, "rendering_configuration")

    @property
    @pulumi.getter(name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(self) -> pulumi.Output[Optional['outputs.KnowledgeBaseServerSideEncryptionConfiguration']]:
        """
        This customer managed key must have a policy that allows `kms:CreateGrant` and `kms:DescribeKey` permissions to the IAM identity using the key to invoke Wisdom. For more information about setting up a customer managed key for Wisdom, see [Enable Amazon Connect Wisdom for your instance](https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html) . For information about valid ID values, see [Key identifiers (KeyId)](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id) in the *AWS Key Management Service Developer Guide* .
        """
        return pulumi.get(self, "server_side_encryption_configuration")

    @property
    @pulumi.getter(name="sourceConfiguration")
    def source_configuration(self) -> pulumi.Output[Optional[Any]]:
        """
        The source of the knowledge base content. Only set this argument for EXTERNAL or Managed knowledge bases.
        """
        return pulumi.get(self, "source_configuration")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.CreateOnlyTag']]]:
        """
        The tags used to organize, track, or control access for this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vectorIngestionConfiguration")
    def vector_ingestion_configuration(self) -> pulumi.Output[Optional['outputs.KnowledgeBaseVectorIngestionConfiguration']]:
        """
        Contains details about how to ingest the documents in a data source.
        """
        return pulumi.get(self, "vector_ingestion_configuration")

