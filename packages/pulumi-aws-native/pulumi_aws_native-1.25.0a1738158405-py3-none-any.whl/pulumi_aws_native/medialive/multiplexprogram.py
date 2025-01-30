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
from ._inputs import *

__all__ = ['MultiplexprogramArgs', 'Multiplexprogram']

@pulumi.input_type
class MultiplexprogramArgs:
    def __init__(__self__, *,
                 multiplex_id: Optional[pulumi.Input[str]] = None,
                 multiplex_program_settings: Optional[pulumi.Input['MultiplexprogramMultiplexProgramSettingsArgs']] = None,
                 packet_identifiers_map: Optional[pulumi.Input['MultiplexprogramMultiplexProgramPacketIdentifiersMapArgs']] = None,
                 pipeline_details: Optional[pulumi.Input[Sequence[pulumi.Input['MultiplexprogramMultiplexProgramPipelineDetailArgs']]]] = None,
                 preferred_channel_pipeline: Optional[pulumi.Input['MultiplexprogramPreferredChannelPipeline']] = None,
                 program_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Multiplexprogram resource.
        :param pulumi.Input[str] multiplex_id: The ID of the multiplex that the program belongs to.
        :param pulumi.Input['MultiplexprogramMultiplexProgramSettingsArgs'] multiplex_program_settings: The settings for this multiplex program.
        :param pulumi.Input['MultiplexprogramMultiplexProgramPacketIdentifiersMapArgs'] packet_identifiers_map: The packet identifier map for this multiplex program.
        :param pulumi.Input[Sequence[pulumi.Input['MultiplexprogramMultiplexProgramPipelineDetailArgs']]] pipeline_details: Contains information about the current sources for the specified program in the specified multiplex. Keep in mind that each multiplex pipeline connects to both pipelines in a given source channel (the channel identified by the program). But only one of those channel pipelines is ever active at one time.
        :param pulumi.Input['MultiplexprogramPreferredChannelPipeline'] preferred_channel_pipeline: The settings for this multiplex program.
        :param pulumi.Input[str] program_name: The name of the multiplex program.
        """
        if multiplex_id is not None:
            pulumi.set(__self__, "multiplex_id", multiplex_id)
        if multiplex_program_settings is not None:
            pulumi.set(__self__, "multiplex_program_settings", multiplex_program_settings)
        if packet_identifiers_map is not None:
            pulumi.set(__self__, "packet_identifiers_map", packet_identifiers_map)
        if pipeline_details is not None:
            pulumi.set(__self__, "pipeline_details", pipeline_details)
        if preferred_channel_pipeline is not None:
            pulumi.set(__self__, "preferred_channel_pipeline", preferred_channel_pipeline)
        if program_name is not None:
            pulumi.set(__self__, "program_name", program_name)

    @property
    @pulumi.getter(name="multiplexId")
    def multiplex_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the multiplex that the program belongs to.
        """
        return pulumi.get(self, "multiplex_id")

    @multiplex_id.setter
    def multiplex_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "multiplex_id", value)

    @property
    @pulumi.getter(name="multiplexProgramSettings")
    def multiplex_program_settings(self) -> Optional[pulumi.Input['MultiplexprogramMultiplexProgramSettingsArgs']]:
        """
        The settings for this multiplex program.
        """
        return pulumi.get(self, "multiplex_program_settings")

    @multiplex_program_settings.setter
    def multiplex_program_settings(self, value: Optional[pulumi.Input['MultiplexprogramMultiplexProgramSettingsArgs']]):
        pulumi.set(self, "multiplex_program_settings", value)

    @property
    @pulumi.getter(name="packetIdentifiersMap")
    def packet_identifiers_map(self) -> Optional[pulumi.Input['MultiplexprogramMultiplexProgramPacketIdentifiersMapArgs']]:
        """
        The packet identifier map for this multiplex program.
        """
        return pulumi.get(self, "packet_identifiers_map")

    @packet_identifiers_map.setter
    def packet_identifiers_map(self, value: Optional[pulumi.Input['MultiplexprogramMultiplexProgramPacketIdentifiersMapArgs']]):
        pulumi.set(self, "packet_identifiers_map", value)

    @property
    @pulumi.getter(name="pipelineDetails")
    def pipeline_details(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MultiplexprogramMultiplexProgramPipelineDetailArgs']]]]:
        """
        Contains information about the current sources for the specified program in the specified multiplex. Keep in mind that each multiplex pipeline connects to both pipelines in a given source channel (the channel identified by the program). But only one of those channel pipelines is ever active at one time.
        """
        return pulumi.get(self, "pipeline_details")

    @pipeline_details.setter
    def pipeline_details(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MultiplexprogramMultiplexProgramPipelineDetailArgs']]]]):
        pulumi.set(self, "pipeline_details", value)

    @property
    @pulumi.getter(name="preferredChannelPipeline")
    def preferred_channel_pipeline(self) -> Optional[pulumi.Input['MultiplexprogramPreferredChannelPipeline']]:
        """
        The settings for this multiplex program.
        """
        return pulumi.get(self, "preferred_channel_pipeline")

    @preferred_channel_pipeline.setter
    def preferred_channel_pipeline(self, value: Optional[pulumi.Input['MultiplexprogramPreferredChannelPipeline']]):
        pulumi.set(self, "preferred_channel_pipeline", value)

    @property
    @pulumi.getter(name="programName")
    def program_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the multiplex program.
        """
        return pulumi.get(self, "program_name")

    @program_name.setter
    def program_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "program_name", value)


class Multiplexprogram(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 multiplex_id: Optional[pulumi.Input[str]] = None,
                 multiplex_program_settings: Optional[pulumi.Input[Union['MultiplexprogramMultiplexProgramSettingsArgs', 'MultiplexprogramMultiplexProgramSettingsArgsDict']]] = None,
                 packet_identifiers_map: Optional[pulumi.Input[Union['MultiplexprogramMultiplexProgramPacketIdentifiersMapArgs', 'MultiplexprogramMultiplexProgramPacketIdentifiersMapArgsDict']]] = None,
                 pipeline_details: Optional[pulumi.Input[Sequence[pulumi.Input[Union['MultiplexprogramMultiplexProgramPipelineDetailArgs', 'MultiplexprogramMultiplexProgramPipelineDetailArgsDict']]]]] = None,
                 preferred_channel_pipeline: Optional[pulumi.Input['MultiplexprogramPreferredChannelPipeline']] = None,
                 program_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for AWS::MediaLive::Multiplexprogram

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] multiplex_id: The ID of the multiplex that the program belongs to.
        :param pulumi.Input[Union['MultiplexprogramMultiplexProgramSettingsArgs', 'MultiplexprogramMultiplexProgramSettingsArgsDict']] multiplex_program_settings: The settings for this multiplex program.
        :param pulumi.Input[Union['MultiplexprogramMultiplexProgramPacketIdentifiersMapArgs', 'MultiplexprogramMultiplexProgramPacketIdentifiersMapArgsDict']] packet_identifiers_map: The packet identifier map for this multiplex program.
        :param pulumi.Input[Sequence[pulumi.Input[Union['MultiplexprogramMultiplexProgramPipelineDetailArgs', 'MultiplexprogramMultiplexProgramPipelineDetailArgsDict']]]] pipeline_details: Contains information about the current sources for the specified program in the specified multiplex. Keep in mind that each multiplex pipeline connects to both pipelines in a given source channel (the channel identified by the program). But only one of those channel pipelines is ever active at one time.
        :param pulumi.Input['MultiplexprogramPreferredChannelPipeline'] preferred_channel_pipeline: The settings for this multiplex program.
        :param pulumi.Input[str] program_name: The name of the multiplex program.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[MultiplexprogramArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::MediaLive::Multiplexprogram

        :param str resource_name: The name of the resource.
        :param MultiplexprogramArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MultiplexprogramArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 multiplex_id: Optional[pulumi.Input[str]] = None,
                 multiplex_program_settings: Optional[pulumi.Input[Union['MultiplexprogramMultiplexProgramSettingsArgs', 'MultiplexprogramMultiplexProgramSettingsArgsDict']]] = None,
                 packet_identifiers_map: Optional[pulumi.Input[Union['MultiplexprogramMultiplexProgramPacketIdentifiersMapArgs', 'MultiplexprogramMultiplexProgramPacketIdentifiersMapArgsDict']]] = None,
                 pipeline_details: Optional[pulumi.Input[Sequence[pulumi.Input[Union['MultiplexprogramMultiplexProgramPipelineDetailArgs', 'MultiplexprogramMultiplexProgramPipelineDetailArgsDict']]]]] = None,
                 preferred_channel_pipeline: Optional[pulumi.Input['MultiplexprogramPreferredChannelPipeline']] = None,
                 program_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MultiplexprogramArgs.__new__(MultiplexprogramArgs)

            __props__.__dict__["multiplex_id"] = multiplex_id
            __props__.__dict__["multiplex_program_settings"] = multiplex_program_settings
            __props__.__dict__["packet_identifiers_map"] = packet_identifiers_map
            __props__.__dict__["pipeline_details"] = pipeline_details
            __props__.__dict__["preferred_channel_pipeline"] = preferred_channel_pipeline
            __props__.__dict__["program_name"] = program_name
            __props__.__dict__["channel_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["multiplexId", "programName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Multiplexprogram, __self__).__init__(
            'aws-native:medialive:Multiplexprogram',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Multiplexprogram':
        """
        Get an existing Multiplexprogram resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MultiplexprogramArgs.__new__(MultiplexprogramArgs)

        __props__.__dict__["channel_id"] = None
        __props__.__dict__["multiplex_id"] = None
        __props__.__dict__["multiplex_program_settings"] = None
        __props__.__dict__["packet_identifiers_map"] = None
        __props__.__dict__["pipeline_details"] = None
        __props__.__dict__["preferred_channel_pipeline"] = None
        __props__.__dict__["program_name"] = None
        return Multiplexprogram(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="channelId")
    def channel_id(self) -> pulumi.Output[str]:
        """
        The MediaLive channel associated with the program.
        """
        return pulumi.get(self, "channel_id")

    @property
    @pulumi.getter(name="multiplexId")
    def multiplex_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the multiplex that the program belongs to.
        """
        return pulumi.get(self, "multiplex_id")

    @property
    @pulumi.getter(name="multiplexProgramSettings")
    def multiplex_program_settings(self) -> pulumi.Output[Optional['outputs.MultiplexprogramMultiplexProgramSettings']]:
        """
        The settings for this multiplex program.
        """
        return pulumi.get(self, "multiplex_program_settings")

    @property
    @pulumi.getter(name="packetIdentifiersMap")
    def packet_identifiers_map(self) -> pulumi.Output[Optional['outputs.MultiplexprogramMultiplexProgramPacketIdentifiersMap']]:
        """
        The packet identifier map for this multiplex program.
        """
        return pulumi.get(self, "packet_identifiers_map")

    @property
    @pulumi.getter(name="pipelineDetails")
    def pipeline_details(self) -> pulumi.Output[Optional[Sequence['outputs.MultiplexprogramMultiplexProgramPipelineDetail']]]:
        """
        Contains information about the current sources for the specified program in the specified multiplex. Keep in mind that each multiplex pipeline connects to both pipelines in a given source channel (the channel identified by the program). But only one of those channel pipelines is ever active at one time.
        """
        return pulumi.get(self, "pipeline_details")

    @property
    @pulumi.getter(name="preferredChannelPipeline")
    def preferred_channel_pipeline(self) -> pulumi.Output[Optional['MultiplexprogramPreferredChannelPipeline']]:
        """
        The settings for this multiplex program.
        """
        return pulumi.get(self, "preferred_channel_pipeline")

    @property
    @pulumi.getter(name="programName")
    def program_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the multiplex program.
        """
        return pulumi.get(self, "program_name")

