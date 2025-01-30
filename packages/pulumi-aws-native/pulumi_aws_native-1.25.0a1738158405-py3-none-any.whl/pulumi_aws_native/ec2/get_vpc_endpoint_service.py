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
from .. import outputs as _root_outputs

__all__ = [
    'GetVpcEndpointServiceResult',
    'AwaitableGetVpcEndpointServiceResult',
    'get_vpc_endpoint_service',
    'get_vpc_endpoint_service_output',
]

@pulumi.output_type
class GetVpcEndpointServiceResult:
    def __init__(__self__, acceptance_required=None, gateway_load_balancer_arns=None, network_load_balancer_arns=None, payer_responsibility=None, service_id=None, tags=None):
        if acceptance_required and not isinstance(acceptance_required, bool):
            raise TypeError("Expected argument 'acceptance_required' to be a bool")
        pulumi.set(__self__, "acceptance_required", acceptance_required)
        if gateway_load_balancer_arns and not isinstance(gateway_load_balancer_arns, list):
            raise TypeError("Expected argument 'gateway_load_balancer_arns' to be a list")
        pulumi.set(__self__, "gateway_load_balancer_arns", gateway_load_balancer_arns)
        if network_load_balancer_arns and not isinstance(network_load_balancer_arns, list):
            raise TypeError("Expected argument 'network_load_balancer_arns' to be a list")
        pulumi.set(__self__, "network_load_balancer_arns", network_load_balancer_arns)
        if payer_responsibility and not isinstance(payer_responsibility, str):
            raise TypeError("Expected argument 'payer_responsibility' to be a str")
        pulumi.set(__self__, "payer_responsibility", payer_responsibility)
        if service_id and not isinstance(service_id, str):
            raise TypeError("Expected argument 'service_id' to be a str")
        pulumi.set(__self__, "service_id", service_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="acceptanceRequired")
    def acceptance_required(self) -> Optional[bool]:
        """
        Indicates whether requests from service consumers to create an endpoint to your service must be accepted.
        """
        return pulumi.get(self, "acceptance_required")

    @property
    @pulumi.getter(name="gatewayLoadBalancerArns")
    def gateway_load_balancer_arns(self) -> Optional[Sequence[str]]:
        """
        The Amazon Resource Names (ARNs) of the Gateway Load Balancers.
        """
        return pulumi.get(self, "gateway_load_balancer_arns")

    @property
    @pulumi.getter(name="networkLoadBalancerArns")
    def network_load_balancer_arns(self) -> Optional[Sequence[str]]:
        """
        The Amazon Resource Names (ARNs) of the Network Load Balancers.
        """
        return pulumi.get(self, "network_load_balancer_arns")

    @property
    @pulumi.getter(name="payerResponsibility")
    def payer_responsibility(self) -> Optional[str]:
        """
        The entity that is responsible for the endpoint costs. The default is the endpoint owner. If you set the payer responsibility to the service owner, you cannot set it back to the endpoint owner.
        """
        return pulumi.get(self, "payer_responsibility")

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> Optional[str]:
        """
        The ID of the endpoint service.
        """
        return pulumi.get(self, "service_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags to add to the VPC endpoint service.
        """
        return pulumi.get(self, "tags")


class AwaitableGetVpcEndpointServiceResult(GetVpcEndpointServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcEndpointServiceResult(
            acceptance_required=self.acceptance_required,
            gateway_load_balancer_arns=self.gateway_load_balancer_arns,
            network_load_balancer_arns=self.network_load_balancer_arns,
            payer_responsibility=self.payer_responsibility,
            service_id=self.service_id,
            tags=self.tags)


def get_vpc_endpoint_service(service_id: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcEndpointServiceResult:
    """
    Resource Type definition for AWS::EC2::VPCEndpointService


    :param str service_id: The ID of the endpoint service.
    """
    __args__ = dict()
    __args__['serviceId'] = service_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getVpcEndpointService', __args__, opts=opts, typ=GetVpcEndpointServiceResult).value

    return AwaitableGetVpcEndpointServiceResult(
        acceptance_required=pulumi.get(__ret__, 'acceptance_required'),
        gateway_load_balancer_arns=pulumi.get(__ret__, 'gateway_load_balancer_arns'),
        network_load_balancer_arns=pulumi.get(__ret__, 'network_load_balancer_arns'),
        payer_responsibility=pulumi.get(__ret__, 'payer_responsibility'),
        service_id=pulumi.get(__ret__, 'service_id'),
        tags=pulumi.get(__ret__, 'tags'))
def get_vpc_endpoint_service_output(service_id: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetVpcEndpointServiceResult]:
    """
    Resource Type definition for AWS::EC2::VPCEndpointService


    :param str service_id: The ID of the endpoint service.
    """
    __args__ = dict()
    __args__['serviceId'] = service_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getVpcEndpointService', __args__, opts=opts, typ=GetVpcEndpointServiceResult)
    return __ret__.apply(lambda __response__: GetVpcEndpointServiceResult(
        acceptance_required=pulumi.get(__response__, 'acceptance_required'),
        gateway_load_balancer_arns=pulumi.get(__response__, 'gateway_load_balancer_arns'),
        network_load_balancer_arns=pulumi.get(__response__, 'network_load_balancer_arns'),
        payer_responsibility=pulumi.get(__response__, 'payer_responsibility'),
        service_id=pulumi.get(__response__, 'service_id'),
        tags=pulumi.get(__response__, 'tags')))
