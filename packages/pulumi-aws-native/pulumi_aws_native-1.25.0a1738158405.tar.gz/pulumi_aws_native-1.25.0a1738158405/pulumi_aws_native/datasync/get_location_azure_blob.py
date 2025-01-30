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
from .. import outputs as _root_outputs
from ._enums import *

__all__ = [
    'GetLocationAzureBlobResult',
    'AwaitableGetLocationAzureBlobResult',
    'get_location_azure_blob',
    'get_location_azure_blob_output',
]

@pulumi.output_type
class GetLocationAzureBlobResult:
    def __init__(__self__, agent_arns=None, azure_access_tier=None, azure_blob_authentication_type=None, azure_blob_type=None, location_arn=None, location_uri=None, tags=None):
        if agent_arns and not isinstance(agent_arns, list):
            raise TypeError("Expected argument 'agent_arns' to be a list")
        pulumi.set(__self__, "agent_arns", agent_arns)
        if azure_access_tier and not isinstance(azure_access_tier, str):
            raise TypeError("Expected argument 'azure_access_tier' to be a str")
        pulumi.set(__self__, "azure_access_tier", azure_access_tier)
        if azure_blob_authentication_type and not isinstance(azure_blob_authentication_type, str):
            raise TypeError("Expected argument 'azure_blob_authentication_type' to be a str")
        pulumi.set(__self__, "azure_blob_authentication_type", azure_blob_authentication_type)
        if azure_blob_type and not isinstance(azure_blob_type, str):
            raise TypeError("Expected argument 'azure_blob_type' to be a str")
        pulumi.set(__self__, "azure_blob_type", azure_blob_type)
        if location_arn and not isinstance(location_arn, str):
            raise TypeError("Expected argument 'location_arn' to be a str")
        pulumi.set(__self__, "location_arn", location_arn)
        if location_uri and not isinstance(location_uri, str):
            raise TypeError("Expected argument 'location_uri' to be a str")
        pulumi.set(__self__, "location_uri", location_uri)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="agentArns")
    def agent_arns(self) -> Optional[Sequence[str]]:
        """
        The Amazon Resource Names (ARNs) of agents to use for an Azure Blob Location.
        """
        return pulumi.get(self, "agent_arns")

    @property
    @pulumi.getter(name="azureAccessTier")
    def azure_access_tier(self) -> Optional['LocationAzureBlobAzureAccessTier']:
        """
        Specifies an access tier for the objects you're transferring into your Azure Blob Storage container.
        """
        return pulumi.get(self, "azure_access_tier")

    @property
    @pulumi.getter(name="azureBlobAuthenticationType")
    def azure_blob_authentication_type(self) -> Optional['LocationAzureBlobAzureBlobAuthenticationType']:
        """
        The specific authentication type that you want DataSync to use to access your Azure Blob Container.
        """
        return pulumi.get(self, "azure_blob_authentication_type")

    @property
    @pulumi.getter(name="azureBlobType")
    def azure_blob_type(self) -> Optional['LocationAzureBlobAzureBlobType']:
        """
        Specifies a blob type for the objects you're transferring into your Azure Blob Storage container.
        """
        return pulumi.get(self, "azure_blob_type")

    @property
    @pulumi.getter(name="locationArn")
    def location_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the Azure Blob Location that is created.
        """
        return pulumi.get(self, "location_arn")

    @property
    @pulumi.getter(name="locationUri")
    def location_uri(self) -> Optional[str]:
        """
        The URL of the Azure Blob Location that was described.
        """
        return pulumi.get(self, "location_uri")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetLocationAzureBlobResult(GetLocationAzureBlobResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLocationAzureBlobResult(
            agent_arns=self.agent_arns,
            azure_access_tier=self.azure_access_tier,
            azure_blob_authentication_type=self.azure_blob_authentication_type,
            azure_blob_type=self.azure_blob_type,
            location_arn=self.location_arn,
            location_uri=self.location_uri,
            tags=self.tags)


def get_location_azure_blob(location_arn: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLocationAzureBlobResult:
    """
    Resource schema for AWS::DataSync::LocationAzureBlob.


    :param str location_arn: The Amazon Resource Name (ARN) of the Azure Blob Location that is created.
    """
    __args__ = dict()
    __args__['locationArn'] = location_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:datasync:getLocationAzureBlob', __args__, opts=opts, typ=GetLocationAzureBlobResult).value

    return AwaitableGetLocationAzureBlobResult(
        agent_arns=pulumi.get(__ret__, 'agent_arns'),
        azure_access_tier=pulumi.get(__ret__, 'azure_access_tier'),
        azure_blob_authentication_type=pulumi.get(__ret__, 'azure_blob_authentication_type'),
        azure_blob_type=pulumi.get(__ret__, 'azure_blob_type'),
        location_arn=pulumi.get(__ret__, 'location_arn'),
        location_uri=pulumi.get(__ret__, 'location_uri'),
        tags=pulumi.get(__ret__, 'tags'))
def get_location_azure_blob_output(location_arn: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetLocationAzureBlobResult]:
    """
    Resource schema for AWS::DataSync::LocationAzureBlob.


    :param str location_arn: The Amazon Resource Name (ARN) of the Azure Blob Location that is created.
    """
    __args__ = dict()
    __args__['locationArn'] = location_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:datasync:getLocationAzureBlob', __args__, opts=opts, typ=GetLocationAzureBlobResult)
    return __ret__.apply(lambda __response__: GetLocationAzureBlobResult(
        agent_arns=pulumi.get(__response__, 'agent_arns'),
        azure_access_tier=pulumi.get(__response__, 'azure_access_tier'),
        azure_blob_authentication_type=pulumi.get(__response__, 'azure_blob_authentication_type'),
        azure_blob_type=pulumi.get(__response__, 'azure_blob_type'),
        location_arn=pulumi.get(__response__, 'location_arn'),
        location_uri=pulumi.get(__response__, 'location_uri'),
        tags=pulumi.get(__response__, 'tags')))
