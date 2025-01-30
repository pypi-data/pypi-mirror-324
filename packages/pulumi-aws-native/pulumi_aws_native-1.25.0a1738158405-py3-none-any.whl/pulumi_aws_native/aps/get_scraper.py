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

__all__ = [
    'GetScraperResult',
    'AwaitableGetScraperResult',
    'get_scraper',
    'get_scraper_output',
]

@pulumi.output_type
class GetScraperResult:
    def __init__(__self__, alias=None, arn=None, destination=None, role_arn=None, scrape_configuration=None, scraper_id=None, tags=None):
        if alias and not isinstance(alias, str):
            raise TypeError("Expected argument 'alias' to be a str")
        pulumi.set(__self__, "alias", alias)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if destination and not isinstance(destination, dict):
            raise TypeError("Expected argument 'destination' to be a dict")
        pulumi.set(__self__, "destination", destination)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if scrape_configuration and not isinstance(scrape_configuration, dict):
            raise TypeError("Expected argument 'scrape_configuration' to be a dict")
        pulumi.set(__self__, "scrape_configuration", scrape_configuration)
        if scraper_id and not isinstance(scraper_id, str):
            raise TypeError("Expected argument 'scraper_id' to be a str")
        pulumi.set(__self__, "scraper_id", scraper_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def alias(self) -> Optional[str]:
        """
        Scraper alias.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Scraper ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def destination(self) -> Optional['outputs.ScraperDestination']:
        """
        The Amazon Managed Service for Prometheus workspace the scraper sends metrics to.
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        IAM role ARN for the scraper.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="scrapeConfiguration")
    def scrape_configuration(self) -> Optional['outputs.ScraperScrapeConfiguration']:
        """
        The configuration in use by the scraper.
        """
        return pulumi.get(self, "scrape_configuration")

    @property
    @pulumi.getter(name="scraperId")
    def scraper_id(self) -> Optional[str]:
        """
        Required to identify a specific scraper.
        """
        return pulumi.get(self, "scraper_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetScraperResult(GetScraperResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScraperResult(
            alias=self.alias,
            arn=self.arn,
            destination=self.destination,
            role_arn=self.role_arn,
            scrape_configuration=self.scrape_configuration,
            scraper_id=self.scraper_id,
            tags=self.tags)


def get_scraper(arn: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScraperResult:
    """
    Resource Type definition for AWS::APS::Scraper


    :param str arn: Scraper ARN.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:aps:getScraper', __args__, opts=opts, typ=GetScraperResult).value

    return AwaitableGetScraperResult(
        alias=pulumi.get(__ret__, 'alias'),
        arn=pulumi.get(__ret__, 'arn'),
        destination=pulumi.get(__ret__, 'destination'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        scrape_configuration=pulumi.get(__ret__, 'scrape_configuration'),
        scraper_id=pulumi.get(__ret__, 'scraper_id'),
        tags=pulumi.get(__ret__, 'tags'))
def get_scraper_output(arn: Optional[pulumi.Input[str]] = None,
                       opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetScraperResult]:
    """
    Resource Type definition for AWS::APS::Scraper


    :param str arn: Scraper ARN.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:aps:getScraper', __args__, opts=opts, typ=GetScraperResult)
    return __ret__.apply(lambda __response__: GetScraperResult(
        alias=pulumi.get(__response__, 'alias'),
        arn=pulumi.get(__response__, 'arn'),
        destination=pulumi.get(__response__, 'destination'),
        role_arn=pulumi.get(__response__, 'role_arn'),
        scrape_configuration=pulumi.get(__response__, 'scrape_configuration'),
        scraper_id=pulumi.get(__response__, 'scraper_id'),
        tags=pulumi.get(__response__, 'tags')))
