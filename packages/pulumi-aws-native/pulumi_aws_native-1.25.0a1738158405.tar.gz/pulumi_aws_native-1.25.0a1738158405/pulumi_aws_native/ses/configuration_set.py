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
from ._inputs import *

__all__ = ['ConfigurationSetArgs', 'ConfigurationSet']

@pulumi.input_type
class ConfigurationSetArgs:
    def __init__(__self__, *,
                 delivery_options: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reputation_options: Optional[pulumi.Input['ConfigurationSetReputationOptionsArgs']] = None,
                 sending_options: Optional[pulumi.Input['ConfigurationSetSendingOptionsArgs']] = None,
                 suppression_options: Optional[pulumi.Input['ConfigurationSetSuppressionOptionsArgs']] = None,
                 tracking_options: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']] = None,
                 vdm_options: Optional[pulumi.Input['ConfigurationSetVdmOptionsArgs']] = None):
        """
        The set of arguments for constructing a ConfigurationSet resource.
        :param pulumi.Input['ConfigurationSetDeliveryOptionsArgs'] delivery_options: Specifies the name of the dedicated IP pool to associate with the configuration set and whether messages that use the configuration set are required to use Transport Layer Security (TLS).
        :param pulumi.Input[str] name: The name of the configuration set.
        :param pulumi.Input['ConfigurationSetReputationOptionsArgs'] reputation_options: An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        :param pulumi.Input['ConfigurationSetSendingOptionsArgs'] sending_options: An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        :param pulumi.Input['ConfigurationSetSuppressionOptionsArgs'] suppression_options: An object that contains information about the suppression list preferences for your account.
        :param pulumi.Input['ConfigurationSetTrackingOptionsArgs'] tracking_options: An object that defines the open and click tracking options for emails that you send using the configuration set.
        :param pulumi.Input['ConfigurationSetVdmOptionsArgs'] vdm_options: The Virtual Deliverability Manager (VDM) options that apply to the configuration set.
        """
        if delivery_options is not None:
            pulumi.set(__self__, "delivery_options", delivery_options)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if reputation_options is not None:
            pulumi.set(__self__, "reputation_options", reputation_options)
        if sending_options is not None:
            pulumi.set(__self__, "sending_options", sending_options)
        if suppression_options is not None:
            pulumi.set(__self__, "suppression_options", suppression_options)
        if tracking_options is not None:
            pulumi.set(__self__, "tracking_options", tracking_options)
        if vdm_options is not None:
            pulumi.set(__self__, "vdm_options", vdm_options)

    @property
    @pulumi.getter(name="deliveryOptions")
    def delivery_options(self) -> Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]:
        """
        Specifies the name of the dedicated IP pool to associate with the configuration set and whether messages that use the configuration set are required to use Transport Layer Security (TLS).
        """
        return pulumi.get(self, "delivery_options")

    @delivery_options.setter
    def delivery_options(self, value: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]):
        pulumi.set(self, "delivery_options", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the configuration set.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="reputationOptions")
    def reputation_options(self) -> Optional[pulumi.Input['ConfigurationSetReputationOptionsArgs']]:
        """
        An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        """
        return pulumi.get(self, "reputation_options")

    @reputation_options.setter
    def reputation_options(self, value: Optional[pulumi.Input['ConfigurationSetReputationOptionsArgs']]):
        pulumi.set(self, "reputation_options", value)

    @property
    @pulumi.getter(name="sendingOptions")
    def sending_options(self) -> Optional[pulumi.Input['ConfigurationSetSendingOptionsArgs']]:
        """
        An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        """
        return pulumi.get(self, "sending_options")

    @sending_options.setter
    def sending_options(self, value: Optional[pulumi.Input['ConfigurationSetSendingOptionsArgs']]):
        pulumi.set(self, "sending_options", value)

    @property
    @pulumi.getter(name="suppressionOptions")
    def suppression_options(self) -> Optional[pulumi.Input['ConfigurationSetSuppressionOptionsArgs']]:
        """
        An object that contains information about the suppression list preferences for your account.
        """
        return pulumi.get(self, "suppression_options")

    @suppression_options.setter
    def suppression_options(self, value: Optional[pulumi.Input['ConfigurationSetSuppressionOptionsArgs']]):
        pulumi.set(self, "suppression_options", value)

    @property
    @pulumi.getter(name="trackingOptions")
    def tracking_options(self) -> Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]:
        """
        An object that defines the open and click tracking options for emails that you send using the configuration set.
        """
        return pulumi.get(self, "tracking_options")

    @tracking_options.setter
    def tracking_options(self, value: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]):
        pulumi.set(self, "tracking_options", value)

    @property
    @pulumi.getter(name="vdmOptions")
    def vdm_options(self) -> Optional[pulumi.Input['ConfigurationSetVdmOptionsArgs']]:
        """
        The Virtual Deliverability Manager (VDM) options that apply to the configuration set.
        """
        return pulumi.get(self, "vdm_options")

    @vdm_options.setter
    def vdm_options(self, value: Optional[pulumi.Input['ConfigurationSetVdmOptionsArgs']]):
        pulumi.set(self, "vdm_options", value)


class ConfigurationSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delivery_options: Optional[pulumi.Input[Union['ConfigurationSetDeliveryOptionsArgs', 'ConfigurationSetDeliveryOptionsArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reputation_options: Optional[pulumi.Input[Union['ConfigurationSetReputationOptionsArgs', 'ConfigurationSetReputationOptionsArgsDict']]] = None,
                 sending_options: Optional[pulumi.Input[Union['ConfigurationSetSendingOptionsArgs', 'ConfigurationSetSendingOptionsArgsDict']]] = None,
                 suppression_options: Optional[pulumi.Input[Union['ConfigurationSetSuppressionOptionsArgs', 'ConfigurationSetSuppressionOptionsArgsDict']]] = None,
                 tracking_options: Optional[pulumi.Input[Union['ConfigurationSetTrackingOptionsArgs', 'ConfigurationSetTrackingOptionsArgsDict']]] = None,
                 vdm_options: Optional[pulumi.Input[Union['ConfigurationSetVdmOptionsArgs', 'ConfigurationSetVdmOptionsArgsDict']]] = None,
                 __props__=None):
        """
        Resource schema for AWS::SES::ConfigurationSet.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        config_set_name = config.require("configSetName")
        config_set = aws_native.ses.ConfigurationSet("configSet", name=config_set_name)

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        config_set_name = config.require("configSetName")
        config_set = aws_native.ses.ConfigurationSet("configSet", name=config_set_name)

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        config_set_name = config.require("configSetName")
        event_destination_name = config.require("eventDestinationName")
        event_type1 = config.require("eventType1")
        event_type2 = config.require("eventType2")
        event_type3 = config.require("eventType3")
        dimension_name1 = config.require("dimensionName1")
        dimension_value_source1 = config.require("dimensionValueSource1")
        default_dimension_value1 = config.require("defaultDimensionValue1")
        dimension_name2 = config.require("dimensionName2")
        dimension_value_source2 = config.require("dimensionValueSource2")
        default_dimension_value2 = config.require("defaultDimensionValue2")
        config_set = aws_native.ses.ConfigurationSet("configSet", name=config_set_name)
        cw_event_destination = aws_native.ses.ConfigurationSetEventDestination("cwEventDestination",
            configuration_set_name=config_set.id,
            event_destination={
                "name": event_destination_name,
                "enabled": True,
                "matching_event_types": [
                    event_type1,
                    event_type2,
                    event_type3,
                ],
                "cloud_watch_destination": {
                    "dimension_configurations": [
                        {
                            "dimension_name": dimension_name1,
                            "dimension_value_source": dimension_value_source1,
                            "default_dimension_value": default_dimension_value1,
                        },
                        {
                            "dimension_name": dimension_name2,
                            "dimension_value_source": dimension_value_source2,
                            "default_dimension_value": default_dimension_value2,
                        },
                    ],
                },
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        config_set_name = config.require("configSetName")
        event_destination_name = config.require("eventDestinationName")
        event_type1 = config.require("eventType1")
        event_type2 = config.require("eventType2")
        event_type3 = config.require("eventType3")
        dimension_name1 = config.require("dimensionName1")
        dimension_value_source1 = config.require("dimensionValueSource1")
        default_dimension_value1 = config.require("defaultDimensionValue1")
        dimension_name2 = config.require("dimensionName2")
        dimension_value_source2 = config.require("dimensionValueSource2")
        default_dimension_value2 = config.require("defaultDimensionValue2")
        config_set = aws_native.ses.ConfigurationSet("configSet", name=config_set_name)
        cw_event_destination = aws_native.ses.ConfigurationSetEventDestination("cwEventDestination",
            configuration_set_name=config_set.id,
            event_destination={
                "name": event_destination_name,
                "enabled": True,
                "matching_event_types": [
                    event_type1,
                    event_type2,
                    event_type3,
                ],
                "cloud_watch_destination": {
                    "dimension_configurations": [
                        {
                            "dimension_name": dimension_name1,
                            "dimension_value_source": dimension_value_source1,
                            "default_dimension_value": default_dimension_value1,
                        },
                        {
                            "dimension_name": dimension_name2,
                            "dimension_value_source": dimension_value_source2,
                            "default_dimension_value": default_dimension_value2,
                        },
                    ],
                },
            })

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['ConfigurationSetDeliveryOptionsArgs', 'ConfigurationSetDeliveryOptionsArgsDict']] delivery_options: Specifies the name of the dedicated IP pool to associate with the configuration set and whether messages that use the configuration set are required to use Transport Layer Security (TLS).
        :param pulumi.Input[str] name: The name of the configuration set.
        :param pulumi.Input[Union['ConfigurationSetReputationOptionsArgs', 'ConfigurationSetReputationOptionsArgsDict']] reputation_options: An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        :param pulumi.Input[Union['ConfigurationSetSendingOptionsArgs', 'ConfigurationSetSendingOptionsArgsDict']] sending_options: An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        :param pulumi.Input[Union['ConfigurationSetSuppressionOptionsArgs', 'ConfigurationSetSuppressionOptionsArgsDict']] suppression_options: An object that contains information about the suppression list preferences for your account.
        :param pulumi.Input[Union['ConfigurationSetTrackingOptionsArgs', 'ConfigurationSetTrackingOptionsArgsDict']] tracking_options: An object that defines the open and click tracking options for emails that you send using the configuration set.
        :param pulumi.Input[Union['ConfigurationSetVdmOptionsArgs', 'ConfigurationSetVdmOptionsArgsDict']] vdm_options: The Virtual Deliverability Manager (VDM) options that apply to the configuration set.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ConfigurationSetArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::SES::ConfigurationSet.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        config_set_name = config.require("configSetName")
        config_set = aws_native.ses.ConfigurationSet("configSet", name=config_set_name)

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        config_set_name = config.require("configSetName")
        config_set = aws_native.ses.ConfigurationSet("configSet", name=config_set_name)

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        config_set_name = config.require("configSetName")
        event_destination_name = config.require("eventDestinationName")
        event_type1 = config.require("eventType1")
        event_type2 = config.require("eventType2")
        event_type3 = config.require("eventType3")
        dimension_name1 = config.require("dimensionName1")
        dimension_value_source1 = config.require("dimensionValueSource1")
        default_dimension_value1 = config.require("defaultDimensionValue1")
        dimension_name2 = config.require("dimensionName2")
        dimension_value_source2 = config.require("dimensionValueSource2")
        default_dimension_value2 = config.require("defaultDimensionValue2")
        config_set = aws_native.ses.ConfigurationSet("configSet", name=config_set_name)
        cw_event_destination = aws_native.ses.ConfigurationSetEventDestination("cwEventDestination",
            configuration_set_name=config_set.id,
            event_destination={
                "name": event_destination_name,
                "enabled": True,
                "matching_event_types": [
                    event_type1,
                    event_type2,
                    event_type3,
                ],
                "cloud_watch_destination": {
                    "dimension_configurations": [
                        {
                            "dimension_name": dimension_name1,
                            "dimension_value_source": dimension_value_source1,
                            "default_dimension_value": default_dimension_value1,
                        },
                        {
                            "dimension_name": dimension_name2,
                            "dimension_value_source": dimension_value_source2,
                            "default_dimension_value": default_dimension_value2,
                        },
                    ],
                },
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        config_set_name = config.require("configSetName")
        event_destination_name = config.require("eventDestinationName")
        event_type1 = config.require("eventType1")
        event_type2 = config.require("eventType2")
        event_type3 = config.require("eventType3")
        dimension_name1 = config.require("dimensionName1")
        dimension_value_source1 = config.require("dimensionValueSource1")
        default_dimension_value1 = config.require("defaultDimensionValue1")
        dimension_name2 = config.require("dimensionName2")
        dimension_value_source2 = config.require("dimensionValueSource2")
        default_dimension_value2 = config.require("defaultDimensionValue2")
        config_set = aws_native.ses.ConfigurationSet("configSet", name=config_set_name)
        cw_event_destination = aws_native.ses.ConfigurationSetEventDestination("cwEventDestination",
            configuration_set_name=config_set.id,
            event_destination={
                "name": event_destination_name,
                "enabled": True,
                "matching_event_types": [
                    event_type1,
                    event_type2,
                    event_type3,
                ],
                "cloud_watch_destination": {
                    "dimension_configurations": [
                        {
                            "dimension_name": dimension_name1,
                            "dimension_value_source": dimension_value_source1,
                            "default_dimension_value": default_dimension_value1,
                        },
                        {
                            "dimension_name": dimension_name2,
                            "dimension_value_source": dimension_value_source2,
                            "default_dimension_value": default_dimension_value2,
                        },
                    ],
                },
            })

        ```

        :param str resource_name: The name of the resource.
        :param ConfigurationSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConfigurationSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delivery_options: Optional[pulumi.Input[Union['ConfigurationSetDeliveryOptionsArgs', 'ConfigurationSetDeliveryOptionsArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reputation_options: Optional[pulumi.Input[Union['ConfigurationSetReputationOptionsArgs', 'ConfigurationSetReputationOptionsArgsDict']]] = None,
                 sending_options: Optional[pulumi.Input[Union['ConfigurationSetSendingOptionsArgs', 'ConfigurationSetSendingOptionsArgsDict']]] = None,
                 suppression_options: Optional[pulumi.Input[Union['ConfigurationSetSuppressionOptionsArgs', 'ConfigurationSetSuppressionOptionsArgsDict']]] = None,
                 tracking_options: Optional[pulumi.Input[Union['ConfigurationSetTrackingOptionsArgs', 'ConfigurationSetTrackingOptionsArgsDict']]] = None,
                 vdm_options: Optional[pulumi.Input[Union['ConfigurationSetVdmOptionsArgs', 'ConfigurationSetVdmOptionsArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConfigurationSetArgs.__new__(ConfigurationSetArgs)

            __props__.__dict__["delivery_options"] = delivery_options
            __props__.__dict__["name"] = name
            __props__.__dict__["reputation_options"] = reputation_options
            __props__.__dict__["sending_options"] = sending_options
            __props__.__dict__["suppression_options"] = suppression_options
            __props__.__dict__["tracking_options"] = tracking_options
            __props__.__dict__["vdm_options"] = vdm_options
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ConfigurationSet, __self__).__init__(
            'aws-native:ses:ConfigurationSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ConfigurationSet':
        """
        Get an existing ConfigurationSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConfigurationSetArgs.__new__(ConfigurationSetArgs)

        __props__.__dict__["delivery_options"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["reputation_options"] = None
        __props__.__dict__["sending_options"] = None
        __props__.__dict__["suppression_options"] = None
        __props__.__dict__["tracking_options"] = None
        __props__.__dict__["vdm_options"] = None
        return ConfigurationSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deliveryOptions")
    def delivery_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetDeliveryOptions']]:
        """
        Specifies the name of the dedicated IP pool to associate with the configuration set and whether messages that use the configuration set are required to use Transport Layer Security (TLS).
        """
        return pulumi.get(self, "delivery_options")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the configuration set.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="reputationOptions")
    def reputation_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetReputationOptions']]:
        """
        An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        """
        return pulumi.get(self, "reputation_options")

    @property
    @pulumi.getter(name="sendingOptions")
    def sending_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetSendingOptions']]:
        """
        An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        """
        return pulumi.get(self, "sending_options")

    @property
    @pulumi.getter(name="suppressionOptions")
    def suppression_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetSuppressionOptions']]:
        """
        An object that contains information about the suppression list preferences for your account.
        """
        return pulumi.get(self, "suppression_options")

    @property
    @pulumi.getter(name="trackingOptions")
    def tracking_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetTrackingOptions']]:
        """
        An object that defines the open and click tracking options for emails that you send using the configuration set.
        """
        return pulumi.get(self, "tracking_options")

    @property
    @pulumi.getter(name="vdmOptions")
    def vdm_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetVdmOptions']]:
        """
        The Virtual Deliverability Manager (VDM) options that apply to the configuration set.
        """
        return pulumi.get(self, "vdm_options")

