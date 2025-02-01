# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, String, Text
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class AccessLog(db.Model):
    __tablename__ = 'access_log'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 正常 ')
    method = db.Column(db.String(6), info='请求方式')
    params = db.Column(db.Text(collation='utf8mb4_0900_ai_ci'), info='请求参数 json {}')
    path = db.Column(db.String(50), info='请求路径')
    admin_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='admin.id 管理员ID')
    admin_name = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, info='admin.name 管理员账号')
    ip = db.Column(db.String(20), info='访问IP')



class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    username = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue(), info='用户名')
    password = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue(), info='密码 md5(md5(password) + salt)')
    salt = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue(), info='salt')
    role_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='角色id -1超管 0 无任何权限')
    store_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='-1 所有场所 0 无场所 - 场所id')
    branch_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='所属分公司 id -1 管理所有 0 无分公司权限')



class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    __table_args__ = (
        db.Index('i_date_hour', 'date', 'hour'),
        db.Index('i_store_device', 'store_id', 'device_id'),
        db.Index('i_user', 'user_id', 'id_type')
    )

    id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 在线 1 离线')
    store_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='场所id')
    device_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='设备id')
    ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='ip地址')
    wan_ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='外网ip地址')
    mac = db.Column(db.String(17, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='MAC地址')
    id_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 手机号 1 护照号 -1 无')
    user_id = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='用户identity')
    name = db.Column(db.String(200, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='设备名称')
    expired_time = db.Column(db.DateTime, info='认证过期时间')
    auth_time = db.Column(db.DateTime, info='认证时间')
    auth_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 未认证 1 已认证')
    msg_version = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), server_default=db.FetchedValue(), info='消息的版本号')
    auth_type = db.Column(db.Integer, server_default=db.FetchedValue(), info='认证类型 0 其他 1 短信认证 2 辅助认证')
    platform = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 未知 1 百卓 2 任子行')
    date = db.Column(db.Date, nullable=False, info='日期')
    hour = db.Column(db.Integer, nullable=False, info='小时')
    is_success = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='1 成功 1 失败')



class AuthCodeLog(db.Model):
    __tablename__ = 'auth_code_log'
    __table_args__ = (
        db.Index('i_store_device', 'store_id', 'device_id'),
        db.Index('i_user', 'user_id', 'id_type')
    )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    store_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='场所id')
    device_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='设备id')
    ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='ip地址')
    wan_ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='外网ip地址')
    mac = db.Column(db.String(17, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='MAC地址')
    id_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 手机号 1 护照号')
    user_id = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='用户identity')
    name = db.Column(db.String(200, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='设备名称')
    auth_code = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='认证code')
    admin_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='管理员id号 0: 默认本人')
    mobile = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), server_default=db.FetchedValue(), info='管理员手机号')
    date = db.Column(db.Date, nullable=False, index=True, info='日期')
    hour = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='小时 0 - 23')



class AuthLog(db.Model):
    __tablename__ = 'auth_log'
    __table_args__ = (
        db.Index('i_user', 'user_id', 'id_type'),
    )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    store_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='场所id')
    device_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='设备id')
    ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='ip地址')
    wan_ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='外网ip地址')
    mac = db.Column(db.String(17, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='MAC地址')
    id_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 手机号 1 护照号')
    user_id = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='用户identity')
    auth_code = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), server_default=db.FetchedValue(), info='认证 code')
    name = db.Column(db.String(200, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='设备名称')
    expired_time = db.Column(db.DateTime, nullable=False, index=True, info='认证过期时间')
    auth_time = db.Column(db.DateTime, info='认证时间')
    date = db.Column(db.Date, nullable=False, index=True, info='认证日期')
    hour = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='小时 0 - 23')
    auth_type = db.Column(db.Integer, server_default=db.FetchedValue(), info='认证类型 0 其他 1 短信认证 2 辅助认证')



class AuthOnline(db.Model):
    __tablename__ = 'auth_online'
    __table_args__ = (
        db.Index('i_user', 'user_id', 'id_type'),
        db.Index('u_store_mac', 'store_id', 'mac')
    )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='1 已认证')
    store_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='场所id')
    ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='ip地址')
    wan_ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='外网ip地址')
    mac = db.Column(db.String(17, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='MAC地址')
    id_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 手机号 1 护照号')
    user_id = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='用户identity')
    auth_code = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), server_default=db.FetchedValue(), info='认证 code')
    name = db.Column(db.String(200, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='设备名称')
    expired_time = db.Column(db.DateTime, nullable=False, index=True, info='认证过期时间')
    auth_time = db.Column(db.DateTime, info='认证时间')
    auth_type = db.Column(db.Integer, server_default=db.FetchedValue(), info='认证类型 0 其他 1 短信认证 2 辅助认证')



class Blackwhite(db.Model):
    __tablename__ = 'blackwhite'
    __table_args__ = (
        db.Index('i_type', 'type', 'range'),
    )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 黑名单 1 白名单')
    range = db.Column(db.Integer, nullable=False, info='范围 0 内网(MAC) 1 外网(IP或域名) ')
    text = db.Column(db.String(200, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    store_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='场所id')



class Branch(db.Model):
    __tablename__ = 'branch'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    name = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='分公司名称')
    regions = db.Column(db.String(2000), nullable=False, server_default=db.FetchedValue(), info='管辖地区 {} json region_code')



class ClientInfo(db.Model):
    __tablename__ = 'client_info'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    mac = db.Column(db.String(17), nullable=False, unique=True, server_default=db.FetchedValue(), info='MAC地址')
    id_type = db.Column(db.Integer, nullable=False, info='id 类型 0 手机号 1 护照号')
    user_id = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='用户id')



class Config(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    key = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue(), info='配置key')
    val = db.Column(db.Text(collation='utf8mb4_0900_ai_ci'), nullable=False, info='配置内容')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0:plain 1: json')



class ConfigCopy1(db.Model):
    __tablename__ = 'config_copy1'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    key = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue(), info='配置key')
    val = db.Column(db.Text(collation='utf8mb4_0900_ai_ci'), nullable=False, info='配置内容')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0:plain 1: json')



class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue(), info='注册时间')
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 1 异常 9 禁用')
    store_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='所属场所')
    name = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='设备名 酒店为房间号 或SSID名字')
    mac = db.Column(db.String(17), nullable=False, unique=True, server_default=db.FetchedValue(), info='mac地址')
    sn = db.Column(db.String(40, 'utf8mb4_0900_ai_ci'), index=True, server_default=db.FetchedValue(), info='设备号')
    remark = db.Column(db.String(200), info='备注')
    loid = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='设备 loid 唯一')
    heartbeat_time = db.Column(db.DateTime, nullable=False, info='心跳时间')
    is_auth = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否开启认证 0 未开启 1 开启 -1 未配置(使用场所配置)')
    ip = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='IP地址')
    info = db.Column(db.String(2000), info='设备信息 传上来的原始信息')
    version = db.Column(db.String(20), nullable=False, index=True, server_default=db.FetchedValue(), info='插件版本号')
    ssid = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='SSID')
    password = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'), info='SSID密码')
    bssid = db.Column(db.String(2000, 'utf8mb4_0900_ai_ci'), info='BSSID')
    platform = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 未知 1 百卓 2 任子行')
    msg_version = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='消息版本号')
    device_model = db.Column(db.String(60, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='设备型号')



class DeviceErrorReport(db.Model):
    __tablename__ = 'device_error_report'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    device_id = db.Column(db.Integer, nullable=False, info='设备id号')
    raw_data = db.Column(db.Text, info='上报信息')



class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    name = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue(), info='菜单名')
    url = db.Column(db.String(200, 'utf8mb4_0900_ai_ci'), server_default=db.FetchedValue(), info='链接')
    parent_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='父级菜单id')
    depth = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='菜单depth')
    icon = db.Column(db.String(200), info='图标')



class Model(db.Model):
    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    name = db.Column(db.String(50), unique=True, info='设备类型名称')



class Online(db.Model):
    __tablename__ = 'online'
    __table_args__ = (
        db.Index('i_store_device', 'store_id', 'device_id'),
        db.Index('i_user', 'user_id', 'id_type'),
        db.Index('u_device_mac', 'device_id', 'mac')
    )

    id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 在线 1 离线')
    store_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='场所id')
    device_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='设备id')
    ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='ip地址')
    wan_ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='外网ip地址')
    mac = db.Column(db.String(17, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='MAC地址')
    id_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 手机号 1 护照号 -1 无')
    user_id = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='用户identity')
    name = db.Column(db.String(200, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='设备名称')
    expired_time = db.Column(db.DateTime, info='认证过期时间')
    auth_time = db.Column(db.DateTime, info='认证时间')
    auth_status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 未认证 1 已认证')
    msg_version = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), server_default=db.FetchedValue(), info='消息的版本号')
    auth_type = db.Column(db.Integer, server_default=db.FetchedValue(), info='认证类型 0 其他 1 短信认证 2 辅助认证')
    admin_id = db.Column(db.Integer, info='辅助认证管理员ID')



class OnlineLog(db.Model):
    __tablename__ = 'online_log'
    __table_args__ = (
        db.Index('i_date_hour', 'date', 'hour'),
    )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 在线 1 离线')
    mac = db.Column(db.String(17), nullable=False, index=True, server_default=db.FetchedValue(), info='MAC地址')
    date = db.Column(db.Date, nullable=False, info='记录日期')
    hour = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='小时 0 - 23')



class PageTemplate(db.Model):
    __tablename__ = 'page_template'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    name = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'), server_default=db.FetchedValue(), info='模板名称')
    logo_title = db.Column(db.String(255), server_default=db.FetchedValue(), info='logo标题')
    logo = db.Column(db.String(255), info='logo地址')
    banner = db.Column(db.String(255), info='banner地址')
    banner_title = db.Column(db.String(255), info='banner标题')
    banner_subtitle = db.Column(db.String(255), info='banner副标题')
    store_id = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue(), info='-1 所有场所 0 无场所 - 场所id')
    branch_id = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue(), info='所属分公司 id -1 管理所有 0 无分公司权限')
    is_default = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否是默认模板 0 否 1 是')
    loadin = db.Column(db.String(255), info='认证前载入图片')



class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    name = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue(), info='权限名')
    path = db.Column(db.String(80), nullable=False, unique=True, server_default=db.FetchedValue(), info='请求路径')
    editable = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否是编辑地址')



class Region(db.Model):
    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 省 1 市 2 区 3 街道')
    name = db.Column(db.String(40), nullable=False, index=True, server_default=db.FetchedValue(), info='名称')
    parent_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='上级id')
    code = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='街道code')
    spell = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='拼音')



class Release(db.Model):
    __tablename__ = 'release'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 未发布 1 已发布')
    version = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='版本号')
    serial_number = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='版本序号')
    filename = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='文件')
    md5sum = db.Column(db.String(80), nullable=False, server_default=db.FetchedValue(), info='md5值')
    device_model = db.Column(db.String(20), nullable=False, info='设备型号')
    change_log = db.Column(db.String(2000, 'utf8mb4_0900_ai_ci'), info='更新日志')



class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    name = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue(), info='角色名称')
    permissions = db.Column(db.String(2000), server_default=db.FetchedValue(), info='权限id json []')
    menus = db.Column(db.String(2000), info='菜单 id json []')
    readonly = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='只读 0 否 1 是')



class SmsLog(db.Model):
    __tablename__ = 'sms_log'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    type = db.Column(db.Integer, nullable=False, info='短信类型 0 其他 1 短信认证 2 APP登录 ')
    mobile = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, info='接受手机号码')
    store_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='场所ID')
    device_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='设备ID')
    content = db.Column(db.String(200, 'utf8mb4_0900_ai_ci'), info='短信内容')
    ip = db.Column(db.String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='ip地址')
    auth_code = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, info='短信验证码')
    date = db.Column(db.Date, nullable=False, info='日期')
    hour = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='小时 0 - 23')



class Stat(db.Model):
    __tablename__ = 'stats'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    date = db.Column(db.Date, nullable=False, index=True, info='统计日期')
    store_total = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='场所数量')
    device_total = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='设备数据量')
    online_total = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='在线数量')
    branch_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='分公司id 0 统计所有')



class StatsAudit(db.Model):
    __tablename__ = 'stats_audit'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    date = db.Column(db.Date, nullable=False, index=True, info='日期')
    hour = db.Column(db.Integer, nullable=False, index=True, info='小时')
    platform = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 未知 1 百卓 2 任子行')
    count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='发送数量')
    failure = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='失败数量')



class StatsOnline(db.Model):
    __tablename__ = 'stats_online'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    date = db.Column(db.Date, nullable=False, index=True, info='统计日期')
    total = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='数量')
    hour = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='小时 0 - 23')
    branch_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='分公司id 0 所有')



class Store(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    name = db.Column(db.String(200, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='场所名')
    address = db.Column(db.String(1000, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='地址')
    region_code = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=db.FetchedValue(), info='地址区域编码')
    code = db.Column(db.String(40, 'utf8mb4_0900_ai_ci'), nullable=False, unique=True, server_default=db.FetchedValue(), info='场所编码')
    lat = db.Column(db.Numeric(10, 7), nullable=False, server_default=db.FetchedValue(), info='纬度')
    lng = db.Column(db.Numeric(10, 7), nullable=False, server_default=db.FetchedValue(), info='经度')
    service_type = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='服务类型')
    business_type = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='经营类型')
    legal_person = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='法人')
    legal_person_id_type = db.Column(db.String(40, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='法人身份类型')
    legal_person_id = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='法人身份证件号')
    legal_person_tel = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='法人联系电话')
    is_auth = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否开启认证 0 未开启 1 开启')
    ssid = db.Column(db.String(80), info='ssid配置')
    ssid_password = db.Column(db.String(100), info='ssid密码')
    template_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='认证页面模板')



class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = (
        db.Index('i_user', 'user_id', 'user_type'),
    )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='0 正常 9 禁用')
    user_id = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='用户id  手机号 或者 其他')
    user_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='0 身份证 1 护照号')
    mac = db.Column(db.String(17), nullable=False, unique=True, server_default=db.FetchedValue(), info='mac地址')



class StoreExt(db.Model):
    __tablename__ = 'store_ext'

    store_id = db.Column(db.Integer, primary_key=True)
    black_mode = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='黑名单模式 0 不开启 1 开启')
    white_prefix = db.Column(db.String(1000), server_default=db.FetchedValue(), info='白名单前缀 多个逗号隔开')
    expires = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='认证过期时间 单位：s')



class Whitelist(db.Model):
    __tablename__ = 'whitelist'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    mac = db.Column(db.String(17, 'utf8mb4_general_ci'), nullable=False, index=True, info='mac地址')
    store_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='场所ID号')
    device_id = db.Column(db.Integer, nullable=False, index=True, info='设备ID号')
    source = db.Column(db.Integer, nullable=False, index=True, info='0 手动 1 自动 21 任子行 22 百卓')



class WhitelistPrefix(db.Model):
    __tablename__ = 'whitelist_prefix'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    prefix = db.Column(db.String(17, 'utf8mb4_general_ci'), nullable=False, index=True, info='mac地址前缀')
    store_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='场所ID号')
    tags = db.Column(db.String(400, 'utf8mb4_general_ci'), nullable=False, server_default=db.FetchedValue(), info='标签 逗号隔开')