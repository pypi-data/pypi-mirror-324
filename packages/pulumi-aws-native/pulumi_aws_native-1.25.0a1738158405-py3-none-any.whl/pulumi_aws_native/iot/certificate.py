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

__all__ = ['CertificateArgs', 'Certificate']

@pulumi.input_type
class CertificateArgs:
    def __init__(__self__, *,
                 status: pulumi.Input['CertificateStatus'],
                 ca_certificate_pem: Optional[pulumi.Input[str]] = None,
                 certificate_mode: Optional[pulumi.Input['CertificateMode']] = None,
                 certificate_pem: Optional[pulumi.Input[str]] = None,
                 certificate_signing_request: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Certificate resource.
        :param pulumi.Input['CertificateStatus'] status: The status of the certificate.
               
               Valid values are ACTIVE, INACTIVE, REVOKED, PENDING_TRANSFER, and PENDING_ACTIVATION.
               
               The status value REGISTER_INACTIVE is deprecated and should not be used.
        :param pulumi.Input[str] ca_certificate_pem: The CA certificate used to sign the device certificate being registered, not available when CertificateMode is SNI_ONLY.
        :param pulumi.Input['CertificateMode'] certificate_mode: Specifies which mode of certificate registration to use with this resource. Valid options are DEFAULT with CaCertificatePem and CertificatePem, SNI_ONLY with CertificatePem, and Default with CertificateSigningRequest.
               
               `DEFAULT` : A certificate in `DEFAULT` mode is either generated by AWS IoT Core or registered with an issuer certificate authority (CA). Devices with certificates in `DEFAULT` mode aren't required to send the Server Name Indication (SNI) extension when connecting to AWS IoT Core . However, to use features such as custom domains and VPC endpoints, we recommend that you use the SNI extension when connecting to AWS IoT Core .
               
               `SNI_ONLY` : A certificate in `SNI_ONLY` mode is registered without an issuer CA. Devices with certificates in `SNI_ONLY` mode must send the SNI extension when connecting to AWS IoT Core .
        :param pulumi.Input[str] certificate_pem: The certificate data in PEM format. Requires SNI_ONLY for the certificate mode or the accompanying CACertificatePem for registration.
        :param pulumi.Input[str] certificate_signing_request: The certificate signing request (CSR).
        """
        pulumi.set(__self__, "status", status)
        if ca_certificate_pem is not None:
            pulumi.set(__self__, "ca_certificate_pem", ca_certificate_pem)
        if certificate_mode is not None:
            pulumi.set(__self__, "certificate_mode", certificate_mode)
        if certificate_pem is not None:
            pulumi.set(__self__, "certificate_pem", certificate_pem)
        if certificate_signing_request is not None:
            pulumi.set(__self__, "certificate_signing_request", certificate_signing_request)

    @property
    @pulumi.getter
    def status(self) -> pulumi.Input['CertificateStatus']:
        """
        The status of the certificate.

        Valid values are ACTIVE, INACTIVE, REVOKED, PENDING_TRANSFER, and PENDING_ACTIVATION.

        The status value REGISTER_INACTIVE is deprecated and should not be used.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: pulumi.Input['CertificateStatus']):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="caCertificatePem")
    def ca_certificate_pem(self) -> Optional[pulumi.Input[str]]:
        """
        The CA certificate used to sign the device certificate being registered, not available when CertificateMode is SNI_ONLY.
        """
        return pulumi.get(self, "ca_certificate_pem")

    @ca_certificate_pem.setter
    def ca_certificate_pem(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ca_certificate_pem", value)

    @property
    @pulumi.getter(name="certificateMode")
    def certificate_mode(self) -> Optional[pulumi.Input['CertificateMode']]:
        """
        Specifies which mode of certificate registration to use with this resource. Valid options are DEFAULT with CaCertificatePem and CertificatePem, SNI_ONLY with CertificatePem, and Default with CertificateSigningRequest.

        `DEFAULT` : A certificate in `DEFAULT` mode is either generated by AWS IoT Core or registered with an issuer certificate authority (CA). Devices with certificates in `DEFAULT` mode aren't required to send the Server Name Indication (SNI) extension when connecting to AWS IoT Core . However, to use features such as custom domains and VPC endpoints, we recommend that you use the SNI extension when connecting to AWS IoT Core .

        `SNI_ONLY` : A certificate in `SNI_ONLY` mode is registered without an issuer CA. Devices with certificates in `SNI_ONLY` mode must send the SNI extension when connecting to AWS IoT Core .
        """
        return pulumi.get(self, "certificate_mode")

    @certificate_mode.setter
    def certificate_mode(self, value: Optional[pulumi.Input['CertificateMode']]):
        pulumi.set(self, "certificate_mode", value)

    @property
    @pulumi.getter(name="certificatePem")
    def certificate_pem(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate data in PEM format. Requires SNI_ONLY for the certificate mode or the accompanying CACertificatePem for registration.
        """
        return pulumi.get(self, "certificate_pem")

    @certificate_pem.setter
    def certificate_pem(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_pem", value)

    @property
    @pulumi.getter(name="certificateSigningRequest")
    def certificate_signing_request(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate signing request (CSR).
        """
        return pulumi.get(self, "certificate_signing_request")

    @certificate_signing_request.setter
    def certificate_signing_request(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_signing_request", value)


class Certificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ca_certificate_pem: Optional[pulumi.Input[str]] = None,
                 certificate_mode: Optional[pulumi.Input['CertificateMode']] = None,
                 certificate_pem: Optional[pulumi.Input[str]] = None,
                 certificate_signing_request: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input['CertificateStatus']] = None,
                 __props__=None):
        """
        Use the AWS::IoT::Certificate resource to declare an AWS IoT X.509 certificate.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ca_certificate_pem: The CA certificate used to sign the device certificate being registered, not available when CertificateMode is SNI_ONLY.
        :param pulumi.Input['CertificateMode'] certificate_mode: Specifies which mode of certificate registration to use with this resource. Valid options are DEFAULT with CaCertificatePem and CertificatePem, SNI_ONLY with CertificatePem, and Default with CertificateSigningRequest.
               
               `DEFAULT` : A certificate in `DEFAULT` mode is either generated by AWS IoT Core or registered with an issuer certificate authority (CA). Devices with certificates in `DEFAULT` mode aren't required to send the Server Name Indication (SNI) extension when connecting to AWS IoT Core . However, to use features such as custom domains and VPC endpoints, we recommend that you use the SNI extension when connecting to AWS IoT Core .
               
               `SNI_ONLY` : A certificate in `SNI_ONLY` mode is registered without an issuer CA. Devices with certificates in `SNI_ONLY` mode must send the SNI extension when connecting to AWS IoT Core .
        :param pulumi.Input[str] certificate_pem: The certificate data in PEM format. Requires SNI_ONLY for the certificate mode or the accompanying CACertificatePem for registration.
        :param pulumi.Input[str] certificate_signing_request: The certificate signing request (CSR).
        :param pulumi.Input['CertificateStatus'] status: The status of the certificate.
               
               Valid values are ACTIVE, INACTIVE, REVOKED, PENDING_TRANSFER, and PENDING_ACTIVATION.
               
               The status value REGISTER_INACTIVE is deprecated and should not be used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Use the AWS::IoT::Certificate resource to declare an AWS IoT X.509 certificate.

        :param str resource_name: The name of the resource.
        :param CertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ca_certificate_pem: Optional[pulumi.Input[str]] = None,
                 certificate_mode: Optional[pulumi.Input['CertificateMode']] = None,
                 certificate_pem: Optional[pulumi.Input[str]] = None,
                 certificate_signing_request: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input['CertificateStatus']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CertificateArgs.__new__(CertificateArgs)

            __props__.__dict__["ca_certificate_pem"] = ca_certificate_pem
            __props__.__dict__["certificate_mode"] = certificate_mode
            __props__.__dict__["certificate_pem"] = certificate_pem
            __props__.__dict__["certificate_signing_request"] = certificate_signing_request
            if status is None and not opts.urn:
                raise TypeError("Missing required property 'status'")
            __props__.__dict__["status"] = status
            __props__.__dict__["arn"] = None
            __props__.__dict__["aws_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["caCertificatePem", "certificateMode", "certificatePem", "certificateSigningRequest"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Certificate, __self__).__init__(
            'aws-native:iot:Certificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Certificate':
        """
        Get an existing Certificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CertificateArgs.__new__(CertificateArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["aws_id"] = None
        __props__.__dict__["ca_certificate_pem"] = None
        __props__.__dict__["certificate_mode"] = None
        __props__.__dict__["certificate_pem"] = None
        __props__.__dict__["certificate_signing_request"] = None
        __props__.__dict__["status"] = None
        return Certificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Returns the Amazon Resource Name (ARN) for the certificate. For example:

        `{ "Fn::GetAtt": ["MyCertificate", "Arn"] }`

        A value similar to the following is returned:

        `arn:aws:iot:ap-southeast-2:123456789012:cert/a1234567b89c012d3e4fg567hij8k9l01mno1p23q45678901rs234567890t1u2`
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The certificate ID.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter(name="caCertificatePem")
    def ca_certificate_pem(self) -> pulumi.Output[Optional[str]]:
        """
        The CA certificate used to sign the device certificate being registered, not available when CertificateMode is SNI_ONLY.
        """
        return pulumi.get(self, "ca_certificate_pem")

    @property
    @pulumi.getter(name="certificateMode")
    def certificate_mode(self) -> pulumi.Output[Optional['CertificateMode']]:
        """
        Specifies which mode of certificate registration to use with this resource. Valid options are DEFAULT with CaCertificatePem and CertificatePem, SNI_ONLY with CertificatePem, and Default with CertificateSigningRequest.

        `DEFAULT` : A certificate in `DEFAULT` mode is either generated by AWS IoT Core or registered with an issuer certificate authority (CA). Devices with certificates in `DEFAULT` mode aren't required to send the Server Name Indication (SNI) extension when connecting to AWS IoT Core . However, to use features such as custom domains and VPC endpoints, we recommend that you use the SNI extension when connecting to AWS IoT Core .

        `SNI_ONLY` : A certificate in `SNI_ONLY` mode is registered without an issuer CA. Devices with certificates in `SNI_ONLY` mode must send the SNI extension when connecting to AWS IoT Core .
        """
        return pulumi.get(self, "certificate_mode")

    @property
    @pulumi.getter(name="certificatePem")
    def certificate_pem(self) -> pulumi.Output[Optional[str]]:
        """
        The certificate data in PEM format. Requires SNI_ONLY for the certificate mode or the accompanying CACertificatePem for registration.
        """
        return pulumi.get(self, "certificate_pem")

    @property
    @pulumi.getter(name="certificateSigningRequest")
    def certificate_signing_request(self) -> pulumi.Output[Optional[str]]:
        """
        The certificate signing request (CSR).
        """
        return pulumi.get(self, "certificate_signing_request")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['CertificateStatus']:
        """
        The status of the certificate.

        Valid values are ACTIVE, INACTIVE, REVOKED, PENDING_TRANSFER, and PENDING_ACTIVATION.

        The status value REGISTER_INACTIVE is deprecated and should not be used.
        """
        return pulumi.get(self, "status")

