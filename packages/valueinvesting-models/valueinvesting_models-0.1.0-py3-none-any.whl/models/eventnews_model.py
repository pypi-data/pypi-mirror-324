from . import db
from datetime import datetime

#事件和币种类型的多对多关联
class EventTokenAssociation(db.Model):
    __tablename__ = 'event_token_association'
    event_id = db.Column(db.Integer, db.ForeignKey('event_calendar.id'), primary_key=True)
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'), primary_key=True)

#大纪元
class EventCalendar(db.Model):
    __tablename__ = 'event_calendar'
    id = db.Column(db.Integer, primary_key=True)  # 事件 ID
    event_name = db.Column(db.String(255), nullable=False)  # 事件名称（如 "美国大选"、"BTC 四年减半"）
    event_date = db.Column(db.DateTime, nullable=True)  # 修改为 DateTime 类型
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_types.id'), nullable=True)
    influence_score = db.Column(db.Integer, nullable=True, default=50)  # 影响力评分（1-100）
    description = db.Column(db.Text, nullable=True)  # 事件描述
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # 创建时间
    # 多对多关联
    event_type = db.relationship('EventType', backref='events')
    related_tokens = db.relationship('Coin',secondary='event_token_association',  # 中间表
        backref=db.backref('related_events', lazy='dynamic'),
        lazy='dynamic'
    )
    # 新增与 SocialMetric 的关系
    social_metrics = db.relationship('SocialMetric', back_populates='event')

class EventType(db.Model):
    __tablename__ = 'event_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 事件类别名称（如 "政治事件"）
    description = db.Column(db.Text, nullable=True)  # 描述

#对事件的 情绪热度 积极/消极 平台提及次数 情绪程度
class SocialMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event_calendar.id'), nullable=False)  # 关联 EventCalendar
    platform = db.Column(db.String(50), nullable=False)  # 平台（如 Twitter、Reddit）
    mentions = db.Column(db.Integer, nullable=False)  # 提及次数
    sentiment_type = db.Column(db.Boolean, nullable=False)  # 情绪类型（True 表示积极，False 表示消极）
    sentiment_intensity = db.Column(db.Integer, nullable=False)  # 情绪程度（0 到 100）
    timestamp = db.Column(db.DateTime, default=datetime.now())  # 记录时间
    # 定义与 EventCalendar 的关系
    event = db.relationship('EventCalendar', back_populates='social_metrics')

