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

__all__ = [
    'GetCapacityReservationFleetResult',
    'AwaitableGetCapacityReservationFleetResult',
    'get_capacity_reservation_fleet',
    'get_capacity_reservation_fleet_output',
]

@pulumi.output_type
class GetCapacityReservationFleetResult:
    def __init__(__self__, capacity_reservation_fleet_id=None, no_remove_end_date=None, remove_end_date=None, total_target_capacity=None):
        if capacity_reservation_fleet_id and not isinstance(capacity_reservation_fleet_id, str):
            raise TypeError("Expected argument 'capacity_reservation_fleet_id' to be a str")
        pulumi.set(__self__, "capacity_reservation_fleet_id", capacity_reservation_fleet_id)
        if no_remove_end_date and not isinstance(no_remove_end_date, bool):
            raise TypeError("Expected argument 'no_remove_end_date' to be a bool")
        pulumi.set(__self__, "no_remove_end_date", no_remove_end_date)
        if remove_end_date and not isinstance(remove_end_date, bool):
            raise TypeError("Expected argument 'remove_end_date' to be a bool")
        pulumi.set(__self__, "remove_end_date", remove_end_date)
        if total_target_capacity and not isinstance(total_target_capacity, int):
            raise TypeError("Expected argument 'total_target_capacity' to be a int")
        pulumi.set(__self__, "total_target_capacity", total_target_capacity)

    @property
    @pulumi.getter(name="capacityReservationFleetId")
    def capacity_reservation_fleet_id(self) -> Optional[str]:
        """
        The ID of the Capacity Reservation Fleet.
        """
        return pulumi.get(self, "capacity_reservation_fleet_id")

    @property
    @pulumi.getter(name="noRemoveEndDate")
    def no_remove_end_date(self) -> Optional[bool]:
        """
        Used to add an end date to a Capacity Reservation Fleet that has no end date and time. To add an end date to a Capacity Reservation Fleet, specify `true` for this paramater and specify the end date and time (in UTC time format) for the *EndDate* parameter.
        """
        return pulumi.get(self, "no_remove_end_date")

    @property
    @pulumi.getter(name="removeEndDate")
    def remove_end_date(self) -> Optional[bool]:
        """
        Used to remove an end date from a Capacity Reservation Fleet that is configured to end automatically at a specific date and time. To remove the end date from a Capacity Reservation Fleet, specify `true` for this paramater and omit the *EndDate* parameter.
        """
        return pulumi.get(self, "remove_end_date")

    @property
    @pulumi.getter(name="totalTargetCapacity")
    def total_target_capacity(self) -> Optional[int]:
        """
        The total number of capacity units to be reserved by the Capacity Reservation Fleet. This value, together with the instance type weights that you assign to each instance type used by the Fleet determine the number of instances for which the Fleet reserves capacity. Both values are based on units that make sense for your workload. For more information, see [Total target capacity](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/crfleet-concepts.html#target-capacity) in the *Amazon EC2 User Guide* .
        """
        return pulumi.get(self, "total_target_capacity")


class AwaitableGetCapacityReservationFleetResult(GetCapacityReservationFleetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCapacityReservationFleetResult(
            capacity_reservation_fleet_id=self.capacity_reservation_fleet_id,
            no_remove_end_date=self.no_remove_end_date,
            remove_end_date=self.remove_end_date,
            total_target_capacity=self.total_target_capacity)


def get_capacity_reservation_fleet(capacity_reservation_fleet_id: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCapacityReservationFleetResult:
    """
    Resource Type definition for AWS::EC2::CapacityReservationFleet


    :param str capacity_reservation_fleet_id: The ID of the Capacity Reservation Fleet.
    """
    __args__ = dict()
    __args__['capacityReservationFleetId'] = capacity_reservation_fleet_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getCapacityReservationFleet', __args__, opts=opts, typ=GetCapacityReservationFleetResult).value

    return AwaitableGetCapacityReservationFleetResult(
        capacity_reservation_fleet_id=pulumi.get(__ret__, 'capacity_reservation_fleet_id'),
        no_remove_end_date=pulumi.get(__ret__, 'no_remove_end_date'),
        remove_end_date=pulumi.get(__ret__, 'remove_end_date'),
        total_target_capacity=pulumi.get(__ret__, 'total_target_capacity'))
def get_capacity_reservation_fleet_output(capacity_reservation_fleet_id: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetCapacityReservationFleetResult]:
    """
    Resource Type definition for AWS::EC2::CapacityReservationFleet


    :param str capacity_reservation_fleet_id: The ID of the Capacity Reservation Fleet.
    """
    __args__ = dict()
    __args__['capacityReservationFleetId'] = capacity_reservation_fleet_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getCapacityReservationFleet', __args__, opts=opts, typ=GetCapacityReservationFleetResult)
    return __ret__.apply(lambda __response__: GetCapacityReservationFleetResult(
        capacity_reservation_fleet_id=pulumi.get(__response__, 'capacity_reservation_fleet_id'),
        no_remove_end_date=pulumi.get(__response__, 'no_remove_end_date'),
        remove_end_date=pulumi.get(__response__, 'remove_end_date'),
        total_target_capacity=pulumi.get(__response__, 'total_target_capacity')))
