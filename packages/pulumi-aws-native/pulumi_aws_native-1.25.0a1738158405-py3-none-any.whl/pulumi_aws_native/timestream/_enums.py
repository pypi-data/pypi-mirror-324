# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'InfluxDbInstanceDbInstanceType',
    'InfluxDbInstanceDbStorageType',
    'InfluxDbInstanceDeploymentType',
    'InfluxDbInstanceNetworkType',
    'InfluxDbInstanceStatus',
    'ScheduledQueryDimensionValueType',
    'ScheduledQueryEncryptionOption',
    'ScheduledQueryMixedMeasureMappingMeasureValueType',
    'ScheduledQueryMultiMeasureAttributeMappingMeasureValueType',
    'TablePartitionKeyEnforcementLevel',
    'TablePartitionKeyType',
]


class InfluxDbInstanceDbInstanceType(str, Enum):
    """
    The compute instance of the InfluxDB instance.
    """
    DB_INFLUX_MEDIUM = "db.influx.medium"
    DB_INFLUX_LARGE = "db.influx.large"
    DB_INFLUX_XLARGE = "db.influx.xlarge"
    DB_INFLUX2XLARGE = "db.influx.2xlarge"
    DB_INFLUX4XLARGE = "db.influx.4xlarge"
    DB_INFLUX8XLARGE = "db.influx.8xlarge"
    DB_INFLUX12XLARGE = "db.influx.12xlarge"
    DB_INFLUX16XLARGE = "db.influx.16xlarge"


class InfluxDbInstanceDbStorageType(str, Enum):
    """
    The storage type of the InfluxDB instance.
    """
    INFLUX_IO_INCLUDED_T1 = "InfluxIOIncludedT1"
    INFLUX_IO_INCLUDED_T2 = "InfluxIOIncludedT2"
    INFLUX_IO_INCLUDED_T3 = "InfluxIOIncludedT3"


class InfluxDbInstanceDeploymentType(str, Enum):
    """
    Deployment type of the InfluxDB Instance.
    """
    SINGLE_AZ = "SINGLE_AZ"
    WITH_MULTIAZ_STANDBY = "WITH_MULTIAZ_STANDBY"


class InfluxDbInstanceNetworkType(str, Enum):
    """
    Network type of the InfluxDB Instance.
    """
    IPV4 = "IPV4"
    DUAL = "DUAL"


class InfluxDbInstanceStatus(str, Enum):
    """
    Status of the InfluxDB Instance.
    """
    CREATING = "CREATING"
    AVAILABLE = "AVAILABLE"
    DELETING = "DELETING"
    MODIFYING = "MODIFYING"
    UPDATING = "UPDATING"
    UPDATING_DEPLOYMENT_TYPE = "UPDATING_DEPLOYMENT_TYPE"
    UPDATING_INSTANCE_TYPE = "UPDATING_INSTANCE_TYPE"
    DELETED = "DELETED"
    FAILED = "FAILED"


class ScheduledQueryDimensionValueType(str, Enum):
    """
    Type for the dimension.
    """
    VARCHAR = "VARCHAR"


class ScheduledQueryEncryptionOption(str, Enum):
    """
    Encryption at rest options for the error reports. If no encryption option is specified, Timestream will choose SSE_S3 as default.
    """
    SSE_S3 = "SSE_S3"
    SSE_KMS = "SSE_KMS"


class ScheduledQueryMixedMeasureMappingMeasureValueType(str, Enum):
    """
    Type of the value that is to be read from SourceColumn. If the mapping is for MULTI, use MeasureValueType.MULTI.
    """
    BIGINT = "BIGINT"
    BOOLEAN = "BOOLEAN"
    DOUBLE = "DOUBLE"
    VARCHAR = "VARCHAR"
    MULTI = "MULTI"


class ScheduledQueryMultiMeasureAttributeMappingMeasureValueType(str, Enum):
    """
    Value type of the measure value column to be read from the query result.
    """
    BIGINT = "BIGINT"
    BOOLEAN = "BOOLEAN"
    DOUBLE = "DOUBLE"
    VARCHAR = "VARCHAR"
    TIMESTAMP = "TIMESTAMP"


class TablePartitionKeyEnforcementLevel(str, Enum):
    """
    The level of enforcement for the specification of a dimension key in ingested records. Options are REQUIRED (dimension key must be specified) and OPTIONAL (dimension key does not have to be specified).
    """
    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"


class TablePartitionKeyType(str, Enum):
    """
    The type of the partition key. Options are DIMENSION (dimension key) and MEASURE (measure key).
    """
    DIMENSION = "DIMENSION"
    MEASURE = "MEASURE"
