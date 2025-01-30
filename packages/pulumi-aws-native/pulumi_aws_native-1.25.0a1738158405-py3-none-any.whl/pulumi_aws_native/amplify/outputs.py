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
from ._enums import *

__all__ = [
    'AppAutoBranchCreationConfig',
    'AppBasicAuthConfig',
    'AppCacheConfig',
    'AppCustomRule',
    'AppEnvironmentVariable',
    'BranchBackend',
    'BranchBasicAuthConfig',
    'BranchEnvironmentVariable',
    'DomainCertificate',
    'DomainCertificateSettings',
    'DomainSubDomainSetting',
]

@pulumi.output_type
class AppAutoBranchCreationConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoBranchCreationPatterns":
            suggest = "auto_branch_creation_patterns"
        elif key == "basicAuthConfig":
            suggest = "basic_auth_config"
        elif key == "buildSpec":
            suggest = "build_spec"
        elif key == "enableAutoBranchCreation":
            suggest = "enable_auto_branch_creation"
        elif key == "enableAutoBuild":
            suggest = "enable_auto_build"
        elif key == "enablePerformanceMode":
            suggest = "enable_performance_mode"
        elif key == "enablePullRequestPreview":
            suggest = "enable_pull_request_preview"
        elif key == "environmentVariables":
            suggest = "environment_variables"
        elif key == "pullRequestEnvironmentName":
            suggest = "pull_request_environment_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AppAutoBranchCreationConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AppAutoBranchCreationConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AppAutoBranchCreationConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_branch_creation_patterns: Optional[Sequence[str]] = None,
                 basic_auth_config: Optional['outputs.AppBasicAuthConfig'] = None,
                 build_spec: Optional[str] = None,
                 enable_auto_branch_creation: Optional[bool] = None,
                 enable_auto_build: Optional[bool] = None,
                 enable_performance_mode: Optional[bool] = None,
                 enable_pull_request_preview: Optional[bool] = None,
                 environment_variables: Optional[Sequence['outputs.AppEnvironmentVariable']] = None,
                 framework: Optional[str] = None,
                 pull_request_environment_name: Optional[str] = None,
                 stage: Optional['AppAutoBranchCreationConfigStage'] = None):
        """
        :param Sequence[str] auto_branch_creation_patterns: Automated branch creation glob patterns for the Amplify app.
        :param 'AppBasicAuthConfig' basic_auth_config: Sets password protection for your auto created branch.
        :param str build_spec: The build specification (build spec) for the autocreated branch.
        :param bool enable_auto_branch_creation: Enables automated branch creation for the Amplify app.
        :param bool enable_auto_build: Enables auto building for the auto created branch.
        :param bool enable_performance_mode: Enables performance mode for the branch.
               
               Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        :param bool enable_pull_request_preview: Sets whether pull request previews are enabled for each branch that Amplify Hosting automatically creates for your app. Amplify creates previews by deploying your app to a unique URL whenever a pull request is opened for the branch. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.
               
               To provide backend support for your preview, Amplify Hosting automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the `PullRequestEnvironmentName` property.
               
               For more information, see [Web Previews](https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html) in the *AWS Amplify Hosting User Guide* .
        :param Sequence['AppEnvironmentVariable'] environment_variables: The environment variables for the autocreated branch.
        :param str framework: The framework for the autocreated branch.
        :param str pull_request_environment_name: If pull request previews are enabled, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named `prod` , `test` , or `dev` that you initialized with the Amplify CLI.
               
               To enable pull request previews, set the `EnablePullRequestPreview` property to `true` .
               
               If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify deletes this environment when the pull request is closed.
               
               For more information about creating backend environments, see [Feature Branch Deployments and Team Workflows](https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html) in the *AWS Amplify Hosting User Guide* .
        :param 'AppAutoBranchCreationConfigStage' stage: Stage for the auto created branch.
        """
        if auto_branch_creation_patterns is not None:
            pulumi.set(__self__, "auto_branch_creation_patterns", auto_branch_creation_patterns)
        if basic_auth_config is not None:
            pulumi.set(__self__, "basic_auth_config", basic_auth_config)
        if build_spec is not None:
            pulumi.set(__self__, "build_spec", build_spec)
        if enable_auto_branch_creation is not None:
            pulumi.set(__self__, "enable_auto_branch_creation", enable_auto_branch_creation)
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

    @property
    @pulumi.getter(name="autoBranchCreationPatterns")
    def auto_branch_creation_patterns(self) -> Optional[Sequence[str]]:
        """
        Automated branch creation glob patterns for the Amplify app.
        """
        return pulumi.get(self, "auto_branch_creation_patterns")

    @property
    @pulumi.getter(name="basicAuthConfig")
    def basic_auth_config(self) -> Optional['outputs.AppBasicAuthConfig']:
        """
        Sets password protection for your auto created branch.
        """
        return pulumi.get(self, "basic_auth_config")

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> Optional[str]:
        """
        The build specification (build spec) for the autocreated branch.
        """
        return pulumi.get(self, "build_spec")

    @property
    @pulumi.getter(name="enableAutoBranchCreation")
    def enable_auto_branch_creation(self) -> Optional[bool]:
        """
        Enables automated branch creation for the Amplify app.
        """
        return pulumi.get(self, "enable_auto_branch_creation")

    @property
    @pulumi.getter(name="enableAutoBuild")
    def enable_auto_build(self) -> Optional[bool]:
        """
        Enables auto building for the auto created branch.
        """
        return pulumi.get(self, "enable_auto_build")

    @property
    @pulumi.getter(name="enablePerformanceMode")
    def enable_performance_mode(self) -> Optional[bool]:
        """
        Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        """
        return pulumi.get(self, "enable_performance_mode")

    @property
    @pulumi.getter(name="enablePullRequestPreview")
    def enable_pull_request_preview(self) -> Optional[bool]:
        """
        Sets whether pull request previews are enabled for each branch that Amplify Hosting automatically creates for your app. Amplify creates previews by deploying your app to a unique URL whenever a pull request is opened for the branch. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

        To provide backend support for your preview, Amplify Hosting automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the `PullRequestEnvironmentName` property.

        For more information, see [Web Previews](https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html) in the *AWS Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "enable_pull_request_preview")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[Sequence['outputs.AppEnvironmentVariable']]:
        """
        The environment variables for the autocreated branch.
        """
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter
    def framework(self) -> Optional[str]:
        """
        The framework for the autocreated branch.
        """
        return pulumi.get(self, "framework")

    @property
    @pulumi.getter(name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> Optional[str]:
        """
        If pull request previews are enabled, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named `prod` , `test` , or `dev` that you initialized with the Amplify CLI.

        To enable pull request previews, set the `EnablePullRequestPreview` property to `true` .

        If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify deletes this environment when the pull request is closed.

        For more information about creating backend environments, see [Feature Branch Deployments and Team Workflows](https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html) in the *AWS Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "pull_request_environment_name")

    @property
    @pulumi.getter
    def stage(self) -> Optional['AppAutoBranchCreationConfigStage']:
        """
        Stage for the auto created branch.
        """
        return pulumi.get(self, "stage")


@pulumi.output_type
class AppBasicAuthConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "enableBasicAuth":
            suggest = "enable_basic_auth"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AppBasicAuthConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AppBasicAuthConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AppBasicAuthConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enable_basic_auth: Optional[bool] = None,
                 password: Optional[str] = None,
                 username: Optional[str] = None):
        """
        :param bool enable_basic_auth: Enables basic authorization for the Amplify app's branches.
        :param str password: The password for basic authorization.
        :param str username: The user name for basic authorization.
        """
        if enable_basic_auth is not None:
            pulumi.set(__self__, "enable_basic_auth", enable_basic_auth)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="enableBasicAuth")
    def enable_basic_auth(self) -> Optional[bool]:
        """
        Enables basic authorization for the Amplify app's branches.
        """
        return pulumi.get(self, "enable_basic_auth")

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        The password for basic authorization.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        The user name for basic authorization.
        """
        return pulumi.get(self, "username")


@pulumi.output_type
class AppCacheConfig(dict):
    def __init__(__self__, *,
                 type: Optional['AppCacheConfigType'] = None):
        """
        :param 'AppCacheConfigType' type: The type of cache configuration to use for an Amplify app.
               
               The `AMPLIFY_MANAGED` cache configuration automatically applies an optimized cache configuration for your app based on its platform, routing rules, and rewrite rules. This is the default setting.
               
               The `AMPLIFY_MANAGED_NO_COOKIES` cache configuration type is the same as `AMPLIFY_MANAGED` , except that it excludes all cookies from the cache key.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional['AppCacheConfigType']:
        """
        The type of cache configuration to use for an Amplify app.

        The `AMPLIFY_MANAGED` cache configuration automatically applies an optimized cache configuration for your app based on its platform, routing rules, and rewrite rules. This is the default setting.

        The `AMPLIFY_MANAGED_NO_COOKIES` cache configuration type is the same as `AMPLIFY_MANAGED` , except that it excludes all cookies from the cache key.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class AppCustomRule(dict):
    def __init__(__self__, *,
                 source: str,
                 target: str,
                 condition: Optional[str] = None,
                 status: Optional[str] = None):
        """
        :param str source: The source pattern for a URL rewrite or redirect rule.
        :param str target: The target pattern for a URL rewrite or redirect rule.
        :param str condition: The condition for a URL rewrite or redirect rule, such as a country code.
        :param str status: The status code for a URL rewrite or redirect rule.
               
               - **200** - Represents a 200 rewrite rule.
               - **301** - Represents a 301 (moved pemanently) redirect rule. This and all future requests should be directed to the target URL.
               - **302** - Represents a 302 temporary redirect rule.
               - **404** - Represents a 404 redirect rule.
               - **404-200** - Represents a 404 rewrite rule.
        """
        pulumi.set(__self__, "source", source)
        pulumi.set(__self__, "target", target)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def source(self) -> str:
        """
        The source pattern for a URL rewrite or redirect rule.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def target(self) -> str:
        """
        The target pattern for a URL rewrite or redirect rule.
        """
        return pulumi.get(self, "target")

    @property
    @pulumi.getter
    def condition(self) -> Optional[str]:
        """
        The condition for a URL rewrite or redirect rule, such as a country code.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status code for a URL rewrite or redirect rule.

        - **200** - Represents a 200 rewrite rule.
        - **301** - Represents a 301 (moved pemanently) redirect rule. This and all future requests should be directed to the target URL.
        - **302** - Represents a 302 temporary redirect rule.
        - **404** - Represents a 404 redirect rule.
        - **404-200** - Represents a 404 rewrite rule.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class AppEnvironmentVariable(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        :param str name: The environment variable name.
        :param str value: The environment variable value.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The environment variable name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The environment variable value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class BranchBackend(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "stackArn":
            suggest = "stack_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BranchBackend. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BranchBackend.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BranchBackend.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 stack_arn: Optional[str] = None):
        """
        :param str stack_arn: The Amazon Resource Name (ARN) for the AWS CloudFormation stack.
        """
        if stack_arn is not None:
            pulumi.set(__self__, "stack_arn", stack_arn)

    @property
    @pulumi.getter(name="stackArn")
    def stack_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for the AWS CloudFormation stack.
        """
        return pulumi.get(self, "stack_arn")


@pulumi.output_type
class BranchBasicAuthConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "enableBasicAuth":
            suggest = "enable_basic_auth"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BranchBasicAuthConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BranchBasicAuthConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BranchBasicAuthConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 password: str,
                 username: str,
                 enable_basic_auth: Optional[bool] = None):
        """
        :param str password: The password for basic authorization.
        :param bool enable_basic_auth: Enables basic authorization for the branch.
        """
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "username", username)
        if enable_basic_auth is not None:
            pulumi.set(__self__, "enable_basic_auth", enable_basic_auth)

    @property
    @pulumi.getter
    def password(self) -> str:
        """
        The password for basic authorization.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def username(self) -> str:
        return pulumi.get(self, "username")

    @property
    @pulumi.getter(name="enableBasicAuth")
    def enable_basic_auth(self) -> Optional[bool]:
        """
        Enables basic authorization for the branch.
        """
        return pulumi.get(self, "enable_basic_auth")


@pulumi.output_type
class BranchEnvironmentVariable(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        :param str name: The environment variable name.
        :param str value: The environment variable value.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The environment variable name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The environment variable value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class DomainCertificate(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "certificateArn":
            suggest = "certificate_arn"
        elif key == "certificateType":
            suggest = "certificate_type"
        elif key == "certificateVerificationDnsRecord":
            suggest = "certificate_verification_dns_record"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DomainCertificate. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DomainCertificate.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DomainCertificate.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 certificate_arn: Optional[str] = None,
                 certificate_type: Optional['DomainCertificateCertificateType'] = None,
                 certificate_verification_dns_record: Optional[str] = None):
        """
        :param str certificate_arn: The Amazon resource name (ARN) for a custom certificate that you have already added to AWS Certificate Manager in your AWS account .
               
               This field is required only when the certificate type is `CUSTOM` .
        :param 'DomainCertificateCertificateType' certificate_type: The type of SSL/TLS certificate that you want to use.
               
               Specify `AMPLIFY_MANAGED` to use the default certificate that Amplify provisions for you.
               
               Specify `CUSTOM` to use your own certificate that you have already added to AWS Certificate Manager in your AWS account . Make sure you request (or import) the certificate in the US East (N. Virginia) Region (us-east-1). For more information about using ACM, see [Importing certificates into AWS Certificate Manager](https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html) in the *ACM User guide* .
        :param str certificate_verification_dns_record: The DNS record for certificate verification.
        """
        if certificate_arn is not None:
            pulumi.set(__self__, "certificate_arn", certificate_arn)
        if certificate_type is not None:
            pulumi.set(__self__, "certificate_type", certificate_type)
        if certificate_verification_dns_record is not None:
            pulumi.set(__self__, "certificate_verification_dns_record", certificate_verification_dns_record)

    @property
    @pulumi.getter(name="certificateArn")
    def certificate_arn(self) -> Optional[str]:
        """
        The Amazon resource name (ARN) for a custom certificate that you have already added to AWS Certificate Manager in your AWS account .

        This field is required only when the certificate type is `CUSTOM` .
        """
        return pulumi.get(self, "certificate_arn")

    @property
    @pulumi.getter(name="certificateType")
    def certificate_type(self) -> Optional['DomainCertificateCertificateType']:
        """
        The type of SSL/TLS certificate that you want to use.

        Specify `AMPLIFY_MANAGED` to use the default certificate that Amplify provisions for you.

        Specify `CUSTOM` to use your own certificate that you have already added to AWS Certificate Manager in your AWS account . Make sure you request (or import) the certificate in the US East (N. Virginia) Region (us-east-1). For more information about using ACM, see [Importing certificates into AWS Certificate Manager](https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html) in the *ACM User guide* .
        """
        return pulumi.get(self, "certificate_type")

    @property
    @pulumi.getter(name="certificateVerificationDnsRecord")
    def certificate_verification_dns_record(self) -> Optional[str]:
        """
        The DNS record for certificate verification.
        """
        return pulumi.get(self, "certificate_verification_dns_record")


@pulumi.output_type
class DomainCertificateSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "certificateType":
            suggest = "certificate_type"
        elif key == "customCertificateArn":
            suggest = "custom_certificate_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DomainCertificateSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DomainCertificateSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DomainCertificateSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 certificate_type: Optional['DomainCertificateSettingsCertificateType'] = None,
                 custom_certificate_arn: Optional[str] = None):
        """
        :param 'DomainCertificateSettingsCertificateType' certificate_type: The certificate type.
               
               Specify `AMPLIFY_MANAGED` to use the default certificate that Amplify provisions for you.
               
               Specify `CUSTOM` to use your own certificate that you have already added to AWS Certificate Manager in your AWS account . Make sure you request (or import) the certificate in the US East (N. Virginia) Region (us-east-1). For more information about using ACM, see [Importing certificates into AWS Certificate Manager](https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html) in the *ACM User guide* .
        :param str custom_certificate_arn: The Amazon resource name (ARN) for the custom certificate that you have already added to AWS Certificate Manager in your AWS account .
               
               This field is required only when the certificate type is `CUSTOM` .
        """
        if certificate_type is not None:
            pulumi.set(__self__, "certificate_type", certificate_type)
        if custom_certificate_arn is not None:
            pulumi.set(__self__, "custom_certificate_arn", custom_certificate_arn)

    @property
    @pulumi.getter(name="certificateType")
    def certificate_type(self) -> Optional['DomainCertificateSettingsCertificateType']:
        """
        The certificate type.

        Specify `AMPLIFY_MANAGED` to use the default certificate that Amplify provisions for you.

        Specify `CUSTOM` to use your own certificate that you have already added to AWS Certificate Manager in your AWS account . Make sure you request (or import) the certificate in the US East (N. Virginia) Region (us-east-1). For more information about using ACM, see [Importing certificates into AWS Certificate Manager](https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html) in the *ACM User guide* .
        """
        return pulumi.get(self, "certificate_type")

    @property
    @pulumi.getter(name="customCertificateArn")
    def custom_certificate_arn(self) -> Optional[str]:
        """
        The Amazon resource name (ARN) for the custom certificate that you have already added to AWS Certificate Manager in your AWS account .

        This field is required only when the certificate type is `CUSTOM` .
        """
        return pulumi.get(self, "custom_certificate_arn")


@pulumi.output_type
class DomainSubDomainSetting(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "branchName":
            suggest = "branch_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DomainSubDomainSetting. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DomainSubDomainSetting.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DomainSubDomainSetting.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 branch_name: str,
                 prefix: str):
        """
        :param str branch_name: The branch name setting for the subdomain.
               
               *Length Constraints:* Minimum length of 1. Maximum length of 255.
               
               *Pattern:* (?s).+
        :param str prefix: The prefix setting for the subdomain.
        """
        pulumi.set(__self__, "branch_name", branch_name)
        pulumi.set(__self__, "prefix", prefix)

    @property
    @pulumi.getter(name="branchName")
    def branch_name(self) -> str:
        """
        The branch name setting for the subdomain.

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        *Pattern:* (?s).+
        """
        return pulumi.get(self, "branch_name")

    @property
    @pulumi.getter
    def prefix(self) -> str:
        """
        The prefix setting for the subdomain.
        """
        return pulumi.get(self, "prefix")


