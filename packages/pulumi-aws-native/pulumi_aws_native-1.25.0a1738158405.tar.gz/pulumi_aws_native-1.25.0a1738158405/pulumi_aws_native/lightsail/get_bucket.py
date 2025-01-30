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
    'GetBucketResult',
    'AwaitableGetBucketResult',
    'get_bucket',
    'get_bucket_output',
]

@pulumi.output_type
class GetBucketResult:
    def __init__(__self__, able_to_update_bundle=None, access_rules=None, bucket_arn=None, bundle_id=None, object_versioning=None, read_only_access_accounts=None, resources_receiving_access=None, tags=None, url=None):
        if able_to_update_bundle and not isinstance(able_to_update_bundle, bool):
            raise TypeError("Expected argument 'able_to_update_bundle' to be a bool")
        pulumi.set(__self__, "able_to_update_bundle", able_to_update_bundle)
        if access_rules and not isinstance(access_rules, dict):
            raise TypeError("Expected argument 'access_rules' to be a dict")
        pulumi.set(__self__, "access_rules", access_rules)
        if bucket_arn and not isinstance(bucket_arn, str):
            raise TypeError("Expected argument 'bucket_arn' to be a str")
        pulumi.set(__self__, "bucket_arn", bucket_arn)
        if bundle_id and not isinstance(bundle_id, str):
            raise TypeError("Expected argument 'bundle_id' to be a str")
        pulumi.set(__self__, "bundle_id", bundle_id)
        if object_versioning and not isinstance(object_versioning, bool):
            raise TypeError("Expected argument 'object_versioning' to be a bool")
        pulumi.set(__self__, "object_versioning", object_versioning)
        if read_only_access_accounts and not isinstance(read_only_access_accounts, list):
            raise TypeError("Expected argument 'read_only_access_accounts' to be a list")
        pulumi.set(__self__, "read_only_access_accounts", read_only_access_accounts)
        if resources_receiving_access and not isinstance(resources_receiving_access, list):
            raise TypeError("Expected argument 'resources_receiving_access' to be a list")
        pulumi.set(__self__, "resources_receiving_access", resources_receiving_access)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter(name="ableToUpdateBundle")
    def able_to_update_bundle(self) -> Optional[bool]:
        """
        Indicates whether the bundle that is currently applied to a bucket can be changed to another bundle. You can update a bucket's bundle only one time within a monthly AWS billing cycle.
        """
        return pulumi.get(self, "able_to_update_bundle")

    @property
    @pulumi.getter(name="accessRules")
    def access_rules(self) -> Optional['outputs.BucketAccessRules']:
        """
        An object that describes the access rules for the bucket.
        """
        return pulumi.get(self, "access_rules")

    @property
    @pulumi.getter(name="bucketArn")
    def bucket_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the bucket.
        """
        return pulumi.get(self, "bucket_arn")

    @property
    @pulumi.getter(name="bundleId")
    def bundle_id(self) -> Optional[str]:
        """
        The ID of the bundle to use for the bucket.
        """
        return pulumi.get(self, "bundle_id")

    @property
    @pulumi.getter(name="objectVersioning")
    def object_versioning(self) -> Optional[bool]:
        """
        Specifies whether to enable or disable versioning of objects in the bucket.
        """
        return pulumi.get(self, "object_versioning")

    @property
    @pulumi.getter(name="readOnlyAccessAccounts")
    def read_only_access_accounts(self) -> Optional[Sequence[str]]:
        """
        An array of strings to specify the AWS account IDs that can access the bucket.
        """
        return pulumi.get(self, "read_only_access_accounts")

    @property
    @pulumi.getter(name="resourcesReceivingAccess")
    def resources_receiving_access(self) -> Optional[Sequence[str]]:
        """
        The names of the Lightsail resources for which to set bucket access.
        """
        return pulumi.get(self, "resources_receiving_access")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def url(self) -> Optional[str]:
        """
        The URL of the bucket.
        """
        return pulumi.get(self, "url")


class AwaitableGetBucketResult(GetBucketResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBucketResult(
            able_to_update_bundle=self.able_to_update_bundle,
            access_rules=self.access_rules,
            bucket_arn=self.bucket_arn,
            bundle_id=self.bundle_id,
            object_versioning=self.object_versioning,
            read_only_access_accounts=self.read_only_access_accounts,
            resources_receiving_access=self.resources_receiving_access,
            tags=self.tags,
            url=self.url)


def get_bucket(bucket_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBucketResult:
    """
    Resource Type definition for AWS::Lightsail::Bucket


    :param str bucket_name: The name for the bucket.
    """
    __args__ = dict()
    __args__['bucketName'] = bucket_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:lightsail:getBucket', __args__, opts=opts, typ=GetBucketResult).value

    return AwaitableGetBucketResult(
        able_to_update_bundle=pulumi.get(__ret__, 'able_to_update_bundle'),
        access_rules=pulumi.get(__ret__, 'access_rules'),
        bucket_arn=pulumi.get(__ret__, 'bucket_arn'),
        bundle_id=pulumi.get(__ret__, 'bundle_id'),
        object_versioning=pulumi.get(__ret__, 'object_versioning'),
        read_only_access_accounts=pulumi.get(__ret__, 'read_only_access_accounts'),
        resources_receiving_access=pulumi.get(__ret__, 'resources_receiving_access'),
        tags=pulumi.get(__ret__, 'tags'),
        url=pulumi.get(__ret__, 'url'))
def get_bucket_output(bucket_name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetBucketResult]:
    """
    Resource Type definition for AWS::Lightsail::Bucket


    :param str bucket_name: The name for the bucket.
    """
    __args__ = dict()
    __args__['bucketName'] = bucket_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:lightsail:getBucket', __args__, opts=opts, typ=GetBucketResult)
    return __ret__.apply(lambda __response__: GetBucketResult(
        able_to_update_bundle=pulumi.get(__response__, 'able_to_update_bundle'),
        access_rules=pulumi.get(__response__, 'access_rules'),
        bucket_arn=pulumi.get(__response__, 'bucket_arn'),
        bundle_id=pulumi.get(__response__, 'bundle_id'),
        object_versioning=pulumi.get(__response__, 'object_versioning'),
        read_only_access_accounts=pulumi.get(__response__, 'read_only_access_accounts'),
        resources_receiving_access=pulumi.get(__response__, 'resources_receiving_access'),
        tags=pulumi.get(__response__, 'tags'),
        url=pulumi.get(__response__, 'url')))
