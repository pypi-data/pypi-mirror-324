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
from .. import outputs as _root_outputs

__all__ = [
    'GetPlaybackRestrictionPolicyResult',
    'AwaitableGetPlaybackRestrictionPolicyResult',
    'get_playback_restriction_policy',
    'get_playback_restriction_policy_output',
]

@pulumi.output_type
class GetPlaybackRestrictionPolicyResult:
    def __init__(__self__, allowed_countries=None, allowed_origins=None, arn=None, enable_strict_origin_enforcement=None, name=None, tags=None):
        if allowed_countries and not isinstance(allowed_countries, list):
            raise TypeError("Expected argument 'allowed_countries' to be a list")
        pulumi.set(__self__, "allowed_countries", allowed_countries)
        if allowed_origins and not isinstance(allowed_origins, list):
            raise TypeError("Expected argument 'allowed_origins' to be a list")
        pulumi.set(__self__, "allowed_origins", allowed_origins)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if enable_strict_origin_enforcement and not isinstance(enable_strict_origin_enforcement, bool):
            raise TypeError("Expected argument 'enable_strict_origin_enforcement' to be a bool")
        pulumi.set(__self__, "enable_strict_origin_enforcement", enable_strict_origin_enforcement)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="allowedCountries")
    def allowed_countries(self) -> Optional[Sequence[str]]:
        """
        A list of country codes that control geoblocking restriction. Allowed values are the officially assigned ISO 3166-1 alpha-2 codes. Default: All countries (an empty array).
        """
        return pulumi.get(self, "allowed_countries")

    @property
    @pulumi.getter(name="allowedOrigins")
    def allowed_origins(self) -> Optional[Sequence[str]]:
        """
        A list of origin sites that control CORS restriction. Allowed values are the same as valid values of the Origin header defined at https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin
        """
        return pulumi.get(self, "allowed_origins")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Playback-restriction-policy identifier.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="enableStrictOriginEnforcement")
    def enable_strict_origin_enforcement(self) -> Optional[bool]:
        """
        Whether channel playback is constrained by origin site.
        """
        return pulumi.get(self, "enable_strict_origin_enforcement")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Playback-restriction-policy name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetPlaybackRestrictionPolicyResult(GetPlaybackRestrictionPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPlaybackRestrictionPolicyResult(
            allowed_countries=self.allowed_countries,
            allowed_origins=self.allowed_origins,
            arn=self.arn,
            enable_strict_origin_enforcement=self.enable_strict_origin_enforcement,
            name=self.name,
            tags=self.tags)


def get_playback_restriction_policy(arn: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPlaybackRestrictionPolicyResult:
    """
    Resource Type definition for AWS::IVS::PlaybackRestrictionPolicy.


    :param str arn: Playback-restriction-policy identifier.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ivs:getPlaybackRestrictionPolicy', __args__, opts=opts, typ=GetPlaybackRestrictionPolicyResult).value

    return AwaitableGetPlaybackRestrictionPolicyResult(
        allowed_countries=pulumi.get(__ret__, 'allowed_countries'),
        allowed_origins=pulumi.get(__ret__, 'allowed_origins'),
        arn=pulumi.get(__ret__, 'arn'),
        enable_strict_origin_enforcement=pulumi.get(__ret__, 'enable_strict_origin_enforcement'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_playback_restriction_policy_output(arn: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPlaybackRestrictionPolicyResult]:
    """
    Resource Type definition for AWS::IVS::PlaybackRestrictionPolicy.


    :param str arn: Playback-restriction-policy identifier.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ivs:getPlaybackRestrictionPolicy', __args__, opts=opts, typ=GetPlaybackRestrictionPolicyResult)
    return __ret__.apply(lambda __response__: GetPlaybackRestrictionPolicyResult(
        allowed_countries=pulumi.get(__response__, 'allowed_countries'),
        allowed_origins=pulumi.get(__response__, 'allowed_origins'),
        arn=pulumi.get(__response__, 'arn'),
        enable_strict_origin_enforcement=pulumi.get(__response__, 'enable_strict_origin_enforcement'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags')))
