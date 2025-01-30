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
    'GetBatchScramSecretResult',
    'AwaitableGetBatchScramSecretResult',
    'get_batch_scram_secret',
    'get_batch_scram_secret_output',
]

@pulumi.output_type
class GetBatchScramSecretResult:
    def __init__(__self__, secret_arn_list=None):
        if secret_arn_list and not isinstance(secret_arn_list, list):
            raise TypeError("Expected argument 'secret_arn_list' to be a list")
        pulumi.set(__self__, "secret_arn_list", secret_arn_list)

    @property
    @pulumi.getter(name="secretArnList")
    def secret_arn_list(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "secret_arn_list")


class AwaitableGetBatchScramSecretResult(GetBatchScramSecretResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBatchScramSecretResult(
            secret_arn_list=self.secret_arn_list)


def get_batch_scram_secret(cluster_arn: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBatchScramSecretResult:
    """
    Resource Type definition for AWS::MSK::BatchScramSecret
    """
    __args__ = dict()
    __args__['clusterArn'] = cluster_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:msk:getBatchScramSecret', __args__, opts=opts, typ=GetBatchScramSecretResult).value

    return AwaitableGetBatchScramSecretResult(
        secret_arn_list=pulumi.get(__ret__, 'secret_arn_list'))
def get_batch_scram_secret_output(cluster_arn: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetBatchScramSecretResult]:
    """
    Resource Type definition for AWS::MSK::BatchScramSecret
    """
    __args__ = dict()
    __args__['clusterArn'] = cluster_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:msk:getBatchScramSecret', __args__, opts=opts, typ=GetBatchScramSecretResult)
    return __ret__.apply(lambda __response__: GetBatchScramSecretResult(
        secret_arn_list=pulumi.get(__response__, 'secret_arn_list')))
