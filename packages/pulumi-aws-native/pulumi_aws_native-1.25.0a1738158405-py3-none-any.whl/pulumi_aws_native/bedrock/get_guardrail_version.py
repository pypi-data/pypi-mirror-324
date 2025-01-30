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
    'GetGuardrailVersionResult',
    'AwaitableGetGuardrailVersionResult',
    'get_guardrail_version',
    'get_guardrail_version_output',
]

@pulumi.output_type
class GetGuardrailVersionResult:
    def __init__(__self__, guardrail_arn=None, guardrail_id=None, version=None):
        if guardrail_arn and not isinstance(guardrail_arn, str):
            raise TypeError("Expected argument 'guardrail_arn' to be a str")
        pulumi.set(__self__, "guardrail_arn", guardrail_arn)
        if guardrail_id and not isinstance(guardrail_id, str):
            raise TypeError("Expected argument 'guardrail_id' to be a str")
        pulumi.set(__self__, "guardrail_id", guardrail_id)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="guardrailArn")
    def guardrail_arn(self) -> Optional[str]:
        """
        Arn representation for the guardrail
        """
        return pulumi.get(self, "guardrail_arn")

    @property
    @pulumi.getter(name="guardrailId")
    def guardrail_id(self) -> Optional[str]:
        """
        Unique id for the guardrail
        """
        return pulumi.get(self, "guardrail_id")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Guardrail version
        """
        return pulumi.get(self, "version")


class AwaitableGetGuardrailVersionResult(GetGuardrailVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGuardrailVersionResult(
            guardrail_arn=self.guardrail_arn,
            guardrail_id=self.guardrail_id,
            version=self.version)


def get_guardrail_version(guardrail_id: Optional[str] = None,
                          version: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGuardrailVersionResult:
    """
    Definition of AWS::Bedrock::GuardrailVersion Resource Type


    :param str guardrail_id: Unique id for the guardrail
    :param str version: Guardrail version
    """
    __args__ = dict()
    __args__['guardrailId'] = guardrail_id
    __args__['version'] = version
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:bedrock:getGuardrailVersion', __args__, opts=opts, typ=GetGuardrailVersionResult).value

    return AwaitableGetGuardrailVersionResult(
        guardrail_arn=pulumi.get(__ret__, 'guardrail_arn'),
        guardrail_id=pulumi.get(__ret__, 'guardrail_id'),
        version=pulumi.get(__ret__, 'version'))
def get_guardrail_version_output(guardrail_id: Optional[pulumi.Input[str]] = None,
                                 version: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetGuardrailVersionResult]:
    """
    Definition of AWS::Bedrock::GuardrailVersion Resource Type


    :param str guardrail_id: Unique id for the guardrail
    :param str version: Guardrail version
    """
    __args__ = dict()
    __args__['guardrailId'] = guardrail_id
    __args__['version'] = version
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:bedrock:getGuardrailVersion', __args__, opts=opts, typ=GetGuardrailVersionResult)
    return __ret__.apply(lambda __response__: GetGuardrailVersionResult(
        guardrail_arn=pulumi.get(__response__, 'guardrail_arn'),
        guardrail_id=pulumi.get(__response__, 'guardrail_id'),
        version=pulumi.get(__response__, 'version')))
