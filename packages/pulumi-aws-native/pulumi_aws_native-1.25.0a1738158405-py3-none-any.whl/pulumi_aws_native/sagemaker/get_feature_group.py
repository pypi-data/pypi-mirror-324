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
    'GetFeatureGroupResult',
    'AwaitableGetFeatureGroupResult',
    'get_feature_group',
    'get_feature_group_output',
]

@pulumi.output_type
class GetFeatureGroupResult:
    def __init__(__self__, creation_time=None, feature_definitions=None, feature_group_status=None, online_store_config=None, throughput_config=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if feature_definitions and not isinstance(feature_definitions, list):
            raise TypeError("Expected argument 'feature_definitions' to be a list")
        pulumi.set(__self__, "feature_definitions", feature_definitions)
        if feature_group_status and not isinstance(feature_group_status, str):
            raise TypeError("Expected argument 'feature_group_status' to be a str")
        pulumi.set(__self__, "feature_group_status", feature_group_status)
        if online_store_config and not isinstance(online_store_config, dict):
            raise TypeError("Expected argument 'online_store_config' to be a dict")
        pulumi.set(__self__, "online_store_config", online_store_config)
        if throughput_config and not isinstance(throughput_config, dict):
            raise TypeError("Expected argument 'throughput_config' to be a dict")
        pulumi.set(__self__, "throughput_config", throughput_config)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        A timestamp of FeatureGroup creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="featureDefinitions")
    def feature_definitions(self) -> Optional[Sequence['outputs.FeatureGroupFeatureDefinition']]:
        """
        An Array of Feature Definition
        """
        return pulumi.get(self, "feature_definitions")

    @property
    @pulumi.getter(name="featureGroupStatus")
    def feature_group_status(self) -> Optional[str]:
        """
        The status of the feature group.
        """
        return pulumi.get(self, "feature_group_status")

    @property
    @pulumi.getter(name="onlineStoreConfig")
    def online_store_config(self) -> Optional['outputs.OnlineStoreConfigProperties']:
        """
        The configuration of an `OnlineStore` .
        """
        return pulumi.get(self, "online_store_config")

    @property
    @pulumi.getter(name="throughputConfig")
    def throughput_config(self) -> Optional['outputs.FeatureGroupThroughputConfig']:
        """
        Used to set feature group throughput configuration. There are two modes: `ON_DEMAND` and `PROVISIONED` . With on-demand mode, you are charged for data reads and writes that your application performs on your feature group. You do not need to specify read and write throughput because Feature Store accommodates your workloads as they ramp up and down. You can switch a feature group to on-demand only once in a 24 hour period. With provisioned throughput mode, you specify the read and write capacity per second that you expect your application to require, and you are billed based on those limits. Exceeding provisioned throughput will result in your requests being throttled.

        Note: `PROVISIONED` throughput mode is supported only for feature groups that are offline-only, or use the [`Standard`](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_OnlineStoreConfig.html#sagemaker-Type-OnlineStoreConfig-StorageType) tier online store.
        """
        return pulumi.get(self, "throughput_config")


class AwaitableGetFeatureGroupResult(GetFeatureGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFeatureGroupResult(
            creation_time=self.creation_time,
            feature_definitions=self.feature_definitions,
            feature_group_status=self.feature_group_status,
            online_store_config=self.online_store_config,
            throughput_config=self.throughput_config)


def get_feature_group(feature_group_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFeatureGroupResult:
    """
    Resource Type definition for AWS::SageMaker::FeatureGroup


    :param str feature_group_name: The Name of the FeatureGroup.
    """
    __args__ = dict()
    __args__['featureGroupName'] = feature_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:sagemaker:getFeatureGroup', __args__, opts=opts, typ=GetFeatureGroupResult).value

    return AwaitableGetFeatureGroupResult(
        creation_time=pulumi.get(__ret__, 'creation_time'),
        feature_definitions=pulumi.get(__ret__, 'feature_definitions'),
        feature_group_status=pulumi.get(__ret__, 'feature_group_status'),
        online_store_config=pulumi.get(__ret__, 'online_store_config'),
        throughput_config=pulumi.get(__ret__, 'throughput_config'))
def get_feature_group_output(feature_group_name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetFeatureGroupResult]:
    """
    Resource Type definition for AWS::SageMaker::FeatureGroup


    :param str feature_group_name: The Name of the FeatureGroup.
    """
    __args__ = dict()
    __args__['featureGroupName'] = feature_group_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:sagemaker:getFeatureGroup', __args__, opts=opts, typ=GetFeatureGroupResult)
    return __ret__.apply(lambda __response__: GetFeatureGroupResult(
        creation_time=pulumi.get(__response__, 'creation_time'),
        feature_definitions=pulumi.get(__response__, 'feature_definitions'),
        feature_group_status=pulumi.get(__response__, 'feature_group_status'),
        online_store_config=pulumi.get(__response__, 'online_store_config'),
        throughput_config=pulumi.get(__response__, 'throughput_config')))
