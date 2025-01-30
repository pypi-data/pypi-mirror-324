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
from ._enums import *

__all__ = [
    'BudgetsActionActionThresholdArgs',
    'BudgetsActionActionThresholdArgsDict',
    'BudgetsActionDefinitionArgs',
    'BudgetsActionDefinitionArgsDict',
    'BudgetsActionIamActionDefinitionArgs',
    'BudgetsActionIamActionDefinitionArgsDict',
    'BudgetsActionScpActionDefinitionArgs',
    'BudgetsActionScpActionDefinitionArgsDict',
    'BudgetsActionSsmActionDefinitionArgs',
    'BudgetsActionSsmActionDefinitionArgsDict',
    'BudgetsActionSubscriberArgs',
    'BudgetsActionSubscriberArgsDict',
]

MYPY = False

if not MYPY:
    class BudgetsActionActionThresholdArgsDict(TypedDict):
        type: pulumi.Input['BudgetsActionActionThresholdType']
        """
        The type of threshold for a notification.
        """
        value: pulumi.Input[float]
        """
        The threshold of a notification.
        """
elif False:
    BudgetsActionActionThresholdArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class BudgetsActionActionThresholdArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['BudgetsActionActionThresholdType'],
                 value: pulumi.Input[float]):
        """
        :param pulumi.Input['BudgetsActionActionThresholdType'] type: The type of threshold for a notification.
        :param pulumi.Input[float] value: The threshold of a notification.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['BudgetsActionActionThresholdType']:
        """
        The type of threshold for a notification.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['BudgetsActionActionThresholdType']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[float]:
        """
        The threshold of a notification.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[float]):
        pulumi.set(self, "value", value)


if not MYPY:
    class BudgetsActionDefinitionArgsDict(TypedDict):
        iam_action_definition: NotRequired[pulumi.Input['BudgetsActionIamActionDefinitionArgsDict']]
        """
        The AWS Identity and Access Management ( IAM ) action definition details.
        """
        scp_action_definition: NotRequired[pulumi.Input['BudgetsActionScpActionDefinitionArgsDict']]
        """
        The service control policies (SCP) action definition details.
        """
        ssm_action_definition: NotRequired[pulumi.Input['BudgetsActionSsmActionDefinitionArgsDict']]
        """
        The Amazon EC2 Systems Manager ( SSM ) action definition details.
        """
elif False:
    BudgetsActionDefinitionArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class BudgetsActionDefinitionArgs:
    def __init__(__self__, *,
                 iam_action_definition: Optional[pulumi.Input['BudgetsActionIamActionDefinitionArgs']] = None,
                 scp_action_definition: Optional[pulumi.Input['BudgetsActionScpActionDefinitionArgs']] = None,
                 ssm_action_definition: Optional[pulumi.Input['BudgetsActionSsmActionDefinitionArgs']] = None):
        """
        :param pulumi.Input['BudgetsActionIamActionDefinitionArgs'] iam_action_definition: The AWS Identity and Access Management ( IAM ) action definition details.
        :param pulumi.Input['BudgetsActionScpActionDefinitionArgs'] scp_action_definition: The service control policies (SCP) action definition details.
        :param pulumi.Input['BudgetsActionSsmActionDefinitionArgs'] ssm_action_definition: The Amazon EC2 Systems Manager ( SSM ) action definition details.
        """
        if iam_action_definition is not None:
            pulumi.set(__self__, "iam_action_definition", iam_action_definition)
        if scp_action_definition is not None:
            pulumi.set(__self__, "scp_action_definition", scp_action_definition)
        if ssm_action_definition is not None:
            pulumi.set(__self__, "ssm_action_definition", ssm_action_definition)

    @property
    @pulumi.getter(name="iamActionDefinition")
    def iam_action_definition(self) -> Optional[pulumi.Input['BudgetsActionIamActionDefinitionArgs']]:
        """
        The AWS Identity and Access Management ( IAM ) action definition details.
        """
        return pulumi.get(self, "iam_action_definition")

    @iam_action_definition.setter
    def iam_action_definition(self, value: Optional[pulumi.Input['BudgetsActionIamActionDefinitionArgs']]):
        pulumi.set(self, "iam_action_definition", value)

    @property
    @pulumi.getter(name="scpActionDefinition")
    def scp_action_definition(self) -> Optional[pulumi.Input['BudgetsActionScpActionDefinitionArgs']]:
        """
        The service control policies (SCP) action definition details.
        """
        return pulumi.get(self, "scp_action_definition")

    @scp_action_definition.setter
    def scp_action_definition(self, value: Optional[pulumi.Input['BudgetsActionScpActionDefinitionArgs']]):
        pulumi.set(self, "scp_action_definition", value)

    @property
    @pulumi.getter(name="ssmActionDefinition")
    def ssm_action_definition(self) -> Optional[pulumi.Input['BudgetsActionSsmActionDefinitionArgs']]:
        """
        The Amazon EC2 Systems Manager ( SSM ) action definition details.
        """
        return pulumi.get(self, "ssm_action_definition")

    @ssm_action_definition.setter
    def ssm_action_definition(self, value: Optional[pulumi.Input['BudgetsActionSsmActionDefinitionArgs']]):
        pulumi.set(self, "ssm_action_definition", value)


if not MYPY:
    class BudgetsActionIamActionDefinitionArgsDict(TypedDict):
        policy_arn: pulumi.Input[str]
        """
        The Amazon Resource Name (ARN) of the policy to be attached.
        """
        groups: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        A list of groups to be attached. There must be at least one group.
        """
        roles: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        A list of roles to be attached. There must be at least one role.
        """
        users: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        A list of users to be attached. There must be at least one user.
        """
elif False:
    BudgetsActionIamActionDefinitionArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class BudgetsActionIamActionDefinitionArgs:
    def __init__(__self__, *,
                 policy_arn: pulumi.Input[str],
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] policy_arn: The Amazon Resource Name (ARN) of the policy to be attached.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: A list of groups to be attached. There must be at least one group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] roles: A list of roles to be attached. There must be at least one role.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users: A list of users to be attached. There must be at least one user.
        """
        pulumi.set(__self__, "policy_arn", policy_arn)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if roles is not None:
            pulumi.set(__self__, "roles", roles)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="policyArn")
    def policy_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the policy to be attached.
        """
        return pulumi.get(self, "policy_arn")

    @policy_arn.setter
    def policy_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_arn", value)

    @property
    @pulumi.getter
    def groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of groups to be attached. There must be at least one group.
        """
        return pulumi.get(self, "groups")

    @groups.setter
    def groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "groups", value)

    @property
    @pulumi.getter
    def roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of roles to be attached. There must be at least one role.
        """
        return pulumi.get(self, "roles")

    @roles.setter
    def roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "roles", value)

    @property
    @pulumi.getter
    def users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of users to be attached. There must be at least one user.
        """
        return pulumi.get(self, "users")

    @users.setter
    def users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "users", value)


if not MYPY:
    class BudgetsActionScpActionDefinitionArgsDict(TypedDict):
        policy_id: pulumi.Input[str]
        """
        The policy ID attached.
        """
        target_ids: pulumi.Input[Sequence[pulumi.Input[str]]]
        """
        A list of target IDs.
        """
elif False:
    BudgetsActionScpActionDefinitionArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class BudgetsActionScpActionDefinitionArgs:
    def __init__(__self__, *,
                 policy_id: pulumi.Input[str],
                 target_ids: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        :param pulumi.Input[str] policy_id: The policy ID attached.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] target_ids: A list of target IDs.
        """
        pulumi.set(__self__, "policy_id", policy_id)
        pulumi.set(__self__, "target_ids", target_ids)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> pulumi.Input[str]:
        """
        The policy ID attached.
        """
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter(name="targetIds")
    def target_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of target IDs.
        """
        return pulumi.get(self, "target_ids")

    @target_ids.setter
    def target_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "target_ids", value)


if not MYPY:
    class BudgetsActionSsmActionDefinitionArgsDict(TypedDict):
        instance_ids: pulumi.Input[Sequence[pulumi.Input[str]]]
        """
        The EC2 and RDS instance IDs.
        """
        region: pulumi.Input[str]
        """
        The Region to run the ( SSM ) document.
        """
        subtype: pulumi.Input['BudgetsActionSsmActionDefinitionSubtype']
        """
        The action subType.
        """
elif False:
    BudgetsActionSsmActionDefinitionArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class BudgetsActionSsmActionDefinitionArgs:
    def __init__(__self__, *,
                 instance_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 region: pulumi.Input[str],
                 subtype: pulumi.Input['BudgetsActionSsmActionDefinitionSubtype']):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] instance_ids: The EC2 and RDS instance IDs.
        :param pulumi.Input[str] region: The Region to run the ( SSM ) document.
        :param pulumi.Input['BudgetsActionSsmActionDefinitionSubtype'] subtype: The action subType.
        """
        pulumi.set(__self__, "instance_ids", instance_ids)
        pulumi.set(__self__, "region", region)
        pulumi.set(__self__, "subtype", subtype)

    @property
    @pulumi.getter(name="instanceIds")
    def instance_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The EC2 and RDS instance IDs.
        """
        return pulumi.get(self, "instance_ids")

    @instance_ids.setter
    def instance_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "instance_ids", value)

    @property
    @pulumi.getter
    def region(self) -> pulumi.Input[str]:
        """
        The Region to run the ( SSM ) document.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: pulumi.Input[str]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def subtype(self) -> pulumi.Input['BudgetsActionSsmActionDefinitionSubtype']:
        """
        The action subType.
        """
        return pulumi.get(self, "subtype")

    @subtype.setter
    def subtype(self, value: pulumi.Input['BudgetsActionSsmActionDefinitionSubtype']):
        pulumi.set(self, "subtype", value)


if not MYPY:
    class BudgetsActionSubscriberArgsDict(TypedDict):
        address: pulumi.Input[str]
        """
        The address that AWS sends budget notifications to, either an SNS topic or an email.

        When you create a subscriber, the value of `Address` can't contain line breaks.
        """
        type: pulumi.Input['BudgetsActionSubscriberType']
        """
        The type of notification that AWS sends to a subscriber.
        """
elif False:
    BudgetsActionSubscriberArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class BudgetsActionSubscriberArgs:
    def __init__(__self__, *,
                 address: pulumi.Input[str],
                 type: pulumi.Input['BudgetsActionSubscriberType']):
        """
        :param pulumi.Input[str] address: The address that AWS sends budget notifications to, either an SNS topic or an email.
               
               When you create a subscriber, the value of `Address` can't contain line breaks.
        :param pulumi.Input['BudgetsActionSubscriberType'] type: The type of notification that AWS sends to a subscriber.
        """
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Input[str]:
        """
        The address that AWS sends budget notifications to, either an SNS topic or an email.

        When you create a subscriber, the value of `Address` can't contain line breaks.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: pulumi.Input[str]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['BudgetsActionSubscriberType']:
        """
        The type of notification that AWS sends to a subscriber.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['BudgetsActionSubscriberType']):
        pulumi.set(self, "type", value)


