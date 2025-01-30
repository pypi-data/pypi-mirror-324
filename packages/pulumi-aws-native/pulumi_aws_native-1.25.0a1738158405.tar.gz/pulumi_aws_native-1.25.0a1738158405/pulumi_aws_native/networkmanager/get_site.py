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
from .. import outputs as _root_outputs

__all__ = [
    'GetSiteResult',
    'AwaitableGetSiteResult',
    'get_site',
    'get_site_output',
]

@pulumi.output_type
class GetSiteResult:
    def __init__(__self__, created_at=None, description=None, location=None, site_arn=None, site_id=None, state=None, tags=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if location and not isinstance(location, dict):
            raise TypeError("Expected argument 'location' to be a dict")
        pulumi.set(__self__, "location", location)
        if site_arn and not isinstance(site_arn, str):
            raise TypeError("Expected argument 'site_arn' to be a str")
        pulumi.set(__self__, "site_arn", site_arn)
        if site_id and not isinstance(site_id, str):
            raise TypeError("Expected argument 'site_id' to be a str")
        pulumi.set(__self__, "site_id", site_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The date and time that the device was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the site.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def location(self) -> Optional['outputs.SiteLocation']:
        """
        The location of the site.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="siteArn")
    def site_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the site.
        """
        return pulumi.get(self, "site_arn")

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> Optional[str]:
        """
        The ID of the site.
        """
        return pulumi.get(self, "site_id")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the site.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags for the site.
        """
        return pulumi.get(self, "tags")


class AwaitableGetSiteResult(GetSiteResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSiteResult(
            created_at=self.created_at,
            description=self.description,
            location=self.location,
            site_arn=self.site_arn,
            site_id=self.site_id,
            state=self.state,
            tags=self.tags)


def get_site(global_network_id: Optional[str] = None,
             site_id: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSiteResult:
    """
    The AWS::NetworkManager::Site type describes a site.


    :param str global_network_id: The ID of the global network.
    :param str site_id: The ID of the site.
    """
    __args__ = dict()
    __args__['globalNetworkId'] = global_network_id
    __args__['siteId'] = site_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:networkmanager:getSite', __args__, opts=opts, typ=GetSiteResult).value

    return AwaitableGetSiteResult(
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        location=pulumi.get(__ret__, 'location'),
        site_arn=pulumi.get(__ret__, 'site_arn'),
        site_id=pulumi.get(__ret__, 'site_id'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'))
def get_site_output(global_network_id: Optional[pulumi.Input[str]] = None,
                    site_id: Optional[pulumi.Input[str]] = None,
                    opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSiteResult]:
    """
    The AWS::NetworkManager::Site type describes a site.


    :param str global_network_id: The ID of the global network.
    :param str site_id: The ID of the site.
    """
    __args__ = dict()
    __args__['globalNetworkId'] = global_network_id
    __args__['siteId'] = site_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:networkmanager:getSite', __args__, opts=opts, typ=GetSiteResult)
    return __ret__.apply(lambda __response__: GetSiteResult(
        created_at=pulumi.get(__response__, 'created_at'),
        description=pulumi.get(__response__, 'description'),
        location=pulumi.get(__response__, 'location'),
        site_arn=pulumi.get(__response__, 'site_arn'),
        site_id=pulumi.get(__response__, 'site_id'),
        state=pulumi.get(__response__, 'state'),
        tags=pulumi.get(__response__, 'tags')))
