from datetime import datetime
from . import db

# 实时价格记录表
class RealTimePrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 价格记录ID
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)  # 外键，关联币种
    timestamp = db.Column(db.DateTime, default=datetime.now())  # 时间戳
    price = db.Column(db.Float, nullable=False)  # 实时价格
    price_source = db.Column(db.String(200), nullable=False)  # 数据来源

# 市场数据表，存储币种的历史市场数据
class MarketData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)  # 外键，关联币种
    date = db.Column(db.Date, nullable=False)  # 日期
    market_cap = db.Column(db.Float, nullable=False)  # 市值
    volume_24h = db.Column(db.Float, nullable=False)  # 交易量


#创建机器学习 Recommendation 表存储推荐的币种和策略
class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)
    recommendation_reason = db.Column(db.String(500), nullable=True)  # 推荐理由
    created_at = db.Column(db.DateTime, default=datetime.now())  # 推荐时间
