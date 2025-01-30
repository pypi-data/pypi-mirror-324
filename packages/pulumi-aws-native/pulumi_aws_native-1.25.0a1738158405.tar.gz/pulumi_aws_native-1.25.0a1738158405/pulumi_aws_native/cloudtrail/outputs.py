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
    'ChannelDestination',
    'DashboardRefreshSchedule',
    'DashboardRefreshScheduleFrequencyProperties',
    'DashboardWidget',
    'EventDataStoreAdvancedEventSelector',
    'EventDataStoreAdvancedFieldSelector',
    'EventDataStoreInsightSelector',
    'TrailAdvancedEventSelector',
    'TrailAdvancedFieldSelector',
    'TrailDataResource',
    'TrailEventSelector',
    'TrailInsightSelector',
]

@pulumi.output_type
class ChannelDestination(dict):
    """
    The resource that receives events arriving from a channel.
    """
    def __init__(__self__, *,
                 location: str,
                 type: 'ChannelDestinationType'):
        """
        The resource that receives events arriving from a channel.
        :param str location: The ARN of a resource that receives events from a channel.
        :param 'ChannelDestinationType' type: The type of destination for events arriving from a channel.
        """
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The ARN of a resource that receives events from a channel.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def type(self) -> 'ChannelDestinationType':
        """
        The type of destination for events arriving from a channel.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class DashboardRefreshSchedule(dict):
    """
    Configures the automatic refresh schedule for the dashboard. Includes the frequency unit (DAYS or HOURS) and value, as well as the status (ENABLED or DISABLED) of the refresh schedule.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "timeOfDay":
            suggest = "time_of_day"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DashboardRefreshSchedule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DashboardRefreshSchedule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DashboardRefreshSchedule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 frequency: Optional['outputs.DashboardRefreshScheduleFrequencyProperties'] = None,
                 status: Optional['DashboardRefreshScheduleStatus'] = None,
                 time_of_day: Optional[str] = None):
        """
        Configures the automatic refresh schedule for the dashboard. Includes the frequency unit (DAYS or HOURS) and value, as well as the status (ENABLED or DISABLED) of the refresh schedule.
        :param 'DashboardRefreshScheduleFrequencyProperties' frequency: The frequency at which you want the dashboard refreshed.
        :param 'DashboardRefreshScheduleStatus' status: The status of the schedule. Supported values are ENABLED and DISABLED.
        :param str time_of_day: StartTime of the automatic schedule refresh.
        """
        if frequency is not None:
            pulumi.set(__self__, "frequency", frequency)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if time_of_day is not None:
            pulumi.set(__self__, "time_of_day", time_of_day)

    @property
    @pulumi.getter
    def frequency(self) -> Optional['outputs.DashboardRefreshScheduleFrequencyProperties']:
        """
        The frequency at which you want the dashboard refreshed.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def status(self) -> Optional['DashboardRefreshScheduleStatus']:
        """
        The status of the schedule. Supported values are ENABLED and DISABLED.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="timeOfDay")
    def time_of_day(self) -> Optional[str]:
        """
        StartTime of the automatic schedule refresh.
        """
        return pulumi.get(self, "time_of_day")


@pulumi.output_type
class DashboardRefreshScheduleFrequencyProperties(dict):
    """
    The frequency at which you want the dashboard refreshed.
    """
    def __init__(__self__, *,
                 unit: 'DashboardRefreshScheduleFrequencyPropertiesUnit',
                 value: int):
        """
        The frequency at which you want the dashboard refreshed.
        :param 'DashboardRefreshScheduleFrequencyPropertiesUnit' unit: The frequency unit. Supported values are HOURS and DAYS.
        :param int value: The frequency value.
        """
        pulumi.set(__self__, "unit", unit)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def unit(self) -> 'DashboardRefreshScheduleFrequencyPropertiesUnit':
        """
        The frequency unit. Supported values are HOURS and DAYS.
        """
        return pulumi.get(self, "unit")

    @property
    @pulumi.getter
    def value(self) -> int:
        """
        The frequency value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class DashboardWidget(dict):
    """
    The dashboard widget
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "queryStatement":
            suggest = "query_statement"
        elif key == "queryParameters":
            suggest = "query_parameters"
        elif key == "viewProperties":
            suggest = "view_properties"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DashboardWidget. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DashboardWidget.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DashboardWidget.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 query_statement: str,
                 query_parameters: Optional[Sequence[str]] = None,
                 view_properties: Optional[Mapping[str, str]] = None):
        """
        The dashboard widget
        :param str query_statement: The SQL query statement on one or more event data stores.
        :param Sequence[str] query_parameters: The placeholder keys in the QueryStatement. For example: $StartTime$, $EndTime$, $Period$.
        :param Mapping[str, str] view_properties: The view properties of the widget.
        """
        pulumi.set(__self__, "query_statement", query_statement)
        if query_parameters is not None:
            pulumi.set(__self__, "query_parameters", query_parameters)
        if view_properties is not None:
            pulumi.set(__self__, "view_properties", view_properties)

    @property
    @pulumi.getter(name="queryStatement")
    def query_statement(self) -> str:
        """
        The SQL query statement on one or more event data stores.
        """
        return pulumi.get(self, "query_statement")

    @property
    @pulumi.getter(name="queryParameters")
    def query_parameters(self) -> Optional[Sequence[str]]:
        """
        The placeholder keys in the QueryStatement. For example: $StartTime$, $EndTime$, $Period$.
        """
        return pulumi.get(self, "query_parameters")

    @property
    @pulumi.getter(name="viewProperties")
    def view_properties(self) -> Optional[Mapping[str, str]]:
        """
        The view properties of the widget.
        """
        return pulumi.get(self, "view_properties")


@pulumi.output_type
class EventDataStoreAdvancedEventSelector(dict):
    """
    Advanced event selectors let you create fine-grained selectors for the following AWS CloudTrail event record ﬁelds. They help you control costs by logging only those events that are important to you.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fieldSelectors":
            suggest = "field_selectors"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventDataStoreAdvancedEventSelector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventDataStoreAdvancedEventSelector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EventDataStoreAdvancedEventSelector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 field_selectors: Sequence['outputs.EventDataStoreAdvancedFieldSelector'],
                 name: Optional[str] = None):
        """
        Advanced event selectors let you create fine-grained selectors for the following AWS CloudTrail event record ﬁelds. They help you control costs by logging only those events that are important to you.
        :param Sequence['EventDataStoreAdvancedFieldSelector'] field_selectors: Contains all selector statements in an advanced event selector.
        :param str name: An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".
        """
        pulumi.set(__self__, "field_selectors", field_selectors)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="fieldSelectors")
    def field_selectors(self) -> Sequence['outputs.EventDataStoreAdvancedFieldSelector']:
        """
        Contains all selector statements in an advanced event selector.
        """
        return pulumi.get(self, "field_selectors")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class EventDataStoreAdvancedFieldSelector(dict):
    """
    A single selector statement in an advanced event selector.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endsWith":
            suggest = "ends_with"
        elif key == "notEndsWith":
            suggest = "not_ends_with"
        elif key == "notEquals":
            suggest = "not_equals"
        elif key == "notStartsWith":
            suggest = "not_starts_with"
        elif key == "startsWith":
            suggest = "starts_with"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventDataStoreAdvancedFieldSelector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventDataStoreAdvancedFieldSelector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EventDataStoreAdvancedFieldSelector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 field: str,
                 ends_with: Optional[Sequence[str]] = None,
                 equals: Optional[Sequence[str]] = None,
                 not_ends_with: Optional[Sequence[str]] = None,
                 not_equals: Optional[Sequence[str]] = None,
                 not_starts_with: Optional[Sequence[str]] = None,
                 starts_with: Optional[Sequence[str]] = None):
        """
        A single selector statement in an advanced event selector.
        :param str field: A field in an event record on which to filter events to be logged. Supported fields include readOnly, eventCategory, eventSource (for management events), eventName, resources.type, and resources.ARN.
        :param Sequence[str] ends_with: An operator that includes events that match the last few characters of the event record field specified as the value of Field.
        :param Sequence[str] equals: An operator that includes events that match the exact value of the event record field specified as the value of Field. This is the only valid operator that you can use with the readOnly, eventCategory, and resources.type fields.
        :param Sequence[str] not_ends_with: An operator that excludes events that match the last few characters of the event record field specified as the value of Field.
        :param Sequence[str] not_equals: An operator that excludes events that match the exact value of the event record field specified as the value of Field.
        :param Sequence[str] not_starts_with: An operator that excludes events that match the first few characters of the event record field specified as the value of Field.
        :param Sequence[str] starts_with: An operator that includes events that match the first few characters of the event record field specified as the value of Field.
        """
        pulumi.set(__self__, "field", field)
        if ends_with is not None:
            pulumi.set(__self__, "ends_with", ends_with)
        if equals is not None:
            pulumi.set(__self__, "equals", equals)
        if not_ends_with is not None:
            pulumi.set(__self__, "not_ends_with", not_ends_with)
        if not_equals is not None:
            pulumi.set(__self__, "not_equals", not_equals)
        if not_starts_with is not None:
            pulumi.set(__self__, "not_starts_with", not_starts_with)
        if starts_with is not None:
            pulumi.set(__self__, "starts_with", starts_with)

    @property
    @pulumi.getter
    def field(self) -> str:
        """
        A field in an event record on which to filter events to be logged. Supported fields include readOnly, eventCategory, eventSource (for management events), eventName, resources.type, and resources.ARN.
        """
        return pulumi.get(self, "field")

    @property
    @pulumi.getter(name="endsWith")
    def ends_with(self) -> Optional[Sequence[str]]:
        """
        An operator that includes events that match the last few characters of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "ends_with")

    @property
    @pulumi.getter
    def equals(self) -> Optional[Sequence[str]]:
        """
        An operator that includes events that match the exact value of the event record field specified as the value of Field. This is the only valid operator that you can use with the readOnly, eventCategory, and resources.type fields.
        """
        return pulumi.get(self, "equals")

    @property
    @pulumi.getter(name="notEndsWith")
    def not_ends_with(self) -> Optional[Sequence[str]]:
        """
        An operator that excludes events that match the last few characters of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "not_ends_with")

    @property
    @pulumi.getter(name="notEquals")
    def not_equals(self) -> Optional[Sequence[str]]:
        """
        An operator that excludes events that match the exact value of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "not_equals")

    @property
    @pulumi.getter(name="notStartsWith")
    def not_starts_with(self) -> Optional[Sequence[str]]:
        """
        An operator that excludes events that match the first few characters of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "not_starts_with")

    @property
    @pulumi.getter(name="startsWith")
    def starts_with(self) -> Optional[Sequence[str]]:
        """
        An operator that includes events that match the first few characters of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "starts_with")


@pulumi.output_type
class EventDataStoreInsightSelector(dict):
    """
    A string that contains Insights types that are logged on an event data store.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "insightType":
            suggest = "insight_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventDataStoreInsightSelector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventDataStoreInsightSelector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EventDataStoreInsightSelector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 insight_type: Optional[str] = None):
        """
        A string that contains Insights types that are logged on an event data store.
        :param str insight_type: The type of Insights to log on an event data store.
        """
        if insight_type is not None:
            pulumi.set(__self__, "insight_type", insight_type)

    @property
    @pulumi.getter(name="insightType")
    def insight_type(self) -> Optional[str]:
        """
        The type of Insights to log on an event data store.
        """
        return pulumi.get(self, "insight_type")


@pulumi.output_type
class TrailAdvancedEventSelector(dict):
    """
    Advanced event selectors let you create fine-grained selectors for the following AWS CloudTrail event record ﬁelds. They help you control costs by logging only those events that are important to you.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fieldSelectors":
            suggest = "field_selectors"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TrailAdvancedEventSelector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TrailAdvancedEventSelector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TrailAdvancedEventSelector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 field_selectors: Sequence['outputs.TrailAdvancedFieldSelector'],
                 name: Optional[str] = None):
        """
        Advanced event selectors let you create fine-grained selectors for the following AWS CloudTrail event record ﬁelds. They help you control costs by logging only those events that are important to you.
        :param Sequence['TrailAdvancedFieldSelector'] field_selectors: Contains all selector statements in an advanced event selector.
        :param str name: An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".
        """
        pulumi.set(__self__, "field_selectors", field_selectors)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="fieldSelectors")
    def field_selectors(self) -> Sequence['outputs.TrailAdvancedFieldSelector']:
        """
        Contains all selector statements in an advanced event selector.
        """
        return pulumi.get(self, "field_selectors")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class TrailAdvancedFieldSelector(dict):
    """
    A single selector statement in an advanced event selector.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endsWith":
            suggest = "ends_with"
        elif key == "notEndsWith":
            suggest = "not_ends_with"
        elif key == "notEquals":
            suggest = "not_equals"
        elif key == "notStartsWith":
            suggest = "not_starts_with"
        elif key == "startsWith":
            suggest = "starts_with"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TrailAdvancedFieldSelector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TrailAdvancedFieldSelector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TrailAdvancedFieldSelector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 field: str,
                 ends_with: Optional[Sequence[str]] = None,
                 equals: Optional[Sequence[str]] = None,
                 not_ends_with: Optional[Sequence[str]] = None,
                 not_equals: Optional[Sequence[str]] = None,
                 not_starts_with: Optional[Sequence[str]] = None,
                 starts_with: Optional[Sequence[str]] = None):
        """
        A single selector statement in an advanced event selector.
        :param str field: A field in an event record on which to filter events to be logged. Supported fields include readOnly, eventCategory, eventSource (for management events), eventName, resources.type, and resources.ARN.
        :param Sequence[str] ends_with: An operator that includes events that match the last few characters of the event record field specified as the value of Field.
        :param Sequence[str] equals: An operator that includes events that match the exact value of the event record field specified as the value of Field. This is the only valid operator that you can use with the readOnly, eventCategory, and resources.type fields.
        :param Sequence[str] not_ends_with: An operator that excludes events that match the last few characters of the event record field specified as the value of Field.
        :param Sequence[str] not_equals: An operator that excludes events that match the exact value of the event record field specified as the value of Field.
        :param Sequence[str] not_starts_with: An operator that excludes events that match the first few characters of the event record field specified as the value of Field.
        :param Sequence[str] starts_with: An operator that includes events that match the first few characters of the event record field specified as the value of Field.
        """
        pulumi.set(__self__, "field", field)
        if ends_with is not None:
            pulumi.set(__self__, "ends_with", ends_with)
        if equals is not None:
            pulumi.set(__self__, "equals", equals)
        if not_ends_with is not None:
            pulumi.set(__self__, "not_ends_with", not_ends_with)
        if not_equals is not None:
            pulumi.set(__self__, "not_equals", not_equals)
        if not_starts_with is not None:
            pulumi.set(__self__, "not_starts_with", not_starts_with)
        if starts_with is not None:
            pulumi.set(__self__, "starts_with", starts_with)

    @property
    @pulumi.getter
    def field(self) -> str:
        """
        A field in an event record on which to filter events to be logged. Supported fields include readOnly, eventCategory, eventSource (for management events), eventName, resources.type, and resources.ARN.
        """
        return pulumi.get(self, "field")

    @property
    @pulumi.getter(name="endsWith")
    def ends_with(self) -> Optional[Sequence[str]]:
        """
        An operator that includes events that match the last few characters of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "ends_with")

    @property
    @pulumi.getter
    def equals(self) -> Optional[Sequence[str]]:
        """
        An operator that includes events that match the exact value of the event record field specified as the value of Field. This is the only valid operator that you can use with the readOnly, eventCategory, and resources.type fields.
        """
        return pulumi.get(self, "equals")

    @property
    @pulumi.getter(name="notEndsWith")
    def not_ends_with(self) -> Optional[Sequence[str]]:
        """
        An operator that excludes events that match the last few characters of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "not_ends_with")

    @property
    @pulumi.getter(name="notEquals")
    def not_equals(self) -> Optional[Sequence[str]]:
        """
        An operator that excludes events that match the exact value of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "not_equals")

    @property
    @pulumi.getter(name="notStartsWith")
    def not_starts_with(self) -> Optional[Sequence[str]]:
        """
        An operator that excludes events that match the first few characters of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "not_starts_with")

    @property
    @pulumi.getter(name="startsWith")
    def starts_with(self) -> Optional[Sequence[str]]:
        """
        An operator that includes events that match the first few characters of the event record field specified as the value of Field.
        """
        return pulumi.get(self, "starts_with")


@pulumi.output_type
class TrailDataResource(dict):
    """
    CloudTrail supports data event logging for Amazon S3 objects and AWS Lambda functions. You can specify up to 250 resources for an individual event selector, but the total number of data resources cannot exceed 250 across all event selectors in a trail. This limit does not apply if you configure resource logging for all data events.
    """
    def __init__(__self__, *,
                 type: str,
                 values: Optional[Sequence[str]] = None):
        """
        CloudTrail supports data event logging for Amazon S3 objects and AWS Lambda functions. You can specify up to 250 resources for an individual event selector, but the total number of data resources cannot exceed 250 across all event selectors in a trail. This limit does not apply if you configure resource logging for all data events.
        :param str type: The resource type in which you want to log data events. You can specify AWS::S3::Object or AWS::Lambda::Function resources.
        :param Sequence[str] values: An array of Amazon Resource Name (ARN) strings or partial ARN strings for the specified objects.
        """
        pulumi.set(__self__, "type", type)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type in which you want to log data events. You can specify AWS::S3::Object or AWS::Lambda::Function resources.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        An array of Amazon Resource Name (ARN) strings or partial ARN strings for the specified objects.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class TrailEventSelector(dict):
    """
    The type of email sending events to publish to the event destination.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dataResources":
            suggest = "data_resources"
        elif key == "excludeManagementEventSources":
            suggest = "exclude_management_event_sources"
        elif key == "includeManagementEvents":
            suggest = "include_management_events"
        elif key == "readWriteType":
            suggest = "read_write_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TrailEventSelector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TrailEventSelector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TrailEventSelector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 data_resources: Optional[Sequence['outputs.TrailDataResource']] = None,
                 exclude_management_event_sources: Optional[Sequence[str]] = None,
                 include_management_events: Optional[bool] = None,
                 read_write_type: Optional['TrailEventSelectorReadWriteType'] = None):
        """
        The type of email sending events to publish to the event destination.
        :param Sequence['TrailDataResource'] data_resources: CloudTrail supports data event logging for Amazon S3 objects in standard S3 buckets, AWS Lambda functions, and Amazon DynamoDB tables with basic event selectors. You can specify up to 250 resources for an individual event selector, but the total number of data resources cannot exceed 250 across all event selectors in a trail. This limit does not apply if you configure resource logging for all data events.
               
               For more information, see [Data Events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html) and [Limits in AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/WhatIsCloudTrail-Limits.html) in the *AWS CloudTrail User Guide* .
               
               > To log data events for all other resource types including objects stored in [directory buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-overview.html) , you must use [AdvancedEventSelectors](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_AdvancedEventSelector.html) . You must also use `AdvancedEventSelectors` if you want to filter on the `eventName` field.
        :param Sequence[str] exclude_management_event_sources: An optional list of service event sources from which you do not want management events to be logged on your trail. In this release, the list can be empty (disables the filter), or it can filter out AWS Key Management Service events by containing "kms.amazonaws.com". By default, ExcludeManagementEventSources is empty, and AWS KMS events are included in events that are logged to your trail.
        :param bool include_management_events: Specify if you want your event selector to include management events for your trail.
        :param 'TrailEventSelectorReadWriteType' read_write_type: Specify if you want your trail to log read-only events, write-only events, or all. For example, the EC2 GetConsoleOutput is a read-only API operation and RunInstances is a write-only API operation.
        """
        if data_resources is not None:
            pulumi.set(__self__, "data_resources", data_resources)
        if exclude_management_event_sources is not None:
            pulumi.set(__self__, "exclude_management_event_sources", exclude_management_event_sources)
        if include_management_events is not None:
            pulumi.set(__self__, "include_management_events", include_management_events)
        if read_write_type is not None:
            pulumi.set(__self__, "read_write_type", read_write_type)

    @property
    @pulumi.getter(name="dataResources")
    def data_resources(self) -> Optional[Sequence['outputs.TrailDataResource']]:
        """
        CloudTrail supports data event logging for Amazon S3 objects in standard S3 buckets, AWS Lambda functions, and Amazon DynamoDB tables with basic event selectors. You can specify up to 250 resources for an individual event selector, but the total number of data resources cannot exceed 250 across all event selectors in a trail. This limit does not apply if you configure resource logging for all data events.

        For more information, see [Data Events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html) and [Limits in AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/WhatIsCloudTrail-Limits.html) in the *AWS CloudTrail User Guide* .

        > To log data events for all other resource types including objects stored in [directory buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-overview.html) , you must use [AdvancedEventSelectors](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_AdvancedEventSelector.html) . You must also use `AdvancedEventSelectors` if you want to filter on the `eventName` field.
        """
        return pulumi.get(self, "data_resources")

    @property
    @pulumi.getter(name="excludeManagementEventSources")
    def exclude_management_event_sources(self) -> Optional[Sequence[str]]:
        """
        An optional list of service event sources from which you do not want management events to be logged on your trail. In this release, the list can be empty (disables the filter), or it can filter out AWS Key Management Service events by containing "kms.amazonaws.com". By default, ExcludeManagementEventSources is empty, and AWS KMS events are included in events that are logged to your trail.
        """
        return pulumi.get(self, "exclude_management_event_sources")

    @property
    @pulumi.getter(name="includeManagementEvents")
    def include_management_events(self) -> Optional[bool]:
        """
        Specify if you want your event selector to include management events for your trail.
        """
        return pulumi.get(self, "include_management_events")

    @property
    @pulumi.getter(name="readWriteType")
    def read_write_type(self) -> Optional['TrailEventSelectorReadWriteType']:
        """
        Specify if you want your trail to log read-only events, write-only events, or all. For example, the EC2 GetConsoleOutput is a read-only API operation and RunInstances is a write-only API operation.
        """
        return pulumi.get(self, "read_write_type")


@pulumi.output_type
class TrailInsightSelector(dict):
    """
    A string that contains insight types that are logged on a trail.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "insightType":
            suggest = "insight_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TrailInsightSelector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TrailInsightSelector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TrailInsightSelector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 insight_type: Optional[str] = None):
        """
        A string that contains insight types that are logged on a trail.
        :param str insight_type: The type of insight to log on a trail.
        """
        if insight_type is not None:
            pulumi.set(__self__, "insight_type", insight_type)

    @property
    @pulumi.getter(name="insightType")
    def insight_type(self) -> Optional[str]:
        """
        The type of insight to log on a trail.
        """
        return pulumi.get(self, "insight_type")


