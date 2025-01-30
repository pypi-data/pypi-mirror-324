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
    'GetSchemaVersionResult',
    'AwaitableGetSchemaVersionResult',
    'get_schema_version',
    'get_schema_version_output',
]

@pulumi.output_type
class GetSchemaVersionResult:
    def __init__(__self__, version_id=None):
        if version_id and not isinstance(version_id, str):
            raise TypeError("Expected argument 'version_id' to be a str")
        pulumi.set(__self__, "version_id", version_id)

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> Optional[str]:
        """
        Represents the version ID associated with the schema version.
        """
        return pulumi.get(self, "version_id")


class AwaitableGetSchemaVersionResult(GetSchemaVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSchemaVersionResult(
            version_id=self.version_id)


def get_schema_version(version_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSchemaVersionResult:
    """
    This resource represents an individual schema version of a schema defined in Glue Schema Registry.


    :param str version_id: Represents the version ID associated with the schema version.
    """
    __args__ = dict()
    __args__['versionId'] = version_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:glue:getSchemaVersion', __args__, opts=opts, typ=GetSchemaVersionResult).value

    return AwaitableGetSchemaVersionResult(
        version_id=pulumi.get(__ret__, 'version_id'))
def get_schema_version_output(version_id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSchemaVersionResult]:
    """
    This resource represents an individual schema version of a schema defined in Glue Schema Registry.


    :param str version_id: Represents the version ID associated with the schema version.
    """
    __args__ = dict()
    __args__['versionId'] = version_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:glue:getSchemaVersion', __args__, opts=opts, typ=GetSchemaVersionResult)
    return __ret__.apply(lambda __response__: GetSchemaVersionResult(
        version_id=pulumi.get(__response__, 'version_id')))
