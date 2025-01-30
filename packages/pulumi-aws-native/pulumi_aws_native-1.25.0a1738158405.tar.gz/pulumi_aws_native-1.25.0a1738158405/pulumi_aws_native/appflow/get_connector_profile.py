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
from ._enums import *

__all__ = [
    'GetConnectorProfileResult',
    'AwaitableGetConnectorProfileResult',
    'get_connector_profile',
    'get_connector_profile_output',
]

@pulumi.output_type
class GetConnectorProfileResult:
    def __init__(__self__, connection_mode=None, connector_profile_arn=None, credentials_arn=None):
        if connection_mode and not isinstance(connection_mode, str):
            raise TypeError("Expected argument 'connection_mode' to be a str")
        pulumi.set(__self__, "connection_mode", connection_mode)
        if connector_profile_arn and not isinstance(connector_profile_arn, str):
            raise TypeError("Expected argument 'connector_profile_arn' to be a str")
        pulumi.set(__self__, "connector_profile_arn", connector_profile_arn)
        if credentials_arn and not isinstance(credentials_arn, str):
            raise TypeError("Expected argument 'credentials_arn' to be a str")
        pulumi.set(__self__, "credentials_arn", credentials_arn)

    @property
    @pulumi.getter(name="connectionMode")
    def connection_mode(self) -> Optional['ConnectorProfileConnectionMode']:
        """
        Mode in which data transfer should be enabled. Private connection mode is currently enabled for Salesforce, Snowflake, Trendmicro and Singular
        """
        return pulumi.get(self, "connection_mode")

    @property
    @pulumi.getter(name="connectorProfileArn")
    def connector_profile_arn(self) -> Optional[str]:
        """
        Unique identifier for connector profile resources
        """
        return pulumi.get(self, "connector_profile_arn")

    @property
    @pulumi.getter(name="credentialsArn")
    def credentials_arn(self) -> Optional[str]:
        """
        A unique Arn for Connector-Profile resource
        """
        return pulumi.get(self, "credentials_arn")


class AwaitableGetConnectorProfileResult(GetConnectorProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectorProfileResult(
            connection_mode=self.connection_mode,
            connector_profile_arn=self.connector_profile_arn,
            credentials_arn=self.credentials_arn)


def get_connector_profile(connector_profile_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectorProfileResult:
    """
    Resource Type definition for AWS::AppFlow::ConnectorProfile


    :param str connector_profile_name: The maximum number of items to retrieve in a single batch.
    """
    __args__ = dict()
    __args__['connectorProfileName'] = connector_profile_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:appflow:getConnectorProfile', __args__, opts=opts, typ=GetConnectorProfileResult).value

    return AwaitableGetConnectorProfileResult(
        connection_mode=pulumi.get(__ret__, 'connection_mode'),
        connector_profile_arn=pulumi.get(__ret__, 'connector_profile_arn'),
        credentials_arn=pulumi.get(__ret__, 'credentials_arn'))
def get_connector_profile_output(connector_profile_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetConnectorProfileResult]:
    """
    Resource Type definition for AWS::AppFlow::ConnectorProfile


    :param str connector_profile_name: The maximum number of items to retrieve in a single batch.
    """
    __args__ = dict()
    __args__['connectorProfileName'] = connector_profile_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:appflow:getConnectorProfile', __args__, opts=opts, typ=GetConnectorProfileResult)
    return __ret__.apply(lambda __response__: GetConnectorProfileResult(
        connection_mode=pulumi.get(__response__, 'connection_mode'),
        connector_profile_arn=pulumi.get(__response__, 'connector_profile_arn'),
        credentials_arn=pulumi.get(__response__, 'credentials_arn')))
