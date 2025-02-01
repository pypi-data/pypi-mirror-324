#!/usr/bin/env python
# coding: utf-8

import json
import time
from enum import Enum, unique
from json.encoder import JSONEncoder
from decimal import Decimal

@unique
class ServerTopic(Enum):
    """
    服务器subscribe topics
    # svcCmd/$ver/$Device
    # svcCfg/$ver/$Device
    # devStatus/$ver/$Device
    # devAuthCheck/$ver/$Device
    # bootstrap/$ver/$Device
    # errReport/$ver/$Device
    """

    S_SVC_CMD = "svcCmd"
    S_SVC_CFG = "svcCfg"
    S_DEV_STATUS = "devStatus"
    S_DEV_AUTH_CHECK = "devAuthCheck"
    S_BOOTSTRAP = "bootstrap"
    S_ERR_REPORT = "errReport"


@unique
class PluginTopic(Enum):
    """
    插件subscribe topics
    # $Device/bootstrap/$ver
    # $Device/devCmd/$ver
    # ($Device | $StoreID | $BranchID | Global)/devAuthCfg/$ver
    # ($Device | $StoreID | $BranchID | Global)/devAuthKick/$ver
    # ($Device | $StoreID | $BranchID | Global)/devAuthCheck/$ver
    # ($Device | $StoreID | $BranchID | Global)/devWifiCfg/$ver
    # ($Device | $StoreID | $BranchID | Global)/svcCfg/$ver
    # ($Device | $StoreID | $BranchID | Global)/svcCmd/$ver
    """

    P_BOOTSTRAP = "bootstrap"
    P_DEV_CMD = "devCmd"
    P_DEV_AUTH_CFG = "devAuthCfg"
    P_DEV_AUTH_KICK = "devAuthKick"
    P_DEV_AUTH_CHECK = "devAuthCheck"
    P_DEV_WIFI_CFG = "devWifiCfg"
    P_SVC_CFG = "svcCfg"
    P_SVC_CMD = "svcCmd"


@unique
class Range(Enum):
    DEVICE = "Device"
    STORE = "Store"
    BRANCH = "Branch"
    GLOBAL = "Global"


class Message(object):
    """
    {
        "id": "",  // 处理消息队列ID 系统自定义
        "ts": "",  // unix timestamp
        "data": "",  // 收到的消息内容
        "version": "",  // 版本号
        "cmd": "",  // 命令
        "range": "",  // 消息的范围类型：Device Store Branch Global 四种 订阅的消息默认Device
        "value": "",  // 消息范围值：Device的时候为MAC地址大写(无冒号和中线) 其他为S+StoreID B+BranchID Global
    }
    """

    id = ""
    ts = ""
    data = ""
    version = ""
    cmd = ""
    range = Range.DEVICE
    value = ""

    def __init__(
        self,
        id="",
        ts="",
        data="",
        version="",
        cmd="",
        range=Range.DEVICE,
        value="",
    ):
        self.id = id
        self.ts = ts or str(int(time.time()))
        self.data = data
        self.version = version
        self.cmd = cmd
        self.range = range if isinstance(range, Range) else Range(range)
        self.value = value

    def __str__(self):
        return json.dumps(self.__dict__, cls=CustomJSONEncoder, ensure_ascii=False)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.__dict__
        elif isinstance(obj, Range):
            return obj.value
        elif isinstance(obj, Decimal):
            return str(obj)

        return JSONEncoder.default(self, obj)


class MQTTTopic(object):
    def __init__(self, topic: PluginTopic, qos=1, retain=False):
        self.topic = topic
        self.qos = qos
        self.retain = retain


class DeviceModel(Enum):
    MODEL_H10G_12 = "H10G-12"
    MODEL_M21G = "M21G"


class AuthType(Enum):
    AUTH_TYPE_OTHER = '其他'
    AUTH_TYPE_SMS = '短信'
    AUTH_TYPE_ASSISTANT = '辅助'
    AUTH_TYPE_MP = '小程序'


class AuthTypeIds(Enum):
    AUTH_TYPE_OTHER = 0
    AUTH_TYPE_SMS = 1
    AUTH_TYPE_ASSISTANT = 2
    AUTH_TYPE_MP = 3


class SmsType(Enum):
    SMS_TYPE_OTHER = '其他'
    SMS_TYPE_SMS_AUTH = '短信认证'
    SMS_TYPE_APP_LOGIN = 'APP登录'


class SmsTypeIds(Enum):
    SMS_TYPE_OTHER = 0
    SMS_TYPE_SMS_AUTH = 1
    SMS_TYPE_APP_LOGIN = 2


MODELS = {1: DeviceModel.MODEL_H10G_12, 2: DeviceModel.MODEL_M21G}
MODELS_MAP = {DeviceModel.MODEL_H10G_12: 1, DeviceModel.MODEL_M21G: 2}

AUTHTYPE_MAP = {AuthTypeIds.AUTH_TYPE_OTHER.value: AuthType.AUTH_TYPE_OTHER, AuthTypeIds.AUTH_TYPE_SMS.value: AuthType.AUTH_TYPE_SMS, AuthTypeIds.AUTH_TYPE_ASSISTANT.value: AuthType.AUTH_TYPE_ASSISTANT}
SMSTYPE_MAP = {SmsTypeIds.SMS_TYPE_OTHER.value: SmsType.SMS_TYPE_OTHER, SmsTypeIds.SMS_TYPE_SMS_AUTH.value: SmsType.SMS_TYPE_SMS_AUTH, SmsTypeIds.SMS_TYPE_APP_LOGIN.value: SmsType.SMS_TYPE_APP_LOGIN}
AUTHTYPE_TO_SMSTYPE = {
    AuthTypeIds.AUTH_TYPE_OTHER.value: SmsTypeIds.SMS_TYPE_OTHER,
    AuthTypeIds.AUTH_TYPE_SMS.value: SmsTypeIds.SMS_TYPE_SMS_AUTH
}

plugin_topic_fmt = "%s/%s/%s"
plugin_topics = {
    PluginTopic.P_BOOTSTRAP: MQTTTopic(PluginTopic.P_BOOTSTRAP),
    PluginTopic.P_DEV_CMD: MQTTTopic(PluginTopic.P_DEV_CMD),
    PluginTopic.P_DEV_AUTH_CFG: MQTTTopic(PluginTopic.P_DEV_AUTH_CFG, retain=True),
    PluginTopic.P_DEV_AUTH_KICK: MQTTTopic(PluginTopic.P_DEV_AUTH_KICK),
    PluginTopic.P_DEV_AUTH_CHECK: MQTTTopic(PluginTopic.P_DEV_AUTH_CHECK),
    PluginTopic.P_DEV_WIFI_CFG: MQTTTopic(PluginTopic.P_DEV_WIFI_CFG),
    PluginTopic.P_SVC_CFG: MQTTTopic(PluginTopic.P_SVC_CFG),
    PluginTopic.P_SVC_CMD: MQTTTopic(PluginTopic.P_SVC_CMD),
}

server_topic_fmt = "$share/spider/%s/#"
server_topics = [
    ServerTopic.S_SVC_CMD,
    ServerTopic.S_SVC_CFG,
    ServerTopic.S_DEV_STATUS,
    ServerTopic.S_DEV_AUTH_CHECK,
    ServerTopic.S_BOOTSTRAP,
    ServerTopic.S_ERR_REPORT,
]

MQ_PENDING_NAME = "MQ_PENDING"
MQ_WAITING_NAME = "MQ_WAITING"
MQ_TEST = "__TEST__"
MQ_GROUP = "SPIDER_GROUP"
MQ_FIELD = "data"

KEY_CONFIG = "TABLE::CONFIG::%s"
KEY_DEVICE = "TABLE::DEVICE"
KEY_DEVICE_MAC = "TABLE::DEVICE::MAC"
KEY_STORE = "TABLE::STORE"

KEY_CODE = "CODE::%s::%s"
KEY_SMS = "CODE::%s"
KEY_ONLINE = "USER::%s:%s"

TOPIC_STORE = "S%s"
TOPIC_BRANCH = "B%s"

QUEUE_AUDIT = "QUEUE_AUDIT"
