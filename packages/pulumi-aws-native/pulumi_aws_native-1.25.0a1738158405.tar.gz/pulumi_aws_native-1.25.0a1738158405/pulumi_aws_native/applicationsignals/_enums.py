# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ServiceLevelObjectiveDurationUnit',
    'ServiceLevelObjectiveEvaluationType',
    'ServiceLevelObjectiveRequestBasedSliComparisonOperator',
    'ServiceLevelObjectiveRequestBasedSliMetricMetricType',
    'ServiceLevelObjectiveSliComparisonOperator',
    'ServiceLevelObjectiveSliMetricMetricType',
]


class ServiceLevelObjectiveDurationUnit(str, Enum):
    """
    Specifies the calendar interval unit.
    """
    DAY = "DAY"
    MONTH = "MONTH"


class ServiceLevelObjectiveEvaluationType(str, Enum):
    """
    Displays whether this is a period-based SLO or a request-based SLO.
    """
    PERIOD_BASED = "PeriodBased"
    REQUEST_BASED = "RequestBased"


class ServiceLevelObjectiveRequestBasedSliComparisonOperator(str, Enum):
    """
    The arithmetic operation used when comparing the specified metric to the threshold.
    """
    GREATER_THAN_OR_EQUAL_TO = "GreaterThanOrEqualTo"
    LESS_THAN_OR_EQUAL_TO = "LessThanOrEqualTo"
    LESS_THAN = "LessThan"
    GREATER_THAN = "GreaterThan"


class ServiceLevelObjectiveRequestBasedSliMetricMetricType(str, Enum):
    """
    If the SLO monitors either the LATENCY or AVAILABILITY metric that Application Signals collects, this field displays which of those metrics is used.
    """
    LATENCY = "LATENCY"
    AVAILABILITY = "AVAILABILITY"


class ServiceLevelObjectiveSliComparisonOperator(str, Enum):
    """
    The arithmetic operation used when comparing the specified metric to the threshold.
    """
    GREATER_THAN_OR_EQUAL_TO = "GreaterThanOrEqualTo"
    LESS_THAN_OR_EQUAL_TO = "LessThanOrEqualTo"
    LESS_THAN = "LessThan"
    GREATER_THAN = "GreaterThan"


class ServiceLevelObjectiveSliMetricMetricType(str, Enum):
    """
    If the SLO monitors either the LATENCY or AVAILABILITY metric that Application Signals collects, this field displays which of those metrics is used.
    """
    LATENCY = "LATENCY"
    AVAILABILITY = "AVAILABILITY"
