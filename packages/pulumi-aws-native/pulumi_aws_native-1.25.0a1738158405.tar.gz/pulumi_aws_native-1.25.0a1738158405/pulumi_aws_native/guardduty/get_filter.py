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
    'GetFilterResult',
    'AwaitableGetFilterResult',
    'get_filter',
    'get_filter_output',
]

@pulumi.output_type
class GetFilterResult:
    def __init__(__self__, action=None, description=None, finding_criteria=None, rank=None, tags=None):
        if action and not isinstance(action, str):
            raise TypeError("Expected argument 'action' to be a str")
        pulumi.set(__self__, "action", action)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if finding_criteria and not isinstance(finding_criteria, dict):
            raise TypeError("Expected argument 'finding_criteria' to be a dict")
        pulumi.set(__self__, "finding_criteria", finding_criteria)
        if rank and not isinstance(rank, int):
            raise TypeError("Expected argument 'rank' to be a int")
        pulumi.set(__self__, "rank", rank)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def action(self) -> Optional[str]:
        """
        Specifies the action that is to be applied to the findings that match the filter.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the filter. Valid characters include alphanumeric characters, and special characters such as hyphen, period, colon, underscore, parentheses ( `{ }` , `[ ]` , and `( )` ), forward slash, horizontal tab, vertical tab, newline, form feed, return, and whitespace.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="findingCriteria")
    def finding_criteria(self) -> Optional['outputs.FilterFindingCriteria']:
        """
        Represents the criteria to be used in the filter for querying findings.
        """
        return pulumi.get(self, "finding_criteria")

    @property
    @pulumi.getter
    def rank(self) -> Optional[int]:
        """
        Specifies the position of the filter in the list of current filters. Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100.

        By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, [DependsOn](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html) , with the following syntax: `"DependsOn":[ "ObjectName" ]` .
        """
        return pulumi.get(self, "rank")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags to be added to a new filter resource. Each tag consists of a key and an optional value, both of which you define.

        For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        return pulumi.get(self, "tags")


class AwaitableGetFilterResult(GetFilterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFilterResult(
            action=self.action,
            description=self.description,
            finding_criteria=self.finding_criteria,
            rank=self.rank,
            tags=self.tags)


def get_filter(detector_id: Optional[str] = None,
               name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFilterResult:
    """
    Resource Type definition for AWS::GuardDuty::Filter


    :param str detector_id: The detector ID associated with the GuardDuty account for which you want to create a filter.
           
           To find the `detectorId` in the current Region, see the
           Settings page in the GuardDuty console, or run the [ListDetectors](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html) API.
    :param str name: The name of the filter. Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.
    """
    __args__ = dict()
    __args__['detectorId'] = detector_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:guardduty:getFilter', __args__, opts=opts, typ=GetFilterResult).value

    return AwaitableGetFilterResult(
        action=pulumi.get(__ret__, 'action'),
        description=pulumi.get(__ret__, 'description'),
        finding_criteria=pulumi.get(__ret__, 'finding_criteria'),
        rank=pulumi.get(__ret__, 'rank'),
        tags=pulumi.get(__ret__, 'tags'))
def get_filter_output(detector_id: Optional[pulumi.Input[str]] = None,
                      name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetFilterResult]:
    """
    Resource Type definition for AWS::GuardDuty::Filter


    :param str detector_id: The detector ID associated with the GuardDuty account for which you want to create a filter.
           
           To find the `detectorId` in the current Region, see the
           Settings page in the GuardDuty console, or run the [ListDetectors](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html) API.
    :param str name: The name of the filter. Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.
    """
    __args__ = dict()
    __args__['detectorId'] = detector_id
    __args__['name'] = name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:guardduty:getFilter', __args__, opts=opts, typ=GetFilterResult)
    return __ret__.apply(lambda __response__: GetFilterResult(
        action=pulumi.get(__response__, 'action'),
        description=pulumi.get(__response__, 'description'),
        finding_criteria=pulumi.get(__response__, 'finding_criteria'),
        rank=pulumi.get(__response__, 'rank'),
        tags=pulumi.get(__response__, 'tags')))
