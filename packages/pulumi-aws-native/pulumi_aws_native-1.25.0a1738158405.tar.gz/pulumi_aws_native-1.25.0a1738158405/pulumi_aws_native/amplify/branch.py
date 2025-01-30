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
from ._enums import *
from ._inputs import *

__all__ = ['BranchArgs', 'Branch']

@pulumi.input_type
class BranchArgs:
    def __init__(__self__, *,
                 app_id: pulumi.Input[str],
                 backend: Optional[pulumi.Input['BranchBackendArgs']] = None,
                 basic_auth_config: Optional[pulumi.Input['BranchBasicAuthConfigArgs']] = None,
                 branch_name: Optional[pulumi.Input[str]] = None,
                 build_spec: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enable_auto_build: Optional[pulumi.Input[bool]] = None,
                 enable_performance_mode: Optional[pulumi.Input[bool]] = None,
                 enable_pull_request_preview: Optional[pulumi.Input[bool]] = None,
                 environment_variables: Optional[pulumi.Input[Sequence[pulumi.Input['BranchEnvironmentVariableArgs']]]] = None,
                 framework: Optional[pulumi.Input[str]] = None,
                 pull_request_environment_name: Optional[pulumi.Input[str]] = None,
                 stage: Optional[pulumi.Input['BranchStage']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Branch resource.
        :param pulumi.Input[str] app_id: The unique ID for an Amplify app.
        :param pulumi.Input['BranchBackendArgs'] backend: The backend for a `Branch` of an Amplify app. Use for a backend created from an AWS CloudFormation stack.
               
               This field is available to Amplify Gen 2 apps only. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code.
        :param pulumi.Input['BranchBasicAuthConfigArgs'] basic_auth_config: The basic authorization credentials for a branch of an Amplify app. You must base64-encode the authorization credentials and provide them in the format `user:password` .
        :param pulumi.Input[str] branch_name: The name for the branch.
        :param pulumi.Input[str] build_spec: The build specification (build spec) for the branch.
        :param pulumi.Input[str] description: The description for the branch that is part of an Amplify app.
        :param pulumi.Input[bool] enable_auto_build: Enables auto building for the branch.
        :param pulumi.Input[bool] enable_performance_mode: Enables performance mode for the branch.
               
               Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        :param pulumi.Input[bool] enable_pull_request_preview: Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.
               
               To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the `PullRequestEnvironmentName` property.
               
               For more information, see [Web Previews](https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html) in the *AWS Amplify Hosting User Guide* .
        :param pulumi.Input[Sequence[pulumi.Input['BranchEnvironmentVariableArgs']]] environment_variables: The environment variables for the branch.
        :param pulumi.Input[str] framework: The framework for the branch.
        :param pulumi.Input[str] pull_request_environment_name: If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named `prod` , `test` , or `dev` that you initialized with the Amplify CLI and mapped to this branch.
               
               To enable pull request previews, set the `EnablePullRequestPreview` property to `true` .
               
               If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.
               
               For more information about creating backend environments, see [Feature Branch Deployments and Team Workflows](https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html) in the *AWS Amplify Hosting User Guide* .
        :param pulumi.Input['BranchStage'] stage: Describes the current stage for the branch.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tag for the branch.
        """
        pulumi.set(__self__, "app_id", app_id)
        if backend is not None:
            pulumi.set(__self__, "backend", backend)
        if basic_auth_config is not None:
            pulumi.set(__self__, "basic_auth_config", basic_auth_config)
        if branch_name is not None:
            pulumi.set(__self__, "branch_name", branch_name)
        if build_spec is not None:
            pulumi.set(__self__, "build_spec", build_spec)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enable_auto_build is not None:
            pulumi.set(__self__, "enable_auto_build", enable_auto_build)
        if enable_performance_mode is not None:
            pulumi.set(__self__, "enable_performance_mode", enable_performance_mode)
        if enable_pull_request_preview is not None:
            pulumi.set(__self__, "enable_pull_request_preview", enable_pull_request_preview)
        if environment_variables is not None:
            pulumi.set(__self__, "environment_variables", environment_variables)
        if framework is not None:
            pulumi.set(__self__, "framework", framework)
        if pull_request_environment_name is not None:
            pulumi.set(__self__, "pull_request_environment_name", pull_request_environment_name)
        if stage is not None:
            pulumi.set(__self__, "stage", stage)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Input[str]:
        """
        The unique ID for an Amplify app.
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter
    def backend(self) -> Optional[pulumi.Input['BranchBackendArgs']]:
        """
        The backend for a `Branch` of an Amplify app. Use for a backend created from an AWS CloudFormation stack.

        This field is available to Amplify Gen 2 apps only. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code.
        """
        return pulumi.get(self, "backend")

    @backend.setter
    def backend(self, value: Optional[pulumi.Input['BranchBackendArgs']]):
        pulumi.set(self, "backend", value)

    @property
    @pulumi.getter(name="basicAuthConfig")
    def basic_auth_config(self) -> Optional[pulumi.Input['BranchBasicAuthConfigArgs']]:
        """
        The basic authorization credentials for a branch of an Amplify app. You must base64-encode the authorization credentials and provide them in the format `user:password` .
        """
        return pulumi.get(self, "basic_auth_config")

    @basic_auth_config.setter
    def basic_auth_config(self, value: Optional[pulumi.Input['BranchBasicAuthConfigArgs']]):
        pulumi.set(self, "basic_auth_config", value)

    @property
    @pulumi.getter(name="branchName")
    def branch_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the branch.
        """
        return pulumi.get(self, "branch_name")

    @branch_name.setter
    def branch_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "branch_name", value)

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> Optional[pulumi.Input[str]]:
        """
        The build specification (build spec) for the branch.
        """
        return pulumi.get(self, "build_spec")

    @build_spec.setter
    def build_spec(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "build_spec", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description for the branch that is part of an Amplify app.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="enableAutoBuild")
    def enable_auto_build(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables auto building for the branch.
        """
        return pulumi.get(self, "enable_auto_build")

    @enable_auto_build.setter
    def enable_auto_build(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_auto_build", value)

    @property
    @pulumi.getter(name="enablePerformanceMode")
    def enable_performance_mode(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        """
        return pulumi.get(self, "enable_performance_mode")

    @enable_performance_mode.setter
    def enable_performance_mode(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_performance_mode", value)

    @property
    @pulumi.getter(name="enablePullRequestPreview")
    def enable_pull_request_preview(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

        To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the `PullRequestEnvironmentName` property.

        For more information, see [Web Previews](https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html) in the *AWS Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "enable_pull_request_preview")

    @enable_pull_request_preview.setter
    def enable_pull_request_preview(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_pull_request_preview", value)

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BranchEnvironmentVariableArgs']]]]:
        """
        The environment variables for the branch.
        """
        return pulumi.get(self, "environment_variables")

    @environment_variables.setter
    def environment_variables(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BranchEnvironmentVariableArgs']]]]):
        pulumi.set(self, "environment_variables", value)

    @property
    @pulumi.getter
    def framework(self) -> Optional[pulumi.Input[str]]:
        """
        The framework for the branch.
        """
        return pulumi.get(self, "framework")

    @framework.setter
    def framework(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "framework", value)

    @property
    @pulumi.getter(name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> Optional[pulumi.Input[str]]:
        """
        If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named `prod` , `test` , or `dev` that you initialized with the Amplify CLI and mapped to this branch.

        To enable pull request previews, set the `EnablePullRequestPreview` property to `true` .

        If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.

        For more information about creating backend environments, see [Feature Branch Deployments and Team Workflows](https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html) in the *AWS Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "pull_request_environment_name")

    @pull_request_environment_name.setter
    def pull_request_environment_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pull_request_environment_name", value)

    @property
    @pulumi.getter
    def stage(self) -> Optional[pulumi.Input['BranchStage']]:
        """
        Describes the current stage for the branch.
        """
        return pulumi.get(self, "stage")

    @stage.setter
    def stage(self, value: Optional[pulumi.Input['BranchStage']]):
        pulumi.set(self, "stage", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tag for the branch.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Branch(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 backend: Optional[pulumi.Input[Union['BranchBackendArgs', 'BranchBackendArgsDict']]] = None,
                 basic_auth_config: Optional[pulumi.Input[Union['BranchBasicAuthConfigArgs', 'BranchBasicAuthConfigArgsDict']]] = None,
                 branch_name: Optional[pulumi.Input[str]] = None,
                 build_spec: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enable_auto_build: Optional[pulumi.Input[bool]] = None,
                 enable_performance_mode: Optional[pulumi.Input[bool]] = None,
                 enable_pull_request_preview: Optional[pulumi.Input[bool]] = None,
                 environment_variables: Optional[pulumi.Input[Sequence[pulumi.Input[Union['BranchEnvironmentVariableArgs', 'BranchEnvironmentVariableArgsDict']]]]] = None,
                 framework: Optional[pulumi.Input[str]] = None,
                 pull_request_environment_name: Optional[pulumi.Input[str]] = None,
                 stage: Optional[pulumi.Input['BranchStage']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        The AWS::Amplify::Branch resource creates a new branch within an app.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_id: The unique ID for an Amplify app.
        :param pulumi.Input[Union['BranchBackendArgs', 'BranchBackendArgsDict']] backend: The backend for a `Branch` of an Amplify app. Use for a backend created from an AWS CloudFormation stack.
               
               This field is available to Amplify Gen 2 apps only. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code.
        :param pulumi.Input[Union['BranchBasicAuthConfigArgs', 'BranchBasicAuthConfigArgsDict']] basic_auth_config: The basic authorization credentials for a branch of an Amplify app. You must base64-encode the authorization credentials and provide them in the format `user:password` .
        :param pulumi.Input[str] branch_name: The name for the branch.
        :param pulumi.Input[str] build_spec: The build specification (build spec) for the branch.
        :param pulumi.Input[str] description: The description for the branch that is part of an Amplify app.
        :param pulumi.Input[bool] enable_auto_build: Enables auto building for the branch.
        :param pulumi.Input[bool] enable_performance_mode: Enables performance mode for the branch.
               
               Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        :param pulumi.Input[bool] enable_pull_request_preview: Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.
               
               To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the `PullRequestEnvironmentName` property.
               
               For more information, see [Web Previews](https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html) in the *AWS Amplify Hosting User Guide* .
        :param pulumi.Input[Sequence[pulumi.Input[Union['BranchEnvironmentVariableArgs', 'BranchEnvironmentVariableArgsDict']]]] environment_variables: The environment variables for the branch.
        :param pulumi.Input[str] framework: The framework for the branch.
        :param pulumi.Input[str] pull_request_environment_name: If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named `prod` , `test` , or `dev` that you initialized with the Amplify CLI and mapped to this branch.
               
               To enable pull request previews, set the `EnablePullRequestPreview` property to `true` .
               
               If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.
               
               For more information about creating backend environments, see [Feature Branch Deployments and Team Workflows](https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html) in the *AWS Amplify Hosting User Guide* .
        :param pulumi.Input['BranchStage'] stage: Describes the current stage for the branch.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tag for the branch.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BranchArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::Amplify::Branch resource creates a new branch within an app.

        :param str resource_name: The name of the resource.
        :param BranchArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BranchArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 backend: Optional[pulumi.Input[Union['BranchBackendArgs', 'BranchBackendArgsDict']]] = None,
                 basic_auth_config: Optional[pulumi.Input[Union['BranchBasicAuthConfigArgs', 'BranchBasicAuthConfigArgsDict']]] = None,
                 branch_name: Optional[pulumi.Input[str]] = None,
                 build_spec: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enable_auto_build: Optional[pulumi.Input[bool]] = None,
                 enable_performance_mode: Optional[pulumi.Input[bool]] = None,
                 enable_pull_request_preview: Optional[pulumi.Input[bool]] = None,
                 environment_variables: Optional[pulumi.Input[Sequence[pulumi.Input[Union['BranchEnvironmentVariableArgs', 'BranchEnvironmentVariableArgsDict']]]]] = None,
                 framework: Optional[pulumi.Input[str]] = None,
                 pull_request_environment_name: Optional[pulumi.Input[str]] = None,
                 stage: Optional[pulumi.Input['BranchStage']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BranchArgs.__new__(BranchArgs)

            if app_id is None and not opts.urn:
                raise TypeError("Missing required property 'app_id'")
            __props__.__dict__["app_id"] = app_id
            __props__.__dict__["backend"] = backend
            __props__.__dict__["basic_auth_config"] = basic_auth_config
            __props__.__dict__["branch_name"] = branch_name
            __props__.__dict__["build_spec"] = build_spec
            __props__.__dict__["description"] = description
            __props__.__dict__["enable_auto_build"] = enable_auto_build
            __props__.__dict__["enable_performance_mode"] = enable_performance_mode
            __props__.__dict__["enable_pull_request_preview"] = enable_pull_request_preview
            __props__.__dict__["environment_variables"] = environment_variables
            __props__.__dict__["framework"] = framework
            __props__.__dict__["pull_request_environment_name"] = pull_request_environment_name
            __props__.__dict__["stage"] = stage
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["appId", "branchName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Branch, __self__).__init__(
            'aws-native:amplify:Branch',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Branch':
        """
        Get an existing Branch resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BranchArgs.__new__(BranchArgs)

        __props__.__dict__["app_id"] = None
        __props__.__dict__["arn"] = None
        __props__.__dict__["backend"] = None
        __props__.__dict__["basic_auth_config"] = None
        __props__.__dict__["branch_name"] = None
        __props__.__dict__["build_spec"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["enable_auto_build"] = None
        __props__.__dict__["enable_performance_mode"] = None
        __props__.__dict__["enable_pull_request_preview"] = None
        __props__.__dict__["environment_variables"] = None
        __props__.__dict__["framework"] = None
        __props__.__dict__["pull_request_environment_name"] = None
        __props__.__dict__["stage"] = None
        __props__.__dict__["tags"] = None
        return Branch(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Output[str]:
        """
        The unique ID for an Amplify app.
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN for a branch, part of an Amplify App.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def backend(self) -> pulumi.Output[Optional['outputs.BranchBackend']]:
        """
        The backend for a `Branch` of an Amplify app. Use for a backend created from an AWS CloudFormation stack.

        This field is available to Amplify Gen 2 apps only. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code.
        """
        return pulumi.get(self, "backend")

    @property
    @pulumi.getter(name="basicAuthConfig")
    def basic_auth_config(self) -> pulumi.Output[Optional['outputs.BranchBasicAuthConfig']]:
        """
        The basic authorization credentials for a branch of an Amplify app. You must base64-encode the authorization credentials and provide them in the format `user:password` .
        """
        return pulumi.get(self, "basic_auth_config")

    @property
    @pulumi.getter(name="branchName")
    def branch_name(self) -> pulumi.Output[str]:
        """
        The name for the branch.
        """
        return pulumi.get(self, "branch_name")

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> pulumi.Output[Optional[str]]:
        """
        The build specification (build spec) for the branch.
        """
        return pulumi.get(self, "build_spec")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description for the branch that is part of an Amplify app.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enableAutoBuild")
    def enable_auto_build(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables auto building for the branch.
        """
        return pulumi.get(self, "enable_auto_build")

    @property
    @pulumi.getter(name="enablePerformanceMode")
    def enable_performance_mode(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        """
        return pulumi.get(self, "enable_performance_mode")

    @property
    @pulumi.getter(name="enablePullRequestPreview")
    def enable_pull_request_preview(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

        To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the `PullRequestEnvironmentName` property.

        For more information, see [Web Previews](https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html) in the *AWS Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "enable_pull_request_preview")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> pulumi.Output[Optional[Sequence['outputs.BranchEnvironmentVariable']]]:
        """
        The environment variables for the branch.
        """
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter
    def framework(self) -> pulumi.Output[Optional[str]]:
        """
        The framework for the branch.
        """
        return pulumi.get(self, "framework")

    @property
    @pulumi.getter(name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> pulumi.Output[Optional[str]]:
        """
        If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named `prod` , `test` , or `dev` that you initialized with the Amplify CLI and mapped to this branch.

        To enable pull request previews, set the `EnablePullRequestPreview` property to `true` .

        If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.

        For more information about creating backend environments, see [Feature Branch Deployments and Team Workflows](https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html) in the *AWS Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "pull_request_environment_name")

    @property
    @pulumi.getter
    def stage(self) -> pulumi.Output[Optional['BranchStage']]:
        """
        Describes the current stage for the branch.
        """
        return pulumi.get(self, "stage")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tag for the branch.
        """
        return pulumi.get(self, "tags")

