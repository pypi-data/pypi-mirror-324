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
    'GetDataAccessorResult',
    'AwaitableGetDataAccessorResult',
    'get_data_accessor',
    'get_data_accessor_output',
]

@pulumi.output_type
class GetDataAccessorResult:
    def __init__(__self__, action_configurations=None, created_at=None, data_accessor_arn=None, data_accessor_id=None, display_name=None, idc_application_arn=None, tags=None, updated_at=None):
        if action_configurations and not isinstance(action_configurations, list):
            raise TypeError("Expected argument 'action_configurations' to be a list")
        pulumi.set(__self__, "action_configurations", action_configurations)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if data_accessor_arn and not isinstance(data_accessor_arn, str):
            raise TypeError("Expected argument 'data_accessor_arn' to be a str")
        pulumi.set(__self__, "data_accessor_arn", data_accessor_arn)
        if data_accessor_id and not isinstance(data_accessor_id, str):
            raise TypeError("Expected argument 'data_accessor_id' to be a str")
        pulumi.set(__self__, "data_accessor_id", data_accessor_id)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if idc_application_arn and not isinstance(idc_application_arn, str):
            raise TypeError("Expected argument 'idc_application_arn' to be a str")
        pulumi.set(__self__, "idc_application_arn", idc_application_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="actionConfigurations")
    def action_configurations(self) -> Optional[Sequence['outputs.DataAccessorActionConfiguration']]:
        """
        A list of action configurations specifying the allowed actions and any associated filters.
        """
        return pulumi.get(self, "action_configurations")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp when the data accessor was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="dataAccessorArn")
    def data_accessor_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the data accessor.
        """
        return pulumi.get(self, "data_accessor_arn")

    @property
    @pulumi.getter(name="dataAccessorId")
    def data_accessor_id(self) -> Optional[str]:
        """
        The unique identifier of the data accessor.
        """
        return pulumi.get(self, "data_accessor_id")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The friendly name of the data accessor.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="idcApplicationArn")
    def idc_application_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the associated IAM Identity Center application.
        """
        return pulumi.get(self, "idc_application_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags to associate with the data accessor.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[str]:
        """
        The timestamp when the data accessor was last updated.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetDataAccessorResult(GetDataAccessorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDataAccessorResult(
            action_configurations=self.action_configurations,
            created_at=self.created_at,
            data_accessor_arn=self.data_accessor_arn,
            data_accessor_id=self.data_accessor_id,
            display_name=self.display_name,
            idc_application_arn=self.idc_application_arn,
            tags=self.tags,
            updated_at=self.updated_at)


def get_data_accessor(application_id: Optional[str] = None,
                      data_accessor_id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDataAccessorResult:
    """
    Definition of AWS::QBusiness::DataAccessor Resource Type


    :param str application_id: The unique identifier of the Amazon Q Business application.
    :param str data_accessor_id: The unique identifier of the data accessor.
    """
    __args__ = dict()
    __args__['applicationId'] = application_id
    __args__['dataAccessorId'] = data_accessor_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:qbusiness:getDataAccessor', __args__, opts=opts, typ=GetDataAccessorResult).value

    return AwaitableGetDataAccessorResult(
        action_configurations=pulumi.get(__ret__, 'action_configurations'),
        created_at=pulumi.get(__ret__, 'created_at'),
        data_accessor_arn=pulumi.get(__ret__, 'data_accessor_arn'),
        data_accessor_id=pulumi.get(__ret__, 'data_accessor_id'),
        display_name=pulumi.get(__ret__, 'display_name'),
        idc_application_arn=pulumi.get(__ret__, 'idc_application_arn'),
        tags=pulumi.get(__ret__, 'tags'),
        updated_at=pulumi.get(__ret__, 'updated_at'))
def get_data_accessor_output(application_id: Optional[pulumi.Input[str]] = None,
                             data_accessor_id: Optional[pulumi.Input[str]] = None,
                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetDataAccessorResult]:
    """
    Definition of AWS::QBusiness::DataAccessor Resource Type


    :param str application_id: The unique identifier of the Amazon Q Business application.
    :param str data_accessor_id: The unique identifier of the data accessor.
    """
    __args__ = dict()
    __args__['applicationId'] = application_id
    __args__['dataAccessorId'] = data_accessor_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:qbusiness:getDataAccessor', __args__, opts=opts, typ=GetDataAccessorResult)
    return __ret__.apply(lambda __response__: GetDataAccessorResult(
        action_configurations=pulumi.get(__response__, 'action_configurations'),
        created_at=pulumi.get(__response__, 'created_at'),
        data_accessor_arn=pulumi.get(__response__, 'data_accessor_arn'),
        data_accessor_id=pulumi.get(__response__, 'data_accessor_id'),
        display_name=pulumi.get(__response__, 'display_name'),
        idc_application_arn=pulumi.get(__response__, 'idc_application_arn'),
        tags=pulumi.get(__response__, 'tags'),
        updated_at=pulumi.get(__response__, 'updated_at')))
