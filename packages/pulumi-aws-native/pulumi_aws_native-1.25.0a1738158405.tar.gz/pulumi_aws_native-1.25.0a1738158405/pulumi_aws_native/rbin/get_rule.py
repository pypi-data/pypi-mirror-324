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
from ._enums import *

__all__ = [
    'GetRuleResult',
    'AwaitableGetRuleResult',
    'get_rule',
    'get_rule_output',
]

@pulumi.output_type
class GetRuleResult:
    def __init__(__self__, arn=None, description=None, exclude_resource_tags=None, identifier=None, lock_state=None, resource_tags=None, retention_period=None, status=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if exclude_resource_tags and not isinstance(exclude_resource_tags, list):
            raise TypeError("Expected argument 'exclude_resource_tags' to be a list")
        pulumi.set(__self__, "exclude_resource_tags", exclude_resource_tags)
        if identifier and not isinstance(identifier, str):
            raise TypeError("Expected argument 'identifier' to be a str")
        pulumi.set(__self__, "identifier", identifier)
        if lock_state and not isinstance(lock_state, str):
            raise TypeError("Expected argument 'lock_state' to be a str")
        pulumi.set(__self__, "lock_state", lock_state)
        if resource_tags and not isinstance(resource_tags, list):
            raise TypeError("Expected argument 'resource_tags' to be a list")
        pulumi.set(__self__, "resource_tags", resource_tags)
        if retention_period and not isinstance(retention_period, dict):
            raise TypeError("Expected argument 'retention_period' to be a dict")
        pulumi.set(__self__, "retention_period", retention_period)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Rule Arn is unique for each rule.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the retention rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="excludeResourceTags")
    def exclude_resource_tags(self) -> Optional[Sequence['outputs.RuleResourceTag']]:
        """
        Information about the exclude resource tags used to identify resources that are excluded by the retention rule.
        """
        return pulumi.get(self, "exclude_resource_tags")

    @property
    @pulumi.getter
    def identifier(self) -> Optional[str]:
        """
        The unique ID of the retention rule.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter(name="lockState")
    def lock_state(self) -> Optional[str]:
        """
        The lock state for the retention rule.
        """
        return pulumi.get(self, "lock_state")

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> Optional[Sequence['outputs.RuleResourceTag']]:
        """
        Information about the resource tags used to identify resources that are retained by the retention rule.
        """
        return pulumi.get(self, "resource_tags")

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> Optional['outputs.RuleRetentionPeriod']:
        """
        Information about the retention period for which the retention rule is to retain resources.
        """
        return pulumi.get(self, "retention_period")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The state of the retention rule. Only retention rules that are in the available state retain resources.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Information about the tags assigned to the retention rule.
        """
        return pulumi.get(self, "tags")


class AwaitableGetRuleResult(GetRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRuleResult(
            arn=self.arn,
            description=self.description,
            exclude_resource_tags=self.exclude_resource_tags,
            identifier=self.identifier,
            lock_state=self.lock_state,
            resource_tags=self.resource_tags,
            retention_period=self.retention_period,
            status=self.status,
            tags=self.tags)


def get_rule(arn: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRuleResult:
    """
    Resource Type definition for AWS::Rbin::Rule


    :param str arn: Rule Arn is unique for each rule.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:rbin:getRule', __args__, opts=opts, typ=GetRuleResult).value

    return AwaitableGetRuleResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        exclude_resource_tags=pulumi.get(__ret__, 'exclude_resource_tags'),
        identifier=pulumi.get(__ret__, 'identifier'),
        lock_state=pulumi.get(__ret__, 'lock_state'),
        resource_tags=pulumi.get(__ret__, 'resource_tags'),
        retention_period=pulumi.get(__ret__, 'retention_period'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'))
def get_rule_output(arn: Optional[pulumi.Input[str]] = None,
                    opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetRuleResult]:
    """
    Resource Type definition for AWS::Rbin::Rule


    :param str arn: Rule Arn is unique for each rule.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:rbin:getRule', __args__, opts=opts, typ=GetRuleResult)
    return __ret__.apply(lambda __response__: GetRuleResult(
        arn=pulumi.get(__response__, 'arn'),
        description=pulumi.get(__response__, 'description'),
        exclude_resource_tags=pulumi.get(__response__, 'exclude_resource_tags'),
        identifier=pulumi.get(__response__, 'identifier'),
        lock_state=pulumi.get(__response__, 'lock_state'),
        resource_tags=pulumi.get(__response__, 'resource_tags'),
        retention_period=pulumi.get(__response__, 'retention_period'),
        status=pulumi.get(__response__, 'status'),
        tags=pulumi.get(__response__, 'tags')))
