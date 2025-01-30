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
    'GetGroupProfileResult',
    'AwaitableGetGroupProfileResult',
    'get_group_profile',
    'get_group_profile_output',
]

@pulumi.output_type
class GetGroupProfileResult:
    def __init__(__self__, domain_id=None, group_name=None, id=None, status=None):
        if domain_id and not isinstance(domain_id, str):
            raise TypeError("Expected argument 'domain_id' to be a str")
        pulumi.set(__self__, "domain_id", domain_id)
        if group_name and not isinstance(group_name, str):
            raise TypeError("Expected argument 'group_name' to be a str")
        pulumi.set(__self__, "group_name", group_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="domainId")
    def domain_id(self) -> Optional[str]:
        """
        The identifier of the Amazon DataZone domain in which the group profile is created.
        """
        return pulumi.get(self, "domain_id")

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> Optional[str]:
        """
        The group-name of the Group Profile.
        """
        return pulumi.get(self, "group_name")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the Amazon DataZone group profile.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def status(self) -> Optional['GroupProfileStatus']:
        """
        The status of a group profile.
        """
        return pulumi.get(self, "status")


class AwaitableGetGroupProfileResult(GetGroupProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupProfileResult(
            domain_id=self.domain_id,
            group_name=self.group_name,
            id=self.id,
            status=self.status)


def get_group_profile(domain_id: Optional[str] = None,
                      id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupProfileResult:
    """
    Group profiles represent groups of Amazon DataZone users. Groups can be manually created, or mapped to Active Directory groups of enterprise customers. In Amazon DataZone, groups serve two purposes. First, a group can map to a team of users in the organizational chart, and thus reduce the administrative work of a Amazon DataZone project owner when there are new employees joining or leaving a team. Second, corporate administrators use Active Directory groups to manage and update user statuses and so Amazon DataZone domain administrators can use these group memberships to implement Amazon DataZone domain policies.


    :param str domain_id: The identifier of the Amazon DataZone domain in which the group profile is created.
    :param str id: The ID of the Amazon DataZone group profile.
    """
    __args__ = dict()
    __args__['domainId'] = domain_id
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:datazone:getGroupProfile', __args__, opts=opts, typ=GetGroupProfileResult).value

    return AwaitableGetGroupProfileResult(
        domain_id=pulumi.get(__ret__, 'domain_id'),
        group_name=pulumi.get(__ret__, 'group_name'),
        id=pulumi.get(__ret__, 'id'),
        status=pulumi.get(__ret__, 'status'))
def get_group_profile_output(domain_id: Optional[pulumi.Input[str]] = None,
                             id: Optional[pulumi.Input[str]] = None,
                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetGroupProfileResult]:
    """
    Group profiles represent groups of Amazon DataZone users. Groups can be manually created, or mapped to Active Directory groups of enterprise customers. In Amazon DataZone, groups serve two purposes. First, a group can map to a team of users in the organizational chart, and thus reduce the administrative work of a Amazon DataZone project owner when there are new employees joining or leaving a team. Second, corporate administrators use Active Directory groups to manage and update user statuses and so Amazon DataZone domain administrators can use these group memberships to implement Amazon DataZone domain policies.


    :param str domain_id: The identifier of the Amazon DataZone domain in which the group profile is created.
    :param str id: The ID of the Amazon DataZone group profile.
    """
    __args__ = dict()
    __args__['domainId'] = domain_id
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:datazone:getGroupProfile', __args__, opts=opts, typ=GetGroupProfileResult)
    return __ret__.apply(lambda __response__: GetGroupProfileResult(
        domain_id=pulumi.get(__response__, 'domain_id'),
        group_name=pulumi.get(__response__, 'group_name'),
        id=pulumi.get(__response__, 'id'),
        status=pulumi.get(__response__, 'status')))
