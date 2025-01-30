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
    'GetMailManagerRelayResult',
    'AwaitableGetMailManagerRelayResult',
    'get_mail_manager_relay',
    'get_mail_manager_relay_output',
]

@pulumi.output_type
class GetMailManagerRelayResult:
    def __init__(__self__, authentication=None, relay_arn=None, relay_id=None, relay_name=None, server_name=None, server_port=None, tags=None):
        if authentication and not isinstance(authentication, dict):
            raise TypeError("Expected argument 'authentication' to be a dict")
        pulumi.set(__self__, "authentication", authentication)
        if relay_arn and not isinstance(relay_arn, str):
            raise TypeError("Expected argument 'relay_arn' to be a str")
        pulumi.set(__self__, "relay_arn", relay_arn)
        if relay_id and not isinstance(relay_id, str):
            raise TypeError("Expected argument 'relay_id' to be a str")
        pulumi.set(__self__, "relay_id", relay_id)
        if relay_name and not isinstance(relay_name, str):
            raise TypeError("Expected argument 'relay_name' to be a str")
        pulumi.set(__self__, "relay_name", relay_name)
        if server_name and not isinstance(server_name, str):
            raise TypeError("Expected argument 'server_name' to be a str")
        pulumi.set(__self__, "server_name", server_name)
        if server_port and not isinstance(server_port, float):
            raise TypeError("Expected argument 'server_port' to be a float")
        pulumi.set(__self__, "server_port", server_port)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def authentication(self) -> Optional[Any]:
        """
        Authentication for the relay destination server—specify the secretARN where the SMTP credentials are stored.
        """
        return pulumi.get(self, "authentication")

    @property
    @pulumi.getter(name="relayArn")
    def relay_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the relay.
        """
        return pulumi.get(self, "relay_arn")

    @property
    @pulumi.getter(name="relayId")
    def relay_id(self) -> Optional[str]:
        """
        The unique relay identifier.
        """
        return pulumi.get(self, "relay_id")

    @property
    @pulumi.getter(name="relayName")
    def relay_name(self) -> Optional[str]:
        """
        The unique relay name.
        """
        return pulumi.get(self, "relay_name")

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> Optional[str]:
        """
        The destination relay server address.
        """
        return pulumi.get(self, "server_name")

    @property
    @pulumi.getter(name="serverPort")
    def server_port(self) -> Optional[float]:
        """
        The destination relay server port.
        """
        return pulumi.get(self, "server_port")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        return pulumi.get(self, "tags")


class AwaitableGetMailManagerRelayResult(GetMailManagerRelayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMailManagerRelayResult(
            authentication=self.authentication,
            relay_arn=self.relay_arn,
            relay_id=self.relay_id,
            relay_name=self.relay_name,
            server_name=self.server_name,
            server_port=self.server_port,
            tags=self.tags)


def get_mail_manager_relay(relay_id: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMailManagerRelayResult:
    """
    Definition of AWS::SES::MailManagerRelay Resource Type


    :param str relay_id: The unique relay identifier.
    """
    __args__ = dict()
    __args__['relayId'] = relay_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ses:getMailManagerRelay', __args__, opts=opts, typ=GetMailManagerRelayResult).value

    return AwaitableGetMailManagerRelayResult(
        authentication=pulumi.get(__ret__, 'authentication'),
        relay_arn=pulumi.get(__ret__, 'relay_arn'),
        relay_id=pulumi.get(__ret__, 'relay_id'),
        relay_name=pulumi.get(__ret__, 'relay_name'),
        server_name=pulumi.get(__ret__, 'server_name'),
        server_port=pulumi.get(__ret__, 'server_port'),
        tags=pulumi.get(__ret__, 'tags'))
def get_mail_manager_relay_output(relay_id: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetMailManagerRelayResult]:
    """
    Definition of AWS::SES::MailManagerRelay Resource Type


    :param str relay_id: The unique relay identifier.
    """
    __args__ = dict()
    __args__['relayId'] = relay_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ses:getMailManagerRelay', __args__, opts=opts, typ=GetMailManagerRelayResult)
    return __ret__.apply(lambda __response__: GetMailManagerRelayResult(
        authentication=pulumi.get(__response__, 'authentication'),
        relay_arn=pulumi.get(__response__, 'relay_arn'),
        relay_id=pulumi.get(__response__, 'relay_id'),
        relay_name=pulumi.get(__response__, 'relay_name'),
        server_name=pulumi.get(__response__, 'server_name'),
        server_port=pulumi.get(__response__, 'server_port'),
        tags=pulumi.get(__response__, 'tags')))
