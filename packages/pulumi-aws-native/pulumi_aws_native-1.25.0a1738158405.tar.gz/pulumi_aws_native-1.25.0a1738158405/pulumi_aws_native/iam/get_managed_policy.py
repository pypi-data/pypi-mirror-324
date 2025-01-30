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
    'GetManagedPolicyResult',
    'AwaitableGetManagedPolicyResult',
    'get_managed_policy',
    'get_managed_policy_output',
]

@pulumi.output_type
class GetManagedPolicyResult:
    def __init__(__self__, attachment_count=None, create_date=None, default_version_id=None, groups=None, is_attachable=None, permissions_boundary_usage_count=None, policy_arn=None, policy_document=None, policy_id=None, roles=None, update_date=None, users=None):
        if attachment_count and not isinstance(attachment_count, int):
            raise TypeError("Expected argument 'attachment_count' to be a int")
        pulumi.set(__self__, "attachment_count", attachment_count)
        if create_date and not isinstance(create_date, str):
            raise TypeError("Expected argument 'create_date' to be a str")
        pulumi.set(__self__, "create_date", create_date)
        if default_version_id and not isinstance(default_version_id, str):
            raise TypeError("Expected argument 'default_version_id' to be a str")
        pulumi.set(__self__, "default_version_id", default_version_id)
        if groups and not isinstance(groups, list):
            raise TypeError("Expected argument 'groups' to be a list")
        pulumi.set(__self__, "groups", groups)
        if is_attachable and not isinstance(is_attachable, bool):
            raise TypeError("Expected argument 'is_attachable' to be a bool")
        pulumi.set(__self__, "is_attachable", is_attachable)
        if permissions_boundary_usage_count and not isinstance(permissions_boundary_usage_count, int):
            raise TypeError("Expected argument 'permissions_boundary_usage_count' to be a int")
        pulumi.set(__self__, "permissions_boundary_usage_count", permissions_boundary_usage_count)
        if policy_arn and not isinstance(policy_arn, str):
            raise TypeError("Expected argument 'policy_arn' to be a str")
        pulumi.set(__self__, "policy_arn", policy_arn)
        if policy_document and not isinstance(policy_document, dict):
            raise TypeError("Expected argument 'policy_document' to be a dict")
        pulumi.set(__self__, "policy_document", policy_document)
        if policy_id and not isinstance(policy_id, str):
            raise TypeError("Expected argument 'policy_id' to be a str")
        pulumi.set(__self__, "policy_id", policy_id)
        if roles and not isinstance(roles, list):
            raise TypeError("Expected argument 'roles' to be a list")
        pulumi.set(__self__, "roles", roles)
        if update_date and not isinstance(update_date, str):
            raise TypeError("Expected argument 'update_date' to be a str")
        pulumi.set(__self__, "update_date", update_date)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="attachmentCount")
    def attachment_count(self) -> Optional[int]:
        return pulumi.get(self, "attachment_count")

    @property
    @pulumi.getter(name="createDate")
    def create_date(self) -> Optional[str]:
        return pulumi.get(self, "create_date")

    @property
    @pulumi.getter(name="defaultVersionId")
    def default_version_id(self) -> Optional[str]:
        return pulumi.get(self, "default_version_id")

    @property
    @pulumi.getter
    def groups(self) -> Optional[Sequence[str]]:
        """
        The name (friendly name, not ARN) of the group to attach the policy to.
         This parameter allows (through its [regex pattern](https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex)) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter(name="isAttachable")
    def is_attachable(self) -> Optional[bool]:
        return pulumi.get(self, "is_attachable")

    @property
    @pulumi.getter(name="permissionsBoundaryUsageCount")
    def permissions_boundary_usage_count(self) -> Optional[int]:
        return pulumi.get(self, "permissions_boundary_usage_count")

    @property
    @pulumi.getter(name="policyArn")
    def policy_arn(self) -> Optional[str]:
        return pulumi.get(self, "policy_arn")

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Optional[Any]:
        """
        The JSON policy document that you want to use as the content for the new policy.
         You must provide policies in JSON format in IAM. However, for CFN templates formatted in YAML, you can provide the policy in JSON or YAML format. CFN always converts a YAML policy to JSON format before submitting it to IAM.
         The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see [IAM and character quotas](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length).
         To learn more about JSON policy grammar, see [Grammar of the IAM JSON policy language](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html) in the *IAM User Guide*. 
         The [regex pattern](https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex) used to validate this parameter is a string of characters consisting of the following:
          +  Any printable ASCII character ranging from the space character (``\\u0020``) through the end of the ASCII character range
          +  The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF``)
          +  The special characters tab (``\\u0009``), line feed (``\\u000A``), and carriage return (``\\u000D``)

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::IAM::ManagedPolicy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy_document")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> Optional[str]:
        return pulumi.get(self, "policy_id")

    @property
    @pulumi.getter
    def roles(self) -> Optional[Sequence[str]]:
        """
        The name (friendly name, not ARN) of the role to attach the policy to.
         This parameter allows (per its [regex pattern](https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex)) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
          If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy``) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service``) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that CFN deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        """
        return pulumi.get(self, "roles")

    @property
    @pulumi.getter(name="updateDate")
    def update_date(self) -> Optional[str]:
        return pulumi.get(self, "update_date")

    @property
    @pulumi.getter
    def users(self) -> Optional[Sequence[str]]:
        """
        The name (friendly name, not ARN) of the IAM user to attach the policy to.
         This parameter allows (through its [regex pattern](https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex)) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        """
        return pulumi.get(self, "users")


class AwaitableGetManagedPolicyResult(GetManagedPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedPolicyResult(
            attachment_count=self.attachment_count,
            create_date=self.create_date,
            default_version_id=self.default_version_id,
            groups=self.groups,
            is_attachable=self.is_attachable,
            permissions_boundary_usage_count=self.permissions_boundary_usage_count,
            policy_arn=self.policy_arn,
            policy_document=self.policy_document,
            policy_id=self.policy_id,
            roles=self.roles,
            update_date=self.update_date,
            users=self.users)


def get_managed_policy(policy_arn: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedPolicyResult:
    """
    Creates a new managed policy for your AWS-account.
     This operation creates a policy version with a version identifier of ``v1`` and sets v1 as the policy's default version. For more information about policy versions, see [Versioning for managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html) in the *IAM User Guide*.
     As a best practice, you can validate your IAM policies. To learn more, see [Validating IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_policy-validator.html) in the *IAM User Guide*.
     For more information about managed policies in general, see [Managed policies and inline policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *IAM User Guide*.
    """
    __args__ = dict()
    __args__['policyArn'] = policy_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iam:getManagedPolicy', __args__, opts=opts, typ=GetManagedPolicyResult).value

    return AwaitableGetManagedPolicyResult(
        attachment_count=pulumi.get(__ret__, 'attachment_count'),
        create_date=pulumi.get(__ret__, 'create_date'),
        default_version_id=pulumi.get(__ret__, 'default_version_id'),
        groups=pulumi.get(__ret__, 'groups'),
        is_attachable=pulumi.get(__ret__, 'is_attachable'),
        permissions_boundary_usage_count=pulumi.get(__ret__, 'permissions_boundary_usage_count'),
        policy_arn=pulumi.get(__ret__, 'policy_arn'),
        policy_document=pulumi.get(__ret__, 'policy_document'),
        policy_id=pulumi.get(__ret__, 'policy_id'),
        roles=pulumi.get(__ret__, 'roles'),
        update_date=pulumi.get(__ret__, 'update_date'),
        users=pulumi.get(__ret__, 'users'))
def get_managed_policy_output(policy_arn: Optional[pulumi.Input[str]] = None,
                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetManagedPolicyResult]:
    """
    Creates a new managed policy for your AWS-account.
     This operation creates a policy version with a version identifier of ``v1`` and sets v1 as the policy's default version. For more information about policy versions, see [Versioning for managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html) in the *IAM User Guide*.
     As a best practice, you can validate your IAM policies. To learn more, see [Validating IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_policy-validator.html) in the *IAM User Guide*.
     For more information about managed policies in general, see [Managed policies and inline policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *IAM User Guide*.
    """
    __args__ = dict()
    __args__['policyArn'] = policy_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iam:getManagedPolicy', __args__, opts=opts, typ=GetManagedPolicyResult)
    return __ret__.apply(lambda __response__: GetManagedPolicyResult(
        attachment_count=pulumi.get(__response__, 'attachment_count'),
        create_date=pulumi.get(__response__, 'create_date'),
        default_version_id=pulumi.get(__response__, 'default_version_id'),
        groups=pulumi.get(__response__, 'groups'),
        is_attachable=pulumi.get(__response__, 'is_attachable'),
        permissions_boundary_usage_count=pulumi.get(__response__, 'permissions_boundary_usage_count'),
        policy_arn=pulumi.get(__response__, 'policy_arn'),
        policy_document=pulumi.get(__response__, 'policy_document'),
        policy_id=pulumi.get(__response__, 'policy_id'),
        roles=pulumi.get(__response__, 'roles'),
        update_date=pulumi.get(__response__, 'update_date'),
        users=pulumi.get(__response__, 'users')))
