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

__all__ = [
    'GetNetworkInsightsAccessScopeResult',
    'AwaitableGetNetworkInsightsAccessScopeResult',
    'get_network_insights_access_scope',
    'get_network_insights_access_scope_output',
]

@pulumi.output_type
class GetNetworkInsightsAccessScopeResult:
    def __init__(__self__, created_date=None, network_insights_access_scope_arn=None, network_insights_access_scope_id=None, tags=None, updated_date=None):
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if network_insights_access_scope_arn and not isinstance(network_insights_access_scope_arn, str):
            raise TypeError("Expected argument 'network_insights_access_scope_arn' to be a str")
        pulumi.set(__self__, "network_insights_access_scope_arn", network_insights_access_scope_arn)
        if network_insights_access_scope_id and not isinstance(network_insights_access_scope_id, str):
            raise TypeError("Expected argument 'network_insights_access_scope_id' to be a str")
        pulumi.set(__self__, "network_insights_access_scope_id", network_insights_access_scope_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if updated_date and not isinstance(updated_date, str):
            raise TypeError("Expected argument 'updated_date' to be a str")
        pulumi.set(__self__, "updated_date", updated_date)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> Optional[str]:
        """
        The creation date.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="networkInsightsAccessScopeArn")
    def network_insights_access_scope_arn(self) -> Optional[str]:
        """
        The ARN of the Network Access Scope.
        """
        return pulumi.get(self, "network_insights_access_scope_arn")

    @property
    @pulumi.getter(name="networkInsightsAccessScopeId")
    def network_insights_access_scope_id(self) -> Optional[str]:
        """
        The ID of the Network Access Scope.
        """
        return pulumi.get(self, "network_insights_access_scope_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updatedDate")
    def updated_date(self) -> Optional[str]:
        """
        The last updated date.
        """
        return pulumi.get(self, "updated_date")


class AwaitableGetNetworkInsightsAccessScopeResult(GetNetworkInsightsAccessScopeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkInsightsAccessScopeResult(
            created_date=self.created_date,
            network_insights_access_scope_arn=self.network_insights_access_scope_arn,
            network_insights_access_scope_id=self.network_insights_access_scope_id,
            tags=self.tags,
            updated_date=self.updated_date)


def get_network_insights_access_scope(network_insights_access_scope_id: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkInsightsAccessScopeResult:
    """
    Resource schema for AWS::EC2::NetworkInsightsAccessScope


    :param str network_insights_access_scope_id: The ID of the Network Access Scope.
    """
    __args__ = dict()
    __args__['networkInsightsAccessScopeId'] = network_insights_access_scope_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getNetworkInsightsAccessScope', __args__, opts=opts, typ=GetNetworkInsightsAccessScopeResult).value

    return AwaitableGetNetworkInsightsAccessScopeResult(
        created_date=pulumi.get(__ret__, 'created_date'),
        network_insights_access_scope_arn=pulumi.get(__ret__, 'network_insights_access_scope_arn'),
        network_insights_access_scope_id=pulumi.get(__ret__, 'network_insights_access_scope_id'),
        tags=pulumi.get(__ret__, 'tags'),
        updated_date=pulumi.get(__ret__, 'updated_date'))
def get_network_insights_access_scope_output(network_insights_access_scope_id: Optional[pulumi.Input[str]] = None,
                                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetNetworkInsightsAccessScopeResult]:
    """
    Resource schema for AWS::EC2::NetworkInsightsAccessScope


    :param str network_insights_access_scope_id: The ID of the Network Access Scope.
    """
    __args__ = dict()
    __args__['networkInsightsAccessScopeId'] = network_insights_access_scope_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getNetworkInsightsAccessScope', __args__, opts=opts, typ=GetNetworkInsightsAccessScopeResult)
    return __ret__.apply(lambda __response__: GetNetworkInsightsAccessScopeResult(
        created_date=pulumi.get(__response__, 'created_date'),
        network_insights_access_scope_arn=pulumi.get(__response__, 'network_insights_access_scope_arn'),
        network_insights_access_scope_id=pulumi.get(__response__, 'network_insights_access_scope_id'),
        tags=pulumi.get(__response__, 'tags'),
        updated_date=pulumi.get(__response__, 'updated_date')))
