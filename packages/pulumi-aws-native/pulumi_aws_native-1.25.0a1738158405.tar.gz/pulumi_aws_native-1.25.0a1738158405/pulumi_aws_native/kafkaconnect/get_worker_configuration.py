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
    'GetWorkerConfigurationResult',
    'AwaitableGetWorkerConfigurationResult',
    'get_worker_configuration',
    'get_worker_configuration_output',
]

@pulumi.output_type
class GetWorkerConfigurationResult:
    def __init__(__self__, revision=None, tags=None, worker_configuration_arn=None):
        if revision and not isinstance(revision, int):
            raise TypeError("Expected argument 'revision' to be a int")
        pulumi.set(__self__, "revision", revision)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if worker_configuration_arn and not isinstance(worker_configuration_arn, str):
            raise TypeError("Expected argument 'worker_configuration_arn' to be a str")
        pulumi.set(__self__, "worker_configuration_arn", worker_configuration_arn)

    @property
    @pulumi.getter
    def revision(self) -> Optional[int]:
        """
        The description of a revision of the worker configuration.
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A collection of tags associated with a resource
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="workerConfigurationArn")
    def worker_configuration_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the custom configuration.
        """
        return pulumi.get(self, "worker_configuration_arn")


class AwaitableGetWorkerConfigurationResult(GetWorkerConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkerConfigurationResult(
            revision=self.revision,
            tags=self.tags,
            worker_configuration_arn=self.worker_configuration_arn)


def get_worker_configuration(worker_configuration_arn: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkerConfigurationResult:
    """
    The configuration of the workers, which are the processes that run the connector logic.


    :param str worker_configuration_arn: The Amazon Resource Name (ARN) of the custom configuration.
    """
    __args__ = dict()
    __args__['workerConfigurationArn'] = worker_configuration_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:kafkaconnect:getWorkerConfiguration', __args__, opts=opts, typ=GetWorkerConfigurationResult).value

    return AwaitableGetWorkerConfigurationResult(
        revision=pulumi.get(__ret__, 'revision'),
        tags=pulumi.get(__ret__, 'tags'),
        worker_configuration_arn=pulumi.get(__ret__, 'worker_configuration_arn'))
def get_worker_configuration_output(worker_configuration_arn: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetWorkerConfigurationResult]:
    """
    The configuration of the workers, which are the processes that run the connector logic.


    :param str worker_configuration_arn: The Amazon Resource Name (ARN) of the custom configuration.
    """
    __args__ = dict()
    __args__['workerConfigurationArn'] = worker_configuration_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:kafkaconnect:getWorkerConfiguration', __args__, opts=opts, typ=GetWorkerConfigurationResult)
    return __ret__.apply(lambda __response__: GetWorkerConfigurationResult(
        revision=pulumi.get(__response__, 'revision'),
        tags=pulumi.get(__response__, 'tags'),
        worker_configuration_arn=pulumi.get(__response__, 'worker_configuration_arn')))
