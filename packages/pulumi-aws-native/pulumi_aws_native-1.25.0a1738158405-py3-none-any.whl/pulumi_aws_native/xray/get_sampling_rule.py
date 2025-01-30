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
from .. import outputs as _root_outputs

__all__ = [
    'GetSamplingRuleResult',
    'AwaitableGetSamplingRuleResult',
    'get_sampling_rule',
    'get_sampling_rule_output',
]

@pulumi.output_type
class GetSamplingRuleResult:
    def __init__(__self__, rule_arn=None, rule_name=None, sampling_rule=None, sampling_rule_record=None, sampling_rule_update=None, tags=None):
        if rule_arn and not isinstance(rule_arn, str):
            raise TypeError("Expected argument 'rule_arn' to be a str")
        pulumi.set(__self__, "rule_arn", rule_arn)
        if rule_name and not isinstance(rule_name, str):
            raise TypeError("Expected argument 'rule_name' to be a str")
        pulumi.set(__self__, "rule_name", rule_name)
        if sampling_rule and not isinstance(sampling_rule, dict):
            raise TypeError("Expected argument 'sampling_rule' to be a dict")
        pulumi.set(__self__, "sampling_rule", sampling_rule)
        if sampling_rule_record and not isinstance(sampling_rule_record, dict):
            raise TypeError("Expected argument 'sampling_rule_record' to be a dict")
        pulumi.set(__self__, "sampling_rule_record", sampling_rule_record)
        if sampling_rule_update and not isinstance(sampling_rule_update, dict):
            raise TypeError("Expected argument 'sampling_rule_update' to be a dict")
        pulumi.set(__self__, "sampling_rule_update", sampling_rule_update)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="ruleArn")
    def rule_arn(self) -> Optional[str]:
        """
        The sampling rule ARN that was created or updated.
        """
        return pulumi.get(self, "rule_arn")

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> Optional[str]:
        return pulumi.get(self, "rule_name")

    @property
    @pulumi.getter(name="samplingRule")
    def sampling_rule(self) -> Optional['outputs.SamplingRule']:
        """
        The sampling rule to be created or updated.
        """
        return pulumi.get(self, "sampling_rule")

    @property
    @pulumi.getter(name="samplingRuleRecord")
    def sampling_rule_record(self) -> Optional['outputs.SamplingRuleRecord']:
        return pulumi.get(self, "sampling_rule_record")

    @property
    @pulumi.getter(name="samplingRuleUpdate")
    def sampling_rule_update(self) -> Optional['outputs.SamplingRuleUpdate']:
        return pulumi.get(self, "sampling_rule_update")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetSamplingRuleResult(GetSamplingRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSamplingRuleResult(
            rule_arn=self.rule_arn,
            rule_name=self.rule_name,
            sampling_rule=self.sampling_rule,
            sampling_rule_record=self.sampling_rule_record,
            sampling_rule_update=self.sampling_rule_update,
            tags=self.tags)


def get_sampling_rule(rule_arn: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSamplingRuleResult:
    """
    This schema provides construct and validation rules for AWS-XRay SamplingRule resource parameters.


    :param str rule_arn: The sampling rule ARN that was created or updated.
    """
    __args__ = dict()
    __args__['ruleArn'] = rule_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:xray:getSamplingRule', __args__, opts=opts, typ=GetSamplingRuleResult).value

    return AwaitableGetSamplingRuleResult(
        rule_arn=pulumi.get(__ret__, 'rule_arn'),
        rule_name=pulumi.get(__ret__, 'rule_name'),
        sampling_rule=pulumi.get(__ret__, 'sampling_rule'),
        sampling_rule_record=pulumi.get(__ret__, 'sampling_rule_record'),
        sampling_rule_update=pulumi.get(__ret__, 'sampling_rule_update'),
        tags=pulumi.get(__ret__, 'tags'))
def get_sampling_rule_output(rule_arn: Optional[pulumi.Input[str]] = None,
                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSamplingRuleResult]:
    """
    This schema provides construct and validation rules for AWS-XRay SamplingRule resource parameters.


    :param str rule_arn: The sampling rule ARN that was created or updated.
    """
    __args__ = dict()
    __args__['ruleArn'] = rule_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:xray:getSamplingRule', __args__, opts=opts, typ=GetSamplingRuleResult)
    return __ret__.apply(lambda __response__: GetSamplingRuleResult(
        rule_arn=pulumi.get(__response__, 'rule_arn'),
        rule_name=pulumi.get(__response__, 'rule_name'),
        sampling_rule=pulumi.get(__response__, 'sampling_rule'),
        sampling_rule_record=pulumi.get(__response__, 'sampling_rule_record'),
        sampling_rule_update=pulumi.get(__response__, 'sampling_rule_update'),
        tags=pulumi.get(__response__, 'tags')))
