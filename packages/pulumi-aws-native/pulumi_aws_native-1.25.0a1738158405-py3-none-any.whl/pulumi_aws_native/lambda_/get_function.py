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
from ._enums import *

__all__ = [
    'GetFunctionResult',
    'AwaitableGetFunctionResult',
    'get_function',
    'get_function_output',
]

@pulumi.output_type
class GetFunctionResult:
    def __init__(__self__, architectures=None, arn=None, code_signing_config_arn=None, dead_letter_config=None, description=None, environment=None, ephemeral_storage=None, file_system_configs=None, handler=None, image_config=None, kms_key_arn=None, layers=None, logging_config=None, memory_size=None, package_type=None, recursive_loop=None, reserved_concurrent_executions=None, role=None, runtime=None, runtime_management_config=None, snap_start_response=None, tags=None, timeout=None, tracing_config=None, vpc_config=None):
        if architectures and not isinstance(architectures, list):
            raise TypeError("Expected argument 'architectures' to be a list")
        pulumi.set(__self__, "architectures", architectures)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if code_signing_config_arn and not isinstance(code_signing_config_arn, str):
            raise TypeError("Expected argument 'code_signing_config_arn' to be a str")
        pulumi.set(__self__, "code_signing_config_arn", code_signing_config_arn)
        if dead_letter_config and not isinstance(dead_letter_config, dict):
            raise TypeError("Expected argument 'dead_letter_config' to be a dict")
        pulumi.set(__self__, "dead_letter_config", dead_letter_config)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if environment and not isinstance(environment, dict):
            raise TypeError("Expected argument 'environment' to be a dict")
        pulumi.set(__self__, "environment", environment)
        if ephemeral_storage and not isinstance(ephemeral_storage, dict):
            raise TypeError("Expected argument 'ephemeral_storage' to be a dict")
        pulumi.set(__self__, "ephemeral_storage", ephemeral_storage)
        if file_system_configs and not isinstance(file_system_configs, list):
            raise TypeError("Expected argument 'file_system_configs' to be a list")
        pulumi.set(__self__, "file_system_configs", file_system_configs)
        if handler and not isinstance(handler, str):
            raise TypeError("Expected argument 'handler' to be a str")
        pulumi.set(__self__, "handler", handler)
        if image_config and not isinstance(image_config, dict):
            raise TypeError("Expected argument 'image_config' to be a dict")
        pulumi.set(__self__, "image_config", image_config)
        if kms_key_arn and not isinstance(kms_key_arn, str):
            raise TypeError("Expected argument 'kms_key_arn' to be a str")
        pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if layers and not isinstance(layers, list):
            raise TypeError("Expected argument 'layers' to be a list")
        pulumi.set(__self__, "layers", layers)
        if logging_config and not isinstance(logging_config, dict):
            raise TypeError("Expected argument 'logging_config' to be a dict")
        pulumi.set(__self__, "logging_config", logging_config)
        if memory_size and not isinstance(memory_size, int):
            raise TypeError("Expected argument 'memory_size' to be a int")
        pulumi.set(__self__, "memory_size", memory_size)
        if package_type and not isinstance(package_type, str):
            raise TypeError("Expected argument 'package_type' to be a str")
        pulumi.set(__self__, "package_type", package_type)
        if recursive_loop and not isinstance(recursive_loop, str):
            raise TypeError("Expected argument 'recursive_loop' to be a str")
        pulumi.set(__self__, "recursive_loop", recursive_loop)
        if reserved_concurrent_executions and not isinstance(reserved_concurrent_executions, int):
            raise TypeError("Expected argument 'reserved_concurrent_executions' to be a int")
        pulumi.set(__self__, "reserved_concurrent_executions", reserved_concurrent_executions)
        if role and not isinstance(role, str):
            raise TypeError("Expected argument 'role' to be a str")
        pulumi.set(__self__, "role", role)
        if runtime and not isinstance(runtime, str):
            raise TypeError("Expected argument 'runtime' to be a str")
        pulumi.set(__self__, "runtime", runtime)
        if runtime_management_config and not isinstance(runtime_management_config, dict):
            raise TypeError("Expected argument 'runtime_management_config' to be a dict")
        pulumi.set(__self__, "runtime_management_config", runtime_management_config)
        if snap_start_response and not isinstance(snap_start_response, dict):
            raise TypeError("Expected argument 'snap_start_response' to be a dict")
        pulumi.set(__self__, "snap_start_response", snap_start_response)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if timeout and not isinstance(timeout, int):
            raise TypeError("Expected argument 'timeout' to be a int")
        pulumi.set(__self__, "timeout", timeout)
        if tracing_config and not isinstance(tracing_config, dict):
            raise TypeError("Expected argument 'tracing_config' to be a dict")
        pulumi.set(__self__, "tracing_config", tracing_config)
        if vpc_config and not isinstance(vpc_config, dict):
            raise TypeError("Expected argument 'vpc_config' to be a dict")
        pulumi.set(__self__, "vpc_config", vpc_config)

    @property
    @pulumi.getter
    def architectures(self) -> Optional[Sequence['FunctionArchitecturesItem']]:
        """
        The instruction set architecture that the function supports. Enter a string array with one of the valid values (arm64 or x86_64). The default value is ``x86_64``.
        """
        return pulumi.get(self, "architectures")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the function.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="codeSigningConfigArn")
    def code_signing_config_arn(self) -> Optional[str]:
        """
        To enable code signing for this function, specify the ARN of a code-signing configuration. A code-signing configuration includes a set of signing profiles, which define the trusted publishers for this function.
        """
        return pulumi.get(self, "code_signing_config_arn")

    @property
    @pulumi.getter(name="deadLetterConfig")
    def dead_letter_config(self) -> Optional['outputs.FunctionDeadLetterConfig']:
        """
        A dead-letter queue configuration that specifies the queue or topic where Lambda sends asynchronous events when they fail processing. For more information, see [Dead-letter queues](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html#invocation-dlq).
        """
        return pulumi.get(self, "dead_letter_config")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the function.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def environment(self) -> Optional['outputs.FunctionEnvironment']:
        """
        Environment variables that are accessible from function code during execution.
        """
        return pulumi.get(self, "environment")

    @property
    @pulumi.getter(name="ephemeralStorage")
    def ephemeral_storage(self) -> Optional['outputs.FunctionEphemeralStorage']:
        """
        The size of the function's ``/tmp`` directory in MB. The default value is 512, but it can be any whole number between 512 and 10,240 MB.
        """
        return pulumi.get(self, "ephemeral_storage")

    @property
    @pulumi.getter(name="fileSystemConfigs")
    def file_system_configs(self) -> Optional[Sequence['outputs.FunctionFileSystemConfig']]:
        """
        Connection settings for an Amazon EFS file system. To connect a function to a file system, a mount target must be available in every Availability Zone that your function connects to. If your template contains an [AWS::EFS::MountTarget](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html) resource, you must also specify a ``DependsOn`` attribute to ensure that the mount target is created or updated before the function.
         For more information about using the ``DependsOn`` attribute, see [DependsOn Attribute](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html).
        """
        return pulumi.get(self, "file_system_configs")

    @property
    @pulumi.getter
    def handler(self) -> Optional[str]:
        """
        The name of the method within your code that Lambda calls to run your function. Handler is required if the deployment package is a .zip file archive. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see [Lambda programming model](https://docs.aws.amazon.com/lambda/latest/dg/foundation-progmodel.html).
        """
        return pulumi.get(self, "handler")

    @property
    @pulumi.getter(name="imageConfig")
    def image_config(self) -> Optional['outputs.FunctionImageConfig']:
        """
        Configuration values that override the container image Dockerfile settings. For more information, see [Container image settings](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-parms).
        """
        return pulumi.get(self, "image_config")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[str]:
        """
        The ARN of the KMSlong (KMS) customer managed key that's used to encrypt your function's [environment variables](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-encryption). When [SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart-security.html) is activated, LAM also uses this key is to encrypt your function's snapshot. If you deploy your function using a container image, LAM also uses this key to encrypt your function when it's deployed. Note that this is not the same key that's used to protect your container image in the ECRlong (ECR). If you don't provide a customer managed key, LAM uses a default service key.
        """
        return pulumi.get(self, "kms_key_arn")

    @property
    @pulumi.getter
    def layers(self) -> Optional[Sequence[str]]:
        """
        A list of [function layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) to add to the function's execution environment. Specify each layer by its ARN, including the version.
        """
        return pulumi.get(self, "layers")

    @property
    @pulumi.getter(name="loggingConfig")
    def logging_config(self) -> Optional['outputs.FunctionLoggingConfig']:
        """
        The function's Amazon CloudWatch Logs configuration settings.
        """
        return pulumi.get(self, "logging_config")

    @property
    @pulumi.getter(name="memorySize")
    def memory_size(self) -> Optional[int]:
        """
        The amount of [memory available to the function](https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html#configuration-memory-console) at runtime. Increasing the function memory also increases its CPU allocation. The default value is 128 MB. The value can be any multiple of 1 MB. Note that new AWS accounts have reduced concurrency and memory quotas. AWS raises these quotas automatically based on your usage. You can also request a quota increase.
        """
        return pulumi.get(self, "memory_size")

    @property
    @pulumi.getter(name="packageType")
    def package_type(self) -> Optional['FunctionPackageType']:
        """
        The type of deployment package. Set to ``Image`` for container image and set ``Zip`` for .zip file archive.
        """
        return pulumi.get(self, "package_type")

    @property
    @pulumi.getter(name="recursiveLoop")
    def recursive_loop(self) -> Optional['FunctionRecursiveLoop']:
        """
        The status of your function's recursive loop detection configuration.
         When this value is set to ``Allow``and Lambda detects your function being invoked as part of a recursive loop, it doesn't take any action.
         When this value is set to ``Terminate`` and Lambda detects your function being invoked as part of a recursive loop, it stops your function being invoked and notifies you.
        """
        return pulumi.get(self, "recursive_loop")

    @property
    @pulumi.getter(name="reservedConcurrentExecutions")
    def reserved_concurrent_executions(self) -> Optional[int]:
        """
        The number of simultaneous executions to reserve for the function.
        """
        return pulumi.get(self, "reserved_concurrent_executions")

    @property
    @pulumi.getter
    def role(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the function's execution role.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter
    def runtime(self) -> Optional[str]:
        """
        The identifier of the function's [runtime](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html). Runtime is required if the deployment package is a .zip file archive. Specifying a runtime results in an error if you're deploying a function using a container image.
         The following list includes deprecated runtimes. Lambda blocks creating new functions and updating existing functions shortly after each runtime is deprecated. For more information, see [Runtime use after deprecation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html#runtime-deprecation-levels).
         For a list of all currently supported runtimes, see [Supported runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html#runtimes-supported).
        """
        return pulumi.get(self, "runtime")

    @property
    @pulumi.getter(name="runtimeManagementConfig")
    def runtime_management_config(self) -> Optional['outputs.FunctionRuntimeManagementConfig']:
        """
        Sets the runtime management configuration for a function's version. For more information, see [Runtime updates](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html).
        """
        return pulumi.get(self, "runtime_management_config")

    @property
    @pulumi.getter(name="snapStartResponse")
    def snap_start_response(self) -> Optional['outputs.FunctionSnapStartResponse']:
        return pulumi.get(self, "snap_start_response")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of [tags](https://docs.aws.amazon.com/lambda/latest/dg/tagging.html) to apply to the function.
          You must have the ``lambda:TagResource``, ``lambda:UntagResource``, and ``lambda:ListTags`` permissions for your [principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) to manage the CFN stack. If you don't have these permissions, there might be unexpected behavior with stack-level tags propagating to the resource during resource creation and update.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def timeout(self) -> Optional[int]:
        """
        The amount of time (in seconds) that Lambda allows a function to run before stopping it. The default is 3 seconds. The maximum allowed value is 900 seconds. For more information, see [Lambda execution environment](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-context.html).
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter(name="tracingConfig")
    def tracing_config(self) -> Optional['outputs.FunctionTracingConfig']:
        """
        Set ``Mode`` to ``Active`` to sample and trace a subset of incoming requests with [X-Ray](https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html).
        """
        return pulumi.get(self, "tracing_config")

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> Optional['outputs.FunctionVpcConfig']:
        """
        For network connectivity to AWS resources in a VPC, specify a list of security groups and subnets in the VPC. When you connect a function to a VPC, it can access resources and the internet only through that VPC. For more information, see [Configuring a Lambda function to access resources in a VPC](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html).
        """
        return pulumi.get(self, "vpc_config")


class AwaitableGetFunctionResult(GetFunctionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFunctionResult(
            architectures=self.architectures,
            arn=self.arn,
            code_signing_config_arn=self.code_signing_config_arn,
            dead_letter_config=self.dead_letter_config,
            description=self.description,
            environment=self.environment,
            ephemeral_storage=self.ephemeral_storage,
            file_system_configs=self.file_system_configs,
            handler=self.handler,
            image_config=self.image_config,
            kms_key_arn=self.kms_key_arn,
            layers=self.layers,
            logging_config=self.logging_config,
            memory_size=self.memory_size,
            package_type=self.package_type,
            recursive_loop=self.recursive_loop,
            reserved_concurrent_executions=self.reserved_concurrent_executions,
            role=self.role,
            runtime=self.runtime,
            runtime_management_config=self.runtime_management_config,
            snap_start_response=self.snap_start_response,
            tags=self.tags,
            timeout=self.timeout,
            tracing_config=self.tracing_config,
            vpc_config=self.vpc_config)


def get_function(function_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFunctionResult:
    """
    The ``AWS::Lambda::Function`` resource creates a Lambda function. To create a function, you need a [deployment package](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html) and an [execution role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html). The deployment package is a .zip file archive or container image that contains your function code. The execution role grants the function permission to use AWS services, such as Amazon CloudWatch Logs for log streaming and AWS X-Ray for request tracing.
     You set the package type to ``Image`` if the deployment package is a [container image](https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html). For these functions, include the URI of the container image in the ECR registry in the [ImageUri property of the Code property](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-imageuri). You do not need to specify the handler and runtime properties.
     You set the package type to ``Zip`` if the deployment package is a [.zip file archive](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip). For these functions, specify the S3 location of your .zip file in the ``Code`` property. Alternatively, for Node.js and Python functions, you can define your function inline in the [ZipFile property of the Code property](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-zipfile). In both cases, you must also specify the handler and runtime properties.
     You can use [code signing](https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning.html) if your deployment package is a .zip file archive. To enable code signing for this function, specify the ARN of a code-signing configuration. When a user attempts to deploy a code package with ``UpdateFunctionCode``, Lambda checks that the code package has a valid signature from a trusted publisher. The code-signing configuration includes a set of signing profiles, which define the trusted publishers for this function.
     When you update a ``AWS::Lambda::Function`` resource, CFNshort calls the [UpdateFunctionConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionConfiguration.html) and [UpdateFunctionCode](https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionCode.html) LAM APIs under the hood. Because these calls happen sequentially, and invocations can happen between these calls, your function may encounter errors in the time between the calls. For example, if you remove an environment variable, and the code that references that environment variable in the same CFNshort update, you may see invocation errors related to a missing environment variable. To work around this, you can invoke your function against a version or alias by default, rather than the ``$LATEST`` version.
     Note that you configure [provisioned concurrency](https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html) on a ``AWS::Lambda::Version`` or a ``AWS::Lambda::Alias``.
     For a complete introduction to Lambda functions, see [What is Lambda?](https://docs.aws.amazon.com/lambda/latest/dg/lambda-welcome.html) in the *Lambda developer guide.*


    :param str function_name: The name of the Lambda function, up to 64 characters in length. If you don't specify a name, CFN generates one.
            If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
    """
    __args__ = dict()
    __args__['functionName'] = function_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:lambda:getFunction', __args__, opts=opts, typ=GetFunctionResult).value

    return AwaitableGetFunctionResult(
        architectures=pulumi.get(__ret__, 'architectures'),
        arn=pulumi.get(__ret__, 'arn'),
        code_signing_config_arn=pulumi.get(__ret__, 'code_signing_config_arn'),
        dead_letter_config=pulumi.get(__ret__, 'dead_letter_config'),
        description=pulumi.get(__ret__, 'description'),
        environment=pulumi.get(__ret__, 'environment'),
        ephemeral_storage=pulumi.get(__ret__, 'ephemeral_storage'),
        file_system_configs=pulumi.get(__ret__, 'file_system_configs'),
        handler=pulumi.get(__ret__, 'handler'),
        image_config=pulumi.get(__ret__, 'image_config'),
        kms_key_arn=pulumi.get(__ret__, 'kms_key_arn'),
        layers=pulumi.get(__ret__, 'layers'),
        logging_config=pulumi.get(__ret__, 'logging_config'),
        memory_size=pulumi.get(__ret__, 'memory_size'),
        package_type=pulumi.get(__ret__, 'package_type'),
        recursive_loop=pulumi.get(__ret__, 'recursive_loop'),
        reserved_concurrent_executions=pulumi.get(__ret__, 'reserved_concurrent_executions'),
        role=pulumi.get(__ret__, 'role'),
        runtime=pulumi.get(__ret__, 'runtime'),
        runtime_management_config=pulumi.get(__ret__, 'runtime_management_config'),
        snap_start_response=pulumi.get(__ret__, 'snap_start_response'),
        tags=pulumi.get(__ret__, 'tags'),
        timeout=pulumi.get(__ret__, 'timeout'),
        tracing_config=pulumi.get(__ret__, 'tracing_config'),
        vpc_config=pulumi.get(__ret__, 'vpc_config'))
def get_function_output(function_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetFunctionResult]:
    """
    The ``AWS::Lambda::Function`` resource creates a Lambda function. To create a function, you need a [deployment package](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html) and an [execution role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html). The deployment package is a .zip file archive or container image that contains your function code. The execution role grants the function permission to use AWS services, such as Amazon CloudWatch Logs for log streaming and AWS X-Ray for request tracing.
     You set the package type to ``Image`` if the deployment package is a [container image](https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html). For these functions, include the URI of the container image in the ECR registry in the [ImageUri property of the Code property](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-imageuri). You do not need to specify the handler and runtime properties.
     You set the package type to ``Zip`` if the deployment package is a [.zip file archive](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip). For these functions, specify the S3 location of your .zip file in the ``Code`` property. Alternatively, for Node.js and Python functions, you can define your function inline in the [ZipFile property of the Code property](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-zipfile). In both cases, you must also specify the handler and runtime properties.
     You can use [code signing](https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning.html) if your deployment package is a .zip file archive. To enable code signing for this function, specify the ARN of a code-signing configuration. When a user attempts to deploy a code package with ``UpdateFunctionCode``, Lambda checks that the code package has a valid signature from a trusted publisher. The code-signing configuration includes a set of signing profiles, which define the trusted publishers for this function.
     When you update a ``AWS::Lambda::Function`` resource, CFNshort calls the [UpdateFunctionConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionConfiguration.html) and [UpdateFunctionCode](https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionCode.html) LAM APIs under the hood. Because these calls happen sequentially, and invocations can happen between these calls, your function may encounter errors in the time between the calls. For example, if you remove an environment variable, and the code that references that environment variable in the same CFNshort update, you may see invocation errors related to a missing environment variable. To work around this, you can invoke your function against a version or alias by default, rather than the ``$LATEST`` version.
     Note that you configure [provisioned concurrency](https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html) on a ``AWS::Lambda::Version`` or a ``AWS::Lambda::Alias``.
     For a complete introduction to Lambda functions, see [What is Lambda?](https://docs.aws.amazon.com/lambda/latest/dg/lambda-welcome.html) in the *Lambda developer guide.*


    :param str function_name: The name of the Lambda function, up to 64 characters in length. If you don't specify a name, CFN generates one.
            If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
    """
    __args__ = dict()
    __args__['functionName'] = function_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:lambda:getFunction', __args__, opts=opts, typ=GetFunctionResult)
    return __ret__.apply(lambda __response__: GetFunctionResult(
        architectures=pulumi.get(__response__, 'architectures'),
        arn=pulumi.get(__response__, 'arn'),
        code_signing_config_arn=pulumi.get(__response__, 'code_signing_config_arn'),
        dead_letter_config=pulumi.get(__response__, 'dead_letter_config'),
        description=pulumi.get(__response__, 'description'),
        environment=pulumi.get(__response__, 'environment'),
        ephemeral_storage=pulumi.get(__response__, 'ephemeral_storage'),
        file_system_configs=pulumi.get(__response__, 'file_system_configs'),
        handler=pulumi.get(__response__, 'handler'),
        image_config=pulumi.get(__response__, 'image_config'),
        kms_key_arn=pulumi.get(__response__, 'kms_key_arn'),
        layers=pulumi.get(__response__, 'layers'),
        logging_config=pulumi.get(__response__, 'logging_config'),
        memory_size=pulumi.get(__response__, 'memory_size'),
        package_type=pulumi.get(__response__, 'package_type'),
        recursive_loop=pulumi.get(__response__, 'recursive_loop'),
        reserved_concurrent_executions=pulumi.get(__response__, 'reserved_concurrent_executions'),
        role=pulumi.get(__response__, 'role'),
        runtime=pulumi.get(__response__, 'runtime'),
        runtime_management_config=pulumi.get(__response__, 'runtime_management_config'),
        snap_start_response=pulumi.get(__response__, 'snap_start_response'),
        tags=pulumi.get(__response__, 'tags'),
        timeout=pulumi.get(__response__, 'timeout'),
        tracing_config=pulumi.get(__response__, 'tracing_config'),
        vpc_config=pulumi.get(__response__, 'vpc_config')))
