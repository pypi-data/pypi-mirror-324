"""
- Create by @Auther: WangWei
- @StudientID: S1034363
- @Email: S1034363@students.lsbf.edu.sg
- @ModuleCode: CN6000
- @Date 2024/11/2/17:43 
"""

from datetime import datetime
from . import db

# 透支周期表，管理用户自定义的投资周期和阶段
class InvestmentCycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户表
    total_stages = db.Column(db.Integer, nullable=False)  # 投掷段数（如三段、四段或更多）
    stage_percentages = db.Column(db.String(200), nullable=False)  # 每段的百分比（逗号分隔，如 "3,5,8,..."）
    cycle_period = db.Column(db.String(20), nullable=False)  # 周期（3个月/6个月/12个月/24个月）
    start_date = db.Column(db.DateTime, nullable=False)  # 周期的起始时间

# 投资阶段表，记录每个投资阶段的细节
class InvestmentStage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户表
    stage_number = db.Column(db.Integer, nullable=False)  # 当前阶段号（如第1段、第2段）
    set_date = db.Column(db.DateTime, default=datetime.now())  # 设置时间
    current_market_price = db.Column(db.Float, nullable=False)  # 当前市场价格
    stage_percentage = db.Column(db.Float, nullable=False)  # 每段对应的百分比
    calculated_overdraft_price = db.Column(db.Float, nullable=False)  # 计算的透支价格
    amount_per_stage = db.Column(db.Float, nullable=False)  # 每段投资金额

# 时序分段表
class TimeSegment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 分段ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户
    segment_number = db.Column(db.Integer, nullable=False)  # 分段序号
    start_time = db.Column(db.Time, nullable=False)  # 起始时间
    end_time = db.Column(db.Time, nullable=False)  # 结束时间
    created_at = db.Column(db.DateTime, default=datetime.now())  # 创建时间


# 策略表
class Strategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 策略ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户
    name = db.Column(db.String(100), nullable=False)  # 策略名称
    conditions = db.Column(db.String(500), nullable=False)  # 策略条件（JSON存储）
    action = db.Column(db.String(100), nullable=False)  # 策略动作（买入/卖出）
    created_at = db.Column(db.DateTime, default=datetime.now())  # 创建时间


# 投资比例表，记录用户投资的分配情况
class InvestmentAllocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户表
    total_investment = db.Column(db.Float, nullable=False)  # 投资总额
    main_coin_percentage = db.Column(db.Float, nullable=False)  # 主流币比例
    meme_coin_percentage = db.Column(db.Float, nullable=False)  # 山寨币比例
    new_coin_percentage = db.Column(db.Float, nullable=False)  # 新型币比例
    main_coin_count = db.Column(db.Integer, nullable=False)  # 主流币数量
    meme_coin_count = db.Column(db.Integer, nullable=False)  # 山寨币数量
    ecosystem_coin_count = db.Column(db.Integer, nullable=False)  # 生态币数量
    new_coin_count = db.Column(db.Integer, nullable=False)  # 新型币数量
    status = db.Column(db.String(50), nullable=False, default="pending")  # 阶段状态（如：pending, completed）


# 投资组合分析表，定期分析用户的投资组合
class PortfolioAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)  # 分析开始日期
    end_date = db.Column(db.Date, nullable=False)  # 分析结束日期
    total_return = db.Column(db.Float, nullable=False)  # 总收益率
    diversification_score = db.Column(db.Float, nullable=False)  # 多样化评分
    asset_distribution = db.Column(db.String(500), nullable=True)  # 各资产分布

