from . import db
from datetime import datetime

# 模拟盘记录表
class SimulationTrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 记录ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=True)  # 外键，关联策略
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)  # 外键，关联币种
    action = db.Column(db.String(50), nullable=False)  # 动作（买入/卖出）
    amount = db.Column(db.Float, nullable=False)  # 交易金额
    price_at_transaction = db.Column(db.Float, nullable=False)  # 交易时价格
    timestamp = db.Column(db.DateTime, default=datetime.now())  # 交易时间
    balance_after_trade = db.Column(db.Float, nullable=False)  # 模拟盘交易后的余额

# 实盘记录表
class RealTrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 记录ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=True)  # 外键，关联策略
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)  # 外键，关联币种
    action = db.Column(db.String(50), nullable=False)  # 动作（买入/卖出）
    amount = db.Column(db.Float, nullable=False)  # 交易金额
    price_at_transaction = db.Column(db.Float, nullable=False)  # 交易时价格
    timestamp = db.Column(db.DateTime, default=datetime.now())  # 交易时间
    balance_after_trade = db.Column(db.Float, nullable=False)  # 实盘交易后的余额
    api_transaction_id = db.Column(db.String(100), nullable=True)  # 币安API返回的交易ID
    fees = db.Column(db.Float, nullable=True)  # 交易费用
    real_profit = db.Column(db.Float, nullable=True)  # 实盘收益

# 投资历史记录表，记录用户每次投资的详细信息
class TransactionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户表
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)  # 外键，关联币种
    transaction_date = db.Column(db.DateTime, default=datetime.now())  # 交易日期
    amount_invested = db.Column(db.Float, nullable=False)  # 投资金额
    price_at_transaction = db.Column(db.Float, nullable=False)  # 交易时的价格
    transaction_type = db.Column(db.String(50), nullable=False)  # 交易类型（买入/卖出）


#模拟盘与实盘收益表可以分别记录日收益曲线，便于长期趋势分析
class DailyProfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    profit = db.Column(db.Float, nullable=False)  # 日收益
    wallet_type = db.Column(db.String(10), nullable=False)  # "simulation" 或 "real"