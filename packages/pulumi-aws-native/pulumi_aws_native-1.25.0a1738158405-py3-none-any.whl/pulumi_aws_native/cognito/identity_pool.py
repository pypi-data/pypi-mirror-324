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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs
from ._inputs import *

__all__ = ['IdentityPoolArgs', 'IdentityPool']

@pulumi.input_type
class IdentityPoolArgs:
    def __init__(__self__, *,
                 allow_unauthenticated_identities: pulumi.Input[bool],
                 allow_classic_flow: Optional[pulumi.Input[bool]] = None,
                 cognito_events: Optional[Any] = None,
                 cognito_identity_providers: Optional[pulumi.Input[Sequence[pulumi.Input['IdentityPoolCognitoIdentityProviderArgs']]]] = None,
                 cognito_streams: Optional[pulumi.Input['IdentityPoolCognitoStreamsArgs']] = None,
                 developer_provider_name: Optional[pulumi.Input[str]] = None,
                 identity_pool_name: Optional[pulumi.Input[str]] = None,
                 identity_pool_tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 open_id_connect_provider_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 push_sync: Optional[pulumi.Input['IdentityPoolPushSyncArgs']] = None,
                 saml_provider_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 supported_login_providers: Optional[Any] = None):
        """
        The set of arguments for constructing a IdentityPool resource.
        :param pulumi.Input[bool] allow_unauthenticated_identities: Specifies whether the identity pool supports unauthenticated logins.
        :param pulumi.Input[bool] allow_classic_flow: Enables the Basic (Classic) authentication flow.
        :param Any cognito_events: The events to configure.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Cognito::IdentityPool` for more information about the expected schema for this property.
        :param pulumi.Input[Sequence[pulumi.Input['IdentityPoolCognitoIdentityProviderArgs']]] cognito_identity_providers: The Amazon Cognito user pools and their client IDs.
        :param pulumi.Input['IdentityPoolCognitoStreamsArgs'] cognito_streams: Configuration options for configuring Amazon Cognito streams.
        :param pulumi.Input[str] developer_provider_name: The "domain" Amazon Cognito uses when referencing your users. This name acts as a placeholder that allows your backend and the Amazon Cognito service to communicate about the developer provider. For the `DeveloperProviderName` , you can use letters and periods (.), underscores (_), and dashes (-).
               
               *Minimum length* : 1
               
               *Maximum length* : 100
        :param pulumi.Input[str] identity_pool_name: The name of your Amazon Cognito identity pool.
               
               *Minimum length* : 1
               
               *Maximum length* : 128
               
               *Pattern* : `[\\w\\s+=,.@-]+`
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] identity_pool_tags: An array of key-value pairs to apply to this resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] open_id_connect_provider_arns: The Amazon Resource Names (ARNs) of the OpenID connect providers.
        :param pulumi.Input['IdentityPoolPushSyncArgs'] push_sync: The configuration options to be applied to the identity pool.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] saml_provider_arns: The Amazon Resource Names (ARNs) of the Security Assertion Markup Language (SAML) providers.
        :param Any supported_login_providers: Key-value pairs that map provider names to provider app IDs.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Cognito::IdentityPool` for more information about the expected schema for this property.
        """
        pulumi.set(__self__, "allow_unauthenticated_identities", allow_unauthenticated_identities)
        if allow_classic_flow is not None:
            pulumi.set(__self__, "allow_classic_flow", allow_classic_flow)
        if cognito_events is not None:
            pulumi.set(__self__, "cognito_events", cognito_events)
        if cognito_identity_providers is not None:
            pulumi.set(__self__, "cognito_identity_providers", cognito_identity_providers)
        if cognito_streams is not None:
            pulumi.set(__self__, "cognito_streams", cognito_streams)
        if developer_provider_name is not None:
            pulumi.set(__self__, "developer_provider_name", developer_provider_name)
        if identity_pool_name is not None:
            pulumi.set(__self__, "identity_pool_name", identity_pool_name)
        if identity_pool_tags is not None:
            pulumi.set(__self__, "identity_pool_tags", identity_pool_tags)
        if open_id_connect_provider_arns is not None:
            pulumi.set(__self__, "open_id_connect_provider_arns", open_id_connect_provider_arns)
        if push_sync is not None:
            pulumi.set(__self__, "push_sync", push_sync)
        if saml_provider_arns is not None:
            pulumi.set(__self__, "saml_provider_arns", saml_provider_arns)
        if supported_login_providers is not None:
            pulumi.set(__self__, "supported_login_providers", supported_login_providers)

    @property
    @pulumi.getter(name="allowUnauthenticatedIdentities")
    def allow_unauthenticated_identities(self) -> pulumi.Input[bool]:
        """
        Specifies whether the identity pool supports unauthenticated logins.
        """
        return pulumi.get(self, "allow_unauthenticated_identities")

    @allow_unauthenticated_identities.setter
    def allow_unauthenticated_identities(self, value: pulumi.Input[bool]):
        pulumi.set(self, "allow_unauthenticated_identities", value)

    @property
    @pulumi.getter(name="allowClassicFlow")
    def allow_classic_flow(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables the Basic (Classic) authentication flow.
        """
        return pulumi.get(self, "allow_classic_flow")

    @allow_classic_flow.setter
    def allow_classic_flow(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_classic_flow", value)

    @property
    @pulumi.getter(name="cognitoEvents")
    def cognito_events(self) -> Optional[Any]:
        """
        The events to configure.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Cognito::IdentityPool` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "cognito_events")

    @cognito_events.setter
    def cognito_events(self, value: Optional[Any]):
        pulumi.set(self, "cognito_events", value)

    @property
    @pulumi.getter(name="cognitoIdentityProviders")
    def cognito_identity_providers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IdentityPoolCognitoIdentityProviderArgs']]]]:
        """
        The Amazon Cognito user pools and their client IDs.
        """
        return pulumi.get(self, "cognito_identity_providers")

    @cognito_identity_providers.setter
    def cognito_identity_providers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IdentityPoolCognitoIdentityProviderArgs']]]]):
        pulumi.set(self, "cognito_identity_providers", value)

    @property
    @pulumi.getter(name="cognitoStreams")
    def cognito_streams(self) -> Optional[pulumi.Input['IdentityPoolCognitoStreamsArgs']]:
        """
        Configuration options for configuring Amazon Cognito streams.
        """
        return pulumi.get(self, "cognito_streams")

    @cognito_streams.setter
    def cognito_streams(self, value: Optional[pulumi.Input['IdentityPoolCognitoStreamsArgs']]):
        pulumi.set(self, "cognito_streams", value)

    @property
    @pulumi.getter(name="developerProviderName")
    def developer_provider_name(self) -> Optional[pulumi.Input[str]]:
        """
        The "domain" Amazon Cognito uses when referencing your users. This name acts as a placeholder that allows your backend and the Amazon Cognito service to communicate about the developer provider. For the `DeveloperProviderName` , you can use letters and periods (.), underscores (_), and dashes (-).

        *Minimum length* : 1

        *Maximum length* : 100
        """
        return pulumi.get(self, "developer_provider_name")

    @developer_provider_name.setter
    def developer_provider_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "developer_provider_name", value)

    @property
    @pulumi.getter(name="identityPoolName")
    def identity_pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of your Amazon Cognito identity pool.

        *Minimum length* : 1

        *Maximum length* : 128

        *Pattern* : `[\\w\\s+=,.@-]+`
        """
        return pulumi.get(self, "identity_pool_name")

    @identity_pool_name.setter
    def identity_pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_pool_name", value)

    @property
    @pulumi.getter(name="identityPoolTags")
    def identity_pool_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "identity_pool_tags")

    @identity_pool_tags.setter
    def identity_pool_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "identity_pool_tags", value)

    @property
    @pulumi.getter(name="openIdConnectProviderArns")
    def open_id_connect_provider_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The Amazon Resource Names (ARNs) of the OpenID connect providers.
        """
        return pulumi.get(self, "open_id_connect_provider_arns")

    @open_id_connect_provider_arns.setter
    def open_id_connect_provider_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "open_id_connect_provider_arns", value)

    @property
    @pulumi.getter(name="pushSync")
    def push_sync(self) -> Optional[pulumi.Input['IdentityPoolPushSyncArgs']]:
        """
        The configuration options to be applied to the identity pool.
        """
        return pulumi.get(self, "push_sync")

    @push_sync.setter
    def push_sync(self, value: Optional[pulumi.Input['IdentityPoolPushSyncArgs']]):
        pulumi.set(self, "push_sync", value)

    @property
    @pulumi.getter(name="samlProviderArns")
    def saml_provider_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The Amazon Resource Names (ARNs) of the Security Assertion Markup Language (SAML) providers.
        """
        return pulumi.get(self, "saml_provider_arns")

    @saml_provider_arns.setter
    def saml_provider_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "saml_provider_arns", value)

    @property
    @pulumi.getter(name="supportedLoginProviders")
    def supported_login_providers(self) -> Optional[Any]:
        """
        Key-value pairs that map provider names to provider app IDs.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Cognito::IdentityPool` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "supported_login_providers")

    @supported_login_providers.setter
    def supported_login_providers(self, value: Optional[Any]):
        pulumi.set(self, "supported_login_providers", value)


class IdentityPool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_classic_flow: Optional[pulumi.Input[bool]] = None,
                 allow_unauthenticated_identities: Optional[pulumi.Input[bool]] = None,
                 cognito_events: Optional[Any] = None,
                 cognito_identity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[Union['IdentityPoolCognitoIdentityProviderArgs', 'IdentityPoolCognitoIdentityProviderArgsDict']]]]] = None,
                 cognito_streams: Optional[pulumi.Input[Union['IdentityPoolCognitoStreamsArgs', 'IdentityPoolCognitoStreamsArgsDict']]] = None,
                 developer_provider_name: Optional[pulumi.Input[str]] = None,
                 identity_pool_name: Optional[pulumi.Input[str]] = None,
                 identity_pool_tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 open_id_connect_provider_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 push_sync: Optional[pulumi.Input[Union['IdentityPoolPushSyncArgs', 'IdentityPoolPushSyncArgsDict']]] = None,
                 saml_provider_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 supported_login_providers: Optional[Any] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Cognito::IdentityPool

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_classic_flow: Enables the Basic (Classic) authentication flow.
        :param pulumi.Input[bool] allow_unauthenticated_identities: Specifies whether the identity pool supports unauthenticated logins.
        :param Any cognito_events: The events to configure.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Cognito::IdentityPool` for more information about the expected schema for this property.
        :param pulumi.Input[Sequence[pulumi.Input[Union['IdentityPoolCognitoIdentityProviderArgs', 'IdentityPoolCognitoIdentityProviderArgsDict']]]] cognito_identity_providers: The Amazon Cognito user pools and their client IDs.
        :param pulumi.Input[Union['IdentityPoolCognitoStreamsArgs', 'IdentityPoolCognitoStreamsArgsDict']] cognito_streams: Configuration options for configuring Amazon Cognito streams.
        :param pulumi.Input[str] developer_provider_name: The "domain" Amazon Cognito uses when referencing your users. This name acts as a placeholder that allows your backend and the Amazon Cognito service to communicate about the developer provider. For the `DeveloperProviderName` , you can use letters and periods (.), underscores (_), and dashes (-).
               
               *Minimum length* : 1
               
               *Maximum length* : 100
        :param pulumi.Input[str] identity_pool_name: The name of your Amazon Cognito identity pool.
               
               *Minimum length* : 1
               
               *Maximum length* : 128
               
               *Pattern* : `[\\w\\s+=,.@-]+`
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] identity_pool_tags: An array of key-value pairs to apply to this resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] open_id_connect_provider_arns: The Amazon Resource Names (ARNs) of the OpenID connect providers.
        :param pulumi.Input[Union['IdentityPoolPushSyncArgs', 'IdentityPoolPushSyncArgsDict']] push_sync: The configuration options to be applied to the identity pool.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] saml_provider_arns: The Amazon Resource Names (ARNs) of the Security Assertion Markup Language (SAML) providers.
        :param Any supported_login_providers: Key-value pairs that map provider names to provider app IDs.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Cognito::IdentityPool` for more information about the expected schema for this property.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IdentityPoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Cognito::IdentityPool

        :param str resource_name: The name of the resource.
        :param IdentityPoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IdentityPoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_classic_flow: Optional[pulumi.Input[bool]] = None,
                 allow_unauthenticated_identities: Optional[pulumi.Input[bool]] = None,
                 cognito_events: Optional[Any] = None,
                 cognito_identity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[Union['IdentityPoolCognitoIdentityProviderArgs', 'IdentityPoolCognitoIdentityProviderArgsDict']]]]] = None,
                 cognito_streams: Optional[pulumi.Input[Union['IdentityPoolCognitoStreamsArgs', 'IdentityPoolCognitoStreamsArgsDict']]] = None,
                 developer_provider_name: Optional[pulumi.Input[str]] = None,
                 identity_pool_name: Optional[pulumi.Input[str]] = None,
                 identity_pool_tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 open_id_connect_provider_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 push_sync: Optional[pulumi.Input[Union['IdentityPoolPushSyncArgs', 'IdentityPoolPushSyncArgsDict']]] = None,
                 saml_provider_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 supported_login_providers: Optional[Any] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IdentityPoolArgs.__new__(IdentityPoolArgs)

            __props__.__dict__["allow_classic_flow"] = allow_classic_flow
            if allow_unauthenticated_identities is None and not opts.urn:
                raise TypeError("Missing required property 'allow_unauthenticated_identities'")
            __props__.__dict__["allow_unauthenticated_identities"] = allow_unauthenticated_identities
            __props__.__dict__["cognito_events"] = cognito_events
            __props__.__dict__["cognito_identity_providers"] = cognito_identity_providers
            __props__.__dict__["cognito_streams"] = cognito_streams
            __props__.__dict__["developer_provider_name"] = developer_provider_name
            __props__.__dict__["identity_pool_name"] = identity_pool_name
            __props__.__dict__["identity_pool_tags"] = identity_pool_tags
            __props__.__dict__["open_id_connect_provider_arns"] = open_id_connect_provider_arns
            __props__.__dict__["push_sync"] = push_sync
            __props__.__dict__["saml_provider_arns"] = saml_provider_arns
            __props__.__dict__["supported_login_providers"] = supported_login_providers
            __props__.__dict__["aws_id"] = None
            __props__.__dict__["name"] = None
        super(IdentityPool, __self__).__init__(
            'aws-native:cognito:IdentityPool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'IdentityPool':
        """
        Get an existing IdentityPool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = IdentityPoolArgs.__new__(IdentityPoolArgs)

        __props__.__dict__["allow_classic_flow"] = None
        __props__.__dict__["allow_unauthenticated_identities"] = None
        __props__.__dict__["aws_id"] = None
        __props__.__dict__["cognito_events"] = None
        __props__.__dict__["cognito_identity_providers"] = None
        __props__.__dict__["cognito_streams"] = None
        __props__.__dict__["developer_provider_name"] = None
        __props__.__dict__["identity_pool_name"] = None
        __props__.__dict__["identity_pool_tags"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["open_id_connect_provider_arns"] = None
        __props__.__dict__["push_sync"] = None
        __props__.__dict__["saml_provider_arns"] = None
        __props__.__dict__["supported_login_providers"] = None
        return IdentityPool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowClassicFlow")
    def allow_classic_flow(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables the Basic (Classic) authentication flow.
        """
        return pulumi.get(self, "allow_classic_flow")

    @property
    @pulumi.getter(name="allowUnauthenticatedIdentities")
    def allow_unauthenticated_identities(self) -> pulumi.Output[bool]:
        """
        Specifies whether the identity pool supports unauthenticated logins.
        """
        return pulumi.get(self, "allow_unauthenticated_identities")

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter(name="cognitoEvents")
    def cognito_events(self) -> pulumi.Output[Optional[Any]]:
        """
        The events to configure.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Cognito::IdentityPool` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "cognito_events")

    @property
    @pulumi.getter(name="cognitoIdentityProviders")
    def cognito_identity_providers(self) -> pulumi.Output[Optional[Sequence['outputs.IdentityPoolCognitoIdentityProvider']]]:
        """
        The Amazon Cognito user pools and their client IDs.
        """
        return pulumi.get(self, "cognito_identity_providers")

    @property
    @pulumi.getter(name="cognitoStreams")
    def cognito_streams(self) -> pulumi.Output[Optional['outputs.IdentityPoolCognitoStreams']]:
        """
        Configuration options for configuring Amazon Cognito streams.
        """
        return pulumi.get(self, "cognito_streams")

    @property
    @pulumi.getter(name="developerProviderName")
    def developer_provider_name(self) -> pulumi.Output[Optional[str]]:
        """
        The "domain" Amazon Cognito uses when referencing your users. This name acts as a placeholder that allows your backend and the Amazon Cognito service to communicate about the developer provider. For the `DeveloperProviderName` , you can use letters and periods (.), underscores (_), and dashes (-).

        *Minimum length* : 1

        *Maximum length* : 100
        """
        return pulumi.get(self, "developer_provider_name")

    @property
    @pulumi.getter(name="identityPoolName")
    def identity_pool_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of your Amazon Cognito identity pool.

        *Minimum length* : 1

        *Maximum length* : 128

        *Pattern* : `[\\w\\s+=,.@-]+`
        """
        return pulumi.get(self, "identity_pool_name")

    @property
    @pulumi.getter(name="identityPoolTags")
    def identity_pool_tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "identity_pool_tags")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Amazon Cognito identity pool, returned as a string.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="openIdConnectProviderArns")
    def open_id_connect_provider_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The Amazon Resource Names (ARNs) of the OpenID connect providers.
        """
        return pulumi.get(self, "open_id_connect_provider_arns")

    @property
    @pulumi.getter(name="pushSync")
    def push_sync(self) -> pulumi.Output[Optional['outputs.IdentityPoolPushSync']]:
        """
        The configuration options to be applied to the identity pool.
        """
        return pulumi.get(self, "push_sync")

    @property
    @pulumi.getter(name="samlProviderArns")
    def saml_provider_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The Amazon Resource Names (ARNs) of the Security Assertion Markup Language (SAML) providers.
        """
        return pulumi.get(self, "saml_provider_arns")

    @property
    @pulumi.getter(name="supportedLoginProviders")
    def supported_login_providers(self) -> pulumi.Output[Optional[Any]]:
        """
        Key-value pairs that map provider names to provider app IDs.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Cognito::IdentityPool` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "supported_login_providers")

