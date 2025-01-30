# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ChannelInputType',
    'OriginEndpointAdMarkerDash',
    'OriginEndpointAdMarkerHls',
    'OriginEndpointCmafEncryptionMethod',
    'OriginEndpointContainerType',
    'OriginEndpointDashDrmSignaling',
    'OriginEndpointDashPeriodTrigger',
    'OriginEndpointDashSegmentTemplateFormat',
    'OriginEndpointDashUtcTimingMode',
    'OriginEndpointDrmSystem',
    'OriginEndpointEndpointErrorCondition',
    'OriginEndpointPresetSpeke20Audio',
    'OriginEndpointPresetSpeke20Video',
    'OriginEndpointScteFilter',
    'OriginEndpointTsEncryptionMethod',
]


class ChannelInputType(str, Enum):
    HLS = "HLS"
    CMAF = "CMAF"


class OriginEndpointAdMarkerDash(str, Enum):
    BINARY = "BINARY"
    XML = "XML"


class OriginEndpointAdMarkerHls(str, Enum):
    DATERANGE = "DATERANGE"


class OriginEndpointCmafEncryptionMethod(str, Enum):
    CENC = "CENC"
    CBCS = "CBCS"


class OriginEndpointContainerType(str, Enum):
    TS = "TS"
    CMAF = "CMAF"


class OriginEndpointDashDrmSignaling(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    REFERENCED = "REFERENCED"


class OriginEndpointDashPeriodTrigger(str, Enum):
    AVAILS = "AVAILS"
    DRM_KEY_ROTATION = "DRM_KEY_ROTATION"
    SOURCE_CHANGES = "SOURCE_CHANGES"
    SOURCE_DISRUPTIONS = "SOURCE_DISRUPTIONS"
    NONE = "NONE"


class OriginEndpointDashSegmentTemplateFormat(str, Enum):
    NUMBER_WITH_TIMELINE = "NUMBER_WITH_TIMELINE"


class OriginEndpointDashUtcTimingMode(str, Enum):
    HTTP_HEAD = "HTTP_HEAD"
    HTTP_ISO = "HTTP_ISO"
    HTTP_XSDATE = "HTTP_XSDATE"
    UTC_DIRECT = "UTC_DIRECT"


class OriginEndpointDrmSystem(str, Enum):
    CLEAR_KEY_AES128 = "CLEAR_KEY_AES_128"
    FAIRPLAY = "FAIRPLAY"
    PLAYREADY = "PLAYREADY"
    WIDEVINE = "WIDEVINE"
    IRDETO = "IRDETO"


class OriginEndpointEndpointErrorCondition(str, Enum):
    STALE_MANIFEST = "STALE_MANIFEST"
    INCOMPLETE_MANIFEST = "INCOMPLETE_MANIFEST"
    MISSING_DRM_KEY = "MISSING_DRM_KEY"
    SLATE_INPUT = "SLATE_INPUT"


class OriginEndpointPresetSpeke20Audio(str, Enum):
    PRESET_AUDIO1 = "PRESET_AUDIO_1"
    PRESET_AUDIO2 = "PRESET_AUDIO_2"
    PRESET_AUDIO3 = "PRESET_AUDIO_3"
    SHARED = "SHARED"
    UNENCRYPTED = "UNENCRYPTED"


class OriginEndpointPresetSpeke20Video(str, Enum):
    PRESET_VIDEO1 = "PRESET_VIDEO_1"
    PRESET_VIDEO2 = "PRESET_VIDEO_2"
    PRESET_VIDEO3 = "PRESET_VIDEO_3"
    PRESET_VIDEO4 = "PRESET_VIDEO_4"
    PRESET_VIDEO5 = "PRESET_VIDEO_5"
    PRESET_VIDEO6 = "PRESET_VIDEO_6"
    PRESET_VIDEO7 = "PRESET_VIDEO_7"
    PRESET_VIDEO8 = "PRESET_VIDEO_8"
    SHARED = "SHARED"
    UNENCRYPTED = "UNENCRYPTED"


class OriginEndpointScteFilter(str, Enum):
    SPLICE_INSERT = "SPLICE_INSERT"
    BREAK_ = "BREAK"
    PROVIDER_ADVERTISEMENT = "PROVIDER_ADVERTISEMENT"
    DISTRIBUTOR_ADVERTISEMENT = "DISTRIBUTOR_ADVERTISEMENT"
    PROVIDER_PLACEMENT_OPPORTUNITY = "PROVIDER_PLACEMENT_OPPORTUNITY"
    DISTRIBUTOR_PLACEMENT_OPPORTUNITY = "DISTRIBUTOR_PLACEMENT_OPPORTUNITY"
    PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY = "PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY"
    DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY = "DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY"
    PROGRAM = "PROGRAM"


class OriginEndpointTsEncryptionMethod(str, Enum):
    AES128 = "AES_128"
    SAMPLE_AES = "SAMPLE_AES"
