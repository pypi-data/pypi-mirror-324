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
    'KeyspaceReplicationSpecification',
    'TableAutoScalingSetting',
    'TableAutoScalingSpecification',
    'TableBillingMode',
    'TableClusteringKeyColumn',
    'TableColumn',
    'TableEncryptionSpecification',
    'TableProvisionedThroughput',
    'TableReplicaSpecification',
    'TableScalingPolicy',
    'TableTargetTrackingScalingPolicyConfiguration',
    'TypeField',
]

@pulumi.output_type
class KeyspaceReplicationSpecification(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "regionList":
            suggest = "region_list"
        elif key == "replicationStrategy":
            suggest = "replication_strategy"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeyspaceReplicationSpecification. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeyspaceReplicationSpecification.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeyspaceReplicationSpecification.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 region_list: Optional[Sequence['KeyspaceRegionListItem']] = None,
                 replication_strategy: Optional['KeyspaceReplicationSpecificationReplicationStrategy'] = None):
        """
        :param Sequence['KeyspaceRegionListItem'] region_list: Specifies the AWS Regions that the keyspace is replicated in. You must specify at least two and up to six Regions, including the Region that the keyspace is being created in.
        :param 'KeyspaceReplicationSpecificationReplicationStrategy' replication_strategy: The options are:
               
               - `SINGLE_REGION` (optional)
               - `MULTI_REGION`
               
               If no value is specified, the default is `SINGLE_REGION` . If `MULTI_REGION` is specified, `RegionList` is required.
        """
        if region_list is not None:
            pulumi.set(__self__, "region_list", region_list)
        if replication_strategy is not None:
            pulumi.set(__self__, "replication_strategy", replication_strategy)

    @property
    @pulumi.getter(name="regionList")
    def region_list(self) -> Optional[Sequence['KeyspaceRegionListItem']]:
        """
        Specifies the AWS Regions that the keyspace is replicated in. You must specify at least two and up to six Regions, including the Region that the keyspace is being created in.
        """
        return pulumi.get(self, "region_list")

    @property
    @pulumi.getter(name="replicationStrategy")
    def replication_strategy(self) -> Optional['KeyspaceReplicationSpecificationReplicationStrategy']:
        """
        The options are:

        - `SINGLE_REGION` (optional)
        - `MULTI_REGION`

        If no value is specified, the default is `SINGLE_REGION` . If `MULTI_REGION` is specified, `RegionList` is required.
        """
        return pulumi.get(self, "replication_strategy")


@pulumi.output_type
class TableAutoScalingSetting(dict):
    """
    Represents configuration for auto scaling.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoScalingDisabled":
            suggest = "auto_scaling_disabled"
        elif key == "maximumUnits":
            suggest = "maximum_units"
        elif key == "minimumUnits":
            suggest = "minimum_units"
        elif key == "scalingPolicy":
            suggest = "scaling_policy"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableAutoScalingSetting. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableAutoScalingSetting.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableAutoScalingSetting.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_scaling_disabled: Optional[bool] = None,
                 maximum_units: Optional[int] = None,
                 minimum_units: Optional[int] = None,
                 scaling_policy: Optional['outputs.TableScalingPolicy'] = None):
        """
        Represents configuration for auto scaling.
        :param bool auto_scaling_disabled: This optional parameter enables auto scaling for the table if set to `false` .
        :param int maximum_units: Manage costs by specifying the maximum amount of throughput to provision. The value must be between 1 and the max throughput per second quota for your account (40,000 by default).
        :param int minimum_units: The minimum level of throughput the table should always be ready to support. The value must be between 1 and the max throughput per second quota for your account (40,000 by default).
        :param 'TableScalingPolicy' scaling_policy: Amazon Keyspaces supports the `target tracking` auto scaling policy. With this policy, Amazon Keyspaces auto scaling ensures that the table's ratio of consumed to provisioned capacity stays at or near the target value that you specify. You define the target value as a percentage between 20 and 90.
        """
        if auto_scaling_disabled is not None:
            pulumi.set(__self__, "auto_scaling_disabled", auto_scaling_disabled)
        if maximum_units is not None:
            pulumi.set(__self__, "maximum_units", maximum_units)
        if minimum_units is not None:
            pulumi.set(__self__, "minimum_units", minimum_units)
        if scaling_policy is not None:
            pulumi.set(__self__, "scaling_policy", scaling_policy)

    @property
    @pulumi.getter(name="autoScalingDisabled")
    def auto_scaling_disabled(self) -> Optional[bool]:
        """
        This optional parameter enables auto scaling for the table if set to `false` .
        """
        return pulumi.get(self, "auto_scaling_disabled")

    @property
    @pulumi.getter(name="maximumUnits")
    def maximum_units(self) -> Optional[int]:
        """
        Manage costs by specifying the maximum amount of throughput to provision. The value must be between 1 and the max throughput per second quota for your account (40,000 by default).
        """
        return pulumi.get(self, "maximum_units")

    @property
    @pulumi.getter(name="minimumUnits")
    def minimum_units(self) -> Optional[int]:
        """
        The minimum level of throughput the table should always be ready to support. The value must be between 1 and the max throughput per second quota for your account (40,000 by default).
        """
        return pulumi.get(self, "minimum_units")

    @property
    @pulumi.getter(name="scalingPolicy")
    def scaling_policy(self) -> Optional['outputs.TableScalingPolicy']:
        """
        Amazon Keyspaces supports the `target tracking` auto scaling policy. With this policy, Amazon Keyspaces auto scaling ensures that the table's ratio of consumed to provisioned capacity stays at or near the target value that you specify. You define the target value as a percentage between 20 and 90.
        """
        return pulumi.get(self, "scaling_policy")


@pulumi.output_type
class TableAutoScalingSpecification(dict):
    """
    Represents the read and write settings used for AutoScaling.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "readCapacityAutoScaling":
            suggest = "read_capacity_auto_scaling"
        elif key == "writeCapacityAutoScaling":
            suggest = "write_capacity_auto_scaling"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableAutoScalingSpecification. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableAutoScalingSpecification.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableAutoScalingSpecification.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 read_capacity_auto_scaling: Optional['outputs.TableAutoScalingSetting'] = None,
                 write_capacity_auto_scaling: Optional['outputs.TableAutoScalingSetting'] = None):
        """
        Represents the read and write settings used for AutoScaling.
        :param 'TableAutoScalingSetting' read_capacity_auto_scaling: The auto scaling settings for the table's read capacity.
        :param 'TableAutoScalingSetting' write_capacity_auto_scaling: The auto scaling settings for the table's write capacity.
        """
        if read_capacity_auto_scaling is not None:
            pulumi.set(__self__, "read_capacity_auto_scaling", read_capacity_auto_scaling)
        if write_capacity_auto_scaling is not None:
            pulumi.set(__self__, "write_capacity_auto_scaling", write_capacity_auto_scaling)

    @property
    @pulumi.getter(name="readCapacityAutoScaling")
    def read_capacity_auto_scaling(self) -> Optional['outputs.TableAutoScalingSetting']:
        """
        The auto scaling settings for the table's read capacity.
        """
        return pulumi.get(self, "read_capacity_auto_scaling")

    @property
    @pulumi.getter(name="writeCapacityAutoScaling")
    def write_capacity_auto_scaling(self) -> Optional['outputs.TableAutoScalingSetting']:
        """
        The auto scaling settings for the table's write capacity.
        """
        return pulumi.get(self, "write_capacity_auto_scaling")


@pulumi.output_type
class TableBillingMode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisionedThroughput":
            suggest = "provisioned_throughput"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableBillingMode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableBillingMode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableBillingMode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 mode: 'TableMode',
                 provisioned_throughput: Optional['outputs.TableProvisionedThroughput'] = None):
        """
        :param 'TableMode' mode: The billing mode for the table:
               
               - On-demand mode - `ON_DEMAND`
               - Provisioned mode - `PROVISIONED`
               
               > If you choose `PROVISIONED` mode, then you also need to specify provisioned throughput (read and write capacity) for the table.
               
               Valid values: `ON_DEMAND` | `PROVISIONED`
        :param 'TableProvisionedThroughput' provisioned_throughput: The provisioned read capacity and write capacity for the table. For more information, see [Provisioned throughput capacity mode](https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html#ReadWriteCapacityMode.Provisioned) in the *Amazon Keyspaces Developer Guide* .
        """
        pulumi.set(__self__, "mode", mode)
        if provisioned_throughput is not None:
            pulumi.set(__self__, "provisioned_throughput", provisioned_throughput)

    @property
    @pulumi.getter
    def mode(self) -> 'TableMode':
        """
        The billing mode for the table:

        - On-demand mode - `ON_DEMAND`
        - Provisioned mode - `PROVISIONED`

        > If you choose `PROVISIONED` mode, then you also need to specify provisioned throughput (read and write capacity) for the table.

        Valid values: `ON_DEMAND` | `PROVISIONED`
        """
        return pulumi.get(self, "mode")

    @property
    @pulumi.getter(name="provisionedThroughput")
    def provisioned_throughput(self) -> Optional['outputs.TableProvisionedThroughput']:
        """
        The provisioned read capacity and write capacity for the table. For more information, see [Provisioned throughput capacity mode](https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html#ReadWriteCapacityMode.Provisioned) in the *Amazon Keyspaces Developer Guide* .
        """
        return pulumi.get(self, "provisioned_throughput")


@pulumi.output_type
class TableClusteringKeyColumn(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "orderBy":
            suggest = "order_by"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableClusteringKeyColumn. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableClusteringKeyColumn.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableClusteringKeyColumn.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 column: 'outputs.TableColumn',
                 order_by: Optional['TableClusteringKeyColumnOrderBy'] = None):
        """
        :param 'TableColumn' column: The name and data type of this clustering key column.
        :param 'TableClusteringKeyColumnOrderBy' order_by: The order in which this column's data is stored:
               
               - `ASC` (default) - The column's data is stored in ascending order.
               - `DESC` - The column's data is stored in descending order.
        """
        pulumi.set(__self__, "column", column)
        if order_by is not None:
            pulumi.set(__self__, "order_by", order_by)

    @property
    @pulumi.getter
    def column(self) -> 'outputs.TableColumn':
        """
        The name and data type of this clustering key column.
        """
        return pulumi.get(self, "column")

    @property
    @pulumi.getter(name="orderBy")
    def order_by(self) -> Optional['TableClusteringKeyColumnOrderBy']:
        """
        The order in which this column's data is stored:

        - `ASC` (default) - The column's data is stored in ascending order.
        - `DESC` - The column's data is stored in descending order.
        """
        return pulumi.get(self, "order_by")


@pulumi.output_type
class TableColumn(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "columnName":
            suggest = "column_name"
        elif key == "columnType":
            suggest = "column_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableColumn. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableColumn.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableColumn.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 column_name: str,
                 column_type: str):
        """
        :param str column_name: The name of the column. For more information, see [Identifiers](https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.elements.identifier) in the *Amazon Keyspaces Developer Guide* .
        :param str column_type: The data type of the column. For more information, see [Data types](https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.data-types) in the *Amazon Keyspaces Developer Guide* .
        """
        pulumi.set(__self__, "column_name", column_name)
        pulumi.set(__self__, "column_type", column_type)

    @property
    @pulumi.getter(name="columnName")
    def column_name(self) -> str:
        """
        The name of the column. For more information, see [Identifiers](https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.elements.identifier) in the *Amazon Keyspaces Developer Guide* .
        """
        return pulumi.get(self, "column_name")

    @property
    @pulumi.getter(name="columnType")
    def column_type(self) -> str:
        """
        The data type of the column. For more information, see [Data types](https://docs.aws.amazon.com/keyspaces/latest/devguide/cql.elements.html#cql.data-types) in the *Amazon Keyspaces Developer Guide* .
        """
        return pulumi.get(self, "column_type")


@pulumi.output_type
class TableEncryptionSpecification(dict):
    """
    Represents the settings used to enable server-side encryption
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "encryptionType":
            suggest = "encryption_type"
        elif key == "kmsKeyIdentifier":
            suggest = "kms_key_identifier"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableEncryptionSpecification. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableEncryptionSpecification.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableEncryptionSpecification.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 encryption_type: 'TableEncryptionType',
                 kms_key_identifier: Optional[str] = None):
        """
        Represents the settings used to enable server-side encryption
        :param 'TableEncryptionType' encryption_type: The encryption at rest options for the table.
               
               - *AWS owned key* (default) - `AWS_OWNED_KMS_KEY`
               - *Customer managed key* - `CUSTOMER_MANAGED_KMS_KEY`
               
               > If you choose `CUSTOMER_MANAGED_KMS_KEY` , a `kms_key_identifier` in the format of a key ARN is required.
               
               Valid values: `CUSTOMER_MANAGED_KMS_KEY` | `AWS_OWNED_KMS_KEY` .
        :param str kms_key_identifier: Requires a `kms_key_identifier` in the format of a key ARN.
        """
        pulumi.set(__self__, "encryption_type", encryption_type)
        if kms_key_identifier is not None:
            pulumi.set(__self__, "kms_key_identifier", kms_key_identifier)

    @property
    @pulumi.getter(name="encryptionType")
    def encryption_type(self) -> 'TableEncryptionType':
        """
        The encryption at rest options for the table.

        - *AWS owned key* (default) - `AWS_OWNED_KMS_KEY`
        - *Customer managed key* - `CUSTOMER_MANAGED_KMS_KEY`

        > If you choose `CUSTOMER_MANAGED_KMS_KEY` , a `kms_key_identifier` in the format of a key ARN is required.

        Valid values: `CUSTOMER_MANAGED_KMS_KEY` | `AWS_OWNED_KMS_KEY` .
        """
        return pulumi.get(self, "encryption_type")

    @property
    @pulumi.getter(name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> Optional[str]:
        """
        Requires a `kms_key_identifier` in the format of a key ARN.
        """
        return pulumi.get(self, "kms_key_identifier")


@pulumi.output_type
class TableProvisionedThroughput(dict):
    """
    Throughput for the specified table, which consists of values for ReadCapacityUnits and WriteCapacityUnits
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "readCapacityUnits":
            suggest = "read_capacity_units"
        elif key == "writeCapacityUnits":
            suggest = "write_capacity_units"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableProvisionedThroughput. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableProvisionedThroughput.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableProvisionedThroughput.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 read_capacity_units: int,
                 write_capacity_units: int):
        """
        Throughput for the specified table, which consists of values for ReadCapacityUnits and WriteCapacityUnits
        :param int read_capacity_units: The amount of read capacity that's provisioned for the table. For more information, see [Read/write capacity mode](https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html) in the *Amazon Keyspaces Developer Guide* .
        :param int write_capacity_units: The amount of write capacity that's provisioned for the table. For more information, see [Read/write capacity mode](https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html) in the *Amazon Keyspaces Developer Guide* .
        """
        pulumi.set(__self__, "read_capacity_units", read_capacity_units)
        pulumi.set(__self__, "write_capacity_units", write_capacity_units)

    @property
    @pulumi.getter(name="readCapacityUnits")
    def read_capacity_units(self) -> int:
        """
        The amount of read capacity that's provisioned for the table. For more information, see [Read/write capacity mode](https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html) in the *Amazon Keyspaces Developer Guide* .
        """
        return pulumi.get(self, "read_capacity_units")

    @property
    @pulumi.getter(name="writeCapacityUnits")
    def write_capacity_units(self) -> int:
        """
        The amount of write capacity that's provisioned for the table. For more information, see [Read/write capacity mode](https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.html) in the *Amazon Keyspaces Developer Guide* .
        """
        return pulumi.get(self, "write_capacity_units")


@pulumi.output_type
class TableReplicaSpecification(dict):
    """
    Represents replica specifications.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "readCapacityAutoScaling":
            suggest = "read_capacity_auto_scaling"
        elif key == "readCapacityUnits":
            suggest = "read_capacity_units"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableReplicaSpecification. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableReplicaSpecification.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableReplicaSpecification.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 region: str,
                 read_capacity_auto_scaling: Optional['outputs.TableAutoScalingSetting'] = None,
                 read_capacity_units: Optional[int] = None):
        """
        Represents replica specifications.
        :param str region: The AWS Region.
        :param 'TableAutoScalingSetting' read_capacity_auto_scaling: The read capacity auto scaling settings for the multi-Region table in the specified AWS Region.
        :param int read_capacity_units: The provisioned read capacity units for the multi-Region table in the specified AWS Region.
        """
        pulumi.set(__self__, "region", region)
        if read_capacity_auto_scaling is not None:
            pulumi.set(__self__, "read_capacity_auto_scaling", read_capacity_auto_scaling)
        if read_capacity_units is not None:
            pulumi.set(__self__, "read_capacity_units", read_capacity_units)

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        The AWS Region.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="readCapacityAutoScaling")
    def read_capacity_auto_scaling(self) -> Optional['outputs.TableAutoScalingSetting']:
        """
        The read capacity auto scaling settings for the multi-Region table in the specified AWS Region.
        """
        return pulumi.get(self, "read_capacity_auto_scaling")

    @property
    @pulumi.getter(name="readCapacityUnits")
    def read_capacity_units(self) -> Optional[int]:
        """
        The provisioned read capacity units for the multi-Region table in the specified AWS Region.
        """
        return pulumi.get(self, "read_capacity_units")


@pulumi.output_type
class TableScalingPolicy(dict):
    """
    Represents scaling policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "targetTrackingScalingPolicyConfiguration":
            suggest = "target_tracking_scaling_policy_configuration"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableScalingPolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableScalingPolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableScalingPolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 target_tracking_scaling_policy_configuration: Optional['outputs.TableTargetTrackingScalingPolicyConfiguration'] = None):
        """
        Represents scaling policy.
        :param 'TableTargetTrackingScalingPolicyConfiguration' target_tracking_scaling_policy_configuration: The auto scaling policy that scales a table based on the ratio of consumed to provisioned capacity.
        """
        if target_tracking_scaling_policy_configuration is not None:
            pulumi.set(__self__, "target_tracking_scaling_policy_configuration", target_tracking_scaling_policy_configuration)

    @property
    @pulumi.getter(name="targetTrackingScalingPolicyConfiguration")
    def target_tracking_scaling_policy_configuration(self) -> Optional['outputs.TableTargetTrackingScalingPolicyConfiguration']:
        """
        The auto scaling policy that scales a table based on the ratio of consumed to provisioned capacity.
        """
        return pulumi.get(self, "target_tracking_scaling_policy_configuration")


@pulumi.output_type
class TableTargetTrackingScalingPolicyConfiguration(dict):
    """
    Represents configuration for target tracking scaling policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "targetValue":
            suggest = "target_value"
        elif key == "disableScaleIn":
            suggest = "disable_scale_in"
        elif key == "scaleInCooldown":
            suggest = "scale_in_cooldown"
        elif key == "scaleOutCooldown":
            suggest = "scale_out_cooldown"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableTargetTrackingScalingPolicyConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableTargetTrackingScalingPolicyConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableTargetTrackingScalingPolicyConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 target_value: int,
                 disable_scale_in: Optional[bool] = None,
                 scale_in_cooldown: Optional[int] = None,
                 scale_out_cooldown: Optional[int] = None):
        """
        Represents configuration for target tracking scaling policy.
        :param int target_value: Specifies the target value for the target tracking auto scaling policy.
               
               Amazon Keyspaces auto scaling scales up capacity automatically when traffic exceeds this target utilization rate, and then back down when it falls below the target. This ensures that the ratio of consumed capacity to provisioned capacity stays at or near this value. You define `targetValue` as a percentage. An `integer` between 20 and 90.
        :param bool disable_scale_in: Specifies if `scale-in` is enabled.
               
               When auto scaling automatically decreases capacity for a table, the table *scales in* . When scaling policies are set, they can't scale in the table lower than its minimum capacity.
        :param int scale_in_cooldown: Specifies a `scale-in` cool down period.
               
               A cooldown period in seconds between scaling activities that lets the table stabilize before another scaling activity starts.
        :param int scale_out_cooldown: Specifies a scale out cool down period.
               
               A cooldown period in seconds between scaling activities that lets the table stabilize before another scaling activity starts.
        """
        pulumi.set(__self__, "target_value", target_value)
        if disable_scale_in is not None:
            pulumi.set(__self__, "disable_scale_in", disable_scale_in)
        if scale_in_cooldown is not None:
            pulumi.set(__self__, "scale_in_cooldown", scale_in_cooldown)
        if scale_out_cooldown is not None:
            pulumi.set(__self__, "scale_out_cooldown", scale_out_cooldown)

    @property
    @pulumi.getter(name="targetValue")
    def target_value(self) -> int:
        """
        Specifies the target value for the target tracking auto scaling policy.

        Amazon Keyspaces auto scaling scales up capacity automatically when traffic exceeds this target utilization rate, and then back down when it falls below the target. This ensures that the ratio of consumed capacity to provisioned capacity stays at or near this value. You define `targetValue` as a percentage. An `integer` between 20 and 90.
        """
        return pulumi.get(self, "target_value")

    @property
    @pulumi.getter(name="disableScaleIn")
    def disable_scale_in(self) -> Optional[bool]:
        """
        Specifies if `scale-in` is enabled.

        When auto scaling automatically decreases capacity for a table, the table *scales in* . When scaling policies are set, they can't scale in the table lower than its minimum capacity.
        """
        return pulumi.get(self, "disable_scale_in")

    @property
    @pulumi.getter(name="scaleInCooldown")
    def scale_in_cooldown(self) -> Optional[int]:
        """
        Specifies a `scale-in` cool down period.

        A cooldown period in seconds between scaling activities that lets the table stabilize before another scaling activity starts.
        """
        return pulumi.get(self, "scale_in_cooldown")

    @property
    @pulumi.getter(name="scaleOutCooldown")
    def scale_out_cooldown(self) -> Optional[int]:
        """
        Specifies a scale out cool down period.

        A cooldown period in seconds between scaling activities that lets the table stabilize before another scaling activity starts.
        """
        return pulumi.get(self, "scale_out_cooldown")


@pulumi.output_type
class TypeField(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fieldName":
            suggest = "field_name"
        elif key == "fieldType":
            suggest = "field_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TypeField. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TypeField.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TypeField.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 field_name: str,
                 field_type: str):
        """
        :param str field_name: The name of the field.
        :param str field_type: The data type of the field. This can be any Cassandra data type or another user-defined type.
        """
        pulumi.set(__self__, "field_name", field_name)
        pulumi.set(__self__, "field_type", field_type)

    @property
    @pulumi.getter(name="fieldName")
    def field_name(self) -> str:
        """
        The name of the field.
        """
        return pulumi.get(self, "field_name")

    @property
    @pulumi.getter(name="fieldType")
    def field_type(self) -> str:
        """
        The data type of the field. This can be any Cassandra data type or another user-defined type.
        """
        return pulumi.get(self, "field_type")


