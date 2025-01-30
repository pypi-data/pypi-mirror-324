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
    'GetEvaluationFormResult',
    'AwaitableGetEvaluationFormResult',
    'get_evaluation_form',
    'get_evaluation_form_output',
]

@pulumi.output_type
class GetEvaluationFormResult:
    def __init__(__self__, description=None, evaluation_form_arn=None, instance_arn=None, items=None, scoring_strategy=None, status=None, tags=None, title=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if evaluation_form_arn and not isinstance(evaluation_form_arn, str):
            raise TypeError("Expected argument 'evaluation_form_arn' to be a str")
        pulumi.set(__self__, "evaluation_form_arn", evaluation_form_arn)
        if instance_arn and not isinstance(instance_arn, str):
            raise TypeError("Expected argument 'instance_arn' to be a str")
        pulumi.set(__self__, "instance_arn", instance_arn)
        if items and not isinstance(items, list):
            raise TypeError("Expected argument 'items' to be a list")
        pulumi.set(__self__, "items", items)
        if scoring_strategy and not isinstance(scoring_strategy, dict):
            raise TypeError("Expected argument 'scoring_strategy' to be a dict")
        pulumi.set(__self__, "scoring_strategy", scoring_strategy)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if title and not isinstance(title, str):
            raise TypeError("Expected argument 'title' to be a str")
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the evaluation form.
          *Length Constraints*: Minimum length of 0. Maximum length of 1024.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="evaluationFormArn")
    def evaluation_form_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the evaluation form.
        """
        return pulumi.get(self, "evaluation_form_arn")

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> Optional[str]:
        """
        The identifier of the Amazon Connect instance.
        """
        return pulumi.get(self, "instance_arn")

    @property
    @pulumi.getter
    def items(self) -> Optional[Sequence['outputs.EvaluationFormBaseItem']]:
        """
        Items that are part of the evaluation form. The total number of sections and questions must not exceed 100 each. Questions must be contained in a section.
          *Minimum size*: 1
          *Maximum size*: 100
        """
        return pulumi.get(self, "items")

    @property
    @pulumi.getter(name="scoringStrategy")
    def scoring_strategy(self) -> Optional['outputs.EvaluationFormScoringStrategy']:
        """
        A scoring strategy of the evaluation form.
        """
        return pulumi.get(self, "scoring_strategy")

    @property
    @pulumi.getter
    def status(self) -> Optional['EvaluationFormStatus']:
        """
        The status of the evaluation form.
          *Allowed values*: ``DRAFT`` | ``ACTIVE``
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        """
        A title of the evaluation form.
        """
        return pulumi.get(self, "title")


class AwaitableGetEvaluationFormResult(GetEvaluationFormResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEvaluationFormResult(
            description=self.description,
            evaluation_form_arn=self.evaluation_form_arn,
            instance_arn=self.instance_arn,
            items=self.items,
            scoring_strategy=self.scoring_strategy,
            status=self.status,
            tags=self.tags,
            title=self.title)


def get_evaluation_form(evaluation_form_arn: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEvaluationFormResult:
    """
    Creates an evaluation form for the specified CON instance.


    :param str evaluation_form_arn: The Amazon Resource Name (ARN) of the evaluation form.
    """
    __args__ = dict()
    __args__['evaluationFormArn'] = evaluation_form_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:connect:getEvaluationForm', __args__, opts=opts, typ=GetEvaluationFormResult).value

    return AwaitableGetEvaluationFormResult(
        description=pulumi.get(__ret__, 'description'),
        evaluation_form_arn=pulumi.get(__ret__, 'evaluation_form_arn'),
        instance_arn=pulumi.get(__ret__, 'instance_arn'),
        items=pulumi.get(__ret__, 'items'),
        scoring_strategy=pulumi.get(__ret__, 'scoring_strategy'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'),
        title=pulumi.get(__ret__, 'title'))
def get_evaluation_form_output(evaluation_form_arn: Optional[pulumi.Input[str]] = None,
                               opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetEvaluationFormResult]:
    """
    Creates an evaluation form for the specified CON instance.


    :param str evaluation_form_arn: The Amazon Resource Name (ARN) of the evaluation form.
    """
    __args__ = dict()
    __args__['evaluationFormArn'] = evaluation_form_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:connect:getEvaluationForm', __args__, opts=opts, typ=GetEvaluationFormResult)
    return __ret__.apply(lambda __response__: GetEvaluationFormResult(
        description=pulumi.get(__response__, 'description'),
        evaluation_form_arn=pulumi.get(__response__, 'evaluation_form_arn'),
        instance_arn=pulumi.get(__response__, 'instance_arn'),
        items=pulumi.get(__response__, 'items'),
        scoring_strategy=pulumi.get(__response__, 'scoring_strategy'),
        status=pulumi.get(__response__, 'status'),
        tags=pulumi.get(__response__, 'tags'),
        title=pulumi.get(__response__, 'title')))
