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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs
from ._inputs import *

__all__ = ['FleetMetricArgs', 'FleetMetric']

@pulumi.input_type
class FleetMetricArgs:
    def __init__(__self__, *,
                 aggregation_field: Optional[pulumi.Input[str]] = None,
                 aggregation_type: Optional[pulumi.Input['FleetMetricAggregationTypeArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 index_name: Optional[pulumi.Input[str]] = None,
                 metric_name: Optional[pulumi.Input[str]] = None,
                 period: Optional[pulumi.Input[int]] = None,
                 query_string: Optional[pulumi.Input[str]] = None,
                 query_version: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 unit: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a FleetMetric resource.
        :param pulumi.Input[str] aggregation_field: The aggregation field to perform aggregation and metric emission
        :param pulumi.Input['FleetMetricAggregationTypeArgs'] aggregation_type: The type of the aggregation query.
        :param pulumi.Input[str] description: The description of a fleet metric
        :param pulumi.Input[str] index_name: The index name of a fleet metric
        :param pulumi.Input[str] metric_name: The name of the fleet metric
        :param pulumi.Input[int] period: The period of metric emission in seconds
        :param pulumi.Input[str] query_string: The Fleet Indexing query used by a fleet metric
        :param pulumi.Input[str] query_version: The version of a Fleet Indexing query used by a fleet metric
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: An array of key-value pairs to apply to this resource
        :param pulumi.Input[str] unit: The unit of data points emitted by a fleet metric
        """
        if aggregation_field is not None:
            pulumi.set(__self__, "aggregation_field", aggregation_field)
        if aggregation_type is not None:
            pulumi.set(__self__, "aggregation_type", aggregation_type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if index_name is not None:
            pulumi.set(__self__, "index_name", index_name)
        if metric_name is not None:
            pulumi.set(__self__, "metric_name", metric_name)
        if period is not None:
            pulumi.set(__self__, "period", period)
        if query_string is not None:
            pulumi.set(__self__, "query_string", query_string)
        if query_version is not None:
            pulumi.set(__self__, "query_version", query_version)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter(name="aggregationField")
    def aggregation_field(self) -> Optional[pulumi.Input[str]]:
        """
        The aggregation field to perform aggregation and metric emission
        """
        return pulumi.get(self, "aggregation_field")

    @aggregation_field.setter
    def aggregation_field(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aggregation_field", value)

    @property
    @pulumi.getter(name="aggregationType")
    def aggregation_type(self) -> Optional[pulumi.Input['FleetMetricAggregationTypeArgs']]:
        """
        The type of the aggregation query.
        """
        return pulumi.get(self, "aggregation_type")

    @aggregation_type.setter
    def aggregation_type(self, value: Optional[pulumi.Input['FleetMetricAggregationTypeArgs']]):
        pulumi.set(self, "aggregation_type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of a fleet metric
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="indexName")
    def index_name(self) -> Optional[pulumi.Input[str]]:
        """
        The index name of a fleet metric
        """
        return pulumi.get(self, "index_name")

    @index_name.setter
    def index_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "index_name", value)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the fleet metric
        """
        return pulumi.get(self, "metric_name")

    @metric_name.setter
    def metric_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_name", value)

    @property
    @pulumi.getter
    def period(self) -> Optional[pulumi.Input[int]]:
        """
        The period of metric emission in seconds
        """
        return pulumi.get(self, "period")

    @period.setter
    def period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "period", value)

    @property
    @pulumi.getter(name="queryString")
    def query_string(self) -> Optional[pulumi.Input[str]]:
        """
        The Fleet Indexing query used by a fleet metric
        """
        return pulumi.get(self, "query_string")

    @query_string.setter
    def query_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query_string", value)

    @property
    @pulumi.getter(name="queryVersion")
    def query_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of a Fleet Indexing query used by a fleet metric
        """
        return pulumi.get(self, "query_version")

    @query_version.setter
    def query_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query_version", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def unit(self) -> Optional[pulumi.Input[str]]:
        """
        The unit of data points emitted by a fleet metric
        """
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "unit", value)


class FleetMetric(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aggregation_field: Optional[pulumi.Input[str]] = None,
                 aggregation_type: Optional[pulumi.Input[Union['FleetMetricAggregationTypeArgs', 'FleetMetricAggregationTypeArgsDict']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 index_name: Optional[pulumi.Input[str]] = None,
                 metric_name: Optional[pulumi.Input[str]] = None,
                 period: Optional[pulumi.Input[int]] = None,
                 query_string: Optional[pulumi.Input[str]] = None,
                 query_version: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 unit: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An aggregated metric of certain devices in your fleet

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] aggregation_field: The aggregation field to perform aggregation and metric emission
        :param pulumi.Input[Union['FleetMetricAggregationTypeArgs', 'FleetMetricAggregationTypeArgsDict']] aggregation_type: The type of the aggregation query.
        :param pulumi.Input[str] description: The description of a fleet metric
        :param pulumi.Input[str] index_name: The index name of a fleet metric
        :param pulumi.Input[str] metric_name: The name of the fleet metric
        :param pulumi.Input[int] period: The period of metric emission in seconds
        :param pulumi.Input[str] query_string: The Fleet Indexing query used by a fleet metric
        :param pulumi.Input[str] query_version: The version of a Fleet Indexing query used by a fleet metric
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: An array of key-value pairs to apply to this resource
        :param pulumi.Input[str] unit: The unit of data points emitted by a fleet metric
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[FleetMetricArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An aggregated metric of certain devices in your fleet

        :param str resource_name: The name of the resource.
        :param FleetMetricArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FleetMetricArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aggregation_field: Optional[pulumi.Input[str]] = None,
                 aggregation_type: Optional[pulumi.Input[Union['FleetMetricAggregationTypeArgs', 'FleetMetricAggregationTypeArgsDict']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 index_name: Optional[pulumi.Input[str]] = None,
                 metric_name: Optional[pulumi.Input[str]] = None,
                 period: Optional[pulumi.Input[int]] = None,
                 query_string: Optional[pulumi.Input[str]] = None,
                 query_version: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 unit: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FleetMetricArgs.__new__(FleetMetricArgs)

            __props__.__dict__["aggregation_field"] = aggregation_field
            __props__.__dict__["aggregation_type"] = aggregation_type
            __props__.__dict__["description"] = description
            __props__.__dict__["index_name"] = index_name
            __props__.__dict__["metric_name"] = metric_name
            __props__.__dict__["period"] = period
            __props__.__dict__["query_string"] = query_string
            __props__.__dict__["query_version"] = query_version
            __props__.__dict__["tags"] = tags
            __props__.__dict__["unit"] = unit
            __props__.__dict__["creation_date"] = None
            __props__.__dict__["last_modified_date"] = None
            __props__.__dict__["metric_arn"] = None
            __props__.__dict__["version"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["metricName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(FleetMetric, __self__).__init__(
            'aws-native:iot:FleetMetric',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FleetMetric':
        """
        Get an existing FleetMetric resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = FleetMetricArgs.__new__(FleetMetricArgs)

        __props__.__dict__["aggregation_field"] = None
        __props__.__dict__["aggregation_type"] = None
        __props__.__dict__["creation_date"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["index_name"] = None
        __props__.__dict__["last_modified_date"] = None
        __props__.__dict__["metric_arn"] = None
        __props__.__dict__["metric_name"] = None
        __props__.__dict__["period"] = None
        __props__.__dict__["query_string"] = None
        __props__.__dict__["query_version"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["unit"] = None
        __props__.__dict__["version"] = None
        return FleetMetric(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="aggregationField")
    def aggregation_field(self) -> pulumi.Output[Optional[str]]:
        """
        The aggregation field to perform aggregation and metric emission
        """
        return pulumi.get(self, "aggregation_field")

    @property
    @pulumi.getter(name="aggregationType")
    def aggregation_type(self) -> pulumi.Output[Optional['outputs.FleetMetricAggregationType']]:
        """
        The type of the aggregation query.
        """
        return pulumi.get(self, "aggregation_type")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The creation date of a fleet metric
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of a fleet metric
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="indexName")
    def index_name(self) -> pulumi.Output[Optional[str]]:
        """
        The index name of a fleet metric
        """
        return pulumi.get(self, "index_name")

    @property
    @pulumi.getter(name="lastModifiedDate")
    def last_modified_date(self) -> pulumi.Output[str]:
        """
        The last modified date of a fleet metric
        """
        return pulumi.get(self, "last_modified_date")

    @property
    @pulumi.getter(name="metricArn")
    def metric_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Number (ARN) of a fleet metric metric
        """
        return pulumi.get(self, "metric_arn")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> pulumi.Output[str]:
        """
        The name of the fleet metric
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def period(self) -> pulumi.Output[Optional[int]]:
        """
        The period of metric emission in seconds
        """
        return pulumi.get(self, "period")

    @property
    @pulumi.getter(name="queryString")
    def query_string(self) -> pulumi.Output[Optional[str]]:
        """
        The Fleet Indexing query used by a fleet metric
        """
        return pulumi.get(self, "query_string")

    @property
    @pulumi.getter(name="queryVersion")
    def query_version(self) -> pulumi.Output[Optional[str]]:
        """
        The version of a Fleet Indexing query used by a fleet metric
        """
        return pulumi.get(self, "query_version")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        An array of key-value pairs to apply to this resource
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def unit(self) -> pulumi.Output[Optional[str]]:
        """
        The unit of data points emitted by a fleet metric
        """
        return pulumi.get(self, "unit")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[float]:
        """
        The version of a fleet metric
        """
        return pulumi.get(self, "version")

