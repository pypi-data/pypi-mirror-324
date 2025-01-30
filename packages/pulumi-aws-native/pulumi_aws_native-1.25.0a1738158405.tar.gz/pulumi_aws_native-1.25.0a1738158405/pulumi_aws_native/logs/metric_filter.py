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
from ._inputs import *

__all__ = ['MetricFilterArgs', 'MetricFilter']

@pulumi.input_type
class MetricFilterArgs:
    def __init__(__self__, *,
                 filter_pattern: pulumi.Input[str],
                 log_group_name: pulumi.Input[str],
                 metric_transformations: pulumi.Input[Sequence[pulumi.Input['MetricFilterMetricTransformationArgs']]],
                 apply_on_transformed_logs: Optional[pulumi.Input[bool]] = None,
                 filter_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MetricFilter resource.
        :param pulumi.Input[str] filter_pattern: A filter pattern for extracting metric data out of ingested log events. For more information, see [Filter and Pattern Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html).
        :param pulumi.Input[str] log_group_name: The name of an existing log group that you want to associate with this metric filter.
        :param pulumi.Input[Sequence[pulumi.Input['MetricFilterMetricTransformationArgs']]] metric_transformations: The metric transformations.
        :param pulumi.Input[bool] apply_on_transformed_logs: This parameter is valid only for log groups that have an active log transformer. For more information about log transformers, see [PutTransformer](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutTransformer.html).
                If this value is ``true``, the metric filter is applied on the transformed version of the log events instead of the original ingested log events.
        :param pulumi.Input[str] filter_name: The name of the metric filter.
        """
        pulumi.set(__self__, "filter_pattern", filter_pattern)
        pulumi.set(__self__, "log_group_name", log_group_name)
        pulumi.set(__self__, "metric_transformations", metric_transformations)
        if apply_on_transformed_logs is not None:
            pulumi.set(__self__, "apply_on_transformed_logs", apply_on_transformed_logs)
        if filter_name is not None:
            pulumi.set(__self__, "filter_name", filter_name)

    @property
    @pulumi.getter(name="filterPattern")
    def filter_pattern(self) -> pulumi.Input[str]:
        """
        A filter pattern for extracting metric data out of ingested log events. For more information, see [Filter and Pattern Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html).
        """
        return pulumi.get(self, "filter_pattern")

    @filter_pattern.setter
    def filter_pattern(self, value: pulumi.Input[str]):
        pulumi.set(self, "filter_pattern", value)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> pulumi.Input[str]:
        """
        The name of an existing log group that you want to associate with this metric filter.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="metricTransformations")
    def metric_transformations(self) -> pulumi.Input[Sequence[pulumi.Input['MetricFilterMetricTransformationArgs']]]:
        """
        The metric transformations.
        """
        return pulumi.get(self, "metric_transformations")

    @metric_transformations.setter
    def metric_transformations(self, value: pulumi.Input[Sequence[pulumi.Input['MetricFilterMetricTransformationArgs']]]):
        pulumi.set(self, "metric_transformations", value)

    @property
    @pulumi.getter(name="applyOnTransformedLogs")
    def apply_on_transformed_logs(self) -> Optional[pulumi.Input[bool]]:
        """
        This parameter is valid only for log groups that have an active log transformer. For more information about log transformers, see [PutTransformer](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutTransformer.html).
         If this value is ``true``, the metric filter is applied on the transformed version of the log events instead of the original ingested log events.
        """
        return pulumi.get(self, "apply_on_transformed_logs")

    @apply_on_transformed_logs.setter
    def apply_on_transformed_logs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "apply_on_transformed_logs", value)

    @property
    @pulumi.getter(name="filterName")
    def filter_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the metric filter.
        """
        return pulumi.get(self, "filter_name")

    @filter_name.setter
    def filter_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter_name", value)


class MetricFilter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 apply_on_transformed_logs: Optional[pulumi.Input[bool]] = None,
                 filter_name: Optional[pulumi.Input[str]] = None,
                 filter_pattern: Optional[pulumi.Input[str]] = None,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 metric_transformations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['MetricFilterMetricTransformationArgs', 'MetricFilterMetricTransformationArgsDict']]]]] = None,
                 __props__=None):
        """
        The ``AWS::Logs::MetricFilter`` resource specifies a metric filter that describes how CWL extracts information from logs and transforms it into Amazon CloudWatch metrics. If you have multiple metric filters that are associated with a log group, all the filters are applied to the log streams in that group.
         The maximum number of metric filters that can be associated with a log group is 100.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] apply_on_transformed_logs: This parameter is valid only for log groups that have an active log transformer. For more information about log transformers, see [PutTransformer](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutTransformer.html).
                If this value is ``true``, the metric filter is applied on the transformed version of the log events instead of the original ingested log events.
        :param pulumi.Input[str] filter_name: The name of the metric filter.
        :param pulumi.Input[str] filter_pattern: A filter pattern for extracting metric data out of ingested log events. For more information, see [Filter and Pattern Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html).
        :param pulumi.Input[str] log_group_name: The name of an existing log group that you want to associate with this metric filter.
        :param pulumi.Input[Sequence[pulumi.Input[Union['MetricFilterMetricTransformationArgs', 'MetricFilterMetricTransformationArgsDict']]]] metric_transformations: The metric transformations.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MetricFilterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ``AWS::Logs::MetricFilter`` resource specifies a metric filter that describes how CWL extracts information from logs and transforms it into Amazon CloudWatch metrics. If you have multiple metric filters that are associated with a log group, all the filters are applied to the log streams in that group.
         The maximum number of metric filters that can be associated with a log group is 100.

        :param str resource_name: The name of the resource.
        :param MetricFilterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MetricFilterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 apply_on_transformed_logs: Optional[pulumi.Input[bool]] = None,
                 filter_name: Optional[pulumi.Input[str]] = None,
                 filter_pattern: Optional[pulumi.Input[str]] = None,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 metric_transformations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['MetricFilterMetricTransformationArgs', 'MetricFilterMetricTransformationArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MetricFilterArgs.__new__(MetricFilterArgs)

            __props__.__dict__["apply_on_transformed_logs"] = apply_on_transformed_logs
            __props__.__dict__["filter_name"] = filter_name
            if filter_pattern is None and not opts.urn:
                raise TypeError("Missing required property 'filter_pattern'")
            __props__.__dict__["filter_pattern"] = filter_pattern
            if log_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'log_group_name'")
            __props__.__dict__["log_group_name"] = log_group_name
            if metric_transformations is None and not opts.urn:
                raise TypeError("Missing required property 'metric_transformations'")
            __props__.__dict__["metric_transformations"] = metric_transformations
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["filterName", "logGroupName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(MetricFilter, __self__).__init__(
            'aws-native:logs:MetricFilter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MetricFilter':
        """
        Get an existing MetricFilter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MetricFilterArgs.__new__(MetricFilterArgs)

        __props__.__dict__["apply_on_transformed_logs"] = None
        __props__.__dict__["filter_name"] = None
        __props__.__dict__["filter_pattern"] = None
        __props__.__dict__["log_group_name"] = None
        __props__.__dict__["metric_transformations"] = None
        return MetricFilter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applyOnTransformedLogs")
    def apply_on_transformed_logs(self) -> pulumi.Output[Optional[bool]]:
        """
        This parameter is valid only for log groups that have an active log transformer. For more information about log transformers, see [PutTransformer](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutTransformer.html).
         If this value is ``true``, the metric filter is applied on the transformed version of the log events instead of the original ingested log events.
        """
        return pulumi.get(self, "apply_on_transformed_logs")

    @property
    @pulumi.getter(name="filterName")
    def filter_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the metric filter.
        """
        return pulumi.get(self, "filter_name")

    @property
    @pulumi.getter(name="filterPattern")
    def filter_pattern(self) -> pulumi.Output[str]:
        """
        A filter pattern for extracting metric data out of ingested log events. For more information, see [Filter and Pattern Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html).
        """
        return pulumi.get(self, "filter_pattern")

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> pulumi.Output[str]:
        """
        The name of an existing log group that you want to associate with this metric filter.
        """
        return pulumi.get(self, "log_group_name")

    @property
    @pulumi.getter(name="metricTransformations")
    def metric_transformations(self) -> pulumi.Output[Sequence['outputs.MetricFilterMetricTransformation']]:
        """
        The metric transformations.
        """
        return pulumi.get(self, "metric_transformations")

