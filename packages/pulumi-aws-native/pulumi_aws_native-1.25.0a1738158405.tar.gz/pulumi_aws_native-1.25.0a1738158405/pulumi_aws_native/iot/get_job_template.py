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
    'GetJobTemplateResult',
    'AwaitableGetJobTemplateResult',
    'get_job_template',
    'get_job_template_output',
]

@pulumi.output_type
class GetJobTemplateResult:
    def __init__(__self__, arn=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the job to use as the basis for the job template.
        """
        return pulumi.get(self, "arn")


class AwaitableGetJobTemplateResult(GetJobTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetJobTemplateResult(
            arn=self.arn)


def get_job_template(job_template_id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetJobTemplateResult:
    """
    Job templates enable you to preconfigure jobs so that you can deploy them to multiple sets of target devices.


    :param str job_template_id: A unique identifier for the job template. We recommend using a UUID. Alpha-numeric characters, "-", and "_" are valid for use here.
    """
    __args__ = dict()
    __args__['jobTemplateId'] = job_template_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iot:getJobTemplate', __args__, opts=opts, typ=GetJobTemplateResult).value

    return AwaitableGetJobTemplateResult(
        arn=pulumi.get(__ret__, 'arn'))
def get_job_template_output(job_template_id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetJobTemplateResult]:
    """
    Job templates enable you to preconfigure jobs so that you can deploy them to multiple sets of target devices.


    :param str job_template_id: A unique identifier for the job template. We recommend using a UUID. Alpha-numeric characters, "-", and "_" are valid for use here.
    """
    __args__ = dict()
    __args__['jobTemplateId'] = job_template_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iot:getJobTemplate', __args__, opts=opts, typ=GetJobTemplateResult)
    return __ret__.apply(lambda __response__: GetJobTemplateResult(
        arn=pulumi.get(__response__, 'arn')))
