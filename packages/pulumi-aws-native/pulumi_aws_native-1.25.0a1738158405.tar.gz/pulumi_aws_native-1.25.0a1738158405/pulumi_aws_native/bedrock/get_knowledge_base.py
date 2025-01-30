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
from ._enums import *

__all__ = [
    'GetKnowledgeBaseResult',
    'AwaitableGetKnowledgeBaseResult',
    'get_knowledge_base',
    'get_knowledge_base_output',
]

@pulumi.output_type
class GetKnowledgeBaseResult:
    def __init__(__self__, created_at=None, description=None, failure_reasons=None, knowledge_base_arn=None, knowledge_base_configuration=None, knowledge_base_id=None, name=None, role_arn=None, status=None, tags=None, updated_at=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if failure_reasons and not isinstance(failure_reasons, list):
            raise TypeError("Expected argument 'failure_reasons' to be a list")
        pulumi.set(__self__, "failure_reasons", failure_reasons)
        if knowledge_base_arn and not isinstance(knowledge_base_arn, str):
            raise TypeError("Expected argument 'knowledge_base_arn' to be a str")
        pulumi.set(__self__, "knowledge_base_arn", knowledge_base_arn)
        if knowledge_base_configuration and not isinstance(knowledge_base_configuration, dict):
            raise TypeError("Expected argument 'knowledge_base_configuration' to be a dict")
        pulumi.set(__self__, "knowledge_base_configuration", knowledge_base_configuration)
        if knowledge_base_id and not isinstance(knowledge_base_id, str):
            raise TypeError("Expected argument 'knowledge_base_id' to be a str")
        pulumi.set(__self__, "knowledge_base_id", knowledge_base_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The time at which the knowledge base was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the Resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="failureReasons")
    def failure_reasons(self) -> Optional[Sequence[str]]:
        """
        A list of reasons that the API operation on the knowledge base failed.
        """
        return pulumi.get(self, "failure_reasons")

    @property
    @pulumi.getter(name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> Optional[str]:
        """
        The ARN of the knowledge base.
        """
        return pulumi.get(self, "knowledge_base_arn")

    @property
    @pulumi.getter(name="knowledgeBaseConfiguration")
    def knowledge_base_configuration(self) -> Optional['outputs.KnowledgeBaseConfiguration']:
        """
        Contains details about the embeddings configuration of the knowledge base.
        """
        return pulumi.get(self, "knowledge_base_configuration")

    @property
    @pulumi.getter(name="knowledgeBaseId")
    def knowledge_base_id(self) -> Optional[str]:
        """
        The unique identifier of the knowledge base.
        """
        return pulumi.get(self, "knowledge_base_id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the knowledge base.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        The ARN of the IAM role with permissions to invoke API operations on the knowledge base. The ARN must begin with AmazonBedrockExecutionRoleForKnowledgeBase_
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def status(self) -> Optional['KnowledgeBaseStatus']:
        """
        The status of the knowledge base.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:

        - [Tag naming limits and requirements](https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions)
        - [Tagging best practices](https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices)
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[str]:
        """
        The time at which the knowledge base was last updated.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetKnowledgeBaseResult(GetKnowledgeBaseResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKnowledgeBaseResult(
            created_at=self.created_at,
            description=self.description,
            failure_reasons=self.failure_reasons,
            knowledge_base_arn=self.knowledge_base_arn,
            knowledge_base_configuration=self.knowledge_base_configuration,
            knowledge_base_id=self.knowledge_base_id,
            name=self.name,
            role_arn=self.role_arn,
            status=self.status,
            tags=self.tags,
            updated_at=self.updated_at)


def get_knowledge_base(knowledge_base_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetKnowledgeBaseResult:
    """
    Definition of AWS::Bedrock::KnowledgeBase Resource Type


    :param str knowledge_base_id: The unique identifier of the knowledge base.
    """
    __args__ = dict()
    __args__['knowledgeBaseId'] = knowledge_base_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:bedrock:getKnowledgeBase', __args__, opts=opts, typ=GetKnowledgeBaseResult).value

    return AwaitableGetKnowledgeBaseResult(
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        failure_reasons=pulumi.get(__ret__, 'failure_reasons'),
        knowledge_base_arn=pulumi.get(__ret__, 'knowledge_base_arn'),
        knowledge_base_configuration=pulumi.get(__ret__, 'knowledge_base_configuration'),
        knowledge_base_id=pulumi.get(__ret__, 'knowledge_base_id'),
        name=pulumi.get(__ret__, 'name'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'),
        updated_at=pulumi.get(__ret__, 'updated_at'))
def get_knowledge_base_output(knowledge_base_id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetKnowledgeBaseResult]:
    """
    Definition of AWS::Bedrock::KnowledgeBase Resource Type


    :param str knowledge_base_id: The unique identifier of the knowledge base.
    """
    __args__ = dict()
    __args__['knowledgeBaseId'] = knowledge_base_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:bedrock:getKnowledgeBase', __args__, opts=opts, typ=GetKnowledgeBaseResult)
    return __ret__.apply(lambda __response__: GetKnowledgeBaseResult(
        created_at=pulumi.get(__response__, 'created_at'),
        description=pulumi.get(__response__, 'description'),
        failure_reasons=pulumi.get(__response__, 'failure_reasons'),
        knowledge_base_arn=pulumi.get(__response__, 'knowledge_base_arn'),
        knowledge_base_configuration=pulumi.get(__response__, 'knowledge_base_configuration'),
        knowledge_base_id=pulumi.get(__response__, 'knowledge_base_id'),
        name=pulumi.get(__response__, 'name'),
        role_arn=pulumi.get(__response__, 'role_arn'),
        status=pulumi.get(__response__, 'status'),
        tags=pulumi.get(__response__, 'tags'),
        updated_at=pulumi.get(__response__, 'updated_at')))
