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
from ._inputs import *

__all__ = ['BackupVaultArgs', 'BackupVault']

@pulumi.input_type
class BackupVaultArgs:
    def __init__(__self__, *,
                 access_policy: Optional[Any] = None,
                 backup_vault_name: Optional[pulumi.Input[str]] = None,
                 backup_vault_tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 encryption_key_arn: Optional[pulumi.Input[str]] = None,
                 lock_configuration: Optional[pulumi.Input['BackupVaultLockConfigurationTypeArgs']] = None,
                 notifications: Optional[pulumi.Input['BackupVaultNotificationObjectTypeArgs']] = None):
        """
        The set of arguments for constructing a BackupVault resource.
        :param Any access_policy: A resource-based policy that is used to manage access permissions on the target backup vault.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Backup::BackupVault` for more information about the expected schema for this property.
        :param pulumi.Input[str] backup_vault_name: The name of a logical container where backups are stored. Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] backup_vault_tags: The tags to assign to the backup vault.
        :param pulumi.Input[str] encryption_key_arn: A server-side encryption key you can specify to encrypt your backups from services that support full AWS Backup management; for example, `arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab` . If you specify a key, you must specify its ARN, not its alias. If you do not specify a key, AWS Backup creates a KMS key for you by default.
               
               To learn which AWS Backup services support full AWS Backup management and how AWS Backup handles encryption for backups from services that do not yet support full AWS Backup , see [Encryption for backups in AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/encryption.html)
        :param pulumi.Input['BackupVaultLockConfigurationTypeArgs'] lock_configuration: Configuration for [AWS Backup Vault Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html) .
        :param pulumi.Input['BackupVaultNotificationObjectTypeArgs'] notifications: The SNS event notifications for the specified backup vault.
        """
        if access_policy is not None:
            pulumi.set(__self__, "access_policy", access_policy)
        if backup_vault_name is not None:
            pulumi.set(__self__, "backup_vault_name", backup_vault_name)
        if backup_vault_tags is not None:
            pulumi.set(__self__, "backup_vault_tags", backup_vault_tags)
        if encryption_key_arn is not None:
            pulumi.set(__self__, "encryption_key_arn", encryption_key_arn)
        if lock_configuration is not None:
            pulumi.set(__self__, "lock_configuration", lock_configuration)
        if notifications is not None:
            pulumi.set(__self__, "notifications", notifications)

    @property
    @pulumi.getter(name="accessPolicy")
    def access_policy(self) -> Optional[Any]:
        """
        A resource-based policy that is used to manage access permissions on the target backup vault.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Backup::BackupVault` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "access_policy")

    @access_policy.setter
    def access_policy(self, value: Optional[Any]):
        pulumi.set(self, "access_policy", value)

    @property
    @pulumi.getter(name="backupVaultName")
    def backup_vault_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of a logical container where backups are stored. Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created.
        """
        return pulumi.get(self, "backup_vault_name")

    @backup_vault_name.setter
    def backup_vault_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backup_vault_name", value)

    @property
    @pulumi.getter(name="backupVaultTags")
    def backup_vault_tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags to assign to the backup vault.
        """
        return pulumi.get(self, "backup_vault_tags")

    @backup_vault_tags.setter
    def backup_vault_tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "backup_vault_tags", value)

    @property
    @pulumi.getter(name="encryptionKeyArn")
    def encryption_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        A server-side encryption key you can specify to encrypt your backups from services that support full AWS Backup management; for example, `arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab` . If you specify a key, you must specify its ARN, not its alias. If you do not specify a key, AWS Backup creates a KMS key for you by default.

        To learn which AWS Backup services support full AWS Backup management and how AWS Backup handles encryption for backups from services that do not yet support full AWS Backup , see [Encryption for backups in AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/encryption.html)
        """
        return pulumi.get(self, "encryption_key_arn")

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encryption_key_arn", value)

    @property
    @pulumi.getter(name="lockConfiguration")
    def lock_configuration(self) -> Optional[pulumi.Input['BackupVaultLockConfigurationTypeArgs']]:
        """
        Configuration for [AWS Backup Vault Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html) .
        """
        return pulumi.get(self, "lock_configuration")

    @lock_configuration.setter
    def lock_configuration(self, value: Optional[pulumi.Input['BackupVaultLockConfigurationTypeArgs']]):
        pulumi.set(self, "lock_configuration", value)

    @property
    @pulumi.getter
    def notifications(self) -> Optional[pulumi.Input['BackupVaultNotificationObjectTypeArgs']]:
        """
        The SNS event notifications for the specified backup vault.
        """
        return pulumi.get(self, "notifications")

    @notifications.setter
    def notifications(self, value: Optional[pulumi.Input['BackupVaultNotificationObjectTypeArgs']]):
        pulumi.set(self, "notifications", value)


class BackupVault(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_policy: Optional[Any] = None,
                 backup_vault_name: Optional[pulumi.Input[str]] = None,
                 backup_vault_tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 encryption_key_arn: Optional[pulumi.Input[str]] = None,
                 lock_configuration: Optional[pulumi.Input[Union['BackupVaultLockConfigurationTypeArgs', 'BackupVaultLockConfigurationTypeArgsDict']]] = None,
                 notifications: Optional[pulumi.Input[Union['BackupVaultNotificationObjectTypeArgs', 'BackupVaultNotificationObjectTypeArgsDict']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Backup::BackupVault

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param Any access_policy: A resource-based policy that is used to manage access permissions on the target backup vault.
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Backup::BackupVault` for more information about the expected schema for this property.
        :param pulumi.Input[str] backup_vault_name: The name of a logical container where backups are stored. Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] backup_vault_tags: The tags to assign to the backup vault.
        :param pulumi.Input[str] encryption_key_arn: A server-side encryption key you can specify to encrypt your backups from services that support full AWS Backup management; for example, `arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab` . If you specify a key, you must specify its ARN, not its alias. If you do not specify a key, AWS Backup creates a KMS key for you by default.
               
               To learn which AWS Backup services support full AWS Backup management and how AWS Backup handles encryption for backups from services that do not yet support full AWS Backup , see [Encryption for backups in AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/encryption.html)
        :param pulumi.Input[Union['BackupVaultLockConfigurationTypeArgs', 'BackupVaultLockConfigurationTypeArgsDict']] lock_configuration: Configuration for [AWS Backup Vault Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html) .
        :param pulumi.Input[Union['BackupVaultNotificationObjectTypeArgs', 'BackupVaultNotificationObjectTypeArgsDict']] notifications: The SNS event notifications for the specified backup vault.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[BackupVaultArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Backup::BackupVault

        :param str resource_name: The name of the resource.
        :param BackupVaultArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BackupVaultArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_policy: Optional[Any] = None,
                 backup_vault_name: Optional[pulumi.Input[str]] = None,
                 backup_vault_tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 encryption_key_arn: Optional[pulumi.Input[str]] = None,
                 lock_configuration: Optional[pulumi.Input[Union['BackupVaultLockConfigurationTypeArgs', 'BackupVaultLockConfigurationTypeArgsDict']]] = None,
                 notifications: Optional[pulumi.Input[Union['BackupVaultNotificationObjectTypeArgs', 'BackupVaultNotificationObjectTypeArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BackupVaultArgs.__new__(BackupVaultArgs)

            __props__.__dict__["access_policy"] = access_policy
            __props__.__dict__["backup_vault_name"] = backup_vault_name
            __props__.__dict__["backup_vault_tags"] = backup_vault_tags
            __props__.__dict__["encryption_key_arn"] = encryption_key_arn
            __props__.__dict__["lock_configuration"] = lock_configuration
            __props__.__dict__["notifications"] = notifications
            __props__.__dict__["backup_vault_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["backupVaultName", "encryptionKeyArn"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(BackupVault, __self__).__init__(
            'aws-native:backup:BackupVault',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BackupVault':
        """
        Get an existing BackupVault resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BackupVaultArgs.__new__(BackupVaultArgs)

        __props__.__dict__["access_policy"] = None
        __props__.__dict__["backup_vault_arn"] = None
        __props__.__dict__["backup_vault_name"] = None
        __props__.__dict__["backup_vault_tags"] = None
        __props__.__dict__["encryption_key_arn"] = None
        __props__.__dict__["lock_configuration"] = None
        __props__.__dict__["notifications"] = None
        return BackupVault(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessPolicy")
    def access_policy(self) -> pulumi.Output[Optional[Any]]:
        """
        A resource-based policy that is used to manage access permissions on the target backup vault.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Backup::BackupVault` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "access_policy")

    @property
    @pulumi.getter(name="backupVaultArn")
    def backup_vault_arn(self) -> pulumi.Output[str]:
        """
        An Amazon Resource Name (ARN) that uniquely identifies a backup vault; for example, `arn:aws:backup:us-east-1:123456789012:backup-vault:aBackupVault` .
        """
        return pulumi.get(self, "backup_vault_arn")

    @property
    @pulumi.getter(name="backupVaultName")
    def backup_vault_name(self) -> pulumi.Output[str]:
        """
        The name of a logical container where backups are stored. Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created.
        """
        return pulumi.get(self, "backup_vault_name")

    @property
    @pulumi.getter(name="backupVaultTags")
    def backup_vault_tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags to assign to the backup vault.
        """
        return pulumi.get(self, "backup_vault_tags")

    @property
    @pulumi.getter(name="encryptionKeyArn")
    def encryption_key_arn(self) -> pulumi.Output[Optional[str]]:
        """
        A server-side encryption key you can specify to encrypt your backups from services that support full AWS Backup management; for example, `arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab` . If you specify a key, you must specify its ARN, not its alias. If you do not specify a key, AWS Backup creates a KMS key for you by default.

        To learn which AWS Backup services support full AWS Backup management and how AWS Backup handles encryption for backups from services that do not yet support full AWS Backup , see [Encryption for backups in AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/encryption.html)
        """
        return pulumi.get(self, "encryption_key_arn")

    @property
    @pulumi.getter(name="lockConfiguration")
    def lock_configuration(self) -> pulumi.Output[Optional['outputs.BackupVaultLockConfigurationType']]:
        """
        Configuration for [AWS Backup Vault Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html) .
        """
        return pulumi.get(self, "lock_configuration")

    @property
    @pulumi.getter
    def notifications(self) -> pulumi.Output[Optional['outputs.BackupVaultNotificationObjectType']]:
        """
        The SNS event notifications for the specified backup vault.
        """
        return pulumi.get(self, "notifications")

