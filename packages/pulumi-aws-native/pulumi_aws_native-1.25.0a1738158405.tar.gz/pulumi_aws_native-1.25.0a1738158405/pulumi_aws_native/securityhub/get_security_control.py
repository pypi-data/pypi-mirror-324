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
    'GetSecurityControlResult',
    'AwaitableGetSecurityControlResult',
    'get_security_control',
    'get_security_control_output',
]

@pulumi.output_type
class GetSecurityControlResult:
    def __init__(__self__, last_update_reason=None, parameters=None, security_control_arn=None):
        if last_update_reason and not isinstance(last_update_reason, str):
            raise TypeError("Expected argument 'last_update_reason' to be a str")
        pulumi.set(__self__, "last_update_reason", last_update_reason)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if security_control_arn and not isinstance(security_control_arn, str):
            raise TypeError("Expected argument 'security_control_arn' to be a str")
        pulumi.set(__self__, "security_control_arn", security_control_arn)

    @property
    @pulumi.getter(name="lastUpdateReason")
    def last_update_reason(self) -> Optional[str]:
        """
        The most recent reason for updating the customizable properties of a security control. This differs from the UpdateReason field of the BatchUpdateStandardsControlAssociations API, which tracks the reason for updating the enablement status of a control. This field accepts alphanumeric characters in addition to white spaces, dashes, and underscores.
        """
        return pulumi.get(self, "last_update_reason")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Mapping[str, 'outputs.SecurityControlParameterConfiguration']]:
        """
        An object that identifies the name of a control parameter, its current value, and whether it has been customized.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="securityControlArn")
    def security_control_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for a security control across standards, such as `arn:aws:securityhub:eu-central-1:123456789012:security-control/S3.1`. This parameter doesn't mention a specific standard.
        """
        return pulumi.get(self, "security_control_arn")


class AwaitableGetSecurityControlResult(GetSecurityControlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecurityControlResult(
            last_update_reason=self.last_update_reason,
            parameters=self.parameters,
            security_control_arn=self.security_control_arn)


def get_security_control(security_control_id: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecurityControlResult:
    """
    A security control in Security Hub describes a security best practice related to a specific resource.


    :param str security_control_id: The unique identifier of a security control across standards. Values for this field typically consist of an AWS service name and a number, such as APIGateway.3.
    """
    __args__ = dict()
    __args__['securityControlId'] = security_control_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:securityhub:getSecurityControl', __args__, opts=opts, typ=GetSecurityControlResult).value

    return AwaitableGetSecurityControlResult(
        last_update_reason=pulumi.get(__ret__, 'last_update_reason'),
        parameters=pulumi.get(__ret__, 'parameters'),
        security_control_arn=pulumi.get(__ret__, 'security_control_arn'))
def get_security_control_output(security_control_id: Optional[pulumi.Input[str]] = None,
                                opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSecurityControlResult]:
    """
    A security control in Security Hub describes a security best practice related to a specific resource.


    :param str security_control_id: The unique identifier of a security control across standards. Values for this field typically consist of an AWS service name and a number, such as APIGateway.3.
    """
    __args__ = dict()
    __args__['securityControlId'] = security_control_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:securityhub:getSecurityControl', __args__, opts=opts, typ=GetSecurityControlResult)
    return __ret__.apply(lambda __response__: GetSecurityControlResult(
        last_update_reason=pulumi.get(__response__, 'last_update_reason'),
        parameters=pulumi.get(__response__, 'parameters'),
        security_control_arn=pulumi.get(__response__, 'security_control_arn')))
