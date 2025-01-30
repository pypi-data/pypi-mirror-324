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
    'GetVpcOriginResult',
    'AwaitableGetVpcOriginResult',
    'get_vpc_origin',
    'get_vpc_origin_output',
]

@pulumi.output_type
class GetVpcOriginResult:
    def __init__(__self__, arn=None, created_time=None, id=None, last_modified_time=None, status=None, tags=None, vpc_origin_endpoint_config=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_time and not isinstance(created_time, str):
            raise TypeError("Expected argument 'created_time' to be a str")
        pulumi.set(__self__, "created_time", created_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if vpc_origin_endpoint_config and not isinstance(vpc_origin_endpoint_config, dict):
            raise TypeError("Expected argument 'vpc_origin_endpoint_config' to be a dict")
        pulumi.set(__self__, "vpc_origin_endpoint_config", vpc_origin_endpoint_config)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> Optional[str]:
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> Optional[str]:
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcOriginEndpointConfig")
    def vpc_origin_endpoint_config(self) -> Optional['outputs.VpcOriginEndpointConfig']:
        return pulumi.get(self, "vpc_origin_endpoint_config")


class AwaitableGetVpcOriginResult(GetVpcOriginResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcOriginResult(
            arn=self.arn,
            created_time=self.created_time,
            id=self.id,
            last_modified_time=self.last_modified_time,
            status=self.status,
            tags=self.tags,
            vpc_origin_endpoint_config=self.vpc_origin_endpoint_config)


def get_vpc_origin(id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcOriginResult:
    """
    Resource Type definition for AWS::CloudFront::VpcOrigin
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cloudfront:getVpcOrigin', __args__, opts=opts, typ=GetVpcOriginResult).value

    return AwaitableGetVpcOriginResult(
        arn=pulumi.get(__ret__, 'arn'),
        created_time=pulumi.get(__ret__, 'created_time'),
        id=pulumi.get(__ret__, 'id'),
        last_modified_time=pulumi.get(__ret__, 'last_modified_time'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'),
        vpc_origin_endpoint_config=pulumi.get(__ret__, 'vpc_origin_endpoint_config'))
def get_vpc_origin_output(id: Optional[pulumi.Input[str]] = None,
                          opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetVpcOriginResult]:
    """
    Resource Type definition for AWS::CloudFront::VpcOrigin
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cloudfront:getVpcOrigin', __args__, opts=opts, typ=GetVpcOriginResult)
    return __ret__.apply(lambda __response__: GetVpcOriginResult(
        arn=pulumi.get(__response__, 'arn'),
        created_time=pulumi.get(__response__, 'created_time'),
        id=pulumi.get(__response__, 'id'),
        last_modified_time=pulumi.get(__response__, 'last_modified_time'),
        status=pulumi.get(__response__, 'status'),
        tags=pulumi.get(__response__, 'tags'),
        vpc_origin_endpoint_config=pulumi.get(__response__, 'vpc_origin_endpoint_config')))
