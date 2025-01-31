from . import db
from datetime import datetime


#通知方式 用户通知设置表
class NotificationSetting(db.Model):
    __tablename__ = 'notification_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键关联用户表
    notification_type = db.Column(db.String(50), nullable=False)  # 通知类型 ('email', 'sms', 'push')
    enabled = db.Column(db.Boolean, default=True)  # 是否启用
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # 创建时间


#创建系统日志
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(200), nullable=False)  # 操作内容
    timestamp = db.Column(db.DateTime, default=datetime.now())  # 操作时间
    # 关系定义
    user = db.relationship('User', backref='audit_logs')  # 通过 user 访问 User 表
