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
    'GetStreamingImageResult',
    'AwaitableGetStreamingImageResult',
    'get_streaming_image',
    'get_streaming_image_output',
]

@pulumi.output_type
class GetStreamingImageResult:
    def __init__(__self__, description=None, encryption_configuration=None, encryption_configuration_key_arn=None, encryption_configuration_key_type=None, eula_ids=None, name=None, owner=None, platform=None, streaming_image_id=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if encryption_configuration and not isinstance(encryption_configuration, dict):
            raise TypeError("Expected argument 'encryption_configuration' to be a dict")
        pulumi.set(__self__, "encryption_configuration", encryption_configuration)
        if encryption_configuration_key_arn and not isinstance(encryption_configuration_key_arn, str):
            raise TypeError("Expected argument 'encryption_configuration_key_arn' to be a str")
        pulumi.set(__self__, "encryption_configuration_key_arn", encryption_configuration_key_arn)
        if encryption_configuration_key_type and not isinstance(encryption_configuration_key_type, str):
            raise TypeError("Expected argument 'encryption_configuration_key_type' to be a str")
        pulumi.set(__self__, "encryption_configuration_key_type", encryption_configuration_key_type)
        if eula_ids and not isinstance(eula_ids, list):
            raise TypeError("Expected argument 'eula_ids' to be a list")
        pulumi.set(__self__, "eula_ids", eula_ids)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if owner and not isinstance(owner, str):
            raise TypeError("Expected argument 'owner' to be a str")
        pulumi.set(__self__, "owner", owner)
        if platform and not isinstance(platform, str):
            raise TypeError("Expected argument 'platform' to be a str")
        pulumi.set(__self__, "platform", platform)
        if streaming_image_id and not isinstance(streaming_image_id, str):
            raise TypeError("Expected argument 'streaming_image_id' to be a str")
        pulumi.set(__self__, "streaming_image_id", streaming_image_id)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A human-readable description of the streaming image.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> Optional['outputs.StreamingImageEncryptionConfiguration']:
        return pulumi.get(self, "encryption_configuration")

    @property
    @pulumi.getter(name="encryptionConfigurationKeyArn")
    def encryption_configuration_key_arn(self) -> Optional[str]:
        return pulumi.get(self, "encryption_configuration_key_arn")

    @property
    @pulumi.getter(name="encryptionConfigurationKeyType")
    def encryption_configuration_key_type(self) -> Optional[str]:
        return pulumi.get(self, "encryption_configuration_key_type")

    @property
    @pulumi.getter(name="eulaIds")
    def eula_ids(self) -> Optional[Sequence[str]]:
        """
        The list of IDs of EULAs that must be accepted before a streaming session can be started using this streaming image.
        """
        return pulumi.get(self, "eula_ids")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A friendly name for a streaming image resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def owner(self) -> Optional[str]:
        """
        The owner of the streaming image, either the studioId that contains the streaming image or 'amazon' for images that are provided by  .
        """
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter
    def platform(self) -> Optional[str]:
        """
        The platform of the streaming image, either WINDOWS or LINUX.
        """
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter(name="streamingImageId")
    def streaming_image_id(self) -> Optional[str]:
        """
        The unique identifier for the streaming image resource.
        """
        return pulumi.get(self, "streaming_image_id")


class AwaitableGetStreamingImageResult(GetStreamingImageResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStreamingImageResult(
            description=self.description,
            encryption_configuration=self.encryption_configuration,
            encryption_configuration_key_arn=self.encryption_configuration_key_arn,
            encryption_configuration_key_type=self.encryption_configuration_key_type,
            eula_ids=self.eula_ids,
            name=self.name,
            owner=self.owner,
            platform=self.platform,
            streaming_image_id=self.streaming_image_id)


def get_streaming_image(streaming_image_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStreamingImageResult:
    """
    Resource Type definition for AWS::NimbleStudio::StreamingImage


    :param str streaming_image_id: The unique identifier for the streaming image resource.
    """
    __args__ = dict()
    __args__['streamingImageId'] = streaming_image_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:nimblestudio:getStreamingImage', __args__, opts=opts, typ=GetStreamingImageResult).value

    return AwaitableGetStreamingImageResult(
        description=pulumi.get(__ret__, 'description'),
        encryption_configuration=pulumi.get(__ret__, 'encryption_configuration'),
        encryption_configuration_key_arn=pulumi.get(__ret__, 'encryption_configuration_key_arn'),
        encryption_configuration_key_type=pulumi.get(__ret__, 'encryption_configuration_key_type'),
        eula_ids=pulumi.get(__ret__, 'eula_ids'),
        name=pulumi.get(__ret__, 'name'),
        owner=pulumi.get(__ret__, 'owner'),
        platform=pulumi.get(__ret__, 'platform'),
        streaming_image_id=pulumi.get(__ret__, 'streaming_image_id'))
def get_streaming_image_output(streaming_image_id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetStreamingImageResult]:
    """
    Resource Type definition for AWS::NimbleStudio::StreamingImage


    :param str streaming_image_id: The unique identifier for the streaming image resource.
    """
    __args__ = dict()
    __args__['streamingImageId'] = streaming_image_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:nimblestudio:getStreamingImage', __args__, opts=opts, typ=GetStreamingImageResult)
    return __ret__.apply(lambda __response__: GetStreamingImageResult(
        description=pulumi.get(__response__, 'description'),
        encryption_configuration=pulumi.get(__response__, 'encryption_configuration'),
        encryption_configuration_key_arn=pulumi.get(__response__, 'encryption_configuration_key_arn'),
        encryption_configuration_key_type=pulumi.get(__response__, 'encryption_configuration_key_type'),
        eula_ids=pulumi.get(__response__, 'eula_ids'),
        name=pulumi.get(__response__, 'name'),
        owner=pulumi.get(__response__, 'owner'),
        platform=pulumi.get(__response__, 'platform'),
        streaming_image_id=pulumi.get(__response__, 'streaming_image_id')))
