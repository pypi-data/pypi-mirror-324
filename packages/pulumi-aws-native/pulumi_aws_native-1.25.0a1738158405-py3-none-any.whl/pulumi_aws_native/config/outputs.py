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
    'AssumeRole',
    'AutoNaming',
    'DefaultTags',
    'Endpoints',
    'IgnoreTags',
]

@pulumi.output_type
class AssumeRole(dict):
    """
    The configuration for a Provider to assume a role.
    """
    def __init__(__self__, *,
                 duration_seconds: Optional[int] = None,
                 external_id: Optional[str] = None,
                 policy: Optional[str] = None,
                 policy_arns: Optional[Sequence[str]] = None,
                 role_arn: Optional[str] = None,
                 session_name: Optional[str] = None,
                 tags: Optional[Mapping[str, str]] = None,
                 transitive_tag_keys: Optional[Sequence[str]] = None):
        """
        The configuration for a Provider to assume a role.
        :param int duration_seconds: Number of seconds to restrict the assume role session duration.
        :param str external_id: External identifier to use when assuming the role.
        :param str policy: IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.
        :param Sequence[str] policy_arns: Set of Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the role.
        :param str role_arn: Amazon Resource Name (ARN) of the IAM Role to assume.
        :param str session_name: Session name to use when assuming the role.
        :param Mapping[str, str] tags: Map of assume role session tags.
        :param Sequence[str] transitive_tag_keys: A list of keys for session tags that you want to set as transitive. If you set a tag key as transitive, the corresponding key and value passes to subsequent sessions in a role chain.
        """
        if duration_seconds is not None:
            pulumi.set(__self__, "duration_seconds", duration_seconds)
        if external_id is not None:
            pulumi.set(__self__, "external_id", external_id)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if policy_arns is not None:
            pulumi.set(__self__, "policy_arns", policy_arns)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if session_name is not None:
            pulumi.set(__self__, "session_name", session_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if transitive_tag_keys is not None:
            pulumi.set(__self__, "transitive_tag_keys", transitive_tag_keys)

    @property
    @pulumi.getter(name="durationSeconds")
    def duration_seconds(self) -> Optional[int]:
        """
        Number of seconds to restrict the assume role session duration.
        """
        return pulumi.get(self, "duration_seconds")

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> Optional[str]:
        """
        External identifier to use when assuming the role.
        """
        return pulumi.get(self, "external_id")

    @property
    @pulumi.getter
    def policy(self) -> Optional[str]:
        """
        IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="policyArns")
    def policy_arns(self) -> Optional[Sequence[str]]:
        """
        Set of Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the role.
        """
        return pulumi.get(self, "policy_arns")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        Amazon Resource Name (ARN) of the IAM Role to assume.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="sessionName")
    def session_name(self) -> Optional[str]:
        """
        Session name to use when assuming the role.
        """
        return pulumi.get(self, "session_name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Map of assume role session tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transitiveTagKeys")
    def transitive_tag_keys(self) -> Optional[Sequence[str]]:
        """
        A list of keys for session tags that you want to set as transitive. If you set a tag key as transitive, the corresponding key and value passes to subsequent sessions in a role chain.
        """
        return pulumi.get(self, "transitive_tag_keys")


@pulumi.output_type
class AutoNaming(dict):
    """
    The configuration for automatically naming resources.
    """
    def __init__(__self__, *,
                 auto_trim: Optional[bool] = None,
                 random_suffix_min_length: Optional[int] = None):
        """
        The configuration for automatically naming resources.
        :param bool auto_trim: Automatically trim the auto-generated name to meet the maximum length constraint.
        :param int random_suffix_min_length: The minimum length of the random suffix to append to the auto-generated name.
        """
        if auto_trim is not None:
            pulumi.set(__self__, "auto_trim", auto_trim)
        if random_suffix_min_length is None:
            random_suffix_min_length = 1
        if random_suffix_min_length is not None:
            pulumi.set(__self__, "random_suffix_min_length", random_suffix_min_length)

    @property
    @pulumi.getter(name="autoTrim")
    def auto_trim(self) -> Optional[bool]:
        """
        Automatically trim the auto-generated name to meet the maximum length constraint.
        """
        return pulumi.get(self, "auto_trim")

    @property
    @pulumi.getter(name="randomSuffixMinLength")
    def random_suffix_min_length(self) -> Optional[int]:
        """
        The minimum length of the random suffix to append to the auto-generated name.
        """
        return pulumi.get(self, "random_suffix_min_length")


@pulumi.output_type
class DefaultTags(dict):
    """
    The configuration with resource tag settings to apply across all resources handled by this provider. This is designed to replace redundant per-resource `tags` configurations. Provider tags can be overridden with new values, but not excluded from specific resources. To override provider tag values, use the `tags` argument within a resource to configure new tag values for matching keys.
    """
    def __init__(__self__, *,
                 tags: Optional[Mapping[str, str]] = None):
        """
        The configuration with resource tag settings to apply across all resources handled by this provider. This is designed to replace redundant per-resource `tags` configurations. Provider tags can be overridden with new values, but not excluded from specific resources. To override provider tag values, use the `tags` argument within a resource to configure new tag values for matching keys.
        :param Mapping[str, str] tags: A group of tags to set across all resources.
        """
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        A group of tags to set across all resources.
        """
        return pulumi.get(self, "tags")


@pulumi.output_type
class Endpoints(dict):
    """
    The configuration for for customizing service endpoints.
    """
    def __init__(__self__, *,
                 cloudcontrol: Optional[str] = None,
                 cloudformation: Optional[str] = None,
                 ec2: Optional[str] = None,
                 ssm: Optional[str] = None,
                 sts: Optional[str] = None):
        """
        The configuration for for customizing service endpoints.
        :param str cloudcontrol: Override the default endpoint for AWS CloudControl
        :param str cloudformation: Override the default endpoint for AWS CloudFormation
        :param str ec2: Override the default endpoint for AWS Elastic Compute Cloud (EC2)
        :param str ssm: Override the default endpoint for AWS Systems Manager
        :param str sts: Override the default endpoint for AWS Security Token Service (STS)
        """
        if cloudcontrol is not None:
            pulumi.set(__self__, "cloudcontrol", cloudcontrol)
        if cloudformation is not None:
            pulumi.set(__self__, "cloudformation", cloudformation)
        if ec2 is not None:
            pulumi.set(__self__, "ec2", ec2)
        if ssm is not None:
            pulumi.set(__self__, "ssm", ssm)
        if sts is not None:
            pulumi.set(__self__, "sts", sts)

    @property
    @pulumi.getter
    def cloudcontrol(self) -> Optional[str]:
        """
        Override the default endpoint for AWS CloudControl
        """
        return pulumi.get(self, "cloudcontrol")

    @property
    @pulumi.getter
    def cloudformation(self) -> Optional[str]:
        """
        Override the default endpoint for AWS CloudFormation
        """
        return pulumi.get(self, "cloudformation")

    @property
    @pulumi.getter
    def ec2(self) -> Optional[str]:
        """
        Override the default endpoint for AWS Elastic Compute Cloud (EC2)
        """
        return pulumi.get(self, "ec2")

    @property
    @pulumi.getter
    def ssm(self) -> Optional[str]:
        """
        Override the default endpoint for AWS Systems Manager
        """
        return pulumi.get(self, "ssm")

    @property
    @pulumi.getter
    def sts(self) -> Optional[str]:
        """
        Override the default endpoint for AWS Security Token Service (STS)
        """
        return pulumi.get(self, "sts")


@pulumi.output_type
class IgnoreTags(dict):
    """
    The configuration with resource tag settings to ignore across all resources handled by this provider (except any individual service tag resources such as `ec2.Tag`) for situations where external systems are managing certain resource tags.
    """
    def __init__(__self__, *,
                 key_prefixes: Optional[Sequence[str]] = None,
                 keys: Optional[Sequence[str]] = None):
        """
        The configuration with resource tag settings to ignore across all resources handled by this provider (except any individual service tag resources such as `ec2.Tag`) for situations where external systems are managing certain resource tags.
        :param Sequence[str] key_prefixes: List of exact resource tag keys to ignore across all resources handled by this provider. This configuration prevents Pulumi from returning the tag in any `tags` attributes and displaying any configuration difference for the tag value. If any resource configuration still has this tag key configured in the `tags` argument, it will display a perpetual difference until the tag is removed from the argument or `ignoreChanges` is also used.
        :param Sequence[str] keys: List of resource tag key prefixes to ignore across all resources handled by this provider. This configuration prevents Pulumi from returning any tag key matching the prefixes in any `tags` attributes and displaying any configuration difference for those tag values. If any resource configuration still has a tag matching one of the prefixes configured in the `tags` argument, it will display a perpetual difference until the tag is removed from the argument or `ignoreChanges` is also used.
        """
        if key_prefixes is not None:
            pulumi.set(__self__, "key_prefixes", key_prefixes)
        if keys is not None:
            pulumi.set(__self__, "keys", keys)

    @property
    @pulumi.getter(name="keyPrefixes")
    def key_prefixes(self) -> Optional[Sequence[str]]:
        """
        List of exact resource tag keys to ignore across all resources handled by this provider. This configuration prevents Pulumi from returning the tag in any `tags` attributes and displaying any configuration difference for the tag value. If any resource configuration still has this tag key configured in the `tags` argument, it will display a perpetual difference until the tag is removed from the argument or `ignoreChanges` is also used.
        """
        return pulumi.get(self, "key_prefixes")

    @property
    @pulumi.getter
    def keys(self) -> Optional[Sequence[str]]:
        """
        List of resource tag key prefixes to ignore across all resources handled by this provider. This configuration prevents Pulumi from returning any tag key matching the prefixes in any `tags` attributes and displaying any configuration difference for those tag values. If any resource configuration still has a tag matching one of the prefixes configured in the `tags` argument, it will display a perpetual difference until the tag is removed from the argument or `ignoreChanges` is also used.
        """
        return pulumi.get(self, "keys")


