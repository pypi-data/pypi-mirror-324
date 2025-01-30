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
from ._enums import *

__all__ = [
    'GetInfluxDbInstanceResult',
    'AwaitableGetInfluxDbInstanceResult',
    'get_influx_db_instance',
    'get_influx_db_instance_output',
]

@pulumi.output_type
class GetInfluxDbInstanceResult:
    def __init__(__self__, arn=None, availability_zone=None, db_instance_type=None, db_parameter_group_identifier=None, deployment_type=None, endpoint=None, id=None, influx_auth_parameters_secret_arn=None, log_delivery_configuration=None, port=None, secondary_availability_zone=None, status=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        pulumi.set(__self__, "availability_zone", availability_zone)
        if db_instance_type and not isinstance(db_instance_type, str):
            raise TypeError("Expected argument 'db_instance_type' to be a str")
        pulumi.set(__self__, "db_instance_type", db_instance_type)
        if db_parameter_group_identifier and not isinstance(db_parameter_group_identifier, str):
            raise TypeError("Expected argument 'db_parameter_group_identifier' to be a str")
        pulumi.set(__self__, "db_parameter_group_identifier", db_parameter_group_identifier)
        if deployment_type and not isinstance(deployment_type, str):
            raise TypeError("Expected argument 'deployment_type' to be a str")
        pulumi.set(__self__, "deployment_type", deployment_type)
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, "endpoint", endpoint)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if influx_auth_parameters_secret_arn and not isinstance(influx_auth_parameters_secret_arn, str):
            raise TypeError("Expected argument 'influx_auth_parameters_secret_arn' to be a str")
        pulumi.set(__self__, "influx_auth_parameters_secret_arn", influx_auth_parameters_secret_arn)
        if log_delivery_configuration and not isinstance(log_delivery_configuration, dict):
            raise TypeError("Expected argument 'log_delivery_configuration' to be a dict")
        pulumi.set(__self__, "log_delivery_configuration", log_delivery_configuration)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if secondary_availability_zone and not isinstance(secondary_availability_zone, str):
            raise TypeError("Expected argument 'secondary_availability_zone' to be a str")
        pulumi.set(__self__, "secondary_availability_zone", secondary_availability_zone)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) that is associated with the InfluxDB instance.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        The Availability Zone (AZ) where the InfluxDB instance is created.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="dbInstanceType")
    def db_instance_type(self) -> Optional['InfluxDbInstanceDbInstanceType']:
        """
        The compute instance of the InfluxDB instance.
        """
        return pulumi.get(self, "db_instance_type")

    @property
    @pulumi.getter(name="dbParameterGroupIdentifier")
    def db_parameter_group_identifier(self) -> Optional[str]:
        """
        The name of an existing InfluxDB parameter group.
        """
        return pulumi.get(self, "db_parameter_group_identifier")

    @property
    @pulumi.getter(name="deploymentType")
    def deployment_type(self) -> Optional['InfluxDbInstanceDeploymentType']:
        """
        Deployment type of the InfluxDB Instance.
        """
        return pulumi.get(self, "deployment_type")

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[str]:
        """
        The connection endpoint for the InfluxDB instance.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The service generated unique identifier for InfluxDB instance.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="influxAuthParametersSecretArn")
    def influx_auth_parameters_secret_arn(self) -> Optional[str]:
        """
        The Auth parameters secret Amazon Resource name (ARN) that is associated with the InfluxDB instance.
        """
        return pulumi.get(self, "influx_auth_parameters_secret_arn")

    @property
    @pulumi.getter(name="logDeliveryConfiguration")
    def log_delivery_configuration(self) -> Optional['outputs.LogDeliveryConfigurationProperties']:
        """
        Configuration for sending logs to customer account from the InfluxDB instance.
        """
        return pulumi.get(self, "log_delivery_configuration")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        The port number on which InfluxDB accepts connections.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="secondaryAvailabilityZone")
    def secondary_availability_zone(self) -> Optional[str]:
        """
        The Secondary Availability Zone (AZ) where the InfluxDB instance is created, if DeploymentType is set as WITH_MULTIAZ_STANDBY.
        """
        return pulumi.get(self, "secondary_availability_zone")

    @property
    @pulumi.getter
    def status(self) -> Optional['InfluxDbInstanceStatus']:
        """
        Status of the InfluxDB Instance.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An arbitrary set of tags (key-value pairs) for this DB instance.
        """
        return pulumi.get(self, "tags")


class AwaitableGetInfluxDbInstanceResult(GetInfluxDbInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInfluxDbInstanceResult(
            arn=self.arn,
            availability_zone=self.availability_zone,
            db_instance_type=self.db_instance_type,
            db_parameter_group_identifier=self.db_parameter_group_identifier,
            deployment_type=self.deployment_type,
            endpoint=self.endpoint,
            id=self.id,
            influx_auth_parameters_secret_arn=self.influx_auth_parameters_secret_arn,
            log_delivery_configuration=self.log_delivery_configuration,
            port=self.port,
            secondary_availability_zone=self.secondary_availability_zone,
            status=self.status,
            tags=self.tags)


def get_influx_db_instance(id: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInfluxDbInstanceResult:
    """
    The AWS::Timestream::InfluxDBInstance resource creates an InfluxDB instance.


    :param str id: The service generated unique identifier for InfluxDB instance.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:timestream:getInfluxDbInstance', __args__, opts=opts, typ=GetInfluxDbInstanceResult).value

    return AwaitableGetInfluxDbInstanceResult(
        arn=pulumi.get(__ret__, 'arn'),
        availability_zone=pulumi.get(__ret__, 'availability_zone'),
        db_instance_type=pulumi.get(__ret__, 'db_instance_type'),
        db_parameter_group_identifier=pulumi.get(__ret__, 'db_parameter_group_identifier'),
        deployment_type=pulumi.get(__ret__, 'deployment_type'),
        endpoint=pulumi.get(__ret__, 'endpoint'),
        id=pulumi.get(__ret__, 'id'),
        influx_auth_parameters_secret_arn=pulumi.get(__ret__, 'influx_auth_parameters_secret_arn'),
        log_delivery_configuration=pulumi.get(__ret__, 'log_delivery_configuration'),
        port=pulumi.get(__ret__, 'port'),
        secondary_availability_zone=pulumi.get(__ret__, 'secondary_availability_zone'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'))
def get_influx_db_instance_output(id: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetInfluxDbInstanceResult]:
    """
    The AWS::Timestream::InfluxDBInstance resource creates an InfluxDB instance.


    :param str id: The service generated unique identifier for InfluxDB instance.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:timestream:getInfluxDbInstance', __args__, opts=opts, typ=GetInfluxDbInstanceResult)
    return __ret__.apply(lambda __response__: GetInfluxDbInstanceResult(
        arn=pulumi.get(__response__, 'arn'),
        availability_zone=pulumi.get(__response__, 'availability_zone'),
        db_instance_type=pulumi.get(__response__, 'db_instance_type'),
        db_parameter_group_identifier=pulumi.get(__response__, 'db_parameter_group_identifier'),
        deployment_type=pulumi.get(__response__, 'deployment_type'),
        endpoint=pulumi.get(__response__, 'endpoint'),
        id=pulumi.get(__response__, 'id'),
        influx_auth_parameters_secret_arn=pulumi.get(__response__, 'influx_auth_parameters_secret_arn'),
        log_delivery_configuration=pulumi.get(__response__, 'log_delivery_configuration'),
        port=pulumi.get(__response__, 'port'),
        secondary_availability_zone=pulumi.get(__response__, 'secondary_availability_zone'),
        status=pulumi.get(__response__, 'status'),
        tags=pulumi.get(__response__, 'tags')))
