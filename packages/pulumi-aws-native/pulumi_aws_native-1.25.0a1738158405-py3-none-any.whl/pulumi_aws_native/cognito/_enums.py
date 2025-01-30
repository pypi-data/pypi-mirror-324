# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ManagedLoginBrandingCategoryType',
    'ManagedLoginBrandingColorModeType',
    'ManagedLoginBrandingExtensionType',
    'UserPoolTier',
]


class ManagedLoginBrandingCategoryType(str, Enum):
    FAVICON_ICO = "FAVICON_ICO"
    FAVICON_SVG = "FAVICON_SVG"
    EMAIL_GRAPHIC = "EMAIL_GRAPHIC"
    SMS_GRAPHIC = "SMS_GRAPHIC"
    AUTH_APP_GRAPHIC = "AUTH_APP_GRAPHIC"
    PASSWORD_GRAPHIC = "PASSWORD_GRAPHIC"
    PASSKEY_GRAPHIC = "PASSKEY_GRAPHIC"
    PAGE_HEADER_LOGO = "PAGE_HEADER_LOGO"
    PAGE_HEADER_BACKGROUND = "PAGE_HEADER_BACKGROUND"
    PAGE_FOOTER_LOGO = "PAGE_FOOTER_LOGO"
    PAGE_FOOTER_BACKGROUND = "PAGE_FOOTER_BACKGROUND"
    PAGE_BACKGROUND = "PAGE_BACKGROUND"
    FORM_BACKGROUND = "FORM_BACKGROUND"
    FORM_LOGO = "FORM_LOGO"
    IDP_BUTTON_ICON = "IDP_BUTTON_ICON"


class ManagedLoginBrandingColorModeType(str, Enum):
    LIGHT = "LIGHT"
    DARK = "DARK"
    DYNAMIC = "DYNAMIC"


class ManagedLoginBrandingExtensionType(str, Enum):
    ICO = "ICO"
    JPEG = "JPEG"
    PNG = "PNG"
    SVG = "SVG"
    WEBP = "WEBP"


class UserPoolTier(str, Enum):
    """
    The user pool [feature plan](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sign-in-feature-plans.html) , or tier. This parameter determines the eligibility of the user pool for features like managed login, access-token customization, and threat protection. Defaults to `ESSENTIALS` .
    """
    LITE = "LITE"
    ESSENTIALS = "ESSENTIALS"
    PLUS = "PLUS"
