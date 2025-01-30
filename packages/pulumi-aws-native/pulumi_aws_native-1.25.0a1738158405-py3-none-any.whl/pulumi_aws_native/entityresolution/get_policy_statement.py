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
from ._enums import *

__all__ = [
    'GetPolicyStatementResult',
    'AwaitableGetPolicyStatementResult',
    'get_policy_statement',
    'get_policy_statement_output',
]

@pulumi.output_type
class GetPolicyStatementResult:
    def __init__(__self__, action=None, condition=None, effect=None, principal=None):
        if action and not isinstance(action, list):
            raise TypeError("Expected argument 'action' to be a list")
        pulumi.set(__self__, "action", action)
        if condition and not isinstance(condition, str):
            raise TypeError("Expected argument 'condition' to be a str")
        pulumi.set(__self__, "condition", condition)
        if effect and not isinstance(effect, str):
            raise TypeError("Expected argument 'effect' to be a str")
        pulumi.set(__self__, "effect", effect)
        if principal and not isinstance(principal, list):
            raise TypeError("Expected argument 'principal' to be a list")
        pulumi.set(__self__, "principal", principal)

    @property
    @pulumi.getter
    def action(self) -> Optional[Sequence[str]]:
        """
        The action that the principal can use on the resource.

        For example, `entityresolution:GetIdMappingJob` , `entityresolution:GetMatchingJob` .
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def condition(self) -> Optional[str]:
        """
        A set of condition keys that you can use in key policies.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def effect(self) -> Optional['PolicyStatementStatementEffect']:
        """
        Determines whether the permissions specified in the policy are to be allowed ( `Allow` ) or denied ( `Deny` ).

        > If you set the value of the `effect` parameter to `Deny` for the `AddPolicyStatement` operation, you must also set the value of the `effect` parameter in the `policy` to `Deny` for the `PutPolicy` operation.
        """
        return pulumi.get(self, "effect")

    @property
    @pulumi.getter
    def principal(self) -> Optional[Sequence[str]]:
        """
        The AWS service or AWS account that can access the resource defined as ARN.
        """
        return pulumi.get(self, "principal")


class AwaitableGetPolicyStatementResult(GetPolicyStatementResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyStatementResult(
            action=self.action,
            condition=self.condition,
            effect=self.effect,
            principal=self.principal)


def get_policy_statement(arn: Optional[str] = None,
                         statement_id: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyStatementResult:
    """
    Policy Statement defined in AWS Entity Resolution Service


    :param str arn: The Amazon Resource Name (ARN) of the resource that will be accessed by the principal.
    :param str statement_id: A statement identifier that differentiates the statement from others in the same policy.
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['statementId'] = statement_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:entityresolution:getPolicyStatement', __args__, opts=opts, typ=GetPolicyStatementResult).value

    return AwaitableGetPolicyStatementResult(
        action=pulumi.get(__ret__, 'action'),
        condition=pulumi.get(__ret__, 'condition'),
        effect=pulumi.get(__ret__, 'effect'),
        principal=pulumi.get(__ret__, 'principal'))
def get_policy_statement_output(arn: Optional[pulumi.Input[str]] = None,
                                statement_id: Optional[pulumi.Input[str]] = None,
                                opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPolicyStatementResult]:
    """
    Policy Statement defined in AWS Entity Resolution Service


    :param str arn: The Amazon Resource Name (ARN) of the resource that will be accessed by the principal.
    :param str statement_id: A statement identifier that differentiates the statement from others in the same policy.
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['statementId'] = statement_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:entityresolution:getPolicyStatement', __args__, opts=opts, typ=GetPolicyStatementResult)
    return __ret__.apply(lambda __response__: GetPolicyStatementResult(
        action=pulumi.get(__response__, 'action'),
        condition=pulumi.get(__response__, 'condition'),
        effect=pulumi.get(__response__, 'effect'),
        principal=pulumi.get(__response__, 'principal')))
