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
    'GetRequestValidatorResult',
    'AwaitableGetRequestValidatorResult',
    'get_request_validator',
    'get_request_validator_output',
]

@pulumi.output_type
class GetRequestValidatorResult:
    def __init__(__self__, request_validator_id=None, validate_request_body=None, validate_request_parameters=None):
        if request_validator_id and not isinstance(request_validator_id, str):
            raise TypeError("Expected argument 'request_validator_id' to be a str")
        pulumi.set(__self__, "request_validator_id", request_validator_id)
        if validate_request_body and not isinstance(validate_request_body, bool):
            raise TypeError("Expected argument 'validate_request_body' to be a bool")
        pulumi.set(__self__, "validate_request_body", validate_request_body)
        if validate_request_parameters and not isinstance(validate_request_parameters, bool):
            raise TypeError("Expected argument 'validate_request_parameters' to be a bool")
        pulumi.set(__self__, "validate_request_parameters", validate_request_parameters)

    @property
    @pulumi.getter(name="requestValidatorId")
    def request_validator_id(self) -> Optional[str]:
        """
        The ID for the request validator. For example: `abc123` .
        """
        return pulumi.get(self, "request_validator_id")

    @property
    @pulumi.getter(name="validateRequestBody")
    def validate_request_body(self) -> Optional[bool]:
        """
        A Boolean flag to indicate whether to validate a request body according to the configured Model schema.
        """
        return pulumi.get(self, "validate_request_body")

    @property
    @pulumi.getter(name="validateRequestParameters")
    def validate_request_parameters(self) -> Optional[bool]:
        """
        A Boolean flag to indicate whether to validate request parameters ( `true` ) or not ( `false` ).
        """
        return pulumi.get(self, "validate_request_parameters")


class AwaitableGetRequestValidatorResult(GetRequestValidatorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRequestValidatorResult(
            request_validator_id=self.request_validator_id,
            validate_request_body=self.validate_request_body,
            validate_request_parameters=self.validate_request_parameters)


def get_request_validator(request_validator_id: Optional[str] = None,
                          rest_api_id: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRequestValidatorResult:
    """
    The ``AWS::ApiGateway::RequestValidator`` resource sets up basic validation rules for incoming requests to your API. For more information, see [Enable Basic Request Validation for an API in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-request-validation.html) in the *API Gateway Developer Guide*.


    :param str request_validator_id: The ID for the request validator. For example: `abc123` .
    :param str rest_api_id: The string identifier of the associated RestApi.
    """
    __args__ = dict()
    __args__['requestValidatorId'] = request_validator_id
    __args__['restApiId'] = rest_api_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigateway:getRequestValidator', __args__, opts=opts, typ=GetRequestValidatorResult).value

    return AwaitableGetRequestValidatorResult(
        request_validator_id=pulumi.get(__ret__, 'request_validator_id'),
        validate_request_body=pulumi.get(__ret__, 'validate_request_body'),
        validate_request_parameters=pulumi.get(__ret__, 'validate_request_parameters'))
def get_request_validator_output(request_validator_id: Optional[pulumi.Input[str]] = None,
                                 rest_api_id: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetRequestValidatorResult]:
    """
    The ``AWS::ApiGateway::RequestValidator`` resource sets up basic validation rules for incoming requests to your API. For more information, see [Enable Basic Request Validation for an API in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-request-validation.html) in the *API Gateway Developer Guide*.


    :param str request_validator_id: The ID for the request validator. For example: `abc123` .
    :param str rest_api_id: The string identifier of the associated RestApi.
    """
    __args__ = dict()
    __args__['requestValidatorId'] = request_validator_id
    __args__['restApiId'] = rest_api_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:apigateway:getRequestValidator', __args__, opts=opts, typ=GetRequestValidatorResult)
    return __ret__.apply(lambda __response__: GetRequestValidatorResult(
        request_validator_id=pulumi.get(__response__, 'request_validator_id'),
        validate_request_body=pulumi.get(__response__, 'validate_request_body'),
        validate_request_parameters=pulumi.get(__response__, 'validate_request_parameters')))
