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
    'GetMultiRegionAccessPointPolicyResult',
    'AwaitableGetMultiRegionAccessPointPolicyResult',
    'get_multi_region_access_point_policy',
    'get_multi_region_access_point_policy_output',
]

@pulumi.output_type
class GetMultiRegionAccessPointPolicyResult:
    def __init__(__self__, policy=None, policy_status=None):
        if policy and not isinstance(policy, dict):
            raise TypeError("Expected argument 'policy' to be a dict")
        pulumi.set(__self__, "policy", policy)
        if policy_status and not isinstance(policy_status, dict):
            raise TypeError("Expected argument 'policy_status' to be a dict")
        pulumi.set(__self__, "policy_status", policy_status)

    @property
    @pulumi.getter
    def policy(self) -> Optional[Any]:
        """
        Policy document to apply to a Multi Region Access Point

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::S3::MultiRegionAccessPointPolicy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="policyStatus")
    def policy_status(self) -> Optional['outputs.PolicyStatusProperties']:
        """
        The Policy Status associated with this Multi Region Access Point
        """
        return pulumi.get(self, "policy_status")


class AwaitableGetMultiRegionAccessPointPolicyResult(GetMultiRegionAccessPointPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMultiRegionAccessPointPolicyResult(
            policy=self.policy,
            policy_status=self.policy_status)


def get_multi_region_access_point_policy(mrap_name: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMultiRegionAccessPointPolicyResult:
    """
    The policy to be attached to a Multi Region Access Point


    :param str mrap_name: The name of the Multi Region Access Point to apply policy
    """
    __args__ = dict()
    __args__['mrapName'] = mrap_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:s3:getMultiRegionAccessPointPolicy', __args__, opts=opts, typ=GetMultiRegionAccessPointPolicyResult).value

    return AwaitableGetMultiRegionAccessPointPolicyResult(
        policy=pulumi.get(__ret__, 'policy'),
        policy_status=pulumi.get(__ret__, 'policy_status'))
def get_multi_region_access_point_policy_output(mrap_name: Optional[pulumi.Input[str]] = None,
                                                opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetMultiRegionAccessPointPolicyResult]:
    """
    The policy to be attached to a Multi Region Access Point


    :param str mrap_name: The name of the Multi Region Access Point to apply policy
    """
    __args__ = dict()
    __args__['mrapName'] = mrap_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:s3:getMultiRegionAccessPointPolicy', __args__, opts=opts, typ=GetMultiRegionAccessPointPolicyResult)
    return __ret__.apply(lambda __response__: GetMultiRegionAccessPointPolicyResult(
        policy=pulumi.get(__response__, 'policy'),
        policy_status=pulumi.get(__response__, 'policy_status')))
