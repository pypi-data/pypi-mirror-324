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
    'GetPolicyStoreResult',
    'AwaitableGetPolicyStoreResult',
    'get_policy_store',
    'get_policy_store_output',
]

@pulumi.output_type
class GetPolicyStoreResult:
    def __init__(__self__, arn=None, description=None, policy_store_id=None, schema=None, validation_settings=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if policy_store_id and not isinstance(policy_store_id, str):
            raise TypeError("Expected argument 'policy_store_id' to be a str")
        pulumi.set(__self__, "policy_store_id", policy_store_id)
        if schema and not isinstance(schema, dict):
            raise TypeError("Expected argument 'schema' to be a dict")
        pulumi.set(__self__, "schema", schema)
        if validation_settings and not isinstance(validation_settings, dict):
            raise TypeError("Expected argument 'validation_settings' to be a dict")
        pulumi.set(__self__, "validation_settings", validation_settings)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The [Amazon Resource Name (ARN)](https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html) of the new or updated policy store.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Descriptive text that you can provide to help with identification of the current policy store.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="policyStoreId")
    def policy_store_id(self) -> Optional[str]:
        """
        The unique ID of the new or updated policy store.
        """
        return pulumi.get(self, "policy_store_id")

    @property
    @pulumi.getter
    def schema(self) -> Optional['outputs.PolicyStoreSchemaDefinition']:
        """
        Creates or updates the policy schema in a policy store. Cedar can use the schema to validate any Cedar policies and policy templates submitted to the policy store. Any changes to the schema validate only policies and templates submitted after the schema change. Existing policies and templates are not re-evaluated against the changed schema. If you later update a policy, then it is evaluated against the new schema at that time.
        """
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter(name="validationSettings")
    def validation_settings(self) -> Optional['outputs.PolicyStoreValidationSettings']:
        """
        Specifies the validation setting for this policy store.

        Currently, the only valid and required value is `Mode` .

        > We recommend that you turn on `STRICT` mode only after you define a schema. If a schema doesn't exist, then `STRICT` mode causes any policy to fail validation, and Verified Permissions rejects the policy. You can turn off validation by using the [UpdatePolicyStore](https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_UpdatePolicyStore) . Then, when you have a schema defined, use [UpdatePolicyStore](https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_UpdatePolicyStore) again to turn validation back on.
        """
        return pulumi.get(self, "validation_settings")


class AwaitableGetPolicyStoreResult(GetPolicyStoreResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyStoreResult(
            arn=self.arn,
            description=self.description,
            policy_store_id=self.policy_store_id,
            schema=self.schema,
            validation_settings=self.validation_settings)


def get_policy_store(policy_store_id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyStoreResult:
    """
    Represents a policy store that you can place schema, policies, and policy templates in to validate authorization requests


    :param str policy_store_id: The unique ID of the new or updated policy store.
    """
    __args__ = dict()
    __args__['policyStoreId'] = policy_store_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:verifiedpermissions:getPolicyStore', __args__, opts=opts, typ=GetPolicyStoreResult).value

    return AwaitableGetPolicyStoreResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        policy_store_id=pulumi.get(__ret__, 'policy_store_id'),
        schema=pulumi.get(__ret__, 'schema'),
        validation_settings=pulumi.get(__ret__, 'validation_settings'))
def get_policy_store_output(policy_store_id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPolicyStoreResult]:
    """
    Represents a policy store that you can place schema, policies, and policy templates in to validate authorization requests


    :param str policy_store_id: The unique ID of the new or updated policy store.
    """
    __args__ = dict()
    __args__['policyStoreId'] = policy_store_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:verifiedpermissions:getPolicyStore', __args__, opts=opts, typ=GetPolicyStoreResult)
    return __ret__.apply(lambda __response__: GetPolicyStoreResult(
        arn=pulumi.get(__response__, 'arn'),
        description=pulumi.get(__response__, 'description'),
        policy_store_id=pulumi.get(__response__, 'policy_store_id'),
        schema=pulumi.get(__response__, 'schema'),
        validation_settings=pulumi.get(__response__, 'validation_settings')))
