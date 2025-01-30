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
    'LicenseBorrowConfigurationArgs',
    'LicenseBorrowConfigurationArgsDict',
    'LicenseConsumptionConfigurationArgs',
    'LicenseConsumptionConfigurationArgsDict',
    'LicenseEntitlementArgs',
    'LicenseEntitlementArgsDict',
    'LicenseIssuerDataArgs',
    'LicenseIssuerDataArgsDict',
    'LicenseMetadataArgs',
    'LicenseMetadataArgsDict',
    'LicenseProvisionalConfigurationArgs',
    'LicenseProvisionalConfigurationArgsDict',
    'LicenseValidityDateFormatArgs',
    'LicenseValidityDateFormatArgsDict',
]

MYPY = False

if not MYPY:
    class LicenseBorrowConfigurationArgsDict(TypedDict):
        allow_early_check_in: pulumi.Input[bool]
        """
        Indicates whether early check-ins are allowed.
        """
        max_time_to_live_in_minutes: pulumi.Input[int]
        """
        Maximum time for the borrow configuration, in minutes.
        """
elif False:
    LicenseBorrowConfigurationArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LicenseBorrowConfigurationArgs:
    def __init__(__self__, *,
                 allow_early_check_in: pulumi.Input[bool],
                 max_time_to_live_in_minutes: pulumi.Input[int]):
        """
        :param pulumi.Input[bool] allow_early_check_in: Indicates whether early check-ins are allowed.
        :param pulumi.Input[int] max_time_to_live_in_minutes: Maximum time for the borrow configuration, in minutes.
        """
        pulumi.set(__self__, "allow_early_check_in", allow_early_check_in)
        pulumi.set(__self__, "max_time_to_live_in_minutes", max_time_to_live_in_minutes)

    @property
    @pulumi.getter(name="allowEarlyCheckIn")
    def allow_early_check_in(self) -> pulumi.Input[bool]:
        """
        Indicates whether early check-ins are allowed.
        """
        return pulumi.get(self, "allow_early_check_in")

    @allow_early_check_in.setter
    def allow_early_check_in(self, value: pulumi.Input[bool]):
        pulumi.set(self, "allow_early_check_in", value)

    @property
    @pulumi.getter(name="maxTimeToLiveInMinutes")
    def max_time_to_live_in_minutes(self) -> pulumi.Input[int]:
        """
        Maximum time for the borrow configuration, in minutes.
        """
        return pulumi.get(self, "max_time_to_live_in_minutes")

    @max_time_to_live_in_minutes.setter
    def max_time_to_live_in_minutes(self, value: pulumi.Input[int]):
        pulumi.set(self, "max_time_to_live_in_minutes", value)


if not MYPY:
    class LicenseConsumptionConfigurationArgsDict(TypedDict):
        borrow_configuration: NotRequired[pulumi.Input['LicenseBorrowConfigurationArgsDict']]
        """
        Details about a borrow configuration.
        """
        provisional_configuration: NotRequired[pulumi.Input['LicenseProvisionalConfigurationArgsDict']]
        """
        Details about a provisional configuration.
        """
        renew_type: NotRequired[pulumi.Input[str]]
        """
        Renewal frequency.
        """
elif False:
    LicenseConsumptionConfigurationArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LicenseConsumptionConfigurationArgs:
    def __init__(__self__, *,
                 borrow_configuration: Optional[pulumi.Input['LicenseBorrowConfigurationArgs']] = None,
                 provisional_configuration: Optional[pulumi.Input['LicenseProvisionalConfigurationArgs']] = None,
                 renew_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input['LicenseBorrowConfigurationArgs'] borrow_configuration: Details about a borrow configuration.
        :param pulumi.Input['LicenseProvisionalConfigurationArgs'] provisional_configuration: Details about a provisional configuration.
        :param pulumi.Input[str] renew_type: Renewal frequency.
        """
        if borrow_configuration is not None:
            pulumi.set(__self__, "borrow_configuration", borrow_configuration)
        if provisional_configuration is not None:
            pulumi.set(__self__, "provisional_configuration", provisional_configuration)
        if renew_type is not None:
            pulumi.set(__self__, "renew_type", renew_type)

    @property
    @pulumi.getter(name="borrowConfiguration")
    def borrow_configuration(self) -> Optional[pulumi.Input['LicenseBorrowConfigurationArgs']]:
        """
        Details about a borrow configuration.
        """
        return pulumi.get(self, "borrow_configuration")

    @borrow_configuration.setter
    def borrow_configuration(self, value: Optional[pulumi.Input['LicenseBorrowConfigurationArgs']]):
        pulumi.set(self, "borrow_configuration", value)

    @property
    @pulumi.getter(name="provisionalConfiguration")
    def provisional_configuration(self) -> Optional[pulumi.Input['LicenseProvisionalConfigurationArgs']]:
        """
        Details about a provisional configuration.
        """
        return pulumi.get(self, "provisional_configuration")

    @provisional_configuration.setter
    def provisional_configuration(self, value: Optional[pulumi.Input['LicenseProvisionalConfigurationArgs']]):
        pulumi.set(self, "provisional_configuration", value)

    @property
    @pulumi.getter(name="renewType")
    def renew_type(self) -> Optional[pulumi.Input[str]]:
        """
        Renewal frequency.
        """
        return pulumi.get(self, "renew_type")

    @renew_type.setter
    def renew_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "renew_type", value)


if not MYPY:
    class LicenseEntitlementArgsDict(TypedDict):
        name: pulumi.Input[str]
        """
        Entitlement name.
        """
        unit: pulumi.Input[str]
        """
        Entitlement unit.
        """
        allow_check_in: NotRequired[pulumi.Input[bool]]
        """
        Indicates whether check-ins are allowed.
        """
        max_count: NotRequired[pulumi.Input[int]]
        """
        Maximum entitlement count. Use if the unit is not None.
        """
        overage: NotRequired[pulumi.Input[bool]]
        """
        Indicates whether overages are allowed.
        """
        value: NotRequired[pulumi.Input[str]]
        """
        Entitlement resource. Use only if the unit is None.
        """
elif False:
    LicenseEntitlementArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LicenseEntitlementArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 unit: pulumi.Input[str],
                 allow_check_in: Optional[pulumi.Input[bool]] = None,
                 max_count: Optional[pulumi.Input[int]] = None,
                 overage: Optional[pulumi.Input[bool]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: Entitlement name.
        :param pulumi.Input[str] unit: Entitlement unit.
        :param pulumi.Input[bool] allow_check_in: Indicates whether check-ins are allowed.
        :param pulumi.Input[int] max_count: Maximum entitlement count. Use if the unit is not None.
        :param pulumi.Input[bool] overage: Indicates whether overages are allowed.
        :param pulumi.Input[str] value: Entitlement resource. Use only if the unit is None.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "unit", unit)
        if allow_check_in is not None:
            pulumi.set(__self__, "allow_check_in", allow_check_in)
        if max_count is not None:
            pulumi.set(__self__, "max_count", max_count)
        if overage is not None:
            pulumi.set(__self__, "overage", overage)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Entitlement name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def unit(self) -> pulumi.Input[str]:
        """
        Entitlement unit.
        """
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: pulumi.Input[str]):
        pulumi.set(self, "unit", value)

    @property
    @pulumi.getter(name="allowCheckIn")
    def allow_check_in(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether check-ins are allowed.
        """
        return pulumi.get(self, "allow_check_in")

    @allow_check_in.setter
    def allow_check_in(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_check_in", value)

    @property
    @pulumi.getter(name="maxCount")
    def max_count(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum entitlement count. Use if the unit is not None.
        """
        return pulumi.get(self, "max_count")

    @max_count.setter
    def max_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_count", value)

    @property
    @pulumi.getter
    def overage(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether overages are allowed.
        """
        return pulumi.get(self, "overage")

    @overage.setter
    def overage(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "overage", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        Entitlement resource. Use only if the unit is None.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


if not MYPY:
    class LicenseIssuerDataArgsDict(TypedDict):
        name: pulumi.Input[str]
        """
        Issuer name.
        """
        sign_key: NotRequired[pulumi.Input[str]]
        """
        Asymmetric KMS key from AWS Key Management Service . The KMS key must have a key usage of sign and verify, and support the RSASSA-PSS SHA-256 signing algorithm.
        """
elif False:
    LicenseIssuerDataArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LicenseIssuerDataArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 sign_key: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: Issuer name.
        :param pulumi.Input[str] sign_key: Asymmetric KMS key from AWS Key Management Service . The KMS key must have a key usage of sign and verify, and support the RSASSA-PSS SHA-256 signing algorithm.
        """
        pulumi.set(__self__, "name", name)
        if sign_key is not None:
            pulumi.set(__self__, "sign_key", sign_key)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Issuer name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="signKey")
    def sign_key(self) -> Optional[pulumi.Input[str]]:
        """
        Asymmetric KMS key from AWS Key Management Service . The KMS key must have a key usage of sign and verify, and support the RSASSA-PSS SHA-256 signing algorithm.
        """
        return pulumi.get(self, "sign_key")

    @sign_key.setter
    def sign_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sign_key", value)


if not MYPY:
    class LicenseMetadataArgsDict(TypedDict):
        name: pulumi.Input[str]
        """
        The key name.
        """
        value: pulumi.Input[str]
        """
        The value.
        """
elif False:
    LicenseMetadataArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LicenseMetadataArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The key name.
        :param pulumi.Input[str] value: The value.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The key name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


if not MYPY:
    class LicenseProvisionalConfigurationArgsDict(TypedDict):
        max_time_to_live_in_minutes: pulumi.Input[int]
        """
        Maximum time for the provisional configuration, in minutes.
        """
elif False:
    LicenseProvisionalConfigurationArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LicenseProvisionalConfigurationArgs:
    def __init__(__self__, *,
                 max_time_to_live_in_minutes: pulumi.Input[int]):
        """
        :param pulumi.Input[int] max_time_to_live_in_minutes: Maximum time for the provisional configuration, in minutes.
        """
        pulumi.set(__self__, "max_time_to_live_in_minutes", max_time_to_live_in_minutes)

    @property
    @pulumi.getter(name="maxTimeToLiveInMinutes")
    def max_time_to_live_in_minutes(self) -> pulumi.Input[int]:
        """
        Maximum time for the provisional configuration, in minutes.
        """
        return pulumi.get(self, "max_time_to_live_in_minutes")

    @max_time_to_live_in_minutes.setter
    def max_time_to_live_in_minutes(self, value: pulumi.Input[int]):
        pulumi.set(self, "max_time_to_live_in_minutes", value)


if not MYPY:
    class LicenseValidityDateFormatArgsDict(TypedDict):
        begin: pulumi.Input[str]
        """
        Validity begin date for the license.
        """
        end: pulumi.Input[str]
        """
        Validity begin date for the license.
        """
elif False:
    LicenseValidityDateFormatArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LicenseValidityDateFormatArgs:
    def __init__(__self__, *,
                 begin: pulumi.Input[str],
                 end: pulumi.Input[str]):
        """
        :param pulumi.Input[str] begin: Validity begin date for the license.
        :param pulumi.Input[str] end: Validity begin date for the license.
        """
        pulumi.set(__self__, "begin", begin)
        pulumi.set(__self__, "end", end)

    @property
    @pulumi.getter
    def begin(self) -> pulumi.Input[str]:
        """
        Validity begin date for the license.
        """
        return pulumi.get(self, "begin")

    @begin.setter
    def begin(self, value: pulumi.Input[str]):
        pulumi.set(self, "begin", value)

    @property
    @pulumi.getter
    def end(self) -> pulumi.Input[str]:
        """
        Validity begin date for the license.
        """
        return pulumi.get(self, "end")

    @end.setter
    def end(self, value: pulumi.Input[str]):
        pulumi.set(self, "end", value)


