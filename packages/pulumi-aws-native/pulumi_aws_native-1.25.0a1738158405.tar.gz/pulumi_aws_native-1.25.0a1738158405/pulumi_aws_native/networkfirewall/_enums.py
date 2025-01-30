# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'FirewallPolicyOverrideAction',
    'FirewallPolicyRuleOrder',
    'FirewallPolicyStreamExceptionPolicy',
    'LoggingConfigurationLogDestinationConfigLogDestinationType',
    'LoggingConfigurationLogDestinationConfigLogType',
    'RuleGroupGeneratedRulesType',
    'RuleGroupHeaderDirection',
    'RuleGroupHeaderProtocol',
    'RuleGroupRuleOrder',
    'RuleGroupStatefulRuleAction',
    'RuleGroupTargetType',
    'RuleGroupTcpFlag',
    'RuleGroupTypeEnum',
    'TlsInspectionConfigurationRevokedStatusAction',
    'TlsInspectionConfigurationUnknownStatusAction',
]


class FirewallPolicyOverrideAction(str, Enum):
    DROP_TO_ALERT = "DROP_TO_ALERT"


class FirewallPolicyRuleOrder(str, Enum):
    DEFAULT_ACTION_ORDER = "DEFAULT_ACTION_ORDER"
    STRICT_ORDER = "STRICT_ORDER"


class FirewallPolicyStreamExceptionPolicy(str, Enum):
    DROP = "DROP"
    CONTINUE_ = "CONTINUE"
    REJECT = "REJECT"


class LoggingConfigurationLogDestinationConfigLogDestinationType(str, Enum):
    """
    The type of storage destination to send these logs to. You can send logs to an Amazon S3 bucket, a CloudWatch log group, or a Firehose delivery stream.
    """
    S3 = "S3"
    CLOUD_WATCH_LOGS = "CloudWatchLogs"
    KINESIS_DATA_FIREHOSE = "KinesisDataFirehose"


class LoggingConfigurationLogDestinationConfigLogType(str, Enum):
    """
    The type of log to record. You can record the following types of logs from your Network Firewall stateful engine.

    - `ALERT` - Logs for traffic that matches your stateful rules and that have an action that sends an alert. A stateful rule sends alerts for the rule actions DROP, ALERT, and REJECT. For more information, see the `StatefulRule` property.
    - `FLOW` - Standard network traffic flow logs. The stateful rules engine records flow logs for all network traffic that it receives. Each flow log record captures the network flow for a specific standard stateless rule group.
    - `TLS` - Logs for events that are related to TLS inspection. For more information, see [Inspecting SSL/TLS traffic with TLS inspection configurations](https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection-configurations.html) in the *Network Firewall Developer Guide* .
    """
    ALERT = "ALERT"
    FLOW = "FLOW"
    TLS = "TLS"


class RuleGroupGeneratedRulesType(str, Enum):
    ALLOWLIST = "ALLOWLIST"
    DENYLIST = "DENYLIST"


class RuleGroupHeaderDirection(str, Enum):
    """
    The direction of traffic flow to inspect. If set to `ANY` , the inspection matches bidirectional traffic, both from the source to the destination and from the destination to the source. If set to `FORWARD` , the inspection only matches traffic going from the source to the destination.
    """
    FORWARD = "FORWARD"
    ANY = "ANY"


class RuleGroupHeaderProtocol(str, Enum):
    """
    The protocol to inspect for. To specify all, you can use `IP` , because all traffic on AWS and on the internet is IP.
    """
    IP = "IP"
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    HTTP = "HTTP"
    FTP = "FTP"
    TLS = "TLS"
    SMB = "SMB"
    DNS = "DNS"
    DCERPC = "DCERPC"
    SSH = "SSH"
    SMTP = "SMTP"
    IMAP = "IMAP"
    MSN = "MSN"
    KRB5 = "KRB5"
    IKEV2 = "IKEV2"
    TFTP = "TFTP"
    NTP = "NTP"
    DHCP = "DHCP"


class RuleGroupRuleOrder(str, Enum):
    DEFAULT_ACTION_ORDER = "DEFAULT_ACTION_ORDER"
    STRICT_ORDER = "STRICT_ORDER"


class RuleGroupStatefulRuleAction(str, Enum):
    """
    Defines what Network Firewall should do with the packets in a traffic flow when the flow matches the stateful rule criteria. For all actions, Network Firewall performs the specified action and discontinues stateful inspection of the traffic flow.

    The actions for a stateful rule are defined as follows:

    - *PASS* - Permits the packets to go to the intended destination.
    - *DROP* - Blocks the packets from going to the intended destination and sends an alert log message, if alert logging is configured in the `Firewall` `LoggingConfiguration` .
    - *REJECT* - Drops traffic that matches the conditions of the stateful rule and sends a TCP reset packet back to sender of the packet. A TCP reset packet is a packet with no payload and a `RST` bit contained in the TCP header flags. `REJECT` is available only for TCP traffic.
    - *ALERT* - Permits the packets to go to the intended destination and sends an alert log message, if alert logging is configured in the `Firewall` `LoggingConfiguration` .

    You can use this action to test a rule that you intend to use to drop traffic. You can enable the rule with `ALERT` action, verify in the logs that the rule is filtering as you want, then change the action to `DROP` .
    - *REJECT* - Drops TCP traffic that matches the conditions of the stateful rule, and sends a TCP reset packet back to sender of the packet. A TCP reset packet is a packet with no payload and a `RST` bit contained in the TCP header flags. Also sends an alert log mesage if alert logging is configured in the `Firewall` `LoggingConfiguration` .

    `REJECT` isn't currently available for use with IMAP and FTP protocols.
    """
    PASS_ = "PASS"
    DROP = "DROP"
    ALERT = "ALERT"
    REJECT = "REJECT"


class RuleGroupTargetType(str, Enum):
    TLS_SNI = "TLS_SNI"
    HTTP_HOST = "HTTP_HOST"


class RuleGroupTcpFlag(str, Enum):
    FIN = "FIN"
    SYN = "SYN"
    RST = "RST"
    PSH = "PSH"
    ACK = "ACK"
    URG = "URG"
    ECE = "ECE"
    CWR = "CWR"


class RuleGroupTypeEnum(str, Enum):
    """
    Indicates whether the rule group is stateless or stateful. If the rule group is stateless, it contains
    stateless rules. If it is stateful, it contains stateful rules.
    """
    STATELESS = "STATELESS"
    STATEFUL = "STATEFUL"


class TlsInspectionConfigurationRevokedStatusAction(str, Enum):
    PASS_ = "PASS"
    DROP = "DROP"
    REJECT = "REJECT"


class TlsInspectionConfigurationUnknownStatusAction(str, Enum):
    PASS_ = "PASS"
    DROP = "DROP"
    REJECT = "REJECT"
