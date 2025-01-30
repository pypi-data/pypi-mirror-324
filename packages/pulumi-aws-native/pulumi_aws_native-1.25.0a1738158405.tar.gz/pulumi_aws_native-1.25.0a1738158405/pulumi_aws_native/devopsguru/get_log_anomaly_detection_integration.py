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

__all__ = [
    'GetLogAnomalyDetectionIntegrationResult',
    'AwaitableGetLogAnomalyDetectionIntegrationResult',
    'get_log_anomaly_detection_integration',
    'get_log_anomaly_detection_integration_output',
]

@pulumi.output_type
class GetLogAnomalyDetectionIntegrationResult:
    def __init__(__self__, account_id=None):
        if account_id and not isinstance(account_id, str):
            raise TypeError("Expected argument 'account_id' to be a str")
        pulumi.set(__self__, "account_id", account_id)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[str]:
        """
        The account ID associated with the integration of DevOps Guru with CloudWatch log groups for log anomaly detection.
        """
        return pulumi.get(self, "account_id")


class AwaitableGetLogAnomalyDetectionIntegrationResult(GetLogAnomalyDetectionIntegrationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLogAnomalyDetectionIntegrationResult(
            account_id=self.account_id)


def get_log_anomaly_detection_integration(account_id: Optional[str] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLogAnomalyDetectionIntegrationResult:
    """
    This resource schema represents the LogAnomalyDetectionIntegration resource in the Amazon DevOps Guru.


    :param str account_id: The account ID associated with the integration of DevOps Guru with CloudWatch log groups for log anomaly detection.
    """
    __args__ = dict()
    __args__['accountId'] = account_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:devopsguru:getLogAnomalyDetectionIntegration', __args__, opts=opts, typ=GetLogAnomalyDetectionIntegrationResult).value

    return AwaitableGetLogAnomalyDetectionIntegrationResult(
        account_id=pulumi.get(__ret__, 'account_id'))
def get_log_anomaly_detection_integration_output(account_id: Optional[pulumi.Input[str]] = None,
                                                 opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetLogAnomalyDetectionIntegrationResult]:
    """
    This resource schema represents the LogAnomalyDetectionIntegration resource in the Amazon DevOps Guru.


    :param str account_id: The account ID associated with the integration of DevOps Guru with CloudWatch log groups for log anomaly detection.
    """
    __args__ = dict()
    __args__['accountId'] = account_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:devopsguru:getLogAnomalyDetectionIntegration', __args__, opts=opts, typ=GetLogAnomalyDetectionIntegrationResult)
    return __ret__.apply(lambda __response__: GetLogAnomalyDetectionIntegrationResult(
        account_id=pulumi.get(__response__, 'account_id')))
