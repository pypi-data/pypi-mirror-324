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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs

__all__ = ['InternetGatewayArgs', 'InternetGateway']

@pulumi.input_type
class InternetGatewayArgs:
    def __init__(__self__, *,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a InternetGateway resource.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: Any tags to assign to the internet gateway.
        """
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        Any tags to assign to the internet gateway.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class InternetGateway(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Allocates an internet gateway for use with a VPC. After creating the Internet gateway, you then attach it to a VPC.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        my_internet_gateway = aws_native.ec2.InternetGateway("myInternetGateway", tags=[{
            "key": "stack",
            "value": "production",
        }])

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: Any tags to assign to the internet gateway.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[InternetGatewayArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Allocates an internet gateway for use with a VPC. After creating the Internet gateway, you then attach it to a VPC.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        my_internet_gateway = aws_native.ec2.InternetGateway("myInternetGateway", tags=[{
            "key": "stack",
            "value": "production",
        }])

        ```

        :param str resource_name: The name of the resource.
        :param InternetGatewayArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InternetGatewayArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InternetGatewayArgs.__new__(InternetGatewayArgs)

            __props__.__dict__["tags"] = tags
            __props__.__dict__["internet_gateway_id"] = None
        super(InternetGateway, __self__).__init__(
            'aws-native:ec2:InternetGateway',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'InternetGateway':
        """
        Get an existing InternetGateway resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = InternetGatewayArgs.__new__(InternetGatewayArgs)

        __props__.__dict__["internet_gateway_id"] = None
        __props__.__dict__["tags"] = None
        return InternetGateway(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="internetGatewayId")
    def internet_gateway_id(self) -> pulumi.Output[str]:
        """
        The ID of the internet gateway.
        """
        return pulumi.get(self, "internet_gateway_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        Any tags to assign to the internet gateway.
        """
        return pulumi.get(self, "tags")

