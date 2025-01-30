# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'EnvironmentFederationMode',
    'EnvironmentStatus',
]


class EnvironmentFederationMode(str, Enum):
    """
    Federation mode used with the Environment
    """
    LOCAL = "LOCAL"
    FEDERATED = "FEDERATED"


class EnvironmentStatus(str, Enum):
    """
    State of the Environment
    """
    CREATE_REQUESTED = "CREATE_REQUESTED"
    CREATING = "CREATING"
    CREATED = "CREATED"
    DELETE_REQUESTED = "DELETE_REQUESTED"
    DELETING = "DELETING"
    DELETED = "DELETED"
    FAILED_CREATION = "FAILED_CREATION"
    FAILED_DELETION = "FAILED_DELETION"
    RETRY_DELETION = "RETRY_DELETION"
    SUSPENDED = "SUSPENDED"
