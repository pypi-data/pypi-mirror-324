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
    'GetConformancePackResult',
    'AwaitableGetConformancePackResult',
    'get_conformance_pack',
    'get_conformance_pack_output',
]

@pulumi.output_type
class GetConformancePackResult:
    def __init__(__self__, conformance_pack_input_parameters=None, delivery_s3_bucket=None, delivery_s3_key_prefix=None):
        if conformance_pack_input_parameters and not isinstance(conformance_pack_input_parameters, list):
            raise TypeError("Expected argument 'conformance_pack_input_parameters' to be a list")
        pulumi.set(__self__, "conformance_pack_input_parameters", conformance_pack_input_parameters)
        if delivery_s3_bucket and not isinstance(delivery_s3_bucket, str):
            raise TypeError("Expected argument 'delivery_s3_bucket' to be a str")
        pulumi.set(__self__, "delivery_s3_bucket", delivery_s3_bucket)
        if delivery_s3_key_prefix and not isinstance(delivery_s3_key_prefix, str):
            raise TypeError("Expected argument 'delivery_s3_key_prefix' to be a str")
        pulumi.set(__self__, "delivery_s3_key_prefix", delivery_s3_key_prefix)

    @property
    @pulumi.getter(name="conformancePackInputParameters")
    def conformance_pack_input_parameters(self) -> Optional[Sequence['outputs.ConformancePackInputParameter']]:
        """
        A list of ConformancePackInputParameter objects.
        """
        return pulumi.get(self, "conformance_pack_input_parameters")

    @property
    @pulumi.getter(name="deliveryS3Bucket")
    def delivery_s3_bucket(self) -> Optional[str]:
        """
        AWS Config stores intermediate files while processing conformance pack template.
        """
        return pulumi.get(self, "delivery_s3_bucket")

    @property
    @pulumi.getter(name="deliveryS3KeyPrefix")
    def delivery_s3_key_prefix(self) -> Optional[str]:
        """
        The prefix for delivery S3 bucket.
        """
        return pulumi.get(self, "delivery_s3_key_prefix")


class AwaitableGetConformancePackResult(GetConformancePackResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConformancePackResult(
            conformance_pack_input_parameters=self.conformance_pack_input_parameters,
            delivery_s3_bucket=self.delivery_s3_bucket,
            delivery_s3_key_prefix=self.delivery_s3_key_prefix)


def get_conformance_pack(conformance_pack_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConformancePackResult:
    """
    A conformance pack is a collection of AWS Config rules and remediation actions that can be easily deployed as a single entity in an account and a region or across an entire AWS Organization.


    :param str conformance_pack_name: Name of the conformance pack which will be assigned as the unique identifier.
    """
    __args__ = dict()
    __args__['conformancePackName'] = conformance_pack_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:configuration:getConformancePack', __args__, opts=opts, typ=GetConformancePackResult).value

    return AwaitableGetConformancePackResult(
        conformance_pack_input_parameters=pulumi.get(__ret__, 'conformance_pack_input_parameters'),
        delivery_s3_bucket=pulumi.get(__ret__, 'delivery_s3_bucket'),
        delivery_s3_key_prefix=pulumi.get(__ret__, 'delivery_s3_key_prefix'))
def get_conformance_pack_output(conformance_pack_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetConformancePackResult]:
    """
    A conformance pack is a collection of AWS Config rules and remediation actions that can be easily deployed as a single entity in an account and a region or across an entire AWS Organization.


    :param str conformance_pack_name: Name of the conformance pack which will be assigned as the unique identifier.
    """
    __args__ = dict()
    __args__['conformancePackName'] = conformance_pack_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:configuration:getConformancePack', __args__, opts=opts, typ=GetConformancePackResult)
    return __ret__.apply(lambda __response__: GetConformancePackResult(
        conformance_pack_input_parameters=pulumi.get(__response__, 'conformance_pack_input_parameters'),
        delivery_s3_bucket=pulumi.get(__response__, 'delivery_s3_bucket'),
        delivery_s3_key_prefix=pulumi.get(__response__, 'delivery_s3_key_prefix')))
