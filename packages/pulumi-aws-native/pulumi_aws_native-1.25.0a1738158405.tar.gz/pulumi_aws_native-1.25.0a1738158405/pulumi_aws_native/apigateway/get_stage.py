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
    'GetStageResult',
    'AwaitableGetStageResult',
    'get_stage',
    'get_stage_output',
]

@pulumi.output_type
class GetStageResult:
    def __init__(__self__, access_log_setting=None, cache_cluster_enabled=None, cache_cluster_size=None, canary_setting=None, client_certificate_id=None, deployment_id=None, description=None, documentation_version=None, method_settings=None, tags=None, tracing_enabled=None, variables=None):
        if access_log_setting and not isinstance(access_log_setting, dict):
            raise TypeError("Expected argument 'access_log_setting' to be a dict")
        pulumi.set(__self__, "access_log_setting", access_log_setting)
        if cache_cluster_enabled and not isinstance(cache_cluster_enabled, bool):
            raise TypeError("Expected argument 'cache_cluster_enabled' to be a bool")
        pulumi.set(__self__, "cache_cluster_enabled", cache_cluster_enabled)
        if cache_cluster_size and not isinstance(cache_cluster_size, str):
            raise TypeError("Expected argument 'cache_cluster_size' to be a str")
        pulumi.set(__self__, "cache_cluster_size", cache_cluster_size)
        if canary_setting and not isinstance(canary_setting, dict):
            raise TypeError("Expected argument 'canary_setting' to be a dict")
        pulumi.set(__self__, "canary_setting", canary_setting)
        if client_certificate_id and not isinstance(client_certificate_id, str):
            raise TypeError("Expected argument 'client_certificate_id' to be a str")
        pulumi.set(__self__, "client_certificate_id", client_certificate_id)
        if deployment_id and not isinstance(deployment_id, str):
            raise TypeError("Expected argument 'deployment_id' to be a str")
        pulumi.set(__self__, "deployment_id", deployment_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if documentation_version and not isinstance(documentation_version, str):
            raise TypeError("Expected argument 'documentation_version' to be a str")
        pulumi.set(__self__, "documentation_version", documentation_version)
        if method_settings and not isinstance(method_settings, list):
            raise TypeError("Expected argument 'method_settings' to be a list")
        pulumi.set(__self__, "method_settings", method_settings)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if tracing_enabled and not isinstance(tracing_enabled, bool):
            raise TypeError("Expected argument 'tracing_enabled' to be a bool")
        pulumi.set(__self__, "tracing_enabled", tracing_enabled)
        if variables and not isinstance(variables, dict):
            raise TypeError("Expected argument 'variables' to be a dict")
        pulumi.set(__self__, "variables", variables)

    @property
    @pulumi.getter(name="accessLogSetting")
    def access_log_setting(self) -> Optional['outputs.StageAccessLogSetting']:
        """
        Access log settings, including the access log format and access log destination ARN.
        """
        return pulumi.get(self, "access_log_setting")

    @property
    @pulumi.getter(name="cacheClusterEnabled")
    def cache_cluster_enabled(self) -> Optional[bool]:
        """
        Specifies whether a cache cluster is enabled for the stage. To activate a method-level cache, set `CachingEnabled` to `true` for a method.
        """
        return pulumi.get(self, "cache_cluster_enabled")

    @property
    @pulumi.getter(name="cacheClusterSize")
    def cache_cluster_size(self) -> Optional[str]:
        """
        The stage's cache capacity in GB. For more information about choosing a cache size, see [Enabling API caching to enhance responsiveness](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html) .
        """
        return pulumi.get(self, "cache_cluster_size")

    @property
    @pulumi.getter(name="canarySetting")
    def canary_setting(self) -> Optional['outputs.StageCanarySetting']:
        """
        Settings for the canary deployment in this stage.
        """
        return pulumi.get(self, "canary_setting")

    @property
    @pulumi.getter(name="clientCertificateId")
    def client_certificate_id(self) -> Optional[str]:
        """
        The identifier of a client certificate for an API stage.
        """
        return pulumi.get(self, "client_certificate_id")

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> Optional[str]:
        """
        The identifier of the Deployment that the stage points to.
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The stage's description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="documentationVersion")
    def documentation_version(self) -> Optional[str]:
        """
        The version of the associated API documentation.
        """
        return pulumi.get(self, "documentation_version")

    @property
    @pulumi.getter(name="methodSettings")
    def method_settings(self) -> Optional[Sequence['outputs.StageMethodSetting']]:
        """
        A map that defines the method settings for a Stage resource. Keys (designated as `/{method_setting_key` below) are method paths defined as `{resource_path}/{http_method}` for an individual method override, or `/\\*/\\*` for overriding all methods in the stage.
        """
        return pulumi.get(self, "method_settings")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The collection of tags. Each tag element is associated with a given resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tracingEnabled")
    def tracing_enabled(self) -> Optional[bool]:
        """
        Specifies whether active tracing with X-ray is enabled for the Stage.
        """
        return pulumi.get(self, "tracing_enabled")

    @property
    @pulumi.getter
    def variables(self) -> Optional[Mapping[str, str]]:
        """
        A map (string-to-string map) that defines the stage variables, where the variable name is the key and the variable value is the value. Variable names are limited to alphanumeric characters. Values must match the following regular expression: ``[A-Za-z0-9-._~:/?#&=,]+``.
        """
        return pulumi.get(self, "variables")


class AwaitableGetStageResult(GetStageResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStageResult(
            access_log_setting=self.access_log_setting,
            cache_cluster_enabled=self.cache_cluster_enabled,
            cache_cluster_size=self.cache_cluster_size,
            canary_setting=self.canary_setting,
            client_certificate_id=self.client_certificate_id,
            deployment_id=self.deployment_id,
            description=self.description,
            documentation_version=self.documentation_version,
            method_settings=self.method_settings,
            tags=self.tags,
            tracing_enabled=self.tracing_enabled,
            variables=self.variables)


def get_stage(rest_api_id: Optional[str] = None,
              stage_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStageResult:
    """
    The ``AWS::ApiGateway::Stage`` resource creates a stage for a deployment.


    :param str rest_api_id: The string identifier of the associated RestApi.
    :param str stage_name: The name of the stage is the first path segment in the Uniform Resource Identifier (URI) of a call to API Gateway. Stage names can only contain alphanumeric characters, hyphens, and underscores. Maximum length is 128 characters.
    """
    __args__ = dict()
    __args__['restApiId'] = rest_api_id
    __args__['stageName'] = stage_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigateway:getStage', __args__, opts=opts, typ=GetStageResult).value

    return AwaitableGetStageResult(
        access_log_setting=pulumi.get(__ret__, 'access_log_setting'),
        cache_cluster_enabled=pulumi.get(__ret__, 'cache_cluster_enabled'),
        cache_cluster_size=pulumi.get(__ret__, 'cache_cluster_size'),
        canary_setting=pulumi.get(__ret__, 'canary_setting'),
        client_certificate_id=pulumi.get(__ret__, 'client_certificate_id'),
        deployment_id=pulumi.get(__ret__, 'deployment_id'),
        description=pulumi.get(__ret__, 'description'),
        documentation_version=pulumi.get(__ret__, 'documentation_version'),
        method_settings=pulumi.get(__ret__, 'method_settings'),
        tags=pulumi.get(__ret__, 'tags'),
        tracing_enabled=pulumi.get(__ret__, 'tracing_enabled'),
        variables=pulumi.get(__ret__, 'variables'))
def get_stage_output(rest_api_id: Optional[pulumi.Input[str]] = None,
                     stage_name: Optional[pulumi.Input[str]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetStageResult]:
    """
    The ``AWS::ApiGateway::Stage`` resource creates a stage for a deployment.


    :param str rest_api_id: The string identifier of the associated RestApi.
    :param str stage_name: The name of the stage is the first path segment in the Uniform Resource Identifier (URI) of a call to API Gateway. Stage names can only contain alphanumeric characters, hyphens, and underscores. Maximum length is 128 characters.
    """
    __args__ = dict()
    __args__['restApiId'] = rest_api_id
    __args__['stageName'] = stage_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:apigateway:getStage', __args__, opts=opts, typ=GetStageResult)
    return __ret__.apply(lambda __response__: GetStageResult(
        access_log_setting=pulumi.get(__response__, 'access_log_setting'),
        cache_cluster_enabled=pulumi.get(__response__, 'cache_cluster_enabled'),
        cache_cluster_size=pulumi.get(__response__, 'cache_cluster_size'),
        canary_setting=pulumi.get(__response__, 'canary_setting'),
        client_certificate_id=pulumi.get(__response__, 'client_certificate_id'),
        deployment_id=pulumi.get(__response__, 'deployment_id'),
        description=pulumi.get(__response__, 'description'),
        documentation_version=pulumi.get(__response__, 'documentation_version'),
        method_settings=pulumi.get(__response__, 'method_settings'),
        tags=pulumi.get(__response__, 'tags'),
        tracing_enabled=pulumi.get(__response__, 'tracing_enabled'),
        variables=pulumi.get(__response__, 'variables')))
