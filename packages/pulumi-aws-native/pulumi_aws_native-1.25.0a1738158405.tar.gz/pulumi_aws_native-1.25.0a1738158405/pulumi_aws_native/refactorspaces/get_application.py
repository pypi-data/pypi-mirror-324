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
    'GetApplicationResult',
    'AwaitableGetApplicationResult',
    'get_application',
    'get_application_output',
]

@pulumi.output_type
class GetApplicationResult:
    def __init__(__self__, api_gateway_id=None, application_identifier=None, arn=None, nlb_arn=None, nlb_name=None, proxy_url=None, stage_name=None, tags=None, vpc_link_id=None):
        if api_gateway_id and not isinstance(api_gateway_id, str):
            raise TypeError("Expected argument 'api_gateway_id' to be a str")
        pulumi.set(__self__, "api_gateway_id", api_gateway_id)
        if application_identifier and not isinstance(application_identifier, str):
            raise TypeError("Expected argument 'application_identifier' to be a str")
        pulumi.set(__self__, "application_identifier", application_identifier)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if nlb_arn and not isinstance(nlb_arn, str):
            raise TypeError("Expected argument 'nlb_arn' to be a str")
        pulumi.set(__self__, "nlb_arn", nlb_arn)
        if nlb_name and not isinstance(nlb_name, str):
            raise TypeError("Expected argument 'nlb_name' to be a str")
        pulumi.set(__self__, "nlb_name", nlb_name)
        if proxy_url and not isinstance(proxy_url, str):
            raise TypeError("Expected argument 'proxy_url' to be a str")
        pulumi.set(__self__, "proxy_url", proxy_url)
        if stage_name and not isinstance(stage_name, str):
            raise TypeError("Expected argument 'stage_name' to be a str")
        pulumi.set(__self__, "stage_name", stage_name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if vpc_link_id and not isinstance(vpc_link_id, str):
            raise TypeError("Expected argument 'vpc_link_id' to be a str")
        pulumi.set(__self__, "vpc_link_id", vpc_link_id)

    @property
    @pulumi.getter(name="apiGatewayId")
    def api_gateway_id(self) -> Optional[str]:
        """
        The resource ID of the API Gateway for the proxy.
        """
        return pulumi.get(self, "api_gateway_id")

    @property
    @pulumi.getter(name="applicationIdentifier")
    def application_identifier(self) -> Optional[str]:
        """
        The unique identifier of the application.
        """
        return pulumi.get(self, "application_identifier")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the application.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="nlbArn")
    def nlb_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the Network Load Balancer .
        """
        return pulumi.get(self, "nlb_arn")

    @property
    @pulumi.getter(name="nlbName")
    def nlb_name(self) -> Optional[str]:
        """
        The name of the Network Load Balancer configured by the API Gateway proxy.
        """
        return pulumi.get(self, "nlb_name")

    @property
    @pulumi.getter(name="proxyUrl")
    def proxy_url(self) -> Optional[str]:
        """
        The endpoint URL of the Amazon API Gateway proxy.
        """
        return pulumi.get(self, "proxy_url")

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> Optional[str]:
        """
        The name of the API Gateway stage. The name defaults to `prod` .
        """
        return pulumi.get(self, "stage_name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Metadata that you can assign to help organize the frameworks that you create. Each tag is a key-value pair.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcLinkId")
    def vpc_link_id(self) -> Optional[str]:
        """
        The `VpcLink` ID of the API Gateway proxy.
        """
        return pulumi.get(self, "vpc_link_id")


class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            api_gateway_id=self.api_gateway_id,
            application_identifier=self.application_identifier,
            arn=self.arn,
            nlb_arn=self.nlb_arn,
            nlb_name=self.nlb_name,
            proxy_url=self.proxy_url,
            stage_name=self.stage_name,
            tags=self.tags,
            vpc_link_id=self.vpc_link_id)


def get_application(application_identifier: Optional[str] = None,
                    environment_identifier: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationResult:
    """
    Definition of AWS::RefactorSpaces::Application Resource Type


    :param str application_identifier: The unique identifier of the application.
    :param str environment_identifier: The unique identifier of the environment.
    """
    __args__ = dict()
    __args__['applicationIdentifier'] = application_identifier
    __args__['environmentIdentifier'] = environment_identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:refactorspaces:getApplication', __args__, opts=opts, typ=GetApplicationResult).value

    return AwaitableGetApplicationResult(
        api_gateway_id=pulumi.get(__ret__, 'api_gateway_id'),
        application_identifier=pulumi.get(__ret__, 'application_identifier'),
        arn=pulumi.get(__ret__, 'arn'),
        nlb_arn=pulumi.get(__ret__, 'nlb_arn'),
        nlb_name=pulumi.get(__ret__, 'nlb_name'),
        proxy_url=pulumi.get(__ret__, 'proxy_url'),
        stage_name=pulumi.get(__ret__, 'stage_name'),
        tags=pulumi.get(__ret__, 'tags'),
        vpc_link_id=pulumi.get(__ret__, 'vpc_link_id'))
def get_application_output(application_identifier: Optional[pulumi.Input[str]] = None,
                           environment_identifier: Optional[pulumi.Input[str]] = None,
                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetApplicationResult]:
    """
    Definition of AWS::RefactorSpaces::Application Resource Type


    :param str application_identifier: The unique identifier of the application.
    :param str environment_identifier: The unique identifier of the environment.
    """
    __args__ = dict()
    __args__['applicationIdentifier'] = application_identifier
    __args__['environmentIdentifier'] = environment_identifier
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:refactorspaces:getApplication', __args__, opts=opts, typ=GetApplicationResult)
    return __ret__.apply(lambda __response__: GetApplicationResult(
        api_gateway_id=pulumi.get(__response__, 'api_gateway_id'),
        application_identifier=pulumi.get(__response__, 'application_identifier'),
        arn=pulumi.get(__response__, 'arn'),
        nlb_arn=pulumi.get(__response__, 'nlb_arn'),
        nlb_name=pulumi.get(__response__, 'nlb_name'),
        proxy_url=pulumi.get(__response__, 'proxy_url'),
        stage_name=pulumi.get(__response__, 'stage_name'),
        tags=pulumi.get(__response__, 'tags'),
        vpc_link_id=pulumi.get(__response__, 'vpc_link_id')))
