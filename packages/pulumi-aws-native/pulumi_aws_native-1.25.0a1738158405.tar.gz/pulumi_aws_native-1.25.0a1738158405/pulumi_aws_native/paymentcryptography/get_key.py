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
    'GetKeyResult',
    'AwaitableGetKeyResult',
    'get_key',
    'get_key_output',
]

@pulumi.output_type
class GetKeyResult:
    def __init__(__self__, enabled=None, exportable=None, key_attributes=None, key_check_value_algorithm=None, key_identifier=None, key_origin=None, key_state=None, tags=None):
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if exportable and not isinstance(exportable, bool):
            raise TypeError("Expected argument 'exportable' to be a bool")
        pulumi.set(__self__, "exportable", exportable)
        if key_attributes and not isinstance(key_attributes, dict):
            raise TypeError("Expected argument 'key_attributes' to be a dict")
        pulumi.set(__self__, "key_attributes", key_attributes)
        if key_check_value_algorithm and not isinstance(key_check_value_algorithm, str):
            raise TypeError("Expected argument 'key_check_value_algorithm' to be a str")
        pulumi.set(__self__, "key_check_value_algorithm", key_check_value_algorithm)
        if key_identifier and not isinstance(key_identifier, str):
            raise TypeError("Expected argument 'key_identifier' to be a str")
        pulumi.set(__self__, "key_identifier", key_identifier)
        if key_origin and not isinstance(key_origin, str):
            raise TypeError("Expected argument 'key_origin' to be a str")
        pulumi.set(__self__, "key_origin", key_origin)
        if key_state and not isinstance(key_state, str):
            raise TypeError("Expected argument 'key_state' to be a str")
        pulumi.set(__self__, "key_state", key_state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Specifies whether the key is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def exportable(self) -> Optional[bool]:
        """
        Specifies whether the key is exportable. This data is immutable after the key is created.
        """
        return pulumi.get(self, "exportable")

    @property
    @pulumi.getter(name="keyAttributes")
    def key_attributes(self) -> Optional['outputs.KeyAttributes']:
        """
        The role of the key, the algorithm it supports, and the cryptographic operations allowed with the key. This data is immutable after the key is created.
        """
        return pulumi.get(self, "key_attributes")

    @property
    @pulumi.getter(name="keyCheckValueAlgorithm")
    def key_check_value_algorithm(self) -> Optional['KeyCheckValueAlgorithm']:
        """
        The algorithm that AWS Payment Cryptography uses to calculate the key check value (KCV). It is used to validate the key integrity.

        For TDES keys, the KCV is computed by encrypting 8 bytes, each with value of zero, with the key to be checked and retaining the 3 highest order bytes of the encrypted result. For AES keys, the KCV is computed using a CMAC algorithm where the input data is 16 bytes of zero and retaining the 3 highest order bytes of the encrypted result.
        """
        return pulumi.get(self, "key_check_value_algorithm")

    @property
    @pulumi.getter(name="keyIdentifier")
    def key_identifier(self) -> Optional[str]:
        return pulumi.get(self, "key_identifier")

    @property
    @pulumi.getter(name="keyOrigin")
    def key_origin(self) -> Optional['KeyOrigin']:
        """
        The source of the key material. For keys created within AWS Payment Cryptography, the value is `AWS_PAYMENT_CRYPTOGRAPHY` . For keys imported into AWS Payment Cryptography, the value is `EXTERNAL` .
        """
        return pulumi.get(self, "key_origin")

    @property
    @pulumi.getter(name="keyState")
    def key_state(self) -> Optional['KeyState']:
        """
        The state of key that is being created or deleted.
        """
        return pulumi.get(self, "key_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        return pulumi.get(self, "tags")


class AwaitableGetKeyResult(GetKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKeyResult(
            enabled=self.enabled,
            exportable=self.exportable,
            key_attributes=self.key_attributes,
            key_check_value_algorithm=self.key_check_value_algorithm,
            key_identifier=self.key_identifier,
            key_origin=self.key_origin,
            key_state=self.key_state,
            tags=self.tags)


def get_key(key_identifier: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetKeyResult:
    """
    Definition of AWS::PaymentCryptography::Key Resource Type
    """
    __args__ = dict()
    __args__['keyIdentifier'] = key_identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:paymentcryptography:getKey', __args__, opts=opts, typ=GetKeyResult).value

    return AwaitableGetKeyResult(
        enabled=pulumi.get(__ret__, 'enabled'),
        exportable=pulumi.get(__ret__, 'exportable'),
        key_attributes=pulumi.get(__ret__, 'key_attributes'),
        key_check_value_algorithm=pulumi.get(__ret__, 'key_check_value_algorithm'),
        key_identifier=pulumi.get(__ret__, 'key_identifier'),
        key_origin=pulumi.get(__ret__, 'key_origin'),
        key_state=pulumi.get(__ret__, 'key_state'),
        tags=pulumi.get(__ret__, 'tags'))
def get_key_output(key_identifier: Optional[pulumi.Input[str]] = None,
                   opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetKeyResult]:
    """
    Definition of AWS::PaymentCryptography::Key Resource Type
    """
    __args__ = dict()
    __args__['keyIdentifier'] = key_identifier
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:paymentcryptography:getKey', __args__, opts=opts, typ=GetKeyResult)
    return __ret__.apply(lambda __response__: GetKeyResult(
        enabled=pulumi.get(__response__, 'enabled'),
        exportable=pulumi.get(__response__, 'exportable'),
        key_attributes=pulumi.get(__response__, 'key_attributes'),
        key_check_value_algorithm=pulumi.get(__response__, 'key_check_value_algorithm'),
        key_identifier=pulumi.get(__response__, 'key_identifier'),
        key_origin=pulumi.get(__response__, 'key_origin'),
        key_state=pulumi.get(__response__, 'key_state'),
        tags=pulumi.get(__response__, 'tags')))
