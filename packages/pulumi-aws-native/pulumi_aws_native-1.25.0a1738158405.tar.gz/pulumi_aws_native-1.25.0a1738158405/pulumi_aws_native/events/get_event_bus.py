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
    'GetEventBusResult',
    'AwaitableGetEventBusResult',
    'get_event_bus',
    'get_event_bus_output',
]

@pulumi.output_type
class GetEventBusResult:
    def __init__(__self__, arn=None, dead_letter_config=None, description=None, kms_key_identifier=None, policy=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if dead_letter_config and not isinstance(dead_letter_config, dict):
            raise TypeError("Expected argument 'dead_letter_config' to be a dict")
        pulumi.set(__self__, "dead_letter_config", dead_letter_config)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if kms_key_identifier and not isinstance(kms_key_identifier, str):
            raise TypeError("Expected argument 'kms_key_identifier' to be a str")
        pulumi.set(__self__, "kms_key_identifier", kms_key_identifier)
        if policy and not isinstance(policy, dict):
            raise TypeError("Expected argument 'policy' to be a dict")
        pulumi.set(__self__, "policy", policy)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for the event bus.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="deadLetterConfig")
    def dead_letter_config(self) -> Optional['outputs.DeadLetterConfigProperties']:
        """
        Dead Letter Queue for the event bus.
        """
        return pulumi.get(self, "dead_letter_config")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the event bus.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> Optional[str]:
        """
        Kms Key Identifier used to encrypt events at rest in the event bus.
        """
        return pulumi.get(self, "kms_key_identifier")

    @property
    @pulumi.getter
    def policy(self) -> Optional[Any]:
        """
        A JSON string that describes the permission policy statement for the event bus.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Events::EventBus` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Any tags assigned to the event bus.
        """
        return pulumi.get(self, "tags")


class AwaitableGetEventBusResult(GetEventBusResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventBusResult(
            arn=self.arn,
            dead_letter_config=self.dead_letter_config,
            description=self.description,
            kms_key_identifier=self.kms_key_identifier,
            policy=self.policy,
            tags=self.tags)


def get_event_bus(name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventBusResult:
    """
    Resource type definition for AWS::Events::EventBus


    :param str name: The name of the event bus.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:events:getEventBus', __args__, opts=opts, typ=GetEventBusResult).value

    return AwaitableGetEventBusResult(
        arn=pulumi.get(__ret__, 'arn'),
        dead_letter_config=pulumi.get(__ret__, 'dead_letter_config'),
        description=pulumi.get(__ret__, 'description'),
        kms_key_identifier=pulumi.get(__ret__, 'kms_key_identifier'),
        policy=pulumi.get(__ret__, 'policy'),
        tags=pulumi.get(__ret__, 'tags'))
def get_event_bus_output(name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetEventBusResult]:
    """
    Resource type definition for AWS::Events::EventBus


    :param str name: The name of the event bus.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:events:getEventBus', __args__, opts=opts, typ=GetEventBusResult)
    return __ret__.apply(lambda __response__: GetEventBusResult(
        arn=pulumi.get(__response__, 'arn'),
        dead_letter_config=pulumi.get(__response__, 'dead_letter_config'),
        description=pulumi.get(__response__, 'description'),
        kms_key_identifier=pulumi.get(__response__, 'kms_key_identifier'),
        policy=pulumi.get(__response__, 'policy'),
        tags=pulumi.get(__response__, 'tags')))
