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
    'GetAuthorizerResult',
    'AwaitableGetAuthorizerResult',
    'get_authorizer',
    'get_authorizer_output',
]

@pulumi.output_type
class GetAuthorizerResult:
    def __init__(__self__, authorizer_credentials_arn=None, authorizer_id=None, authorizer_payload_format_version=None, authorizer_result_ttl_in_seconds=None, authorizer_type=None, authorizer_uri=None, enable_simple_responses=None, identity_source=None, identity_validation_expression=None, jwt_configuration=None, name=None):
        if authorizer_credentials_arn and not isinstance(authorizer_credentials_arn, str):
            raise TypeError("Expected argument 'authorizer_credentials_arn' to be a str")
        pulumi.set(__self__, "authorizer_credentials_arn", authorizer_credentials_arn)
        if authorizer_id and not isinstance(authorizer_id, str):
            raise TypeError("Expected argument 'authorizer_id' to be a str")
        pulumi.set(__self__, "authorizer_id", authorizer_id)
        if authorizer_payload_format_version and not isinstance(authorizer_payload_format_version, str):
            raise TypeError("Expected argument 'authorizer_payload_format_version' to be a str")
        pulumi.set(__self__, "authorizer_payload_format_version", authorizer_payload_format_version)
        if authorizer_result_ttl_in_seconds and not isinstance(authorizer_result_ttl_in_seconds, int):
            raise TypeError("Expected argument 'authorizer_result_ttl_in_seconds' to be a int")
        pulumi.set(__self__, "authorizer_result_ttl_in_seconds", authorizer_result_ttl_in_seconds)
        if authorizer_type and not isinstance(authorizer_type, str):
            raise TypeError("Expected argument 'authorizer_type' to be a str")
        pulumi.set(__self__, "authorizer_type", authorizer_type)
        if authorizer_uri and not isinstance(authorizer_uri, str):
            raise TypeError("Expected argument 'authorizer_uri' to be a str")
        pulumi.set(__self__, "authorizer_uri", authorizer_uri)
        if enable_simple_responses and not isinstance(enable_simple_responses, bool):
            raise TypeError("Expected argument 'enable_simple_responses' to be a bool")
        pulumi.set(__self__, "enable_simple_responses", enable_simple_responses)
        if identity_source and not isinstance(identity_source, list):
            raise TypeError("Expected argument 'identity_source' to be a list")
        pulumi.set(__self__, "identity_source", identity_source)
        if identity_validation_expression and not isinstance(identity_validation_expression, str):
            raise TypeError("Expected argument 'identity_validation_expression' to be a str")
        pulumi.set(__self__, "identity_validation_expression", identity_validation_expression)
        if jwt_configuration and not isinstance(jwt_configuration, dict):
            raise TypeError("Expected argument 'jwt_configuration' to be a dict")
        pulumi.set(__self__, "jwt_configuration", jwt_configuration)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="authorizerCredentialsArn")
    def authorizer_credentials_arn(self) -> Optional[str]:
        """
        Specifies the required credentials as an IAM role for API Gateway to invoke the authorizer. To specify an IAM role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To use resource-based permissions on the Lambda function, specify null. Supported only for ``REQUEST`` authorizers.
        """
        return pulumi.get(self, "authorizer_credentials_arn")

    @property
    @pulumi.getter(name="authorizerId")
    def authorizer_id(self) -> Optional[str]:
        """
        The authorizer ID.
        """
        return pulumi.get(self, "authorizer_id")

    @property
    @pulumi.getter(name="authorizerPayloadFormatVersion")
    def authorizer_payload_format_version(self) -> Optional[str]:
        """
        Specifies the format of the payload sent to an HTTP API Lambda authorizer. Required for HTTP API Lambda authorizers. Supported values are ``1.0`` and ``2.0``. To learn more, see [Working with Lambda authorizers for HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html).
        """
        return pulumi.get(self, "authorizer_payload_format_version")

    @property
    @pulumi.getter(name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> Optional[int]:
        """
        The time to live (TTL) for cached authorizer results, in seconds. If it equals 0, authorization caching is disabled. If it is greater than 0, API Gateway caches authorizer responses. The maximum value is 3600, or 1 hour. Supported only for HTTP API Lambda authorizers.
        """
        return pulumi.get(self, "authorizer_result_ttl_in_seconds")

    @property
    @pulumi.getter(name="authorizerType")
    def authorizer_type(self) -> Optional[str]:
        """
        The authorizer type. Specify ``REQUEST`` for a Lambda function using incoming request parameters. Specify ``JWT`` to use JSON Web Tokens (supported only for HTTP APIs).
        """
        return pulumi.get(self, "authorizer_type")

    @property
    @pulumi.getter(name="authorizerUri")
    def authorizer_uri(self) -> Optional[str]:
        """
        The authorizer's Uniform Resource Identifier (URI). For ``REQUEST`` authorizers, this must be a well-formed Lambda function URI, for example, ``arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2:{account_id}:function:{lambda_function_name}/invocations``. In general, the URI has this form: ``arn:aws:apigateway:{region}:lambda:path/{service_api}``, where *{region}* is the same as the region hosting the Lambda function, path indicates that the remaining substring in the URI should be treated as the path to the resource, including the initial ``/``. For Lambda functions, this is usually of the form ``/2015-03-31/functions/[FunctionARN]/invocations``.
        """
        return pulumi.get(self, "authorizer_uri")

    @property
    @pulumi.getter(name="enableSimpleResponses")
    def enable_simple_responses(self) -> Optional[bool]:
        """
        Specifies whether a Lambda authorizer returns a response in a simple format. By default, a Lambda authorizer must return an IAM policy. If enabled, the Lambda authorizer can return a boolean value instead of an IAM policy. Supported only for HTTP APIs. To learn more, see [Working with Lambda authorizers for HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html).
        """
        return pulumi.get(self, "enable_simple_responses")

    @property
    @pulumi.getter(name="identitySource")
    def identity_source(self) -> Optional[Sequence[str]]:
        """
        The identity source for which authorization is requested.
         For a ``REQUEST`` authorizer, this is optional. The value is a set of one or more mapping expressions of the specified request parameters. The identity source can be headers, query string parameters, stage variables, and context parameters. For example, if an Auth header and a Name query string parameter are defined as identity sources, this value is route.request.header.Auth, route.request.querystring.Name for WebSocket APIs. For HTTP APIs, use selection expressions prefixed with ``$``, for example, ``$request.header.Auth``, ``$request.querystring.Name``. These parameters are used to perform runtime validation for Lambda-based authorizers by verifying all of the identity-related request parameters are present in the request, not null, and non-empty. Only when this is true does the authorizer invoke the authorizer Lambda function. Otherwise, it returns a 401 Unauthorized response without calling the Lambda function. For HTTP APIs, identity sources are also used as the cache key when caching is enabled. To learn more, see [Working with Lambda authorizers for HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html).
         For ``JWT``, a single entry that specifies where to extract the JSON Web Token (JWT) from inbound requests. Currently only header-based and query parameter-based selections are supported, for example ``$request.header.Authorization``.
        """
        return pulumi.get(self, "identity_source")

    @property
    @pulumi.getter(name="identityValidationExpression")
    def identity_validation_expression(self) -> Optional[str]:
        """
        This parameter is not used.
        """
        return pulumi.get(self, "identity_validation_expression")

    @property
    @pulumi.getter(name="jwtConfiguration")
    def jwt_configuration(self) -> Optional['outputs.AuthorizerJwtConfiguration']:
        """
        The ``JWTConfiguration`` property specifies the configuration of a JWT authorizer. Required for the ``JWT`` authorizer type. Supported only for HTTP APIs.
        """
        return pulumi.get(self, "jwt_configuration")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the authorizer.
        """
        return pulumi.get(self, "name")


class AwaitableGetAuthorizerResult(GetAuthorizerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAuthorizerResult(
            authorizer_credentials_arn=self.authorizer_credentials_arn,
            authorizer_id=self.authorizer_id,
            authorizer_payload_format_version=self.authorizer_payload_format_version,
            authorizer_result_ttl_in_seconds=self.authorizer_result_ttl_in_seconds,
            authorizer_type=self.authorizer_type,
            authorizer_uri=self.authorizer_uri,
            enable_simple_responses=self.enable_simple_responses,
            identity_source=self.identity_source,
            identity_validation_expression=self.identity_validation_expression,
            jwt_configuration=self.jwt_configuration,
            name=self.name)


def get_authorizer(api_id: Optional[str] = None,
                   authorizer_id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAuthorizerResult:
    """
    The ``AWS::ApiGatewayV2::Authorizer`` resource creates an authorizer for a WebSocket API or an HTTP API. To learn more, see [Controlling and managing access to a WebSocket API in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-control-access.html) and [Controlling and managing access to an HTTP API in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control.html) in the *API Gateway Developer Guide*.


    :param str api_id: The API identifier.
    :param str authorizer_id: The authorizer ID.
    """
    __args__ = dict()
    __args__['apiId'] = api_id
    __args__['authorizerId'] = authorizer_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigatewayv2:getAuthorizer', __args__, opts=opts, typ=GetAuthorizerResult).value

    return AwaitableGetAuthorizerResult(
        authorizer_credentials_arn=pulumi.get(__ret__, 'authorizer_credentials_arn'),
        authorizer_id=pulumi.get(__ret__, 'authorizer_id'),
        authorizer_payload_format_version=pulumi.get(__ret__, 'authorizer_payload_format_version'),
        authorizer_result_ttl_in_seconds=pulumi.get(__ret__, 'authorizer_result_ttl_in_seconds'),
        authorizer_type=pulumi.get(__ret__, 'authorizer_type'),
        authorizer_uri=pulumi.get(__ret__, 'authorizer_uri'),
        enable_simple_responses=pulumi.get(__ret__, 'enable_simple_responses'),
        identity_source=pulumi.get(__ret__, 'identity_source'),
        identity_validation_expression=pulumi.get(__ret__, 'identity_validation_expression'),
        jwt_configuration=pulumi.get(__ret__, 'jwt_configuration'),
        name=pulumi.get(__ret__, 'name'))
def get_authorizer_output(api_id: Optional[pulumi.Input[str]] = None,
                          authorizer_id: Optional[pulumi.Input[str]] = None,
                          opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetAuthorizerResult]:
    """
    The ``AWS::ApiGatewayV2::Authorizer`` resource creates an authorizer for a WebSocket API or an HTTP API. To learn more, see [Controlling and managing access to a WebSocket API in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-control-access.html) and [Controlling and managing access to an HTTP API in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control.html) in the *API Gateway Developer Guide*.


    :param str api_id: The API identifier.
    :param str authorizer_id: The authorizer ID.
    """
    __args__ = dict()
    __args__['apiId'] = api_id
    __args__['authorizerId'] = authorizer_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:apigatewayv2:getAuthorizer', __args__, opts=opts, typ=GetAuthorizerResult)
    return __ret__.apply(lambda __response__: GetAuthorizerResult(
        authorizer_credentials_arn=pulumi.get(__response__, 'authorizer_credentials_arn'),
        authorizer_id=pulumi.get(__response__, 'authorizer_id'),
        authorizer_payload_format_version=pulumi.get(__response__, 'authorizer_payload_format_version'),
        authorizer_result_ttl_in_seconds=pulumi.get(__response__, 'authorizer_result_ttl_in_seconds'),
        authorizer_type=pulumi.get(__response__, 'authorizer_type'),
        authorizer_uri=pulumi.get(__response__, 'authorizer_uri'),
        enable_simple_responses=pulumi.get(__response__, 'enable_simple_responses'),
        identity_source=pulumi.get(__response__, 'identity_source'),
        identity_validation_expression=pulumi.get(__response__, 'identity_validation_expression'),
        jwt_configuration=pulumi.get(__response__, 'jwt_configuration'),
        name=pulumi.get(__response__, 'name')))
