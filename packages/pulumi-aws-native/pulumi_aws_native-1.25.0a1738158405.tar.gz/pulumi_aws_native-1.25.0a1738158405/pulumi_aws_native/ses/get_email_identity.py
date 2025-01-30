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
    'GetEmailIdentityResult',
    'AwaitableGetEmailIdentityResult',
    'get_email_identity',
    'get_email_identity_output',
]

@pulumi.output_type
class GetEmailIdentityResult:
    def __init__(__self__, configuration_set_attributes=None, dkim_attributes=None, dkim_dns_token_name1=None, dkim_dns_token_name2=None, dkim_dns_token_name3=None, dkim_dns_token_value1=None, dkim_dns_token_value2=None, dkim_dns_token_value3=None, dkim_signing_attributes=None, feedback_attributes=None, mail_from_attributes=None):
        if configuration_set_attributes and not isinstance(configuration_set_attributes, dict):
            raise TypeError("Expected argument 'configuration_set_attributes' to be a dict")
        pulumi.set(__self__, "configuration_set_attributes", configuration_set_attributes)
        if dkim_attributes and not isinstance(dkim_attributes, dict):
            raise TypeError("Expected argument 'dkim_attributes' to be a dict")
        pulumi.set(__self__, "dkim_attributes", dkim_attributes)
        if dkim_dns_token_name1 and not isinstance(dkim_dns_token_name1, str):
            raise TypeError("Expected argument 'dkim_dns_token_name1' to be a str")
        pulumi.set(__self__, "dkim_dns_token_name1", dkim_dns_token_name1)
        if dkim_dns_token_name2 and not isinstance(dkim_dns_token_name2, str):
            raise TypeError("Expected argument 'dkim_dns_token_name2' to be a str")
        pulumi.set(__self__, "dkim_dns_token_name2", dkim_dns_token_name2)
        if dkim_dns_token_name3 and not isinstance(dkim_dns_token_name3, str):
            raise TypeError("Expected argument 'dkim_dns_token_name3' to be a str")
        pulumi.set(__self__, "dkim_dns_token_name3", dkim_dns_token_name3)
        if dkim_dns_token_value1 and not isinstance(dkim_dns_token_value1, str):
            raise TypeError("Expected argument 'dkim_dns_token_value1' to be a str")
        pulumi.set(__self__, "dkim_dns_token_value1", dkim_dns_token_value1)
        if dkim_dns_token_value2 and not isinstance(dkim_dns_token_value2, str):
            raise TypeError("Expected argument 'dkim_dns_token_value2' to be a str")
        pulumi.set(__self__, "dkim_dns_token_value2", dkim_dns_token_value2)
        if dkim_dns_token_value3 and not isinstance(dkim_dns_token_value3, str):
            raise TypeError("Expected argument 'dkim_dns_token_value3' to be a str")
        pulumi.set(__self__, "dkim_dns_token_value3", dkim_dns_token_value3)
        if dkim_signing_attributes and not isinstance(dkim_signing_attributes, dict):
            raise TypeError("Expected argument 'dkim_signing_attributes' to be a dict")
        pulumi.set(__self__, "dkim_signing_attributes", dkim_signing_attributes)
        if feedback_attributes and not isinstance(feedback_attributes, dict):
            raise TypeError("Expected argument 'feedback_attributes' to be a dict")
        pulumi.set(__self__, "feedback_attributes", feedback_attributes)
        if mail_from_attributes and not isinstance(mail_from_attributes, dict):
            raise TypeError("Expected argument 'mail_from_attributes' to be a dict")
        pulumi.set(__self__, "mail_from_attributes", mail_from_attributes)

    @property
    @pulumi.getter(name="configurationSetAttributes")
    def configuration_set_attributes(self) -> Optional['outputs.EmailIdentityConfigurationSetAttributes']:
        """
        Used to associate a configuration set with an email identity.
        """
        return pulumi.get(self, "configuration_set_attributes")

    @property
    @pulumi.getter(name="dkimAttributes")
    def dkim_attributes(self) -> Optional['outputs.EmailIdentityDkimAttributes']:
        """
        An object that contains information about the DKIM attributes for the identity.
        """
        return pulumi.get(self, "dkim_attributes")

    @property
    @pulumi.getter(name="dkimDnsTokenName1")
    def dkim_dns_token_name1(self) -> Optional[str]:
        """
        The host name for the first token that you have to add to the DNS configuration for your domain.
        """
        return pulumi.get(self, "dkim_dns_token_name1")

    @property
    @pulumi.getter(name="dkimDnsTokenName2")
    def dkim_dns_token_name2(self) -> Optional[str]:
        """
        The host name for the second token that you have to add to the DNS configuration for your domain.
        """
        return pulumi.get(self, "dkim_dns_token_name2")

    @property
    @pulumi.getter(name="dkimDnsTokenName3")
    def dkim_dns_token_name3(self) -> Optional[str]:
        """
        The host name for the third token that you have to add to the DNS configuration for your domain.
        """
        return pulumi.get(self, "dkim_dns_token_name3")

    @property
    @pulumi.getter(name="dkimDnsTokenValue1")
    def dkim_dns_token_value1(self) -> Optional[str]:
        """
        The record value for the first token that you have to add to the DNS configuration for your domain.
        """
        return pulumi.get(self, "dkim_dns_token_value1")

    @property
    @pulumi.getter(name="dkimDnsTokenValue2")
    def dkim_dns_token_value2(self) -> Optional[str]:
        """
        The record value for the second token that you have to add to the DNS configuration for your domain.
        """
        return pulumi.get(self, "dkim_dns_token_value2")

    @property
    @pulumi.getter(name="dkimDnsTokenValue3")
    def dkim_dns_token_value3(self) -> Optional[str]:
        """
        The record value for the third token that you have to add to the DNS configuration for your domain.
        """
        return pulumi.get(self, "dkim_dns_token_value3")

    @property
    @pulumi.getter(name="dkimSigningAttributes")
    def dkim_signing_attributes(self) -> Optional['outputs.EmailIdentityDkimSigningAttributes']:
        """
        If your request includes this object, Amazon SES configures the identity to use Bring Your Own DKIM (BYODKIM) for DKIM authentication purposes, or, configures the key length to be used for [Easy DKIM](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/easy-dkim.html) .

        You can only specify this object if the email identity is a domain, as opposed to an address.
        """
        return pulumi.get(self, "dkim_signing_attributes")

    @property
    @pulumi.getter(name="feedbackAttributes")
    def feedback_attributes(self) -> Optional['outputs.EmailIdentityFeedbackAttributes']:
        """
        Used to enable or disable feedback forwarding for an identity.
        """
        return pulumi.get(self, "feedback_attributes")

    @property
    @pulumi.getter(name="mailFromAttributes")
    def mail_from_attributes(self) -> Optional['outputs.EmailIdentityMailFromAttributes']:
        """
        Used to enable or disable the custom Mail-From domain configuration for an email identity.
        """
        return pulumi.get(self, "mail_from_attributes")


class AwaitableGetEmailIdentityResult(GetEmailIdentityResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEmailIdentityResult(
            configuration_set_attributes=self.configuration_set_attributes,
            dkim_attributes=self.dkim_attributes,
            dkim_dns_token_name1=self.dkim_dns_token_name1,
            dkim_dns_token_name2=self.dkim_dns_token_name2,
            dkim_dns_token_name3=self.dkim_dns_token_name3,
            dkim_dns_token_value1=self.dkim_dns_token_value1,
            dkim_dns_token_value2=self.dkim_dns_token_value2,
            dkim_dns_token_value3=self.dkim_dns_token_value3,
            dkim_signing_attributes=self.dkim_signing_attributes,
            feedback_attributes=self.feedback_attributes,
            mail_from_attributes=self.mail_from_attributes)


def get_email_identity(email_identity: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEmailIdentityResult:
    """
    Resource Type definition for AWS::SES::EmailIdentity


    :param str email_identity: The email address or domain to verify.
    """
    __args__ = dict()
    __args__['emailIdentity'] = email_identity
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ses:getEmailIdentity', __args__, opts=opts, typ=GetEmailIdentityResult).value

    return AwaitableGetEmailIdentityResult(
        configuration_set_attributes=pulumi.get(__ret__, 'configuration_set_attributes'),
        dkim_attributes=pulumi.get(__ret__, 'dkim_attributes'),
        dkim_dns_token_name1=pulumi.get(__ret__, 'dkim_dns_token_name1'),
        dkim_dns_token_name2=pulumi.get(__ret__, 'dkim_dns_token_name2'),
        dkim_dns_token_name3=pulumi.get(__ret__, 'dkim_dns_token_name3'),
        dkim_dns_token_value1=pulumi.get(__ret__, 'dkim_dns_token_value1'),
        dkim_dns_token_value2=pulumi.get(__ret__, 'dkim_dns_token_value2'),
        dkim_dns_token_value3=pulumi.get(__ret__, 'dkim_dns_token_value3'),
        dkim_signing_attributes=pulumi.get(__ret__, 'dkim_signing_attributes'),
        feedback_attributes=pulumi.get(__ret__, 'feedback_attributes'),
        mail_from_attributes=pulumi.get(__ret__, 'mail_from_attributes'))
def get_email_identity_output(email_identity: Optional[pulumi.Input[str]] = None,
                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetEmailIdentityResult]:
    """
    Resource Type definition for AWS::SES::EmailIdentity


    :param str email_identity: The email address or domain to verify.
    """
    __args__ = dict()
    __args__['emailIdentity'] = email_identity
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ses:getEmailIdentity', __args__, opts=opts, typ=GetEmailIdentityResult)
    return __ret__.apply(lambda __response__: GetEmailIdentityResult(
        configuration_set_attributes=pulumi.get(__response__, 'configuration_set_attributes'),
        dkim_attributes=pulumi.get(__response__, 'dkim_attributes'),
        dkim_dns_token_name1=pulumi.get(__response__, 'dkim_dns_token_name1'),
        dkim_dns_token_name2=pulumi.get(__response__, 'dkim_dns_token_name2'),
        dkim_dns_token_name3=pulumi.get(__response__, 'dkim_dns_token_name3'),
        dkim_dns_token_value1=pulumi.get(__response__, 'dkim_dns_token_value1'),
        dkim_dns_token_value2=pulumi.get(__response__, 'dkim_dns_token_value2'),
        dkim_dns_token_value3=pulumi.get(__response__, 'dkim_dns_token_value3'),
        dkim_signing_attributes=pulumi.get(__response__, 'dkim_signing_attributes'),
        feedback_attributes=pulumi.get(__response__, 'feedback_attributes'),
        mail_from_attributes=pulumi.get(__response__, 'mail_from_attributes')))
