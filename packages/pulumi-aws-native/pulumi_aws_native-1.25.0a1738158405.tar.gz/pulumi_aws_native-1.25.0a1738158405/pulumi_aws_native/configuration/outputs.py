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

__all__ = [
    'ComplianceProperties',
    'ConfigRuleCustomPolicyDetails',
    'ConfigRuleEvaluationModeConfiguration',
    'ConfigRuleScope',
    'ConfigRuleSource',
    'ConfigRuleSourceDetail',
    'ConfigurationAggregatorAccountAggregationSource',
    'ConfigurationAggregatorOrganizationAggregationSource',
    'ConformancePackInputParameter',
    'OrganizationConformancePackConformancePackInputParameter',
    'TemplateSsmDocumentDetailsProperties',
]

@pulumi.output_type
class ComplianceProperties(dict):
    """
    Indicates whether an AWS resource or CC rule is compliant and provides the number of contributors that affect the compliance.
    """
    def __init__(__self__, *,
                 type: Optional[str] = None):
        """
        Indicates whether an AWS resource or CC rule is compliant and provides the number of contributors that affect the compliance.
        :param str type: Compliance type determined by the Config rule
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Compliance type determined by the Config rule
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class ConfigRuleCustomPolicyDetails(dict):
    """
    Provides the CustomPolicyDetails, the rule owner (```` for managed rules, ``CUSTOM_POLICY`` for Custom Policy rules, and ``CUSTOM_LAMBDA`` for Custom Lambda rules), the rule identifier, and the events that cause the evaluation of your AWS resources.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "enableDebugLogDelivery":
            suggest = "enable_debug_log_delivery"
        elif key == "policyRuntime":
            suggest = "policy_runtime"
        elif key == "policyText":
            suggest = "policy_text"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigRuleCustomPolicyDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigRuleCustomPolicyDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigRuleCustomPolicyDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enable_debug_log_delivery: Optional[bool] = None,
                 policy_runtime: Optional[str] = None,
                 policy_text: Optional[str] = None):
        """
        Provides the CustomPolicyDetails, the rule owner (```` for managed rules, ``CUSTOM_POLICY`` for Custom Policy rules, and ``CUSTOM_LAMBDA`` for Custom Lambda rules), the rule identifier, and the events that cause the evaluation of your AWS resources.
        :param bool enable_debug_log_delivery: The boolean expression for enabling debug logging for your CC Custom Policy rule. The default value is ``false``.
        :param str policy_runtime: The runtime system for your CC Custom Policy rule. Guard is a policy-as-code language that allows you to write policies that are enforced by CC Custom Policy rules. For more information about Guard, see the [Guard GitHub Repository](https://docs.aws.amazon.com/https://github.com/aws-cloudformation/cloudformation-guard).
        :param str policy_text: The policy definition containing the logic for your CC Custom Policy rule.
        """
        if enable_debug_log_delivery is not None:
            pulumi.set(__self__, "enable_debug_log_delivery", enable_debug_log_delivery)
        if policy_runtime is not None:
            pulumi.set(__self__, "policy_runtime", policy_runtime)
        if policy_text is not None:
            pulumi.set(__self__, "policy_text", policy_text)

    @property
    @pulumi.getter(name="enableDebugLogDelivery")
    def enable_debug_log_delivery(self) -> Optional[bool]:
        """
        The boolean expression for enabling debug logging for your CC Custom Policy rule. The default value is ``false``.
        """
        return pulumi.get(self, "enable_debug_log_delivery")

    @property
    @pulumi.getter(name="policyRuntime")
    def policy_runtime(self) -> Optional[str]:
        """
        The runtime system for your CC Custom Policy rule. Guard is a policy-as-code language that allows you to write policies that are enforced by CC Custom Policy rules. For more information about Guard, see the [Guard GitHub Repository](https://docs.aws.amazon.com/https://github.com/aws-cloudformation/cloudformation-guard).
        """
        return pulumi.get(self, "policy_runtime")

    @property
    @pulumi.getter(name="policyText")
    def policy_text(self) -> Optional[str]:
        """
        The policy definition containing the logic for your CC Custom Policy rule.
        """
        return pulumi.get(self, "policy_text")


@pulumi.output_type
class ConfigRuleEvaluationModeConfiguration(dict):
    """
    The configuration object for CC rule evaluation mode. The supported valid values are Detective or Proactive.
    """
    def __init__(__self__, *,
                 mode: Optional[str] = None):
        """
        The configuration object for CC rule evaluation mode. The supported valid values are Detective or Proactive.
        :param str mode: The mode of an evaluation. The valid values are Detective or Proactive.
        """
        if mode is not None:
            pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter
    def mode(self) -> Optional[str]:
        """
        The mode of an evaluation. The valid values are Detective or Proactive.
        """
        return pulumi.get(self, "mode")


@pulumi.output_type
class ConfigRuleScope(dict):
    """
    Defines which resources trigger an evaluation for an CC rule. The scope can include one or more resource types, a combination of a tag key and value, or a combination of one resource type and one resource ID. Specify a scope to constrain which resources trigger an evaluation for a rule. Otherwise, evaluations for the rule are triggered when any resource in your recording group changes in configuration.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "complianceResourceId":
            suggest = "compliance_resource_id"
        elif key == "complianceResourceTypes":
            suggest = "compliance_resource_types"
        elif key == "tagKey":
            suggest = "tag_key"
        elif key == "tagValue":
            suggest = "tag_value"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigRuleScope. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigRuleScope.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigRuleScope.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 compliance_resource_id: Optional[str] = None,
                 compliance_resource_types: Optional[Sequence[str]] = None,
                 tag_key: Optional[str] = None,
                 tag_value: Optional[str] = None):
        """
        Defines which resources trigger an evaluation for an CC rule. The scope can include one or more resource types, a combination of a tag key and value, or a combination of one resource type and one resource ID. Specify a scope to constrain which resources trigger an evaluation for a rule. Otherwise, evaluations for the rule are triggered when any resource in your recording group changes in configuration.
        :param str compliance_resource_id: The ID of the only AWS resource that you want to trigger an evaluation for the rule. If you specify a resource ID, you must specify one resource type for ``ComplianceResourceTypes``.
        :param Sequence[str] compliance_resource_types: The resource types of only those AWS resources that you want to trigger an evaluation for the rule. You can only specify one type if you also specify a resource ID for ``ComplianceResourceId``.
        :param str tag_key: The tag key that is applied to only those AWS resources that you want to trigger an evaluation for the rule.
        :param str tag_value: The tag value applied to only those AWS resources that you want to trigger an evaluation for the rule. If you specify a value for ``TagValue``, you must also specify a value for ``TagKey``.
        """
        if compliance_resource_id is not None:
            pulumi.set(__self__, "compliance_resource_id", compliance_resource_id)
        if compliance_resource_types is not None:
            pulumi.set(__self__, "compliance_resource_types", compliance_resource_types)
        if tag_key is not None:
            pulumi.set(__self__, "tag_key", tag_key)
        if tag_value is not None:
            pulumi.set(__self__, "tag_value", tag_value)

    @property
    @pulumi.getter(name="complianceResourceId")
    def compliance_resource_id(self) -> Optional[str]:
        """
        The ID of the only AWS resource that you want to trigger an evaluation for the rule. If you specify a resource ID, you must specify one resource type for ``ComplianceResourceTypes``.
        """
        return pulumi.get(self, "compliance_resource_id")

    @property
    @pulumi.getter(name="complianceResourceTypes")
    def compliance_resource_types(self) -> Optional[Sequence[str]]:
        """
        The resource types of only those AWS resources that you want to trigger an evaluation for the rule. You can only specify one type if you also specify a resource ID for ``ComplianceResourceId``.
        """
        return pulumi.get(self, "compliance_resource_types")

    @property
    @pulumi.getter(name="tagKey")
    def tag_key(self) -> Optional[str]:
        """
        The tag key that is applied to only those AWS resources that you want to trigger an evaluation for the rule.
        """
        return pulumi.get(self, "tag_key")

    @property
    @pulumi.getter(name="tagValue")
    def tag_value(self) -> Optional[str]:
        """
        The tag value applied to only those AWS resources that you want to trigger an evaluation for the rule. If you specify a value for ``TagValue``, you must also specify a value for ``TagKey``.
        """
        return pulumi.get(self, "tag_value")


@pulumi.output_type
class ConfigRuleSource(dict):
    """
    Provides the CustomPolicyDetails, the rule owner (```` for managed rules, ``CUSTOM_POLICY`` for Custom Policy rules, and ``CUSTOM_LAMBDA`` for Custom Lambda rules), the rule identifier, and the events that cause the evaluation of your AWS resources.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "customPolicyDetails":
            suggest = "custom_policy_details"
        elif key == "sourceDetails":
            suggest = "source_details"
        elif key == "sourceIdentifier":
            suggest = "source_identifier"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigRuleSource. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigRuleSource.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigRuleSource.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 owner: str,
                 custom_policy_details: Optional['outputs.ConfigRuleCustomPolicyDetails'] = None,
                 source_details: Optional[Sequence['outputs.ConfigRuleSourceDetail']] = None,
                 source_identifier: Optional[str] = None):
        """
        Provides the CustomPolicyDetails, the rule owner (```` for managed rules, ``CUSTOM_POLICY`` for Custom Policy rules, and ``CUSTOM_LAMBDA`` for Custom Lambda rules), the rule identifier, and the events that cause the evaluation of your AWS resources.
        :param str owner: Indicates whether AWS or the customer owns and manages the CC rule.
                 CC Managed Rules are predefined rules owned by AWS. For more information, see [Managed Rules](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_use-managed-rules.html) in the *developer guide*.
                 CC Custom Rules are rules that you can develop either with Guard (``CUSTOM_POLICY``) or LAMlong (``CUSTOM_LAMBDA``). For more information, see [Custom Rules](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html) in the *developer guide*.
        :param 'ConfigRuleCustomPolicyDetails' custom_policy_details: Provides the runtime system, policy definition, and whether debug logging is enabled. Required when owner is set to ``CUSTOM_POLICY``.
        :param Sequence['ConfigRuleSourceDetail'] source_details: Provides the source and the message types that cause CC to evaluate your AWS resources against a rule. It also provides the frequency with which you want CC to run evaluations for the rule if the trigger type is periodic.
                If the owner is set to ``CUSTOM_POLICY``, the only acceptable values for the CC rule trigger message type are ``ConfigurationItemChangeNotification`` and ``OversizedConfigurationItemChangeNotification``.
        :param str source_identifier: For CC Managed rules, a predefined identifier from a list. For example, ``IAM_PASSWORD_POLICY`` is a managed rule. To reference a managed rule, see [List of Managed Rules](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html).
                For CC Custom Lambda rules, the identifier is the Amazon Resource Name (ARN) of the rule's LAMlong function, such as ``arn:aws:lambda:us-east-2:123456789012:function:custom_rule_name``.
                For CC Custom Policy rules, this field will be ignored.
        """
        pulumi.set(__self__, "owner", owner)
        if custom_policy_details is not None:
            pulumi.set(__self__, "custom_policy_details", custom_policy_details)
        if source_details is not None:
            pulumi.set(__self__, "source_details", source_details)
        if source_identifier is not None:
            pulumi.set(__self__, "source_identifier", source_identifier)

    @property
    @pulumi.getter
    def owner(self) -> str:
        """
        Indicates whether AWS or the customer owns and manages the CC rule.
          CC Managed Rules are predefined rules owned by AWS. For more information, see [Managed Rules](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_use-managed-rules.html) in the *developer guide*.
          CC Custom Rules are rules that you can develop either with Guard (``CUSTOM_POLICY``) or LAMlong (``CUSTOM_LAMBDA``). For more information, see [Custom Rules](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html) in the *developer guide*.
        """
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter(name="customPolicyDetails")
    def custom_policy_details(self) -> Optional['outputs.ConfigRuleCustomPolicyDetails']:
        """
        Provides the runtime system, policy definition, and whether debug logging is enabled. Required when owner is set to ``CUSTOM_POLICY``.
        """
        return pulumi.get(self, "custom_policy_details")

    @property
    @pulumi.getter(name="sourceDetails")
    def source_details(self) -> Optional[Sequence['outputs.ConfigRuleSourceDetail']]:
        """
        Provides the source and the message types that cause CC to evaluate your AWS resources against a rule. It also provides the frequency with which you want CC to run evaluations for the rule if the trigger type is periodic.
         If the owner is set to ``CUSTOM_POLICY``, the only acceptable values for the CC rule trigger message type are ``ConfigurationItemChangeNotification`` and ``OversizedConfigurationItemChangeNotification``.
        """
        return pulumi.get(self, "source_details")

    @property
    @pulumi.getter(name="sourceIdentifier")
    def source_identifier(self) -> Optional[str]:
        """
        For CC Managed rules, a predefined identifier from a list. For example, ``IAM_PASSWORD_POLICY`` is a managed rule. To reference a managed rule, see [List of Managed Rules](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html).
         For CC Custom Lambda rules, the identifier is the Amazon Resource Name (ARN) of the rule's LAMlong function, such as ``arn:aws:lambda:us-east-2:123456789012:function:custom_rule_name``.
         For CC Custom Policy rules, this field will be ignored.
        """
        return pulumi.get(self, "source_identifier")


@pulumi.output_type
class ConfigRuleSourceDetail(dict):
    """
    Provides the source and the message types that trigger CC to evaluate your AWS resources against a rule. It also provides the frequency with which you want CC to run evaluations for the rule if the trigger type is periodic. You can specify the parameter values for ``SourceDetail`` only for custom rules.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "eventSource":
            suggest = "event_source"
        elif key == "messageType":
            suggest = "message_type"
        elif key == "maximumExecutionFrequency":
            suggest = "maximum_execution_frequency"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigRuleSourceDetail. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigRuleSourceDetail.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigRuleSourceDetail.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 event_source: str,
                 message_type: str,
                 maximum_execution_frequency: Optional[str] = None):
        """
        Provides the source and the message types that trigger CC to evaluate your AWS resources against a rule. It also provides the frequency with which you want CC to run evaluations for the rule if the trigger type is periodic. You can specify the parameter values for ``SourceDetail`` only for custom rules.
        :param str event_source: The source of the event, such as an AWS service, that triggers CC to evaluate your AWS resources.
        :param str message_type: The type of notification that triggers CC to run an evaluation for a rule. You can specify the following notification types:
                 +   ``ConfigurationItemChangeNotification`` - Triggers an evaluation when CC delivers a configuration item as a result of a resource change.
                 +   ``OversizedConfigurationItemChangeNotification`` - Triggers an evaluation when CC delivers an oversized configuration item. CC may generate this notification type when a resource changes and the notification exceeds the maximum size allowed by Amazon SNS.
                 +   ``ScheduledNotification`` - Triggers a periodic evaluation at the frequency specified for ``MaximumExecutionFrequency``.
                 +   ``ConfigurationSnapshotDeliveryCompleted`` - Triggers a periodic evaluation when CC delivers a configuration snapshot.
                 
                If you want your custom rule to be triggered by configuration changes, specify two SourceDetail objects, one for ``ConfigurationItemChangeNotification`` and one for ``OversizedConfigurationItemChangeNotification``.
        :param str maximum_execution_frequency: The frequency at which you want CC to run evaluations for a custom rule with a periodic trigger. If you specify a value for ``MaximumExecutionFrequency``, then ``MessageType`` must use the ``ScheduledNotification`` value.
                 By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter.
                Based on the valid value you choose, CC runs evaluations once for each valid value. For example, if you choose ``Three_Hours``, CC runs evaluations once every three hours. In this case, ``Three_Hours`` is the frequency of this rule.
        """
        pulumi.set(__self__, "event_source", event_source)
        pulumi.set(__self__, "message_type", message_type)
        if maximum_execution_frequency is not None:
            pulumi.set(__self__, "maximum_execution_frequency", maximum_execution_frequency)

    @property
    @pulumi.getter(name="eventSource")
    def event_source(self) -> str:
        """
        The source of the event, such as an AWS service, that triggers CC to evaluate your AWS resources.
        """
        return pulumi.get(self, "event_source")

    @property
    @pulumi.getter(name="messageType")
    def message_type(self) -> str:
        """
        The type of notification that triggers CC to run an evaluation for a rule. You can specify the following notification types:
          +   ``ConfigurationItemChangeNotification`` - Triggers an evaluation when CC delivers a configuration item as a result of a resource change.
          +   ``OversizedConfigurationItemChangeNotification`` - Triggers an evaluation when CC delivers an oversized configuration item. CC may generate this notification type when a resource changes and the notification exceeds the maximum size allowed by Amazon SNS.
          +   ``ScheduledNotification`` - Triggers a periodic evaluation at the frequency specified for ``MaximumExecutionFrequency``.
          +   ``ConfigurationSnapshotDeliveryCompleted`` - Triggers a periodic evaluation when CC delivers a configuration snapshot.
          
         If you want your custom rule to be triggered by configuration changes, specify two SourceDetail objects, one for ``ConfigurationItemChangeNotification`` and one for ``OversizedConfigurationItemChangeNotification``.
        """
        return pulumi.get(self, "message_type")

    @property
    @pulumi.getter(name="maximumExecutionFrequency")
    def maximum_execution_frequency(self) -> Optional[str]:
        """
        The frequency at which you want CC to run evaluations for a custom rule with a periodic trigger. If you specify a value for ``MaximumExecutionFrequency``, then ``MessageType`` must use the ``ScheduledNotification`` value.
          By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter.
         Based on the valid value you choose, CC runs evaluations once for each valid value. For example, if you choose ``Three_Hours``, CC runs evaluations once every three hours. In this case, ``Three_Hours`` is the frequency of this rule.
        """
        return pulumi.get(self, "maximum_execution_frequency")


@pulumi.output_type
class ConfigurationAggregatorAccountAggregationSource(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accountIds":
            suggest = "account_ids"
        elif key == "allAwsRegions":
            suggest = "all_aws_regions"
        elif key == "awsRegions":
            suggest = "aws_regions"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigurationAggregatorAccountAggregationSource. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigurationAggregatorAccountAggregationSource.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigurationAggregatorAccountAggregationSource.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 account_ids: Sequence[str],
                 all_aws_regions: Optional[bool] = None,
                 aws_regions: Optional[Sequence[str]] = None):
        """
        :param Sequence[str] account_ids: The 12-digit account ID of the account being aggregated.
        :param bool all_aws_regions: If true, aggregate existing AWS Config regions and future regions.
        :param Sequence[str] aws_regions: The source regions being aggregated.
        """
        pulumi.set(__self__, "account_ids", account_ids)
        if all_aws_regions is not None:
            pulumi.set(__self__, "all_aws_regions", all_aws_regions)
        if aws_regions is not None:
            pulumi.set(__self__, "aws_regions", aws_regions)

    @property
    @pulumi.getter(name="accountIds")
    def account_ids(self) -> Sequence[str]:
        """
        The 12-digit account ID of the account being aggregated.
        """
        return pulumi.get(self, "account_ids")

    @property
    @pulumi.getter(name="allAwsRegions")
    def all_aws_regions(self) -> Optional[bool]:
        """
        If true, aggregate existing AWS Config regions and future regions.
        """
        return pulumi.get(self, "all_aws_regions")

    @property
    @pulumi.getter(name="awsRegions")
    def aws_regions(self) -> Optional[Sequence[str]]:
        """
        The source regions being aggregated.
        """
        return pulumi.get(self, "aws_regions")


@pulumi.output_type
class ConfigurationAggregatorOrganizationAggregationSource(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "roleArn":
            suggest = "role_arn"
        elif key == "allAwsRegions":
            suggest = "all_aws_regions"
        elif key == "awsRegions":
            suggest = "aws_regions"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigurationAggregatorOrganizationAggregationSource. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigurationAggregatorOrganizationAggregationSource.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigurationAggregatorOrganizationAggregationSource.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 role_arn: str,
                 all_aws_regions: Optional[bool] = None,
                 aws_regions: Optional[Sequence[str]] = None):
        """
        :param str role_arn: ARN of the IAM role used to retrieve AWS Organizations details associated with the aggregator account.
        :param bool all_aws_regions: If true, aggregate existing AWS Config regions and future regions.
        :param Sequence[str] aws_regions: The source regions being aggregated.
        """
        pulumi.set(__self__, "role_arn", role_arn)
        if all_aws_regions is not None:
            pulumi.set(__self__, "all_aws_regions", all_aws_regions)
        if aws_regions is not None:
            pulumi.set(__self__, "aws_regions", aws_regions)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> str:
        """
        ARN of the IAM role used to retrieve AWS Organizations details associated with the aggregator account.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="allAwsRegions")
    def all_aws_regions(self) -> Optional[bool]:
        """
        If true, aggregate existing AWS Config regions and future regions.
        """
        return pulumi.get(self, "all_aws_regions")

    @property
    @pulumi.getter(name="awsRegions")
    def aws_regions(self) -> Optional[Sequence[str]]:
        """
        The source regions being aggregated.
        """
        return pulumi.get(self, "aws_regions")


@pulumi.output_type
class ConformancePackInputParameter(dict):
    """
    Input parameters in the form of key-value pairs for the conformance pack.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "parameterName":
            suggest = "parameter_name"
        elif key == "parameterValue":
            suggest = "parameter_value"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConformancePackInputParameter. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConformancePackInputParameter.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConformancePackInputParameter.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 parameter_name: str,
                 parameter_value: str):
        """
        Input parameters in the form of key-value pairs for the conformance pack.
        :param str parameter_name: One part of a key-value pair.
        :param str parameter_value: Another part of the key-value pair.
        """
        pulumi.set(__self__, "parameter_name", parameter_name)
        pulumi.set(__self__, "parameter_value", parameter_value)

    @property
    @pulumi.getter(name="parameterName")
    def parameter_name(self) -> str:
        """
        One part of a key-value pair.
        """
        return pulumi.get(self, "parameter_name")

    @property
    @pulumi.getter(name="parameterValue")
    def parameter_value(self) -> str:
        """
        Another part of the key-value pair.
        """
        return pulumi.get(self, "parameter_value")


@pulumi.output_type
class OrganizationConformancePackConformancePackInputParameter(dict):
    """
    Input parameters in the form of key-value pairs for the conformance pack.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "parameterName":
            suggest = "parameter_name"
        elif key == "parameterValue":
            suggest = "parameter_value"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationConformancePackConformancePackInputParameter. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationConformancePackConformancePackInputParameter.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationConformancePackConformancePackInputParameter.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 parameter_name: str,
                 parameter_value: str):
        """
        Input parameters in the form of key-value pairs for the conformance pack.
        :param str parameter_name: One part of a key-value pair.
        :param str parameter_value: One part of a key-value pair.
        """
        pulumi.set(__self__, "parameter_name", parameter_name)
        pulumi.set(__self__, "parameter_value", parameter_value)

    @property
    @pulumi.getter(name="parameterName")
    def parameter_name(self) -> str:
        """
        One part of a key-value pair.
        """
        return pulumi.get(self, "parameter_name")

    @property
    @pulumi.getter(name="parameterValue")
    def parameter_value(self) -> str:
        """
        One part of a key-value pair.
        """
        return pulumi.get(self, "parameter_value")


@pulumi.output_type
class TemplateSsmDocumentDetailsProperties(dict):
    """
    The TemplateSSMDocumentDetails object contains the name of the SSM document and the version of the SSM document.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "documentName":
            suggest = "document_name"
        elif key == "documentVersion":
            suggest = "document_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TemplateSsmDocumentDetailsProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TemplateSsmDocumentDetailsProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TemplateSsmDocumentDetailsProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 document_name: Optional[str] = None,
                 document_version: Optional[str] = None):
        """
        The TemplateSSMDocumentDetails object contains the name of the SSM document and the version of the SSM document.
        :param str document_name: The name or Amazon Resource Name (ARN) of the SSM document to use to create a conformance pack. If you use the document name, AWS Config checks only your account and AWS Region for the SSM document.
        :param str document_version: The version of the SSM document to use to create a conformance pack. By default, AWS Config uses the latest version.
               
               > This field is optional.
        """
        if document_name is not None:
            pulumi.set(__self__, "document_name", document_name)
        if document_version is not None:
            pulumi.set(__self__, "document_version", document_version)

    @property
    @pulumi.getter(name="documentName")
    def document_name(self) -> Optional[str]:
        """
        The name or Amazon Resource Name (ARN) of the SSM document to use to create a conformance pack. If you use the document name, AWS Config checks only your account and AWS Region for the SSM document.
        """
        return pulumi.get(self, "document_name")

    @property
    @pulumi.getter(name="documentVersion")
    def document_version(self) -> Optional[str]:
        """
        The version of the SSM document to use to create a conformance pack. By default, AWS Config uses the latest version.

        > This field is optional.
        """
        return pulumi.get(self, "document_version")


