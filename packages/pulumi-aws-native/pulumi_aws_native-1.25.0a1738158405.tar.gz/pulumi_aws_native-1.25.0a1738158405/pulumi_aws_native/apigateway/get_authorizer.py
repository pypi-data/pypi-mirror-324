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

__all__ = [
    'GetAuthorizerResult',
    'AwaitableGetAuthorizerResult',
    'get_authorizer',
    'get_authorizer_output',
]

@pulumi.output_type
class GetAuthorizerResult:
    def __init__(__self__, auth_type=None, authorizer_credentials=None, authorizer_id=None, authorizer_result_ttl_in_seconds=None, authorizer_uri=None, identity_source=None, identity_validation_expression=None, name=None, provider_arns=None, type=None):
        if auth_type and not isinstance(auth_type, str):
            raise TypeError("Expected argument 'auth_type' to be a str")
        pulumi.set(__self__, "auth_type", auth_type)
        if authorizer_credentials and not isinstance(authorizer_credentials, str):
            raise TypeError("Expected argument 'authorizer_credentials' to be a str")
        pulumi.set(__self__, "authorizer_credentials", authorizer_credentials)
        if authorizer_id and not isinstance(authorizer_id, str):
            raise TypeError("Expected argument 'authorizer_id' to be a str")
        pulumi.set(__self__, "authorizer_id", authorizer_id)
        if authorizer_result_ttl_in_seconds and not isinstance(authorizer_result_ttl_in_seconds, int):
            raise TypeError("Expected argument 'authorizer_result_ttl_in_seconds' to be a int")
        pulumi.set(__self__, "authorizer_result_ttl_in_seconds", authorizer_result_ttl_in_seconds)
        if authorizer_uri and not isinstance(authorizer_uri, str):
            raise TypeError("Expected argument 'authorizer_uri' to be a str")
        pulumi.set(__self__, "authorizer_uri", authorizer_uri)
        if identity_source and not isinstance(identity_source, str):
            raise TypeError("Expected argument 'identity_source' to be a str")
        pulumi.set(__self__, "identity_source", identity_source)
        if identity_validation_expression and not isinstance(identity_validation_expression, str):
            raise TypeError("Expected argument 'identity_validation_expression' to be a str")
        pulumi.set(__self__, "identity_validation_expression", identity_validation_expression)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provider_arns and not isinstance(provider_arns, list):
            raise TypeError("Expected argument 'provider_arns' to be a list")
        pulumi.set(__self__, "provider_arns", provider_arns)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="authType")
    def auth_type(self) -> Optional[str]:
        """
        Optional customer-defined field, used in OpenAPI imports and exports without functional impact.
        """
        return pulumi.get(self, "auth_type")

    @property
    @pulumi.getter(name="authorizerCredentials")
    def authorizer_credentials(self) -> Optional[str]:
        """
        Specifies the required credentials as an IAM role for API Gateway to invoke the authorizer. To specify an IAM role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To use resource-based permissions on the Lambda function, specify null.
        """
        return pulumi.get(self, "authorizer_credentials")

    @property
    @pulumi.getter(name="authorizerId")
    def authorizer_id(self) -> Optional[str]:
        """
        The ID for the authorizer. For example: `abc123` .
        """
        return pulumi.get(self, "authorizer_id")

    @property
    @pulumi.getter(name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> Optional[int]:
        """
        The TTL in seconds of cached authorizer results. If it equals 0, authorization caching is disabled. If it is greater than 0, API Gateway will cache authorizer responses. If this field is not set, the default value is 300. The maximum value is 3600, or 1 hour.
        """
        return pulumi.get(self, "authorizer_result_ttl_in_seconds")

    @property
    @pulumi.getter(name="authorizerUri")
    def authorizer_uri(self) -> Optional[str]:
        """
        Specifies the authorizer's Uniform Resource Identifier (URI). For `TOKEN` or `REQUEST` authorizers, this must be a well-formed Lambda function URI, for example, `arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2:{account_id}:function:{lambda_function_name}/invocations` . In general, the URI has this form `arn:aws:apigateway:{region}:lambda:path/{service_api}` , where `{region}` is the same as the region hosting the Lambda function, `path` indicates that the remaining substring in the URI should be treated as the path to the resource, including the initial `/` . For Lambda functions, this is usually of the form `/2015-03-31/functions/[FunctionARN]/invocations` .
        """
        return pulumi.get(self, "authorizer_uri")

    @property
    @pulumi.getter(name="identitySource")
    def identity_source(self) -> Optional[str]:
        """
        The identity source for which authorization is requested. For a `TOKEN` or `COGNITO_USER_POOLS` authorizer, this is required and specifies the request header mapping expression for the custom header holding the authorization token submitted by the client. For example, if the token header name is `Auth` , the header mapping expression is `method.request.header.Auth` . For the `REQUEST` authorizer, this is required when authorization caching is enabled. The value is a comma-separated string of one or more mapping expressions of the specified request parameters. For example, if an `Auth` header, a `Name` query string parameter are defined as identity sources, this value is `method.request.header.Auth, method.request.querystring.Name` . These parameters will be used to derive the authorization caching key and to perform runtime validation of the `REQUEST` authorizer by verifying all of the identity-related request parameters are present, not null and non-empty. Only when this is true does the authorizer invoke the authorizer Lambda function, otherwise, it returns a 401 Unauthorized response without calling the Lambda function. The valid value is a string of comma-separated mapping expressions of the specified request parameters. When the authorization caching is not enabled, this property is optional.
        """
        return pulumi.get(self, "identity_source")

    @property
    @pulumi.getter(name="identityValidationExpression")
    def identity_validation_expression(self) -> Optional[str]:
        """
        A validation expression for the incoming identity token. For `TOKEN` authorizers, this value is a regular expression. For `COGNITO_USER_POOLS` authorizers, API Gateway will match the `aud` field of the incoming token from the client against the specified regular expression. It will invoke the authorizer's Lambda function when there is a match. Otherwise, it will return a 401 Unauthorized response without calling the Lambda function. The validation expression does not apply to the `REQUEST` authorizer.
        """
        return pulumi.get(self, "identity_validation_expression")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the authorizer.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="providerArns")
    def provider_arns(self) -> Optional[Sequence[str]]:
        """
        A list of the Amazon Cognito user pool ARNs for the `COGNITO_USER_POOLS` authorizer. Each element is of this format: `arn:aws:cognito-idp:{region}:{account_id}:userpool/{user_pool_id}` . For a `TOKEN` or `REQUEST` authorizer, this is not defined.
        """
        return pulumi.get(self, "provider_arns")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The authorizer type. Valid values are `TOKEN` for a Lambda function using a single authorization token submitted in a custom header, `REQUEST` for a Lambda function using incoming request parameters, and `COGNITO_USER_POOLS` for using an Amazon Cognito user pool.
        """
        return pulumi.get(self, "type")


class AwaitableGetAuthorizerResult(GetAuthorizerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAuthorizerResult(
            auth_type=self.auth_type,
            authorizer_credentials=self.authorizer_credentials,
            authorizer_id=self.authorizer_id,
            authorizer_result_ttl_in_seconds=self.authorizer_result_ttl_in_seconds,
            authorizer_uri=self.authorizer_uri,
            identity_source=self.identity_source,
            identity_validation_expression=self.identity_validation_expression,
            name=self.name,
            provider_arns=self.provider_arns,
            type=self.type)


def get_authorizer(authorizer_id: Optional[str] = None,
                   rest_api_id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAuthorizerResult:
    """
    The ``AWS::ApiGateway::Authorizer`` resource creates an authorization layer that API Gateway activates for methods that have authorization enabled. API Gateway activates the authorizer when a client calls those methods.


    :param str authorizer_id: The ID for the authorizer. For example: `abc123` .
    :param str rest_api_id: The string identifier of the associated RestApi.
    """
    __args__ = dict()
    __args__['authorizerId'] = authorizer_id
    __args__['restApiId'] = rest_api_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigateway:getAuthorizer', __args__, opts=opts, typ=GetAuthorizerResult).value

    return AwaitableGetAuthorizerResult(
        auth_type=pulumi.get(__ret__, 'auth_type'),
        authorizer_credentials=pulumi.get(__ret__, 'authorizer_credentials'),
        authorizer_id=pulumi.get(__ret__, 'authorizer_id'),
        authorizer_result_ttl_in_seconds=pulumi.get(__ret__, 'authorizer_result_ttl_in_seconds'),
        authorizer_uri=pulumi.get(__ret__, 'authorizer_uri'),
        identity_source=pulumi.get(__ret__, 'identity_source'),
        identity_validation_expression=pulumi.get(__ret__, 'identity_validation_expression'),
        name=pulumi.get(__ret__, 'name'),
        provider_arns=pulumi.get(__ret__, 'provider_arns'),
        type=pulumi.get(__ret__, 'type'))
def get_authorizer_output(authorizer_id: Optional[pulumi.Input[str]] = None,
                          rest_api_id: Optional[pulumi.Input[str]] = None,
                          opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetAuthorizerResult]:
    """
    The ``AWS::ApiGateway::Authorizer`` resource creates an authorization layer that API Gateway activates for methods that have authorization enabled. API Gateway activates the authorizer when a client calls those methods.


    :param str authorizer_id: The ID for the authorizer. For example: `abc123` .
    :param str rest_api_id: The string identifier of the associated RestApi.
    """
    __args__ = dict()
    __args__['authorizerId'] = authorizer_id
    __args__['restApiId'] = rest_api_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:apigateway:getAuthorizer', __args__, opts=opts, typ=GetAuthorizerResult)
    return __ret__.apply(lambda __response__: GetAuthorizerResult(
        auth_type=pulumi.get(__response__, 'auth_type'),
        authorizer_credentials=pulumi.get(__response__, 'authorizer_credentials'),
        authorizer_id=pulumi.get(__response__, 'authorizer_id'),
        authorizer_result_ttl_in_seconds=pulumi.get(__response__, 'authorizer_result_ttl_in_seconds'),
        authorizer_uri=pulumi.get(__response__, 'authorizer_uri'),
        identity_source=pulumi.get(__response__, 'identity_source'),
        identity_validation_expression=pulumi.get(__response__, 'identity_validation_expression'),
        name=pulumi.get(__response__, 'name'),
        provider_arns=pulumi.get(__response__, 'provider_arns'),
        type=pulumi.get(__response__, 'type')))
