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
    'GetReportPlanResult',
    'AwaitableGetReportPlanResult',
    'get_report_plan',
    'get_report_plan_output',
]

@pulumi.output_type
class GetReportPlanResult:
    def __init__(__self__, report_delivery_channel=None, report_plan_arn=None, report_plan_description=None, report_plan_tags=None, report_setting=None):
        if report_delivery_channel and not isinstance(report_delivery_channel, dict):
            raise TypeError("Expected argument 'report_delivery_channel' to be a dict")
        pulumi.set(__self__, "report_delivery_channel", report_delivery_channel)
        if report_plan_arn and not isinstance(report_plan_arn, str):
            raise TypeError("Expected argument 'report_plan_arn' to be a str")
        pulumi.set(__self__, "report_plan_arn", report_plan_arn)
        if report_plan_description and not isinstance(report_plan_description, str):
            raise TypeError("Expected argument 'report_plan_description' to be a str")
        pulumi.set(__self__, "report_plan_description", report_plan_description)
        if report_plan_tags and not isinstance(report_plan_tags, list):
            raise TypeError("Expected argument 'report_plan_tags' to be a list")
        pulumi.set(__self__, "report_plan_tags", report_plan_tags)
        if report_setting and not isinstance(report_setting, dict):
            raise TypeError("Expected argument 'report_setting' to be a dict")
        pulumi.set(__self__, "report_setting", report_setting)

    @property
    @pulumi.getter(name="reportDeliveryChannel")
    def report_delivery_channel(self) -> Optional['outputs.ReportDeliveryChannelProperties']:
        """
        A structure that contains information about where and how to deliver your reports, specifically your Amazon S3 bucket name, S3 key prefix, and the formats of your reports.
        """
        return pulumi.get(self, "report_delivery_channel")

    @property
    @pulumi.getter(name="reportPlanArn")
    def report_plan_arn(self) -> Optional[str]:
        """
        An Amazon Resource Name (ARN) that uniquely identifies a resource. The format of the ARN depends on the resource type.
        """
        return pulumi.get(self, "report_plan_arn")

    @property
    @pulumi.getter(name="reportPlanDescription")
    def report_plan_description(self) -> Optional[str]:
        """
        An optional description of the report plan with a maximum of 1,024 characters.
        """
        return pulumi.get(self, "report_plan_description")

    @property
    @pulumi.getter(name="reportPlanTags")
    def report_plan_tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Metadata that you can assign to help organize the report plans that you create. Each tag is a key-value pair.
        """
        return pulumi.get(self, "report_plan_tags")

    @property
    @pulumi.getter(name="reportSetting")
    def report_setting(self) -> Optional['outputs.ReportSettingProperties']:
        """
        Identifies the report template for the report. Reports are built using a report template.
        """
        return pulumi.get(self, "report_setting")


class AwaitableGetReportPlanResult(GetReportPlanResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetReportPlanResult(
            report_delivery_channel=self.report_delivery_channel,
            report_plan_arn=self.report_plan_arn,
            report_plan_description=self.report_plan_description,
            report_plan_tags=self.report_plan_tags,
            report_setting=self.report_setting)


def get_report_plan(report_plan_arn: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetReportPlanResult:
    """
    Contains detailed information about a report plan in AWS Backup Audit Manager.


    :param str report_plan_arn: An Amazon Resource Name (ARN) that uniquely identifies a resource. The format of the ARN depends on the resource type.
    """
    __args__ = dict()
    __args__['reportPlanArn'] = report_plan_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:backup:getReportPlan', __args__, opts=opts, typ=GetReportPlanResult).value

    return AwaitableGetReportPlanResult(
        report_delivery_channel=pulumi.get(__ret__, 'report_delivery_channel'),
        report_plan_arn=pulumi.get(__ret__, 'report_plan_arn'),
        report_plan_description=pulumi.get(__ret__, 'report_plan_description'),
        report_plan_tags=pulumi.get(__ret__, 'report_plan_tags'),
        report_setting=pulumi.get(__ret__, 'report_setting'))
def get_report_plan_output(report_plan_arn: Optional[pulumi.Input[str]] = None,
                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetReportPlanResult]:
    """
    Contains detailed information about a report plan in AWS Backup Audit Manager.


    :param str report_plan_arn: An Amazon Resource Name (ARN) that uniquely identifies a resource. The format of the ARN depends on the resource type.
    """
    __args__ = dict()
    __args__['reportPlanArn'] = report_plan_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:backup:getReportPlan', __args__, opts=opts, typ=GetReportPlanResult)
    return __ret__.apply(lambda __response__: GetReportPlanResult(
        report_delivery_channel=pulumi.get(__response__, 'report_delivery_channel'),
        report_plan_arn=pulumi.get(__response__, 'report_plan_arn'),
        report_plan_description=pulumi.get(__response__, 'report_plan_description'),
        report_plan_tags=pulumi.get(__response__, 'report_plan_tags'),
        report_setting=pulumi.get(__response__, 'report_setting')))
