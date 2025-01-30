# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AssessmentDelegationStatus',
    'AssessmentReportDestinationType',
    'AssessmentRoleType',
    'AssessmentStatus',
]


class AssessmentDelegationStatus(str, Enum):
    """
    The status of the delegation.
    """
    IN_PROGRESS = "IN_PROGRESS"
    UNDER_REVIEW = "UNDER_REVIEW"
    COMPLETE = "COMPLETE"


class AssessmentReportDestinationType(str, Enum):
    """
    The destination type, such as Amazon S3.
    """
    S3 = "S3"


class AssessmentRoleType(str, Enum):
    """
     The IAM role type.
    """
    PROCESS_OWNER = "PROCESS_OWNER"
    RESOURCE_OWNER = "RESOURCE_OWNER"


class AssessmentStatus(str, Enum):
    """
    The status of the specified assessment. 
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
