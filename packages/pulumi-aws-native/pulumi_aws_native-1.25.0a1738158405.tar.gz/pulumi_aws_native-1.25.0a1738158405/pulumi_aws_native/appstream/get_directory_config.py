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
    'GetDirectoryConfigResult',
    'AwaitableGetDirectoryConfigResult',
    'get_directory_config',
    'get_directory_config_output',
]

@pulumi.output_type
class GetDirectoryConfigResult:
    def __init__(__self__, certificate_based_auth_properties=None, organizational_unit_distinguished_names=None, service_account_credentials=None):
        if certificate_based_auth_properties and not isinstance(certificate_based_auth_properties, dict):
            raise TypeError("Expected argument 'certificate_based_auth_properties' to be a dict")
        pulumi.set(__self__, "certificate_based_auth_properties", certificate_based_auth_properties)
        if organizational_unit_distinguished_names and not isinstance(organizational_unit_distinguished_names, list):
            raise TypeError("Expected argument 'organizational_unit_distinguished_names' to be a list")
        pulumi.set(__self__, "organizational_unit_distinguished_names", organizational_unit_distinguished_names)
        if service_account_credentials and not isinstance(service_account_credentials, dict):
            raise TypeError("Expected argument 'service_account_credentials' to be a dict")
        pulumi.set(__self__, "service_account_credentials", service_account_credentials)

    @property
    @pulumi.getter(name="certificateBasedAuthProperties")
    def certificate_based_auth_properties(self) -> Optional['outputs.DirectoryConfigCertificateBasedAuthProperties']:
        """
        The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.
        """
        return pulumi.get(self, "certificate_based_auth_properties")

    @property
    @pulumi.getter(name="organizationalUnitDistinguishedNames")
    def organizational_unit_distinguished_names(self) -> Optional[Sequence[str]]:
        """
        The distinguished names of the organizational units for computer accounts.
        """
        return pulumi.get(self, "organizational_unit_distinguished_names")

    @property
    @pulumi.getter(name="serviceAccountCredentials")
    def service_account_credentials(self) -> Optional['outputs.DirectoryConfigServiceAccountCredentials']:
        """
        The credentials for the service account used by the streaming instance to connect to the directory. Do not use this parameter directly. Use `ServiceAccountCredentials` as an input parameter with `noEcho` as shown in the [Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html) . For best practices information, see [Do Not Embed Credentials in Your Templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds) .
        """
        return pulumi.get(self, "service_account_credentials")


class AwaitableGetDirectoryConfigResult(GetDirectoryConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDirectoryConfigResult(
            certificate_based_auth_properties=self.certificate_based_auth_properties,
            organizational_unit_distinguished_names=self.organizational_unit_distinguished_names,
            service_account_credentials=self.service_account_credentials)


def get_directory_config(directory_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDirectoryConfigResult:
    """
    Resource Type definition for AWS::AppStream::DirectoryConfig


    :param str directory_name: The fully qualified name of the directory (for example, corp.example.com).
    """
    __args__ = dict()
    __args__['directoryName'] = directory_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:appstream:getDirectoryConfig', __args__, opts=opts, typ=GetDirectoryConfigResult).value

    return AwaitableGetDirectoryConfigResult(
        certificate_based_auth_properties=pulumi.get(__ret__, 'certificate_based_auth_properties'),
        organizational_unit_distinguished_names=pulumi.get(__ret__, 'organizational_unit_distinguished_names'),
        service_account_credentials=pulumi.get(__ret__, 'service_account_credentials'))
def get_directory_config_output(directory_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetDirectoryConfigResult]:
    """
    Resource Type definition for AWS::AppStream::DirectoryConfig


    :param str directory_name: The fully qualified name of the directory (for example, corp.example.com).
    """
    __args__ = dict()
    __args__['directoryName'] = directory_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:appstream:getDirectoryConfig', __args__, opts=opts, typ=GetDirectoryConfigResult)
    return __ret__.apply(lambda __response__: GetDirectoryConfigResult(
        certificate_based_auth_properties=pulumi.get(__response__, 'certificate_based_auth_properties'),
        organizational_unit_distinguished_names=pulumi.get(__response__, 'organizational_unit_distinguished_names'),
        service_account_credentials=pulumi.get(__response__, 'service_account_credentials')))
