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
    'MonitorHealthEventsConfig',
    'MonitorInternetMeasurementsLogDelivery',
    'MonitorLocalHealthEventsConfig',
    'MonitorS3Config',
]

@pulumi.output_type
class MonitorHealthEventsConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "availabilityLocalHealthEventsConfig":
            suggest = "availability_local_health_events_config"
        elif key == "availabilityScoreThreshold":
            suggest = "availability_score_threshold"
        elif key == "performanceLocalHealthEventsConfig":
            suggest = "performance_local_health_events_config"
        elif key == "performanceScoreThreshold":
            suggest = "performance_score_threshold"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorHealthEventsConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorHealthEventsConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorHealthEventsConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 availability_local_health_events_config: Optional['outputs.MonitorLocalHealthEventsConfig'] = None,
                 availability_score_threshold: Optional[float] = None,
                 performance_local_health_events_config: Optional['outputs.MonitorLocalHealthEventsConfig'] = None,
                 performance_score_threshold: Optional[float] = None):
        """
        :param 'MonitorLocalHealthEventsConfig' availability_local_health_events_config: The configuration that determines the threshold and other conditions for when Internet Monitor creates a health event for a local availability issue.
        :param float availability_score_threshold: The health event threshold percentage set for availability scores. When the overall availability score is at or below this percentage, Internet Monitor creates a health event.
        :param 'MonitorLocalHealthEventsConfig' performance_local_health_events_config: The configuration that determines the threshold and other conditions for when Internet Monitor creates a health event for a local performance issue.
        :param float performance_score_threshold: The health event threshold percentage set for performance scores. When the overall performance score is at or below this percentage, Internet Monitor creates a health event.
        """
        if availability_local_health_events_config is not None:
            pulumi.set(__self__, "availability_local_health_events_config", availability_local_health_events_config)
        if availability_score_threshold is not None:
            pulumi.set(__self__, "availability_score_threshold", availability_score_threshold)
        if performance_local_health_events_config is not None:
            pulumi.set(__self__, "performance_local_health_events_config", performance_local_health_events_config)
        if performance_score_threshold is not None:
            pulumi.set(__self__, "performance_score_threshold", performance_score_threshold)

    @property
    @pulumi.getter(name="availabilityLocalHealthEventsConfig")
    def availability_local_health_events_config(self) -> Optional['outputs.MonitorLocalHealthEventsConfig']:
        """
        The configuration that determines the threshold and other conditions for when Internet Monitor creates a health event for a local availability issue.
        """
        return pulumi.get(self, "availability_local_health_events_config")

    @property
    @pulumi.getter(name="availabilityScoreThreshold")
    def availability_score_threshold(self) -> Optional[float]:
        """
        The health event threshold percentage set for availability scores. When the overall availability score is at or below this percentage, Internet Monitor creates a health event.
        """
        return pulumi.get(self, "availability_score_threshold")

    @property
    @pulumi.getter(name="performanceLocalHealthEventsConfig")
    def performance_local_health_events_config(self) -> Optional['outputs.MonitorLocalHealthEventsConfig']:
        """
        The configuration that determines the threshold and other conditions for when Internet Monitor creates a health event for a local performance issue.
        """
        return pulumi.get(self, "performance_local_health_events_config")

    @property
    @pulumi.getter(name="performanceScoreThreshold")
    def performance_score_threshold(self) -> Optional[float]:
        """
        The health event threshold percentage set for performance scores. When the overall performance score is at or below this percentage, Internet Monitor creates a health event.
        """
        return pulumi.get(self, "performance_score_threshold")


@pulumi.output_type
class MonitorInternetMeasurementsLogDelivery(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "s3Config":
            suggest = "s3_config"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorInternetMeasurementsLogDelivery. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorInternetMeasurementsLogDelivery.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorInternetMeasurementsLogDelivery.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 s3_config: Optional['outputs.MonitorS3Config'] = None):
        """
        :param 'MonitorS3Config' s3_config: The configuration for publishing Amazon CloudWatch Internet Monitor internet measurements to Amazon S3.
        """
        if s3_config is not None:
            pulumi.set(__self__, "s3_config", s3_config)

    @property
    @pulumi.getter(name="s3Config")
    def s3_config(self) -> Optional['outputs.MonitorS3Config']:
        """
        The configuration for publishing Amazon CloudWatch Internet Monitor internet measurements to Amazon S3.
        """
        return pulumi.get(self, "s3_config")


@pulumi.output_type
class MonitorLocalHealthEventsConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "healthScoreThreshold":
            suggest = "health_score_threshold"
        elif key == "minTrafficImpact":
            suggest = "min_traffic_impact"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorLocalHealthEventsConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorLocalHealthEventsConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorLocalHealthEventsConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 health_score_threshold: Optional[float] = None,
                 min_traffic_impact: Optional[float] = None,
                 status: Optional['MonitorLocalHealthEventsConfigStatus'] = None):
        """
        :param float health_score_threshold: The health event threshold percentage set for a local health score.
        :param float min_traffic_impact: The minimum percentage of overall traffic for an application that must be impacted by an issue before Internet Monitor creates an event when a threshold is crossed for a local health score.
               
               If you don't set a minimum traffic impact threshold, the default value is 0.01%.
        :param 'MonitorLocalHealthEventsConfigStatus' status: The status of whether Internet Monitor creates a health event based on a threshold percentage set for a local health score. The status can be `ENABLED` or `DISABLED` .
        """
        if health_score_threshold is not None:
            pulumi.set(__self__, "health_score_threshold", health_score_threshold)
        if min_traffic_impact is not None:
            pulumi.set(__self__, "min_traffic_impact", min_traffic_impact)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="healthScoreThreshold")
    def health_score_threshold(self) -> Optional[float]:
        """
        The health event threshold percentage set for a local health score.
        """
        return pulumi.get(self, "health_score_threshold")

    @property
    @pulumi.getter(name="minTrafficImpact")
    def min_traffic_impact(self) -> Optional[float]:
        """
        The minimum percentage of overall traffic for an application that must be impacted by an issue before Internet Monitor creates an event when a threshold is crossed for a local health score.

        If you don't set a minimum traffic impact threshold, the default value is 0.01%.
        """
        return pulumi.get(self, "min_traffic_impact")

    @property
    @pulumi.getter
    def status(self) -> Optional['MonitorLocalHealthEventsConfigStatus']:
        """
        The status of whether Internet Monitor creates a health event based on a threshold percentage set for a local health score. The status can be `ENABLED` or `DISABLED` .
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class MonitorS3Config(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"
        elif key == "bucketPrefix":
            suggest = "bucket_prefix"
        elif key == "logDeliveryStatus":
            suggest = "log_delivery_status"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorS3Config. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorS3Config.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorS3Config.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_name: Optional[str] = None,
                 bucket_prefix: Optional[str] = None,
                 log_delivery_status: Optional['MonitorS3ConfigLogDeliveryStatus'] = None):
        """
        :param str bucket_name: The Amazon S3 bucket name for internet measurements publishing.
        :param str bucket_prefix: An optional Amazon S3 bucket prefix for internet measurements publishing.
        :param 'MonitorS3ConfigLogDeliveryStatus' log_delivery_status: The status of publishing Internet Monitor internet measurements to an Amazon S3 bucket. The delivery status is `ENABLED` if you choose to deliver internet measurements to an S3 bucket, and `DISABLED` otherwise.
        """
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if bucket_prefix is not None:
            pulumi.set(__self__, "bucket_prefix", bucket_prefix)
        if log_delivery_status is not None:
            pulumi.set(__self__, "log_delivery_status", log_delivery_status)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[str]:
        """
        The Amazon S3 bucket name for internet measurements publishing.
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter(name="bucketPrefix")
    def bucket_prefix(self) -> Optional[str]:
        """
        An optional Amazon S3 bucket prefix for internet measurements publishing.
        """
        return pulumi.get(self, "bucket_prefix")

    @property
    @pulumi.getter(name="logDeliveryStatus")
    def log_delivery_status(self) -> Optional['MonitorS3ConfigLogDeliveryStatus']:
        """
        The status of publishing Internet Monitor internet measurements to an Amazon S3 bucket. The delivery status is `ENABLED` if you choose to deliver internet measurements to an S3 bucket, and `DISABLED` otherwise.
        """
        return pulumi.get(self, "log_delivery_status")


