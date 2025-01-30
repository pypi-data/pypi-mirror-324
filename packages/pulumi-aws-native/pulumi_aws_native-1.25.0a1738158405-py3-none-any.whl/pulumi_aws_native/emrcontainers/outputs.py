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
    'VirtualClusterContainerInfo',
    'VirtualClusterContainerProvider',
    'VirtualClusterEksInfo',
]

@pulumi.output_type
class VirtualClusterContainerInfo(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "eksInfo":
            suggest = "eks_info"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VirtualClusterContainerInfo. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VirtualClusterContainerInfo.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VirtualClusterContainerInfo.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 eks_info: 'outputs.VirtualClusterEksInfo'):
        """
        :param 'VirtualClusterEksInfo' eks_info: The information about the Amazon EKS cluster.
        """
        pulumi.set(__self__, "eks_info", eks_info)

    @property
    @pulumi.getter(name="eksInfo")
    def eks_info(self) -> 'outputs.VirtualClusterEksInfo':
        """
        The information about the Amazon EKS cluster.
        """
        return pulumi.get(self, "eks_info")


@pulumi.output_type
class VirtualClusterContainerProvider(dict):
    def __init__(__self__, *,
                 id: str,
                 info: 'outputs.VirtualClusterContainerInfo',
                 type: str):
        """
        :param str id: The ID of the container cluster
        :param 'VirtualClusterContainerInfo' info: The information about the container cluster.
        :param str type: The type of the container provider
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "info", info)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the container cluster
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def info(self) -> 'outputs.VirtualClusterContainerInfo':
        """
        The information about the container cluster.
        """
        return pulumi.get(self, "info")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the container provider
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class VirtualClusterEksInfo(dict):
    def __init__(__self__, *,
                 namespace: str):
        """
        :param str namespace: The namespaces of the EKS cluster.
               
               *Minimum* : 1
               
               *Maximum* : 63
               
               *Pattern* : `[a-z0-9]([-a-z0-9]*[a-z0-9])?`
        """
        pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def namespace(self) -> str:
        """
        The namespaces of the EKS cluster.

        *Minimum* : 1

        *Maximum* : 63

        *Pattern* : `[a-z0-9]([-a-z0-9]*[a-z0-9])?`
        """
        return pulumi.get(self, "namespace")


