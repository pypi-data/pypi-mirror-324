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

__all__ = ['LogAnomalyDetectorArgs', 'LogAnomalyDetector']

@pulumi.input_type
class LogAnomalyDetectorArgs:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 anomaly_visibility_time: Optional[pulumi.Input[float]] = None,
                 detector_name: Optional[pulumi.Input[str]] = None,
                 evaluation_frequency: Optional[pulumi.Input['LogAnomalyDetectorEvaluationFrequency']] = None,
                 filter_pattern: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_group_arn_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a LogAnomalyDetector resource.
        :param pulumi.Input[str] account_id: Account ID for owner of detector
        :param pulumi.Input[float] anomaly_visibility_time: The number of days to have visibility on an anomaly. After this time period has elapsed for an anomaly, it will be automatically baselined and the anomaly detector will treat new occurrences of a similar anomaly as normal. Therefore, if you do not correct the cause of an anomaly during the time period specified in `AnomalyVisibilityTime` , it will be considered normal going forward and will not be detected as an anomaly.
        :param pulumi.Input[str] detector_name: Name of detector
        :param pulumi.Input['LogAnomalyDetectorEvaluationFrequency'] evaluation_frequency: How often log group is evaluated
        :param pulumi.Input[str] filter_pattern: You can use this parameter to limit the anomaly detection model to examine only log events that match the pattern you specify here. For more information, see [Filter and Pattern Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html) .
        :param pulumi.Input[str] kms_key_id: The Amazon Resource Name (ARN) of the CMK to use when encrypting log data.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] log_group_arn_list: List of Arns for the given log group
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if anomaly_visibility_time is not None:
            pulumi.set(__self__, "anomaly_visibility_time", anomaly_visibility_time)
        if detector_name is not None:
            pulumi.set(__self__, "detector_name", detector_name)
        if evaluation_frequency is not None:
            pulumi.set(__self__, "evaluation_frequency", evaluation_frequency)
        if filter_pattern is not None:
            pulumi.set(__self__, "filter_pattern", filter_pattern)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if log_group_arn_list is not None:
            pulumi.set(__self__, "log_group_arn_list", log_group_arn_list)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        Account ID for owner of detector
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="anomalyVisibilityTime")
    def anomaly_visibility_time(self) -> Optional[pulumi.Input[float]]:
        """
        The number of days to have visibility on an anomaly. After this time period has elapsed for an anomaly, it will be automatically baselined and the anomaly detector will treat new occurrences of a similar anomaly as normal. Therefore, if you do not correct the cause of an anomaly during the time period specified in `AnomalyVisibilityTime` , it will be considered normal going forward and will not be detected as an anomaly.
        """
        return pulumi.get(self, "anomaly_visibility_time")

    @anomaly_visibility_time.setter
    def anomaly_visibility_time(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "anomaly_visibility_time", value)

    @property
    @pulumi.getter(name="detectorName")
    def detector_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of detector
        """
        return pulumi.get(self, "detector_name")

    @detector_name.setter
    def detector_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "detector_name", value)

    @property
    @pulumi.getter(name="evaluationFrequency")
    def evaluation_frequency(self) -> Optional[pulumi.Input['LogAnomalyDetectorEvaluationFrequency']]:
        """
        How often log group is evaluated
        """
        return pulumi.get(self, "evaluation_frequency")

    @evaluation_frequency.setter
    def evaluation_frequency(self, value: Optional[pulumi.Input['LogAnomalyDetectorEvaluationFrequency']]):
        pulumi.set(self, "evaluation_frequency", value)

    @property
    @pulumi.getter(name="filterPattern")
    def filter_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        You can use this parameter to limit the anomaly detection model to examine only log events that match the pattern you specify here. For more information, see [Filter and Pattern Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html) .
        """
        return pulumi.get(self, "filter_pattern")

    @filter_pattern.setter
    def filter_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter_pattern", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the CMK to use when encrypting log data.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter(name="logGroupArnList")
    def log_group_arn_list(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of Arns for the given log group
        """
        return pulumi.get(self, "log_group_arn_list")

    @log_group_arn_list.setter
    def log_group_arn_list(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "log_group_arn_list", value)


class LogAnomalyDetector(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 anomaly_visibility_time: Optional[pulumi.Input[float]] = None,
                 detector_name: Optional[pulumi.Input[str]] = None,
                 evaluation_frequency: Optional[pulumi.Input['LogAnomalyDetectorEvaluationFrequency']] = None,
                 filter_pattern: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_group_arn_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The AWS::Logs::LogAnomalyDetector resource specifies a CloudWatch Logs LogAnomalyDetector.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: Account ID for owner of detector
        :param pulumi.Input[float] anomaly_visibility_time: The number of days to have visibility on an anomaly. After this time period has elapsed for an anomaly, it will be automatically baselined and the anomaly detector will treat new occurrences of a similar anomaly as normal. Therefore, if you do not correct the cause of an anomaly during the time period specified in `AnomalyVisibilityTime` , it will be considered normal going forward and will not be detected as an anomaly.
        :param pulumi.Input[str] detector_name: Name of detector
        :param pulumi.Input['LogAnomalyDetectorEvaluationFrequency'] evaluation_frequency: How often log group is evaluated
        :param pulumi.Input[str] filter_pattern: You can use this parameter to limit the anomaly detection model to examine only log events that match the pattern you specify here. For more information, see [Filter and Pattern Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html) .
        :param pulumi.Input[str] kms_key_id: The Amazon Resource Name (ARN) of the CMK to use when encrypting log data.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] log_group_arn_list: List of Arns for the given log group
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[LogAnomalyDetectorArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::Logs::LogAnomalyDetector resource specifies a CloudWatch Logs LogAnomalyDetector.

        :param str resource_name: The name of the resource.
        :param LogAnomalyDetectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LogAnomalyDetectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 anomaly_visibility_time: Optional[pulumi.Input[float]] = None,
                 detector_name: Optional[pulumi.Input[str]] = None,
                 evaluation_frequency: Optional[pulumi.Input['LogAnomalyDetectorEvaluationFrequency']] = None,
                 filter_pattern: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_group_arn_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LogAnomalyDetectorArgs.__new__(LogAnomalyDetectorArgs)

            __props__.__dict__["account_id"] = account_id
            __props__.__dict__["anomaly_visibility_time"] = anomaly_visibility_time
            __props__.__dict__["detector_name"] = detector_name
            __props__.__dict__["evaluation_frequency"] = evaluation_frequency
            __props__.__dict__["filter_pattern"] = filter_pattern
            __props__.__dict__["kms_key_id"] = kms_key_id
            __props__.__dict__["log_group_arn_list"] = log_group_arn_list
            __props__.__dict__["anomaly_detector_arn"] = None
            __props__.__dict__["anomaly_detector_status"] = None
            __props__.__dict__["creation_time_stamp"] = None
            __props__.__dict__["last_modified_time_stamp"] = None
        super(LogAnomalyDetector, __self__).__init__(
            'aws-native:logs:LogAnomalyDetector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'LogAnomalyDetector':
        """
        Get an existing LogAnomalyDetector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = LogAnomalyDetectorArgs.__new__(LogAnomalyDetectorArgs)

        __props__.__dict__["account_id"] = None
        __props__.__dict__["anomaly_detector_arn"] = None
        __props__.__dict__["anomaly_detector_status"] = None
        __props__.__dict__["anomaly_visibility_time"] = None
        __props__.__dict__["creation_time_stamp"] = None
        __props__.__dict__["detector_name"] = None
        __props__.__dict__["evaluation_frequency"] = None
        __props__.__dict__["filter_pattern"] = None
        __props__.__dict__["kms_key_id"] = None
        __props__.__dict__["last_modified_time_stamp"] = None
        __props__.__dict__["log_group_arn_list"] = None
        return LogAnomalyDetector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[Optional[str]]:
        """
        Account ID for owner of detector
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="anomalyDetectorArn")
    def anomaly_detector_arn(self) -> pulumi.Output[str]:
        """
        ARN of LogAnomalyDetector
        """
        return pulumi.get(self, "anomaly_detector_arn")

    @property
    @pulumi.getter(name="anomalyDetectorStatus")
    def anomaly_detector_status(self) -> pulumi.Output[str]:
        """
        Current status of detector.
        """
        return pulumi.get(self, "anomaly_detector_status")

    @property
    @pulumi.getter(name="anomalyVisibilityTime")
    def anomaly_visibility_time(self) -> pulumi.Output[Optional[float]]:
        """
        The number of days to have visibility on an anomaly. After this time period has elapsed for an anomaly, it will be automatically baselined and the anomaly detector will treat new occurrences of a similar anomaly as normal. Therefore, if you do not correct the cause of an anomaly during the time period specified in `AnomalyVisibilityTime` , it will be considered normal going forward and will not be detected as an anomaly.
        """
        return pulumi.get(self, "anomaly_visibility_time")

    @property
    @pulumi.getter(name="creationTimeStamp")
    def creation_time_stamp(self) -> pulumi.Output[float]:
        """
        When detector was created.
        """
        return pulumi.get(self, "creation_time_stamp")

    @property
    @pulumi.getter(name="detectorName")
    def detector_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of detector
        """
        return pulumi.get(self, "detector_name")

    @property
    @pulumi.getter(name="evaluationFrequency")
    def evaluation_frequency(self) -> pulumi.Output[Optional['LogAnomalyDetectorEvaluationFrequency']]:
        """
        How often log group is evaluated
        """
        return pulumi.get(self, "evaluation_frequency")

    @property
    @pulumi.getter(name="filterPattern")
    def filter_pattern(self) -> pulumi.Output[Optional[str]]:
        """
        You can use this parameter to limit the anomaly detection model to examine only log events that match the pattern you specify here. For more information, see [Filter and Pattern Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html) .
        """
        return pulumi.get(self, "filter_pattern")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the CMK to use when encrypting log data.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="lastModifiedTimeStamp")
    def last_modified_time_stamp(self) -> pulumi.Output[float]:
        """
        When detector was lsat modified.
        """
        return pulumi.get(self, "last_modified_time_stamp")

    @property
    @pulumi.getter(name="logGroupArnList")
    def log_group_arn_list(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of Arns for the given log group
        """
        return pulumi.get(self, "log_group_arn_list")

