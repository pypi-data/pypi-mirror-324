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
    'GetListenerResult',
    'AwaitableGetListenerResult',
    'get_listener',
    'get_listener_output',
]

@pulumi.output_type
class GetListenerResult:
    def __init__(__self__, alpn_policy=None, certificates=None, default_actions=None, listener_arn=None, listener_attributes=None, mutual_authentication=None, port=None, protocol=None, ssl_policy=None):
        if alpn_policy and not isinstance(alpn_policy, list):
            raise TypeError("Expected argument 'alpn_policy' to be a list")
        pulumi.set(__self__, "alpn_policy", alpn_policy)
        if certificates and not isinstance(certificates, list):
            raise TypeError("Expected argument 'certificates' to be a list")
        pulumi.set(__self__, "certificates", certificates)
        if default_actions and not isinstance(default_actions, list):
            raise TypeError("Expected argument 'default_actions' to be a list")
        pulumi.set(__self__, "default_actions", default_actions)
        if listener_arn and not isinstance(listener_arn, str):
            raise TypeError("Expected argument 'listener_arn' to be a str")
        pulumi.set(__self__, "listener_arn", listener_arn)
        if listener_attributes and not isinstance(listener_attributes, list):
            raise TypeError("Expected argument 'listener_attributes' to be a list")
        pulumi.set(__self__, "listener_attributes", listener_attributes)
        if mutual_authentication and not isinstance(mutual_authentication, dict):
            raise TypeError("Expected argument 'mutual_authentication' to be a dict")
        pulumi.set(__self__, "mutual_authentication", mutual_authentication)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if protocol and not isinstance(protocol, str):
            raise TypeError("Expected argument 'protocol' to be a str")
        pulumi.set(__self__, "protocol", protocol)
        if ssl_policy and not isinstance(ssl_policy, str):
            raise TypeError("Expected argument 'ssl_policy' to be a str")
        pulumi.set(__self__, "ssl_policy", ssl_policy)

    @property
    @pulumi.getter(name="alpnPolicy")
    def alpn_policy(self) -> Optional[Sequence[str]]:
        """
        [TLS listener] The name of the Application-Layer Protocol Negotiation (ALPN) policy.
        """
        return pulumi.get(self, "alpn_policy")

    @property
    @pulumi.getter
    def certificates(self) -> Optional[Sequence['outputs.ListenerCertificate']]:
        """
        The default SSL server certificate for a secure listener. You must provide exactly one certificate if the listener protocol is HTTPS or TLS.
         To create a certificate list for a secure listener, use [AWS::ElasticLoadBalancingV2::ListenerCertificate](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html).
        """
        return pulumi.get(self, "certificates")

    @property
    @pulumi.getter(name="defaultActions")
    def default_actions(self) -> Optional[Sequence['outputs.ListenerAction']]:
        """
        The actions for the default rule. You cannot define a condition for a default rule.
         To create additional rules for an Application Load Balancer, use [AWS::ElasticLoadBalancingV2::ListenerRule](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html).
        """
        return pulumi.get(self, "default_actions")

    @property
    @pulumi.getter(name="listenerArn")
    def listener_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the listener.
        """
        return pulumi.get(self, "listener_arn")

    @property
    @pulumi.getter(name="listenerAttributes")
    def listener_attributes(self) -> Optional[Sequence['outputs.ListenerAttribute']]:
        """
        The listener attributes.
        """
        return pulumi.get(self, "listener_attributes")

    @property
    @pulumi.getter(name="mutualAuthentication")
    def mutual_authentication(self) -> Optional['outputs.ListenerMutualAuthentication']:
        """
        The mutual authentication configuration information.
        """
        return pulumi.get(self, "mutual_authentication")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        The port on which the load balancer is listening. You can't specify a port for a Gateway Load Balancer.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> Optional[str]:
        """
        The protocol for connections from clients to the load balancer. For Application Load Balancers, the supported protocols are HTTP and HTTPS. For Network Load Balancers, the supported protocols are TCP, TLS, UDP, and TCP_UDP. You can’t specify the UDP or TCP_UDP protocol if dual-stack mode is enabled. You can't specify a protocol for a Gateway Load Balancer.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="sslPolicy")
    def ssl_policy(self) -> Optional[str]:
        """
        [HTTPS and TLS listeners] The security policy that defines which protocols and ciphers are supported.
         Updating the security policy can result in interruptions if the load balancer is handling a high volume of traffic.
         For more information, see [Security policies](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html#describe-ssl-policies) in the *Application Load Balancers Guide* and [Security policies](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-tls-listener.html#describe-ssl-policies) in the *Network Load Balancers Guide*.
        """
        return pulumi.get(self, "ssl_policy")


class AwaitableGetListenerResult(GetListenerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetListenerResult(
            alpn_policy=self.alpn_policy,
            certificates=self.certificates,
            default_actions=self.default_actions,
            listener_arn=self.listener_arn,
            listener_attributes=self.listener_attributes,
            mutual_authentication=self.mutual_authentication,
            port=self.port,
            protocol=self.protocol,
            ssl_policy=self.ssl_policy)


def get_listener(listener_arn: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetListenerResult:
    """
    Specifies a listener for an Application Load Balancer, Network Load Balancer, or Gateway Load Balancer.


    :param str listener_arn: The Amazon Resource Name (ARN) of the listener.
    """
    __args__ = dict()
    __args__['listenerArn'] = listener_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:elasticloadbalancingv2:getListener', __args__, opts=opts, typ=GetListenerResult).value

    return AwaitableGetListenerResult(
        alpn_policy=pulumi.get(__ret__, 'alpn_policy'),
        certificates=pulumi.get(__ret__, 'certificates'),
        default_actions=pulumi.get(__ret__, 'default_actions'),
        listener_arn=pulumi.get(__ret__, 'listener_arn'),
        listener_attributes=pulumi.get(__ret__, 'listener_attributes'),
        mutual_authentication=pulumi.get(__ret__, 'mutual_authentication'),
        port=pulumi.get(__ret__, 'port'),
        protocol=pulumi.get(__ret__, 'protocol'),
        ssl_policy=pulumi.get(__ret__, 'ssl_policy'))
def get_listener_output(listener_arn: Optional[pulumi.Input[str]] = None,
                        opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetListenerResult]:
    """
    Specifies a listener for an Application Load Balancer, Network Load Balancer, or Gateway Load Balancer.


    :param str listener_arn: The Amazon Resource Name (ARN) of the listener.
    """
    __args__ = dict()
    __args__['listenerArn'] = listener_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:elasticloadbalancingv2:getListener', __args__, opts=opts, typ=GetListenerResult)
    return __ret__.apply(lambda __response__: GetListenerResult(
        alpn_policy=pulumi.get(__response__, 'alpn_policy'),
        certificates=pulumi.get(__response__, 'certificates'),
        default_actions=pulumi.get(__response__, 'default_actions'),
        listener_arn=pulumi.get(__response__, 'listener_arn'),
        listener_attributes=pulumi.get(__response__, 'listener_attributes'),
        mutual_authentication=pulumi.get(__response__, 'mutual_authentication'),
        port=pulumi.get(__response__, 'port'),
        protocol=pulumi.get(__response__, 'protocol'),
        ssl_policy=pulumi.get(__response__, 'ssl_policy')))
