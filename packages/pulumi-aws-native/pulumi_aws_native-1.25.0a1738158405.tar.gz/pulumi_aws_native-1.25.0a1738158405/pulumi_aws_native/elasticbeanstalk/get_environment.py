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
    'GetEnvironmentResult',
    'AwaitableGetEnvironmentResult',
    'get_environment',
    'get_environment_output',
]

@pulumi.output_type
class GetEnvironmentResult:
    def __init__(__self__, description=None, endpoint_url=None, operations_role=None, platform_arn=None, tags=None, tier=None, version_label=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if endpoint_url and not isinstance(endpoint_url, str):
            raise TypeError("Expected argument 'endpoint_url' to be a str")
        pulumi.set(__self__, "endpoint_url", endpoint_url)
        if operations_role and not isinstance(operations_role, str):
            raise TypeError("Expected argument 'operations_role' to be a str")
        pulumi.set(__self__, "operations_role", operations_role)
        if platform_arn and not isinstance(platform_arn, str):
            raise TypeError("Expected argument 'platform_arn' to be a str")
        pulumi.set(__self__, "platform_arn", platform_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if tier and not isinstance(tier, dict):
            raise TypeError("Expected argument 'tier' to be a dict")
        pulumi.set(__self__, "tier", tier)
        if version_label and not isinstance(version_label, str):
            raise TypeError("Expected argument 'version_label' to be a str")
        pulumi.set(__self__, "version_label", version_label)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Your description for this environment.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endpointUrl")
    def endpoint_url(self) -> Optional[str]:
        """
        For load-balanced, autoscaling environments, the URL to the load balancer. For single-instance environments, the IP address of the instance.

        Example load balancer URL:

        Example instance IP address:

        `192.0.2.0`
        """
        return pulumi.get(self, "endpoint_url")

    @property
    @pulumi.getter(name="operationsRole")
    def operations_role(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of an existing IAM role to be used as the environment's operations role.
        """
        return pulumi.get(self, "operations_role")

    @property
    @pulumi.getter(name="platformArn")
    def platform_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the custom platform to use with the environment.
        """
        return pulumi.get(self, "platform_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Specifies the tags applied to resources in the environment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def tier(self) -> Optional['outputs.EnvironmentTier']:
        """
        Specifies the tier to use in creating this environment. The environment tier that you choose determines whether Elastic Beanstalk provisions resources to support a web application that handles HTTP(S) requests or a web application that handles background-processing tasks.
        """
        return pulumi.get(self, "tier")

    @property
    @pulumi.getter(name="versionLabel")
    def version_label(self) -> Optional[str]:
        """
        The name of the application version to deploy.
        """
        return pulumi.get(self, "version_label")


class AwaitableGetEnvironmentResult(GetEnvironmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEnvironmentResult(
            description=self.description,
            endpoint_url=self.endpoint_url,
            operations_role=self.operations_role,
            platform_arn=self.platform_arn,
            tags=self.tags,
            tier=self.tier,
            version_label=self.version_label)


def get_environment(environment_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEnvironmentResult:
    """
    Resource Type definition for AWS::ElasticBeanstalk::Environment


    :param str environment_name: A unique name for the environment.
    """
    __args__ = dict()
    __args__['environmentName'] = environment_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:elasticbeanstalk:getEnvironment', __args__, opts=opts, typ=GetEnvironmentResult).value

    return AwaitableGetEnvironmentResult(
        description=pulumi.get(__ret__, 'description'),
        endpoint_url=pulumi.get(__ret__, 'endpoint_url'),
        operations_role=pulumi.get(__ret__, 'operations_role'),
        platform_arn=pulumi.get(__ret__, 'platform_arn'),
        tags=pulumi.get(__ret__, 'tags'),
        tier=pulumi.get(__ret__, 'tier'),
        version_label=pulumi.get(__ret__, 'version_label'))
def get_environment_output(environment_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetEnvironmentResult]:
    """
    Resource Type definition for AWS::ElasticBeanstalk::Environment


    :param str environment_name: A unique name for the environment.
    """
    __args__ = dict()
    __args__['environmentName'] = environment_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:elasticbeanstalk:getEnvironment', __args__, opts=opts, typ=GetEnvironmentResult)
    return __ret__.apply(lambda __response__: GetEnvironmentResult(
        description=pulumi.get(__response__, 'description'),
        endpoint_url=pulumi.get(__response__, 'endpoint_url'),
        operations_role=pulumi.get(__response__, 'operations_role'),
        platform_arn=pulumi.get(__response__, 'platform_arn'),
        tags=pulumi.get(__response__, 'tags'),
        tier=pulumi.get(__response__, 'tier'),
        version_label=pulumi.get(__response__, 'version_label')))
