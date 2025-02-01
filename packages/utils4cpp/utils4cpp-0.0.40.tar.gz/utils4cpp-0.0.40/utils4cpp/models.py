# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, MetaData, Numeric, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class AccessLog(Base):
    __tablename__ = 'access_log'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 正常 ')
    method = Column(String(6), info='请求方式')
    params = Column(Text(collation='utf8mb4_0900_ai_ci'), info='请求参数 json {}')
    path = Column(String(50), info='请求路径')
    admin_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='admin.id 管理员ID')
    admin_name = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, info='admin.name 管理员账号')
    ip = Column(String(20), info='访问IP')



class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    username = Column(String(20), nullable=False, unique=True, server_default=FetchedValue(), info='用户名')
    password = Column(String(40), nullable=False, server_default=FetchedValue(), info='密码 md5(md5(password) + salt)')
    salt = Column(String(10), nullable=False, server_default=FetchedValue(), info='salt')
    role_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='角色id -1超管 0 无任何权限')
    store_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='-1 所有场所 0 无场所 - 场所id')
    branch_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='所属分公司 id -1 管理所有 0 无分公司权限')



class AuditLog(Base):
    __tablename__ = 'audit_log'
    __table_args__ = (
        Index('i_date_hour', 'date', 'hour'),
        Index('i_store_device', 'store_id', 'device_id'),
        Index('i_user', 'user_id', 'id_type')
    )

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 在线 1 离线')
    store_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='场所id')
    device_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='设备id')
    ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='ip地址')
    wan_ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='外网ip地址')
    mac = Column(String(17, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='MAC地址')
    id_type = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 手机号 1 护照号 -1 无')
    user_id = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='用户identity')
    name = Column(String(200, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='设备名称')
    expired_time = Column(DateTime, info='认证过期时间')
    auth_time = Column(DateTime, info='认证时间')
    auth_status = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 未认证 1 已认证')
    msg_version = Column(String(10, 'utf8mb4_0900_ai_ci'), server_default=FetchedValue(), info='消息的版本号')
    auth_type = Column(Integer, server_default=FetchedValue(), info='认证类型 0 其他 1 短信认证 2 辅助认证')
    platform = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 未知 1 百卓 2 任子行')
    date = Column(Date, nullable=False, info='日期')
    hour = Column(Integer, nullable=False, info='小时')
    is_success = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='1 成功 1 失败')



class AuthCodeLog(Base):
    __tablename__ = 'auth_code_log'
    __table_args__ = (
        Index('i_store_device', 'store_id', 'device_id'),
        Index('i_user', 'user_id', 'id_type')
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue())
    store_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='场所id')
    device_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='设备id')
    ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='ip地址')
    wan_ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='外网ip地址')
    mac = Column(String(17, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='MAC地址')
    id_type = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 手机号 1 护照号')
    user_id = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='用户identity')
    name = Column(String(200, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='设备名称')
    auth_code = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='认证code')
    admin_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='管理员id号 0: 默认本人')
    mobile = Column(String(20, 'utf8mb4_0900_ai_ci'), server_default=FetchedValue(), info='管理员手机号')
    date = Column(Date, nullable=False, index=True, info='日期')
    hour = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='小时 0 - 23')



class AuthLog(Base):
    __tablename__ = 'auth_log'
    __table_args__ = (
        Index('i_user', 'user_id', 'id_type'),
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue())
    store_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='场所id')
    device_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='设备id')
    ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='ip地址')
    wan_ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='外网ip地址')
    mac = Column(String(17, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='MAC地址')
    id_type = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 手机号 1 护照号')
    user_id = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='用户identity')
    auth_code = Column(String(20, 'utf8mb4_0900_ai_ci'), server_default=FetchedValue(), info='认证 code')
    name = Column(String(200, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='设备名称')
    expired_time = Column(DateTime, nullable=False, index=True, info='认证过期时间')
    auth_time = Column(DateTime, info='认证时间')
    date = Column(Date, nullable=False, index=True, info='认证日期')
    hour = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='小时 0 - 23')
    auth_type = Column(Integer, server_default=FetchedValue(), info='认证类型 0 其他 1 短信认证 2 辅助认证')



class AuthOnline(Base):
    __tablename__ = 'auth_online'
    __table_args__ = (
        Index('i_user', 'user_id', 'id_type'),
        Index('u_store_mac', 'store_id', 'mac')
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='1 已认证')
    store_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='场所id')
    ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='ip地址')
    wan_ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='外网ip地址')
    mac = Column(String(17, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='MAC地址')
    id_type = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 手机号 1 护照号')
    user_id = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='用户identity')
    auth_code = Column(String(20, 'utf8mb4_0900_ai_ci'), server_default=FetchedValue(), info='认证 code')
    name = Column(String(200, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='设备名称')
    expired_time = Column(DateTime, nullable=False, index=True, info='认证过期时间')
    auth_time = Column(DateTime, info='认证时间')
    auth_type = Column(Integer, server_default=FetchedValue(), info='认证类型 0 其他 1 短信认证 2 辅助认证')



class Blackwhite(Base):
    __tablename__ = 'blackwhite'
    __table_args__ = (
        Index('i_type', 'type', 'range'),
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    type = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 黑名单 1 白名单')
    range = Column(Integer, nullable=False, info='范围 0 内网(MAC) 1 外网(IP或域名) ')
    text = Column(String(200, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue())
    store_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='场所id')



class Branch(Base):
    __tablename__ = 'branch'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    name = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='分公司名称')
    regions = Column(String(2000), nullable=False, server_default=FetchedValue(), info='管辖地区 {} json region_code')



class ClientInfo(Base):
    __tablename__ = 'client_info'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    mac = Column(String(17), nullable=False, unique=True, server_default=FetchedValue(), info='MAC地址')
    id_type = Column(Integer, nullable=False, info='id 类型 0 手机号 1 护照号')
    user_id = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='用户id')



class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    key = Column(String(20), nullable=False, unique=True, server_default=FetchedValue(), info='配置key')
    val = Column(Text(collation='utf8mb4_0900_ai_ci'), nullable=False, info='配置内容')
    type = Column(Integer, nullable=False, server_default=FetchedValue(), info='0:plain 1: json')



class ConfigCopy1(Base):
    __tablename__ = 'config_copy1'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    key = Column(String(20), nullable=False, unique=True, server_default=FetchedValue(), info='配置key')
    val = Column(Text(collation='utf8mb4_0900_ai_ci'), nullable=False, info='配置内容')
    type = Column(Integer, nullable=False, server_default=FetchedValue(), info='0:plain 1: json')



class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue(), info='注册时间')
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 1 异常 9 禁用')
    store_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='所属场所')
    name = Column(String(100, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='设备名 酒店为房间号 或SSID名字')
    mac = Column(String(17), nullable=False, unique=True, server_default=FetchedValue(), info='mac地址')
    sn = Column(String(40, 'utf8mb4_0900_ai_ci'), index=True, server_default=FetchedValue(), info='设备号')
    remark = Column(String(200), info='备注')
    loid = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='设备 loid 唯一')
    heartbeat_time = Column(DateTime, nullable=False, info='心跳时间')
    is_auth = Column(Integer, nullable=False, server_default=FetchedValue(), info='是否开启认证 0 未开启 1 开启 -1 未配置(使用场所配置)')
    ip = Column(String(15, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='IP地址')
    info = Column(String(2000), info='设备信息 传上来的原始信息')
    version = Column(String(20), nullable=False, index=True, server_default=FetchedValue(), info='插件版本号')
    ssid = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='SSID')
    password = Column(String(100, 'utf8mb4_0900_ai_ci'), info='SSID密码')
    bssid = Column(String(2000, 'utf8mb4_0900_ai_ci'), info='BSSID')
    platform = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 未知 1 百卓 2 任子行')
    msg_version = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='消息版本号')
    device_model = Column(String(60, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='设备型号')



class DeviceErrorReport(Base):
    __tablename__ = 'device_error_report'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    device_id = Column(Integer, nullable=False, info='设备id号')
    raw_data = Column(Text, info='上报信息')



class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    name = Column(String(40), nullable=False, server_default=FetchedValue(), info='菜单名')
    url = Column(String(200, 'utf8mb4_0900_ai_ci'), server_default=FetchedValue(), info='链接')
    parent_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='父级菜单id')
    depth = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='菜单depth')
    icon = Column(String(200), info='图标')



class Model(Base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    name = Column(String(50), unique=True, info='设备类型名称')



class Online(Base):
    __tablename__ = 'online'
    __table_args__ = (
        Index('i_store_device', 'store_id', 'device_id'),
        Index('i_user', 'user_id', 'id_type'),
        Index('u_device_mac', 'device_id', 'mac')
    )

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 在线 1 离线')
    store_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='场所id')
    device_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='设备id')
    ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='ip地址')
    wan_ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='外网ip地址')
    mac = Column(String(17, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='MAC地址')
    id_type = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 手机号 1 护照号 -1 无')
    user_id = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='用户identity')
    name = Column(String(200, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='设备名称')
    expired_time = Column(DateTime, info='认证过期时间')
    auth_time = Column(DateTime, info='认证时间')
    auth_status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 未认证 1 已认证')
    msg_version = Column(String(10, 'utf8mb4_0900_ai_ci'), server_default=FetchedValue(), info='消息的版本号')
    auth_type = Column(Integer, server_default=FetchedValue(), info='认证类型 0 其他 1 短信认证 2 辅助认证')
    admin_id = Column(Integer, info='辅助认证管理员ID')



class OnlineLog(Base):
    __tablename__ = 'online_log'
    __table_args__ = (
        Index('i_date_hour', 'date', 'hour'),
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 在线 1 离线')
    mac = Column(String(17), nullable=False, index=True, server_default=FetchedValue(), info='MAC地址')
    date = Column(Date, nullable=False, info='记录日期')
    hour = Column(Integer, nullable=False, server_default=FetchedValue(), info='小时 0 - 23')



class PageTemplate(Base):
    __tablename__ = 'page_template'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    name = Column(String(50, 'utf8mb4_0900_ai_ci'), server_default=FetchedValue(), info='模板名称')
    logo_title = Column(String(255), server_default=FetchedValue(), info='logo标题')
    logo = Column(String(255), info='logo地址')
    banner = Column(String(255), info='banner地址')
    banner_title = Column(String(255), info='banner标题')
    banner_subtitle = Column(String(255), info='banner副标题')
    store_id = Column(String(255), nullable=False, server_default=FetchedValue(), info='-1 所有场所 0 无场所 - 场所id')
    branch_id = Column(String(255), nullable=False, server_default=FetchedValue(), info='所属分公司 id -1 管理所有 0 无分公司权限')
    is_default = Column(Integer, nullable=False, server_default=FetchedValue(), info='是否是默认模板 0 否 1 是')
    loadin = Column(String(255), info='认证前载入图片')



class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    name = Column(String(40), nullable=False, server_default=FetchedValue(), info='权限名')
    path = Column(String(80), nullable=False, unique=True, server_default=FetchedValue(), info='请求路径')
    editable = Column(Integer, nullable=False, server_default=FetchedValue(), info='是否是编辑地址')



class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue())
    type = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 省 1 市 2 区 3 街道')
    name = Column(String(40), nullable=False, index=True, server_default=FetchedValue(), info='名称')
    parent_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='上级id')
    code = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='街道code')
    spell = Column(String(200), nullable=False, server_default=FetchedValue(), info='拼音')



class Release(Base):
    __tablename__ = 'release'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 未发布 1 已发布')
    version = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='版本号')
    serial_number = Column(Integer, nullable=False, server_default=FetchedValue(), info='版本序号')
    filename = Column(String(200), nullable=False, server_default=FetchedValue(), info='文件')
    md5sum = Column(String(80), nullable=False, server_default=FetchedValue(), info='md5值')
    device_model = Column(String(20), nullable=False, info='设备型号')
    change_log = Column(String(2000, 'utf8mb4_0900_ai_ci'), info='更新日志')



class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    name = Column(String(40), nullable=False, server_default=FetchedValue(), info='角色名称')
    permissions = Column(String(2000), server_default=FetchedValue(), info='权限id json []')
    menus = Column(String(2000), info='菜单 id json []')
    readonly = Column(Integer, nullable=False, server_default=FetchedValue(), info='只读 0 否 1 是')



class SmsLog(Base):
    __tablename__ = 'sms_log'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    type = Column(Integer, nullable=False, info='短信类型 0 其他 1 短信认证 2 APP登录 ')
    mobile = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, info='接受手机号码')
    store_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='场所ID')
    device_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='设备ID')
    content = Column(String(200, 'utf8mb4_0900_ai_ci'), info='短信内容')
    ip = Column(String(80, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='ip地址')
    auth_code = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, info='短信验证码')
    date = Column(Date, nullable=False, info='日期')
    hour = Column(Integer, nullable=False, server_default=FetchedValue(), info='小时 0 - 23')



class Stat(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    date = Column(Date, nullable=False, index=True, info='统计日期')
    store_total = Column(Integer, nullable=False, server_default=FetchedValue(), info='场所数量')
    device_total = Column(Integer, nullable=False, server_default=FetchedValue(), info='设备数据量')
    online_total = Column(Integer, nullable=False, server_default=FetchedValue(), info='在线数量')
    branch_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='分公司id 0 统计所有')



class StatsAudit(Base):
    __tablename__ = 'stats_audit'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    date = Column(Date, nullable=False, index=True, info='日期')
    hour = Column(Integer, nullable=False, index=True, info='小时')
    platform = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 未知 1 百卓 2 任子行')
    count = Column(Integer, nullable=False, server_default=FetchedValue(), info='发送数量')
    failure = Column(Integer, nullable=False, server_default=FetchedValue(), info='失败数量')



class StatsOnline(Base):
    __tablename__ = 'stats_online'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    date = Column(Date, nullable=False, index=True, info='统计日期')
    total = Column(Integer, nullable=False, server_default=FetchedValue(), info='数量')
    hour = Column(Integer, nullable=False, server_default=FetchedValue(), info='小时 0 - 23')
    branch_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='分公司id 0 所有')



class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    name = Column(String(200, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='场所名')
    address = Column(String(1000, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='地址')
    region_code = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, index=True, server_default=FetchedValue(), info='地址区域编码')
    code = Column(String(40, 'utf8mb4_0900_ai_ci'), nullable=False, unique=True, server_default=FetchedValue(), info='场所编码')
    lat = Column(Numeric(10, 7), nullable=False, server_default=FetchedValue(), info='纬度')
    lng = Column(Numeric(10, 7), nullable=False, server_default=FetchedValue(), info='经度')
    service_type = Column(String(100), nullable=False, server_default=FetchedValue(), info='服务类型')
    business_type = Column(String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='经营类型')
    legal_person = Column(String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='法人')
    legal_person_id_type = Column(String(40, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='法人身份类型')
    legal_person_id = Column(String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='法人身份证件号')
    legal_person_tel = Column(String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='法人联系电话')
    is_auth = Column(Integer, nullable=False, server_default=FetchedValue(), info='是否开启认证 0 未开启 1 开启')
    ssid = Column(String(80), info='ssid配置')
    ssid_password = Column(String(100), info='ssid密码')
    template_id = Column(Integer, nullable=False, server_default=FetchedValue(), info='认证页面模板')



class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        Index('i_user', 'user_id', 'user_type'),
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    status = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='0 正常 9 禁用')
    user_id = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=FetchedValue(), info='用户id  手机号 或者 其他')
    user_type = Column(Integer, nullable=False, server_default=FetchedValue(), info='0 身份证 1 护照号')
    mac = Column(String(17), nullable=False, unique=True, server_default=FetchedValue(), info='mac地址')



class StoreExt(Base):
    __tablename__ = 'store_ext'

    store_id = Column(Integer, primary_key=True)
    black_mode = Column(Integer, nullable=False, server_default=FetchedValue(), info='黑名单模式 0 不开启 1 开启')
    white_prefix = Column(String(1000), server_default=FetchedValue(), info='白名单前缀 多个逗号隔开')
    expires = Column(Integer, nullable=False, server_default=FetchedValue(), info='认证过期时间 单位：s')



class Whitelist(Base):
    __tablename__ = 'whitelist'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    mac = Column(String(17, 'utf8mb4_general_ci'), nullable=False, index=True, info='mac地址')
    store_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='场所ID号')
    device_id = Column(Integer, nullable=False, index=True, info='设备ID号')
    source = Column(Integer, nullable=False, index=True, info='0 手动 1 自动 21 任子行 22 百卓')



class WhitelistPrefix(Base):
    __tablename__ = 'whitelist_prefix'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    prefix = Column(String(17, 'utf8mb4_general_ci'), nullable=False, index=True, info='mac地址前缀')
    store_id = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='场所ID号')
    tags = Column(String(400, 'utf8mb4_general_ci'), nullable=False, server_default=FetchedValue(), info='标签 逗号隔开')