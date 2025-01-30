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
from ._enums import *
from ._inputs import *

__all__ = ['DomainArgs', 'Domain']

@pulumi.input_type
class DomainArgs:
    def __init__(__self__, *,
                 app_id: pulumi.Input[str],
                 sub_domain_settings: pulumi.Input[Sequence[pulumi.Input['DomainSubDomainSettingArgs']]],
                 auto_sub_domain_creation_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 auto_sub_domain_iam_role: Optional[pulumi.Input[str]] = None,
                 certificate_settings: Optional[pulumi.Input['DomainCertificateSettingsArgs']] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 enable_auto_sub_domain: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Domain resource.
        :param pulumi.Input[str] app_id: The unique ID for an Amplify app.
        :param pulumi.Input[Sequence[pulumi.Input['DomainSubDomainSettingArgs']]] sub_domain_settings: The setting for the subdomain.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] auto_sub_domain_creation_patterns: Sets the branch patterns for automatic subdomain creation.
        :param pulumi.Input[str] auto_sub_domain_iam_role: The required AWS Identity and Access Management (IAMlong) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.
        :param pulumi.Input['DomainCertificateSettingsArgs'] certificate_settings: The type of SSL/TLS certificate to use for your custom domain. If you don't specify a certificate type, Amplify uses the default certificate that it provisions and manages for you.
        :param pulumi.Input[str] domain_name: The domain name for the domain association.
        :param pulumi.Input[bool] enable_auto_sub_domain: Enables the automated creation of subdomains for branches.
        """
        pulumi.set(__self__, "app_id", app_id)
        pulumi.set(__self__, "sub_domain_settings", sub_domain_settings)
        if auto_sub_domain_creation_patterns is not None:
            pulumi.set(__self__, "auto_sub_domain_creation_patterns", auto_sub_domain_creation_patterns)
        if auto_sub_domain_iam_role is not None:
            pulumi.set(__self__, "auto_sub_domain_iam_role", auto_sub_domain_iam_role)
        if certificate_settings is not None:
            pulumi.set(__self__, "certificate_settings", certificate_settings)
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if enable_auto_sub_domain is not None:
            pulumi.set(__self__, "enable_auto_sub_domain", enable_auto_sub_domain)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Input[str]:
        """
        The unique ID for an Amplify app.
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter(name="subDomainSettings")
    def sub_domain_settings(self) -> pulumi.Input[Sequence[pulumi.Input['DomainSubDomainSettingArgs']]]:
        """
        The setting for the subdomain.
        """
        return pulumi.get(self, "sub_domain_settings")

    @sub_domain_settings.setter
    def sub_domain_settings(self, value: pulumi.Input[Sequence[pulumi.Input['DomainSubDomainSettingArgs']]]):
        pulumi.set(self, "sub_domain_settings", value)

    @property
    @pulumi.getter(name="autoSubDomainCreationPatterns")
    def auto_sub_domain_creation_patterns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Sets the branch patterns for automatic subdomain creation.
        """
        return pulumi.get(self, "auto_sub_domain_creation_patterns")

    @auto_sub_domain_creation_patterns.setter
    def auto_sub_domain_creation_patterns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "auto_sub_domain_creation_patterns", value)

    @property
    @pulumi.getter(name="autoSubDomainIamRole")
    def auto_sub_domain_iam_role(self) -> Optional[pulumi.Input[str]]:
        """
        The required AWS Identity and Access Management (IAMlong) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.
        """
        return pulumi.get(self, "auto_sub_domain_iam_role")

    @auto_sub_domain_iam_role.setter
    def auto_sub_domain_iam_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auto_sub_domain_iam_role", value)

    @property
    @pulumi.getter(name="certificateSettings")
    def certificate_settings(self) -> Optional[pulumi.Input['DomainCertificateSettingsArgs']]:
        """
        The type of SSL/TLS certificate to use for your custom domain. If you don't specify a certificate type, Amplify uses the default certificate that it provisions and manages for you.
        """
        return pulumi.get(self, "certificate_settings")

    @certificate_settings.setter
    def certificate_settings(self, value: Optional[pulumi.Input['DomainCertificateSettingsArgs']]):
        pulumi.set(self, "certificate_settings", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name for the domain association.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="enableAutoSubDomain")
    def enable_auto_sub_domain(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables the automated creation of subdomains for branches.
        """
        return pulumi.get(self, "enable_auto_sub_domain")

    @enable_auto_sub_domain.setter
    def enable_auto_sub_domain(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_auto_sub_domain", value)


class Domain(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 auto_sub_domain_creation_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 auto_sub_domain_iam_role: Optional[pulumi.Input[str]] = None,
                 certificate_settings: Optional[pulumi.Input[Union['DomainCertificateSettingsArgs', 'DomainCertificateSettingsArgsDict']]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 enable_auto_sub_domain: Optional[pulumi.Input[bool]] = None,
                 sub_domain_settings: Optional[pulumi.Input[Sequence[pulumi.Input[Union['DomainSubDomainSettingArgs', 'DomainSubDomainSettingArgsDict']]]]] = None,
                 __props__=None):
        """
        The AWS::Amplify::Domain resource allows you to connect a custom domain to your app.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_id: The unique ID for an Amplify app.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] auto_sub_domain_creation_patterns: Sets the branch patterns for automatic subdomain creation.
        :param pulumi.Input[str] auto_sub_domain_iam_role: The required AWS Identity and Access Management (IAMlong) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.
        :param pulumi.Input[Union['DomainCertificateSettingsArgs', 'DomainCertificateSettingsArgsDict']] certificate_settings: The type of SSL/TLS certificate to use for your custom domain. If you don't specify a certificate type, Amplify uses the default certificate that it provisions and manages for you.
        :param pulumi.Input[str] domain_name: The domain name for the domain association.
        :param pulumi.Input[bool] enable_auto_sub_domain: Enables the automated creation of subdomains for branches.
        :param pulumi.Input[Sequence[pulumi.Input[Union['DomainSubDomainSettingArgs', 'DomainSubDomainSettingArgsDict']]]] sub_domain_settings: The setting for the subdomain.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DomainArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::Amplify::Domain resource allows you to connect a custom domain to your app.

        :param str resource_name: The name of the resource.
        :param DomainArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DomainArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 auto_sub_domain_creation_patterns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 auto_sub_domain_iam_role: Optional[pulumi.Input[str]] = None,
                 certificate_settings: Optional[pulumi.Input[Union['DomainCertificateSettingsArgs', 'DomainCertificateSettingsArgsDict']]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 enable_auto_sub_domain: Optional[pulumi.Input[bool]] = None,
                 sub_domain_settings: Optional[pulumi.Input[Sequence[pulumi.Input[Union['DomainSubDomainSettingArgs', 'DomainSubDomainSettingArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DomainArgs.__new__(DomainArgs)

            if app_id is None and not opts.urn:
                raise TypeError("Missing required property 'app_id'")
            __props__.__dict__["app_id"] = app_id
            __props__.__dict__["auto_sub_domain_creation_patterns"] = auto_sub_domain_creation_patterns
            __props__.__dict__["auto_sub_domain_iam_role"] = auto_sub_domain_iam_role
            __props__.__dict__["certificate_settings"] = certificate_settings
            __props__.__dict__["domain_name"] = domain_name
            __props__.__dict__["enable_auto_sub_domain"] = enable_auto_sub_domain
            if sub_domain_settings is None and not opts.urn:
                raise TypeError("Missing required property 'sub_domain_settings'")
            __props__.__dict__["sub_domain_settings"] = sub_domain_settings
            __props__.__dict__["arn"] = None
            __props__.__dict__["certificate"] = None
            __props__.__dict__["certificate_record"] = None
            __props__.__dict__["domain_status"] = None
            __props__.__dict__["status_reason"] = None
            __props__.__dict__["update_status"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["appId", "domainName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Domain, __self__).__init__(
            'aws-native:amplify:Domain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Domain':
        """
        Get an existing Domain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DomainArgs.__new__(DomainArgs)

        __props__.__dict__["app_id"] = None
        __props__.__dict__["arn"] = None
        __props__.__dict__["auto_sub_domain_creation_patterns"] = None
        __props__.__dict__["auto_sub_domain_iam_role"] = None
        __props__.__dict__["certificate"] = None
        __props__.__dict__["certificate_record"] = None
        __props__.__dict__["certificate_settings"] = None
        __props__.__dict__["domain_name"] = None
        __props__.__dict__["domain_status"] = None
        __props__.__dict__["enable_auto_sub_domain"] = None
        __props__.__dict__["status_reason"] = None
        __props__.__dict__["sub_domain_settings"] = None
        __props__.__dict__["update_status"] = None
        return Domain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Output[str]:
        """
        The unique ID for an Amplify app.
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN for the Domain Association.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoSubDomainCreationPatterns")
    def auto_sub_domain_creation_patterns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Sets the branch patterns for automatic subdomain creation.
        """
        return pulumi.get(self, "auto_sub_domain_creation_patterns")

    @property
    @pulumi.getter(name="autoSubDomainIamRole")
    def auto_sub_domain_iam_role(self) -> pulumi.Output[Optional[str]]:
        """
        The required AWS Identity and Access Management (IAMlong) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.
        """
        return pulumi.get(self, "auto_sub_domain_iam_role")

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Output['outputs.DomainCertificate']:
        return pulumi.get(self, "certificate")

    @property
    @pulumi.getter(name="certificateRecord")
    def certificate_record(self) -> pulumi.Output[str]:
        """
        DNS Record for certificate verification.
        """
        return pulumi.get(self, "certificate_record")

    @property
    @pulumi.getter(name="certificateSettings")
    def certificate_settings(self) -> pulumi.Output[Optional['outputs.DomainCertificateSettings']]:
        """
        The type of SSL/TLS certificate to use for your custom domain. If you don't specify a certificate type, Amplify uses the default certificate that it provisions and manages for you.
        """
        return pulumi.get(self, "certificate_settings")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        The domain name for the domain association.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="domainStatus")
    def domain_status(self) -> pulumi.Output[str]:
        """
        Status for the Domain Association.
        """
        return pulumi.get(self, "domain_status")

    @property
    @pulumi.getter(name="enableAutoSubDomain")
    def enable_auto_sub_domain(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables the automated creation of subdomains for branches.
        """
        return pulumi.get(self, "enable_auto_sub_domain")

    @property
    @pulumi.getter(name="statusReason")
    def status_reason(self) -> pulumi.Output[str]:
        """
        Reason for the current status of the domain.
        """
        return pulumi.get(self, "status_reason")

    @property
    @pulumi.getter(name="subDomainSettings")
    def sub_domain_settings(self) -> pulumi.Output[Sequence['outputs.DomainSubDomainSetting']]:
        """
        The setting for the subdomain.
        """
        return pulumi.get(self, "sub_domain_settings")

    @property
    @pulumi.getter(name="updateStatus")
    def update_status(self) -> pulumi.Output[str]:
        """
        The status of the domain update operation that is currently in progress. The following list describes the valid update states.

        - **REQUESTING_CERTIFICATE** - The certificate is in the process of being updated.
        - **PENDING_VERIFICATION** - Indicates that an Amplify managed certificate is in the process of being verified. This occurs during the creation of a custom domain or when a custom domain is updated to use a managed certificate.
        - **IMPORTING_CUSTOM_CERTIFICATE** - Indicates that an Amplify custom certificate is in the process of being imported. This occurs during the creation of a custom domain or when a custom domain is updated to use a custom certificate.
        - **PENDING_DEPLOYMENT** - Indicates that the subdomain or certificate changes are being propagated.
        - **AWAITING_APP_CNAME** - Amplify is waiting for CNAME records corresponding to subdomains to be propagated. If your custom domain is on Route 53, Amplify handles this for you automatically. For more information about custom domains, see [Setting up custom domains](https://docs.aws.amazon.com/amplify/latest/userguide/custom-domains.html) in the *Amplify Hosting User Guide* .
        - **UPDATE_COMPLETE** - The certificate has been associated with a domain.
        - **UPDATE_FAILED** - The certificate has failed to be provisioned or associated, and there is no existing active certificate to roll back to.
        """
        return pulumi.get(self, "update_status")

