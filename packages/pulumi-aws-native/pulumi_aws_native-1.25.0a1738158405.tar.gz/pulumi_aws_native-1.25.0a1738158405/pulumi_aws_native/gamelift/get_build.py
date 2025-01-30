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
    'GetBuildResult',
    'AwaitableGetBuildResult',
    'get_build',
    'get_build_output',
]

@pulumi.output_type
class GetBuildResult:
    def __init__(__self__, build_id=None, name=None, version=None):
        if build_id and not isinstance(build_id, str):
            raise TypeError("Expected argument 'build_id' to be a str")
        pulumi.set(__self__, "build_id", build_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="buildId")
    def build_id(self) -> Optional[str]:
        """
        A unique identifier for a build to be deployed on the new fleet. If you are deploying the fleet with a custom game build, you must specify this property. The build must have been successfully uploaded to Amazon GameLift and be in a READY status. This fleet setting cannot be changed once the fleet is created.
        """
        return pulumi.get(self, "build_id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A descriptive label that is associated with a build. Build names do not need to be unique.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version information that is associated with this build. Version strings do not need to be unique.
        """
        return pulumi.get(self, "version")


class AwaitableGetBuildResult(GetBuildResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBuildResult(
            build_id=self.build_id,
            name=self.name,
            version=self.version)


def get_build(build_id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBuildResult:
    """
    Resource Type definition for AWS::GameLift::Build


    :param str build_id: A unique identifier for a build to be deployed on the new fleet. If you are deploying the fleet with a custom game build, you must specify this property. The build must have been successfully uploaded to Amazon GameLift and be in a READY status. This fleet setting cannot be changed once the fleet is created.
    """
    __args__ = dict()
    __args__['buildId'] = build_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:gamelift:getBuild', __args__, opts=opts, typ=GetBuildResult).value

    return AwaitableGetBuildResult(
        build_id=pulumi.get(__ret__, 'build_id'),
        name=pulumi.get(__ret__, 'name'),
        version=pulumi.get(__ret__, 'version'))
def get_build_output(build_id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetBuildResult]:
    """
    Resource Type definition for AWS::GameLift::Build


    :param str build_id: A unique identifier for a build to be deployed on the new fleet. If you are deploying the fleet with a custom game build, you must specify this property. The build must have been successfully uploaded to Amazon GameLift and be in a READY status. This fleet setting cannot be changed once the fleet is created.
    """
    __args__ = dict()
    __args__['buildId'] = build_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:gamelift:getBuild', __args__, opts=opts, typ=GetBuildResult)
    return __ret__.apply(lambda __response__: GetBuildResult(
        build_id=pulumi.get(__response__, 'build_id'),
        name=pulumi.get(__response__, 'name'),
        version=pulumi.get(__response__, 'version')))
