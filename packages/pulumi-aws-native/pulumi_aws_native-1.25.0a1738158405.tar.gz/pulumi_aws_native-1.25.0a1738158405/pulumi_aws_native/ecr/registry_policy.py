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

__all__ = ['RegistryPolicyArgs', 'RegistryPolicy']

@pulumi.input_type
class RegistryPolicyArgs:
    def __init__(__self__, *,
                 policy_text: Any):
        """
        The set of arguments for constructing a RegistryPolicy resource.
        :param Any policy_text: The JSON policy text for your registry.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::ECR::RegistryPolicy` for more information about the expected schema for this property.
        """
        pulumi.set(__self__, "policy_text", policy_text)

    @property
    @pulumi.getter(name="policyText")
    def policy_text(self) -> Any:
        """
        The JSON policy text for your registry.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::ECR::RegistryPolicy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy_text")

    @policy_text.setter
    def policy_text(self, value: Any):
        pulumi.set(self, "policy_text", value)


class RegistryPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_text: Optional[Any] = None,
                 __props__=None):
        """
        The ``AWS::ECR::RegistryPolicy`` resource creates or updates the permissions policy for a private registry.
         A private registry policy is used to specify permissions for another AWS-account and is used when configuring cross-account replication. For more information, see [Registry permissions](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-permissions.html) in the *Amazon Elastic Container Registry User Guide*.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        test_registry_policy = aws_native.ecr.RegistryPolicy("testRegistryPolicy", policy_text={
            "version": "2012-10-17",
            "statement": [{
                "sid": "UpdatedRegistryPolicy",
                "effect": "Allow",
                "principal": {
                    "aws": "arn:aws:iam::210987654321:root",
                },
                "action": [
                    "ecr:CreateRepository",
                    "ecr:ReplicateImage",
                ],
                "resource": "arn:aws:ecr:us-west-2:123456789012:repository/*",
            }],
        })

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param Any policy_text: The JSON policy text for your registry.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::ECR::RegistryPolicy` for more information about the expected schema for this property.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RegistryPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ``AWS::ECR::RegistryPolicy`` resource creates or updates the permissions policy for a private registry.
         A private registry policy is used to specify permissions for another AWS-account and is used when configuring cross-account replication. For more information, see [Registry permissions](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-permissions.html) in the *Amazon Elastic Container Registry User Guide*.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        test_registry_policy = aws_native.ecr.RegistryPolicy("testRegistryPolicy", policy_text={
            "version": "2012-10-17",
            "statement": [{
                "sid": "UpdatedRegistryPolicy",
                "effect": "Allow",
                "principal": {
                    "aws": "arn:aws:iam::210987654321:root",
                },
                "action": [
                    "ecr:CreateRepository",
                    "ecr:ReplicateImage",
                ],
                "resource": "arn:aws:ecr:us-west-2:123456789012:repository/*",
            }],
        })

        ```

        :param str resource_name: The name of the resource.
        :param RegistryPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RegistryPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_text: Optional[Any] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RegistryPolicyArgs.__new__(RegistryPolicyArgs)

            if policy_text is None and not opts.urn:
                raise TypeError("Missing required property 'policy_text'")
            __props__.__dict__["policy_text"] = policy_text
            __props__.__dict__["registry_id"] = None
        super(RegistryPolicy, __self__).__init__(
            'aws-native:ecr:RegistryPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RegistryPolicy':
        """
        Get an existing RegistryPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RegistryPolicyArgs.__new__(RegistryPolicyArgs)

        __props__.__dict__["policy_text"] = None
        __props__.__dict__["registry_id"] = None
        return RegistryPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="policyText")
    def policy_text(self) -> pulumi.Output[Any]:
        """
        The JSON policy text for your registry.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::ECR::RegistryPolicy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy_text")

    @property
    @pulumi.getter(name="registryId")
    def registry_id(self) -> pulumi.Output[str]:
        """
        The account ID of the private registry the policy is associated with.
        """
        return pulumi.get(self, "registry_id")

