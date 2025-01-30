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
from .. import outputs as _root_outputs
from ._enums import *

__all__ = [
    'GetCapabilityResult',
    'AwaitableGetCapabilityResult',
    'get_capability',
    'get_capability_output',
]

@pulumi.output_type
class GetCapabilityResult:
    def __init__(__self__, capability_arn=None, capability_id=None, configuration=None, created_at=None, instructions_documents=None, modified_at=None, name=None, tags=None):
        if capability_arn and not isinstance(capability_arn, str):
            raise TypeError("Expected argument 'capability_arn' to be a str")
        pulumi.set(__self__, "capability_arn", capability_arn)
        if capability_id and not isinstance(capability_id, str):
            raise TypeError("Expected argument 'capability_id' to be a str")
        pulumi.set(__self__, "capability_id", capability_id)
        if configuration and not isinstance(configuration, dict):
            raise TypeError("Expected argument 'configuration' to be a dict")
        pulumi.set(__self__, "configuration", configuration)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if instructions_documents and not isinstance(instructions_documents, list):
            raise TypeError("Expected argument 'instructions_documents' to be a list")
        pulumi.set(__self__, "instructions_documents", instructions_documents)
        if modified_at and not isinstance(modified_at, str):
            raise TypeError("Expected argument 'modified_at' to be a str")
        pulumi.set(__self__, "modified_at", modified_at)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="capabilityArn")
    def capability_arn(self) -> Optional[str]:
        """
        Returns an Amazon Resource Name (ARN) for a specific AWS resource, such as a capability, partnership, profile, or transformer.
        """
        return pulumi.get(self, "capability_arn")

    @property
    @pulumi.getter(name="capabilityId")
    def capability_id(self) -> Optional[str]:
        """
        Returns a system-assigned unique identifier for the capability.
        """
        return pulumi.get(self, "capability_id")

    @property
    @pulumi.getter
    def configuration(self) -> Optional['outputs.CapabilityConfigurationProperties']:
        """
        Specifies a structure that contains the details for a capability.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        Returns a timestamp for creation date and time of the capability.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="instructionsDocuments")
    def instructions_documents(self) -> Optional[Sequence['outputs.CapabilityS3Location']]:
        """
        Specifies one or more locations in Amazon S3, each specifying an EDI document that can be used with this capability. Each item contains the name of the bucket and the key, to identify the document's location.
        """
        return pulumi.get(self, "instructions_documents")

    @property
    @pulumi.getter(name="modifiedAt")
    def modified_at(self) -> Optional[str]:
        """
        Returns a timestamp that identifies the most recent date and time that the capability was modified.
        """
        return pulumi.get(self, "modified_at")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The display name of the capability.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Specifies the key-value pairs assigned to ARNs that you can use to group and search for resources by type. You can attach this metadata to resources (capabilities, partnerships, and so on) for any purpose.
        """
        return pulumi.get(self, "tags")


class AwaitableGetCapabilityResult(GetCapabilityResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCapabilityResult(
            capability_arn=self.capability_arn,
            capability_id=self.capability_id,
            configuration=self.configuration,
            created_at=self.created_at,
            instructions_documents=self.instructions_documents,
            modified_at=self.modified_at,
            name=self.name,
            tags=self.tags)


def get_capability(capability_id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCapabilityResult:
    """
    Definition of AWS::B2BI::Capability Resource Type


    :param str capability_id: Returns a system-assigned unique identifier for the capability.
    """
    __args__ = dict()
    __args__['capabilityId'] = capability_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:b2bi:getCapability', __args__, opts=opts, typ=GetCapabilityResult).value

    return AwaitableGetCapabilityResult(
        capability_arn=pulumi.get(__ret__, 'capability_arn'),
        capability_id=pulumi.get(__ret__, 'capability_id'),
        configuration=pulumi.get(__ret__, 'configuration'),
        created_at=pulumi.get(__ret__, 'created_at'),
        instructions_documents=pulumi.get(__ret__, 'instructions_documents'),
        modified_at=pulumi.get(__ret__, 'modified_at'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_capability_output(capability_id: Optional[pulumi.Input[str]] = None,
                          opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetCapabilityResult]:
    """
    Definition of AWS::B2BI::Capability Resource Type


    :param str capability_id: Returns a system-assigned unique identifier for the capability.
    """
    __args__ = dict()
    __args__['capabilityId'] = capability_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:b2bi:getCapability', __args__, opts=opts, typ=GetCapabilityResult)
    return __ret__.apply(lambda __response__: GetCapabilityResult(
        capability_arn=pulumi.get(__response__, 'capability_arn'),
        capability_id=pulumi.get(__response__, 'capability_id'),
        configuration=pulumi.get(__response__, 'configuration'),
        created_at=pulumi.get(__response__, 'created_at'),
        instructions_documents=pulumi.get(__response__, 'instructions_documents'),
        modified_at=pulumi.get(__response__, 'modified_at'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags')))
