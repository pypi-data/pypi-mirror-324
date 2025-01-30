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
    'GetFargateProfileResult',
    'AwaitableGetFargateProfileResult',
    'get_fargate_profile',
    'get_fargate_profile_output',
]

@pulumi.output_type
class GetFargateProfileResult:
    def __init__(__self__, arn=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the cluster, such as `arn:aws:eks:us-west-2:666666666666:fargateprofile/myCluster/myFargateProfile/1cb1a11a-1dc1-1d11-cf11-1111f11fa111` .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetFargateProfileResult(GetFargateProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFargateProfileResult(
            arn=self.arn,
            tags=self.tags)


def get_fargate_profile(cluster_name: Optional[str] = None,
                        fargate_profile_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFargateProfileResult:
    """
    Resource Schema for AWS::EKS::FargateProfile


    :param str cluster_name: Name of the Cluster
    :param str fargate_profile_name: Name of FargateProfile
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['fargateProfileName'] = fargate_profile_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:eks:getFargateProfile', __args__, opts=opts, typ=GetFargateProfileResult).value

    return AwaitableGetFargateProfileResult(
        arn=pulumi.get(__ret__, 'arn'),
        tags=pulumi.get(__ret__, 'tags'))
def get_fargate_profile_output(cluster_name: Optional[pulumi.Input[str]] = None,
                               fargate_profile_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetFargateProfileResult]:
    """
    Resource Schema for AWS::EKS::FargateProfile


    :param str cluster_name: Name of the Cluster
    :param str fargate_profile_name: Name of FargateProfile
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['fargateProfileName'] = fargate_profile_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:eks:getFargateProfile', __args__, opts=opts, typ=GetFargateProfileResult)
    return __ret__.apply(lambda __response__: GetFargateProfileResult(
        arn=pulumi.get(__response__, 'arn'),
        tags=pulumi.get(__response__, 'tags')))
