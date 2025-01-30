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
    'AppBlockBuilderAccessEndpointArgs',
    'AppBlockBuilderAccessEndpointArgsDict',
    'AppBlockBuilderVpcConfigArgs',
    'AppBlockBuilderVpcConfigArgsDict',
    'AppBlockS3LocationArgs',
    'AppBlockS3LocationArgsDict',
    'AppBlockScriptDetailsArgs',
    'AppBlockScriptDetailsArgsDict',
    'AppBlockTag0PropertiesArgs',
    'AppBlockTag0PropertiesArgsDict',
    'AppBlockTag1PropertiesArgs',
    'AppBlockTag1PropertiesArgsDict',
    'ApplicationS3LocationArgs',
    'ApplicationS3LocationArgsDict',
    'ApplicationTag0PropertiesArgs',
    'ApplicationTag0PropertiesArgsDict',
    'ApplicationTag1PropertiesArgs',
    'ApplicationTag1PropertiesArgsDict',
    'DirectoryConfigCertificateBasedAuthPropertiesArgs',
    'DirectoryConfigCertificateBasedAuthPropertiesArgsDict',
    'DirectoryConfigServiceAccountCredentialsArgs',
    'DirectoryConfigServiceAccountCredentialsArgsDict',
    'EntitlementAttributeArgs',
    'EntitlementAttributeArgsDict',
    'ImageBuilderAccessEndpointArgs',
    'ImageBuilderAccessEndpointArgsDict',
    'ImageBuilderDomainJoinInfoArgs',
    'ImageBuilderDomainJoinInfoArgsDict',
    'ImageBuilderVpcConfigArgs',
    'ImageBuilderVpcConfigArgsDict',
]

MYPY = False

if not MYPY:
    class AppBlockBuilderAccessEndpointArgsDict(TypedDict):
        endpoint_type: pulumi.Input[str]
        """
        The type of interface endpoint.
        """
        vpce_id: pulumi.Input[str]
        """
        The identifier (ID) of the VPC in which the interface endpoint is used.
        """
elif False:
    AppBlockBuilderAccessEndpointArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppBlockBuilderAccessEndpointArgs:
    def __init__(__self__, *,
                 endpoint_type: pulumi.Input[str],
                 vpce_id: pulumi.Input[str]):
        """
        :param pulumi.Input[str] endpoint_type: The type of interface endpoint.
        :param pulumi.Input[str] vpce_id: The identifier (ID) of the VPC in which the interface endpoint is used.
        """
        pulumi.set(__self__, "endpoint_type", endpoint_type)
        pulumi.set(__self__, "vpce_id", vpce_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> pulumi.Input[str]:
        """
        The type of interface endpoint.
        """
        return pulumi.get(self, "endpoint_type")

    @endpoint_type.setter
    def endpoint_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint_type", value)

    @property
    @pulumi.getter(name="vpceId")
    def vpce_id(self) -> pulumi.Input[str]:
        """
        The identifier (ID) of the VPC in which the interface endpoint is used.
        """
        return pulumi.get(self, "vpce_id")

    @vpce_id.setter
    def vpce_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpce_id", value)


if not MYPY:
    class AppBlockBuilderVpcConfigArgsDict(TypedDict):
        security_group_ids: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The identifiers of the security groups for the fleet or image builder.
        """
        subnet_ids: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The identifiers of the subnets to which a network interface is attached from the fleet instance or image builder instance. Fleet instances use one or more subnets. Image builder instances use one subnet.
        """
elif False:
    AppBlockBuilderVpcConfigArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppBlockBuilderVpcConfigArgs:
    def __init__(__self__, *,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_ids: The identifiers of the security groups for the fleet or image builder.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: The identifiers of the subnets to which a network interface is attached from the fleet instance or image builder instance. Fleet instances use one or more subnets. Image builder instances use one subnet.
        """
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The identifiers of the security groups for the fleet or image builder.
        """
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The identifiers of the subnets to which a network interface is attached from the fleet instance or image builder instance. Fleet instances use one or more subnets. Image builder instances use one subnet.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subnet_ids", value)


if not MYPY:
    class AppBlockS3LocationArgsDict(TypedDict):
        s3_bucket: pulumi.Input[str]
        """
        The S3 bucket of the app block.
        """
        s3_key: NotRequired[pulumi.Input[str]]
        """
        The S3 key of the S3 object of the virtual hard disk.

        This is required when it's used by `SetupScriptDetails` and `PostSetupScriptDetails` .
        """
elif False:
    AppBlockS3LocationArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppBlockS3LocationArgs:
    def __init__(__self__, *,
                 s3_bucket: pulumi.Input[str],
                 s3_key: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] s3_bucket: The S3 bucket of the app block.
        :param pulumi.Input[str] s3_key: The S3 key of the S3 object of the virtual hard disk.
               
               This is required when it's used by `SetupScriptDetails` and `PostSetupScriptDetails` .
        """
        pulumi.set(__self__, "s3_bucket", s3_bucket)
        if s3_key is not None:
            pulumi.set(__self__, "s3_key", s3_key)

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> pulumi.Input[str]:
        """
        The S3 bucket of the app block.
        """
        return pulumi.get(self, "s3_bucket")

    @s3_bucket.setter
    def s3_bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_bucket", value)

    @property
    @pulumi.getter(name="s3Key")
    def s3_key(self) -> Optional[pulumi.Input[str]]:
        """
        The S3 key of the S3 object of the virtual hard disk.

        This is required when it's used by `SetupScriptDetails` and `PostSetupScriptDetails` .
        """
        return pulumi.get(self, "s3_key")

    @s3_key.setter
    def s3_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s3_key", value)


if not MYPY:
    class AppBlockScriptDetailsArgsDict(TypedDict):
        executable_path: pulumi.Input[str]
        """
        The run path for the script.
        """
        script_s3_location: pulumi.Input['AppBlockS3LocationArgsDict']
        """
        The S3 object location of the script.
        """
        timeout_in_seconds: pulumi.Input[int]
        """
        The run timeout, in seconds, for the script.
        """
        executable_parameters: NotRequired[pulumi.Input[str]]
        """
        The parameters used in the run path for the script.
        """
elif False:
    AppBlockScriptDetailsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppBlockScriptDetailsArgs:
    def __init__(__self__, *,
                 executable_path: pulumi.Input[str],
                 script_s3_location: pulumi.Input['AppBlockS3LocationArgs'],
                 timeout_in_seconds: pulumi.Input[int],
                 executable_parameters: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] executable_path: The run path for the script.
        :param pulumi.Input['AppBlockS3LocationArgs'] script_s3_location: The S3 object location of the script.
        :param pulumi.Input[int] timeout_in_seconds: The run timeout, in seconds, for the script.
        :param pulumi.Input[str] executable_parameters: The parameters used in the run path for the script.
        """
        pulumi.set(__self__, "executable_path", executable_path)
        pulumi.set(__self__, "script_s3_location", script_s3_location)
        pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)
        if executable_parameters is not None:
            pulumi.set(__self__, "executable_parameters", executable_parameters)

    @property
    @pulumi.getter(name="executablePath")
    def executable_path(self) -> pulumi.Input[str]:
        """
        The run path for the script.
        """
        return pulumi.get(self, "executable_path")

    @executable_path.setter
    def executable_path(self, value: pulumi.Input[str]):
        pulumi.set(self, "executable_path", value)

    @property
    @pulumi.getter(name="scriptS3Location")
    def script_s3_location(self) -> pulumi.Input['AppBlockS3LocationArgs']:
        """
        The S3 object location of the script.
        """
        return pulumi.get(self, "script_s3_location")

    @script_s3_location.setter
    def script_s3_location(self, value: pulumi.Input['AppBlockS3LocationArgs']):
        pulumi.set(self, "script_s3_location", value)

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> pulumi.Input[int]:
        """
        The run timeout, in seconds, for the script.
        """
        return pulumi.get(self, "timeout_in_seconds")

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: pulumi.Input[int]):
        pulumi.set(self, "timeout_in_seconds", value)

    @property
    @pulumi.getter(name="executableParameters")
    def executable_parameters(self) -> Optional[pulumi.Input[str]]:
        """
        The parameters used in the run path for the script.
        """
        return pulumi.get(self, "executable_parameters")

    @executable_parameters.setter
    def executable_parameters(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "executable_parameters", value)


if not MYPY:
    class AppBlockTag0PropertiesArgsDict(TypedDict):
        key: pulumi.Input[str]
        value: pulumi.Input[str]
elif False:
    AppBlockTag0PropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppBlockTag0PropertiesArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


if not MYPY:
    class AppBlockTag1PropertiesArgsDict(TypedDict):
        tag_key: pulumi.Input[str]
        tag_value: pulumi.Input[str]
elif False:
    AppBlockTag1PropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppBlockTag1PropertiesArgs:
    def __init__(__self__, *,
                 tag_key: pulumi.Input[str],
                 tag_value: pulumi.Input[str]):
        pulumi.set(__self__, "tag_key", tag_key)
        pulumi.set(__self__, "tag_value", tag_value)

    @property
    @pulumi.getter(name="tagKey")
    def tag_key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "tag_key")

    @tag_key.setter
    def tag_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "tag_key", value)

    @property
    @pulumi.getter(name="tagValue")
    def tag_value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "tag_value")

    @tag_value.setter
    def tag_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "tag_value", value)


if not MYPY:
    class ApplicationS3LocationArgsDict(TypedDict):
        s3_bucket: pulumi.Input[str]
        """
        The S3 bucket of the S3 object.
        """
        s3_key: pulumi.Input[str]
        """
        The S3 key of the S3 object.
        """
elif False:
    ApplicationS3LocationArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ApplicationS3LocationArgs:
    def __init__(__self__, *,
                 s3_bucket: pulumi.Input[str],
                 s3_key: pulumi.Input[str]):
        """
        :param pulumi.Input[str] s3_bucket: The S3 bucket of the S3 object.
        :param pulumi.Input[str] s3_key: The S3 key of the S3 object.
        """
        pulumi.set(__self__, "s3_bucket", s3_bucket)
        pulumi.set(__self__, "s3_key", s3_key)

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> pulumi.Input[str]:
        """
        The S3 bucket of the S3 object.
        """
        return pulumi.get(self, "s3_bucket")

    @s3_bucket.setter
    def s3_bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_bucket", value)

    @property
    @pulumi.getter(name="s3Key")
    def s3_key(self) -> pulumi.Input[str]:
        """
        The S3 key of the S3 object.
        """
        return pulumi.get(self, "s3_key")

    @s3_key.setter
    def s3_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_key", value)


if not MYPY:
    class ApplicationTag0PropertiesArgsDict(TypedDict):
        key: pulumi.Input[str]
        value: pulumi.Input[str]
elif False:
    ApplicationTag0PropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ApplicationTag0PropertiesArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


if not MYPY:
    class ApplicationTag1PropertiesArgsDict(TypedDict):
        tag_key: pulumi.Input[str]
        tag_value: pulumi.Input[str]
elif False:
    ApplicationTag1PropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ApplicationTag1PropertiesArgs:
    def __init__(__self__, *,
                 tag_key: pulumi.Input[str],
                 tag_value: pulumi.Input[str]):
        pulumi.set(__self__, "tag_key", tag_key)
        pulumi.set(__self__, "tag_value", tag_value)

    @property
    @pulumi.getter(name="tagKey")
    def tag_key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "tag_key")

    @tag_key.setter
    def tag_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "tag_key", value)

    @property
    @pulumi.getter(name="tagValue")
    def tag_value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "tag_value")

    @tag_value.setter
    def tag_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "tag_value", value)


if not MYPY:
    class DirectoryConfigCertificateBasedAuthPropertiesArgsDict(TypedDict):
        certificate_authority_arn: NotRequired[pulumi.Input[str]]
        """
        The ARN of the AWS Certificate Manager Private CA resource.
        """
        status: NotRequired[pulumi.Input[str]]
        """
        The status of the certificate-based authentication properties. Fallback is turned on by default when certificate-based authentication is *Enabled* . Fallback allows users to log in using their AD domain password if certificate-based authentication is unsuccessful, or to unlock a desktop lock screen. *Enabled_no_directory_login_fallback* enables certificate-based authentication, but does not allow users to log in using their AD domain password. Users will be disconnected to re-authenticate using certificates.
        """
elif False:
    DirectoryConfigCertificateBasedAuthPropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DirectoryConfigCertificateBasedAuthPropertiesArgs:
    def __init__(__self__, *,
                 certificate_authority_arn: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] certificate_authority_arn: The ARN of the AWS Certificate Manager Private CA resource.
        :param pulumi.Input[str] status: The status of the certificate-based authentication properties. Fallback is turned on by default when certificate-based authentication is *Enabled* . Fallback allows users to log in using their AD domain password if certificate-based authentication is unsuccessful, or to unlock a desktop lock screen. *Enabled_no_directory_login_fallback* enables certificate-based authentication, but does not allow users to log in using their AD domain password. Users will be disconnected to re-authenticate using certificates.
        """
        if certificate_authority_arn is not None:
            pulumi.set(__self__, "certificate_authority_arn", certificate_authority_arn)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the AWS Certificate Manager Private CA resource.
        """
        return pulumi.get(self, "certificate_authority_arn")

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_authority_arn", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the certificate-based authentication properties. Fallback is turned on by default when certificate-based authentication is *Enabled* . Fallback allows users to log in using their AD domain password if certificate-based authentication is unsuccessful, or to unlock a desktop lock screen. *Enabled_no_directory_login_fallback* enables certificate-based authentication, but does not allow users to log in using their AD domain password. Users will be disconnected to re-authenticate using certificates.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


if not MYPY:
    class DirectoryConfigServiceAccountCredentialsArgsDict(TypedDict):
        account_name: pulumi.Input[str]
        """
        The user name of the account. This account must have the following privileges: create computer objects, join computers to the domain, and change/reset the password on descendant computer objects for the organizational units specified.
        """
        account_password: pulumi.Input[str]
        """
        The password for the account.
        """
elif False:
    DirectoryConfigServiceAccountCredentialsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DirectoryConfigServiceAccountCredentialsArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 account_password: pulumi.Input[str]):
        """
        :param pulumi.Input[str] account_name: The user name of the account. This account must have the following privileges: create computer objects, join computers to the domain, and change/reset the password on descendant computer objects for the organizational units specified.
        :param pulumi.Input[str] account_password: The password for the account.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "account_password", account_password)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The user name of the account. This account must have the following privileges: create computer objects, join computers to the domain, and change/reset the password on descendant computer objects for the organizational units specified.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="accountPassword")
    def account_password(self) -> pulumi.Input[str]:
        """
        The password for the account.
        """
        return pulumi.get(self, "account_password")

    @account_password.setter
    def account_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_password", value)


if not MYPY:
    class EntitlementAttributeArgsDict(TypedDict):
        name: pulumi.Input[str]
        """
        A supported AWS IAM SAML PrincipalTag attribute that is matched to a value when a user identity federates to an AppStream 2.0 SAML application.

        The following are supported values:

        - roles
        - department
        - organization
        - groups
        - title
        - costCenter
        - userType
        """
        value: pulumi.Input[str]
        """
        A value that is matched to a supported SAML attribute name when a user identity federates to an AppStream 2.0 SAML application.
        """
elif False:
    EntitlementAttributeArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class EntitlementAttributeArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: A supported AWS IAM SAML PrincipalTag attribute that is matched to a value when a user identity federates to an AppStream 2.0 SAML application.
               
               The following are supported values:
               
               - roles
               - department
               - organization
               - groups
               - title
               - costCenter
               - userType
        :param pulumi.Input[str] value: A value that is matched to a supported SAML attribute name when a user identity federates to an AppStream 2.0 SAML application.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        A supported AWS IAM SAML PrincipalTag attribute that is matched to a value when a user identity federates to an AppStream 2.0 SAML application.

        The following are supported values:

        - roles
        - department
        - organization
        - groups
        - title
        - costCenter
        - userType
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        A value that is matched to a supported SAML attribute name when a user identity federates to an AppStream 2.0 SAML application.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


if not MYPY:
    class ImageBuilderAccessEndpointArgsDict(TypedDict):
        endpoint_type: pulumi.Input[str]
        """
        The type of interface endpoint.
        """
        vpce_id: pulumi.Input[str]
        """
        The identifier (ID) of the VPC in which the interface endpoint is used.
        """
elif False:
    ImageBuilderAccessEndpointArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ImageBuilderAccessEndpointArgs:
    def __init__(__self__, *,
                 endpoint_type: pulumi.Input[str],
                 vpce_id: pulumi.Input[str]):
        """
        :param pulumi.Input[str] endpoint_type: The type of interface endpoint.
        :param pulumi.Input[str] vpce_id: The identifier (ID) of the VPC in which the interface endpoint is used.
        """
        pulumi.set(__self__, "endpoint_type", endpoint_type)
        pulumi.set(__self__, "vpce_id", vpce_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> pulumi.Input[str]:
        """
        The type of interface endpoint.
        """
        return pulumi.get(self, "endpoint_type")

    @endpoint_type.setter
    def endpoint_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint_type", value)

    @property
    @pulumi.getter(name="vpceId")
    def vpce_id(self) -> pulumi.Input[str]:
        """
        The identifier (ID) of the VPC in which the interface endpoint is used.
        """
        return pulumi.get(self, "vpce_id")

    @vpce_id.setter
    def vpce_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpce_id", value)


if not MYPY:
    class ImageBuilderDomainJoinInfoArgsDict(TypedDict):
        directory_name: NotRequired[pulumi.Input[str]]
        """
        The fully qualified name of the directory (for example, corp.example.com).
        """
        organizational_unit_distinguished_name: NotRequired[pulumi.Input[str]]
        """
        The distinguished name of the organizational unit for computer accounts.
        """
elif False:
    ImageBuilderDomainJoinInfoArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ImageBuilderDomainJoinInfoArgs:
    def __init__(__self__, *,
                 directory_name: Optional[pulumi.Input[str]] = None,
                 organizational_unit_distinguished_name: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] directory_name: The fully qualified name of the directory (for example, corp.example.com).
        :param pulumi.Input[str] organizational_unit_distinguished_name: The distinguished name of the organizational unit for computer accounts.
        """
        if directory_name is not None:
            pulumi.set(__self__, "directory_name", directory_name)
        if organizational_unit_distinguished_name is not None:
            pulumi.set(__self__, "organizational_unit_distinguished_name", organizational_unit_distinguished_name)

    @property
    @pulumi.getter(name="directoryName")
    def directory_name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of the directory (for example, corp.example.com).
        """
        return pulumi.get(self, "directory_name")

    @directory_name.setter
    def directory_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "directory_name", value)

    @property
    @pulumi.getter(name="organizationalUnitDistinguishedName")
    def organizational_unit_distinguished_name(self) -> Optional[pulumi.Input[str]]:
        """
        The distinguished name of the organizational unit for computer accounts.
        """
        return pulumi.get(self, "organizational_unit_distinguished_name")

    @organizational_unit_distinguished_name.setter
    def organizational_unit_distinguished_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organizational_unit_distinguished_name", value)


if not MYPY:
    class ImageBuilderVpcConfigArgsDict(TypedDict):
        security_group_ids: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The identifiers of the security groups for the image builder.
        """
        subnet_ids: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The identifier of the subnet to which a network interface is attached from the image builder instance. An image builder instance can use one subnet.
        """
elif False:
    ImageBuilderVpcConfigArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ImageBuilderVpcConfigArgs:
    def __init__(__self__, *,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_ids: The identifiers of the security groups for the image builder.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: The identifier of the subnet to which a network interface is attached from the image builder instance. An image builder instance can use one subnet.
        """
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The identifiers of the security groups for the image builder.
        """
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The identifier of the subnet to which a network interface is attached from the image builder instance. An image builder instance can use one subnet.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subnet_ids", value)


