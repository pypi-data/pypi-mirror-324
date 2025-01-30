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

__all__ = [
    'GetPermissionSetResult',
    'AwaitableGetPermissionSetResult',
    'get_permission_set',
    'get_permission_set_output',
]

@pulumi.output_type
class GetPermissionSetResult:
    def __init__(__self__, customer_managed_policy_references=None, description=None, inline_policy=None, managed_policies=None, permission_set_arn=None, permissions_boundary=None, relay_state_type=None, session_duration=None, tags=None):
        if customer_managed_policy_references and not isinstance(customer_managed_policy_references, list):
            raise TypeError("Expected argument 'customer_managed_policy_references' to be a list")
        pulumi.set(__self__, "customer_managed_policy_references", customer_managed_policy_references)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if inline_policy and not isinstance(inline_policy, dict):
            raise TypeError("Expected argument 'inline_policy' to be a dict")
        pulumi.set(__self__, "inline_policy", inline_policy)
        if managed_policies and not isinstance(managed_policies, list):
            raise TypeError("Expected argument 'managed_policies' to be a list")
        pulumi.set(__self__, "managed_policies", managed_policies)
        if permission_set_arn and not isinstance(permission_set_arn, str):
            raise TypeError("Expected argument 'permission_set_arn' to be a str")
        pulumi.set(__self__, "permission_set_arn", permission_set_arn)
        if permissions_boundary and not isinstance(permissions_boundary, dict):
            raise TypeError("Expected argument 'permissions_boundary' to be a dict")
        pulumi.set(__self__, "permissions_boundary", permissions_boundary)
        if relay_state_type and not isinstance(relay_state_type, str):
            raise TypeError("Expected argument 'relay_state_type' to be a str")
        pulumi.set(__self__, "relay_state_type", relay_state_type)
        if session_duration and not isinstance(session_duration, str):
            raise TypeError("Expected argument 'session_duration' to be a str")
        pulumi.set(__self__, "session_duration", session_duration)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="customerManagedPolicyReferences")
    def customer_managed_policy_references(self) -> Optional[Sequence['outputs.PermissionSetCustomerManagedPolicyReference']]:
        """
        Specifies the names and paths of the customer managed policies that you have attached to your permission set.
        """
        return pulumi.get(self, "customer_managed_policy_references")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The permission set description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="inlinePolicy")
    def inline_policy(self) -> Optional[Any]:
        """
        The inline policy to put in permission set.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::SSO::PermissionSet` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "inline_policy")

    @property
    @pulumi.getter(name="managedPolicies")
    def managed_policies(self) -> Optional[Sequence[str]]:
        """
        A structure that stores a list of managed policy ARNs that describe the associated AWS managed policy.
        """
        return pulumi.get(self, "managed_policies")

    @property
    @pulumi.getter(name="permissionSetArn")
    def permission_set_arn(self) -> Optional[str]:
        """
        The permission set that the policy will be attached to
        """
        return pulumi.get(self, "permission_set_arn")

    @property
    @pulumi.getter(name="permissionsBoundary")
    def permissions_boundary(self) -> Optional['outputs.PermissionSetPermissionsBoundary']:
        """
        Specifies the configuration of the AWS managed or customer managed policy that you want to set as a permissions boundary. Specify either `CustomerManagedPolicyReference` to use the name and path of a customer managed policy, or `ManagedPolicyArn` to use the ARN of an AWS managed policy. A permissions boundary represents the maximum permissions that any policy can grant your role. For more information, see [Permissions boundaries for IAM entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) in the *IAM User Guide* .

        > Policies used as permissions boundaries don't provide permissions. You must also attach an IAM policy to the role. To learn how the effective permissions for a role are evaluated, see [IAM JSON policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) in the *IAM User Guide* .
        """
        return pulumi.get(self, "permissions_boundary")

    @property
    @pulumi.getter(name="relayStateType")
    def relay_state_type(self) -> Optional[str]:
        """
        The relay state URL that redirect links to any service in the AWS Management Console.
        """
        return pulumi.get(self, "relay_state_type")

    @property
    @pulumi.getter(name="sessionDuration")
    def session_duration(self) -> Optional[str]:
        """
        The length of time that a user can be signed in to an AWS account.
        """
        return pulumi.get(self, "session_duration")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags to attach to the new `PermissionSet` .
        """
        return pulumi.get(self, "tags")


class AwaitableGetPermissionSetResult(GetPermissionSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPermissionSetResult(
            customer_managed_policy_references=self.customer_managed_policy_references,
            description=self.description,
            inline_policy=self.inline_policy,
            managed_policies=self.managed_policies,
            permission_set_arn=self.permission_set_arn,
            permissions_boundary=self.permissions_boundary,
            relay_state_type=self.relay_state_type,
            session_duration=self.session_duration,
            tags=self.tags)


def get_permission_set(instance_arn: Optional[str] = None,
                       permission_set_arn: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPermissionSetResult:
    """
    Resource Type definition for SSO PermissionSet


    :param str instance_arn: The sso instance arn that the permission set is owned.
    :param str permission_set_arn: The permission set that the policy will be attached to
    """
    __args__ = dict()
    __args__['instanceArn'] = instance_arn
    __args__['permissionSetArn'] = permission_set_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:sso:getPermissionSet', __args__, opts=opts, typ=GetPermissionSetResult).value

    return AwaitableGetPermissionSetResult(
        customer_managed_policy_references=pulumi.get(__ret__, 'customer_managed_policy_references'),
        description=pulumi.get(__ret__, 'description'),
        inline_policy=pulumi.get(__ret__, 'inline_policy'),
        managed_policies=pulumi.get(__ret__, 'managed_policies'),
        permission_set_arn=pulumi.get(__ret__, 'permission_set_arn'),
        permissions_boundary=pulumi.get(__ret__, 'permissions_boundary'),
        relay_state_type=pulumi.get(__ret__, 'relay_state_type'),
        session_duration=pulumi.get(__ret__, 'session_duration'),
        tags=pulumi.get(__ret__, 'tags'))
def get_permission_set_output(instance_arn: Optional[pulumi.Input[str]] = None,
                              permission_set_arn: Optional[pulumi.Input[str]] = None,
                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPermissionSetResult]:
    """
    Resource Type definition for SSO PermissionSet


    :param str instance_arn: The sso instance arn that the permission set is owned.
    :param str permission_set_arn: The permission set that the policy will be attached to
    """
    __args__ = dict()
    __args__['instanceArn'] = instance_arn
    __args__['permissionSetArn'] = permission_set_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:sso:getPermissionSet', __args__, opts=opts, typ=GetPermissionSetResult)
    return __ret__.apply(lambda __response__: GetPermissionSetResult(
        customer_managed_policy_references=pulumi.get(__response__, 'customer_managed_policy_references'),
        description=pulumi.get(__response__, 'description'),
        inline_policy=pulumi.get(__response__, 'inline_policy'),
        managed_policies=pulumi.get(__response__, 'managed_policies'),
        permission_set_arn=pulumi.get(__response__, 'permission_set_arn'),
        permissions_boundary=pulumi.get(__response__, 'permissions_boundary'),
        relay_state_type=pulumi.get(__response__, 'relay_state_type'),
        session_duration=pulumi.get(__response__, 'session_duration'),
        tags=pulumi.get(__response__, 'tags')))
