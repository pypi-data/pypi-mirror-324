from datetime import datetime
from . import db
class InvestmentValueAssessment(db.Model):
    """投资价值评估表"""
    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)  # 外键，关联币种
    crypto_symbol = db.Column(db.String(20), nullable=False)  # 代币符号
    assessment_date = db.Column(db.DateTime, default=datetime.now())  # 评估日期
    # 代币基本信息
    main_features = db.Column(db.String(200), nullable=True)  # 主要特点
    launch_date = db.Column(db.DateTime, nullable=True)  # 发行时间
    total_supply = db.Column(db.Float, nullable=True)  # 发行量
    market_cap = db.Column(db.Float, nullable=True)  # 市值
    all_time_high = db.Column(db.Float, nullable=True)  # 历史最高价
    growth_potential_info=db.Column(db.String(200),nullable=True)
    notable_figures_info=db.Column(db.String(200),nullable=True)
    # 评分字段
    growth_potential_score = db.Column(db.Integer, nullable=False)  # 增长潜力评分
    notable_figures_score = db.Column(db.Integer, nullable=False)  # 名人推荐评分
    chain_scale_score = db.Column(db.Integer, nullable=False)  # 链上规模及主流性评分
    lockup_release_score = db.Column(db.Integer, nullable=False)  # 锁仓与释放计划评分
    market_cap_scarcity_score = db.Column(db.Integer, nullable=False)  # 市值与稀缺性评分
    historical_performance_score = db.Column(db.Integer, nullable=False)  # 历史表现评分
    institutional_holdings_score = db.Column(db.Integer, nullable=False)  # 机构持仓评分
    fdv_ratio_score = db.Column(db.Integer, nullable=False)  # FDV比率评分
    supply_inflation_score = db.Column(db.Integer, nullable=False)  # 供应与通胀评分
    has_main_chain = db.Column(db.Boolean, nullable=False)  # 是否有主链

    # 综合评分
    overall_score = db.Column(db.Float, nullable=False)  # 综合评分（100分）

    # 评估元数据
    last_updated = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())  # 最后更新时间
    data_confidence_score = db.Column(db.Integer, nullable=False)  # 数据可信度评分(1-100)

    def calculate_overall_score(self):
        """计算综合评分"""
        # 各维度权重
        weights = {
            'growth_potential': 0.15,
            'notable_figures': 0.05,
            'chain_scale': 0.10,
            'lockup_release': 0.10,
            'market_cap_scarcity': 0.15,
            'historical_performance': 0.05,
            'institutional_holdings': 0.05,
            'fdv_ratio': 0.05,
            'supply_inflation': 0.05,
            'has_main_chain': 0.10
        }

        # 计算综合评分
        self.overall_score = (
            self.growth_potential_score * weights['growth_potential'] +
            self.notable_figures_score * weights['notable_figures'] +
            self.chain_scale_score * weights['chain_scale'] +
            self.lockup_release_score * weights['lockup_release'] +
            self.market_cap_scarcity_score * weights['market_cap_scarcity'] +
            self.historical_performance_score * weights['historical_performance'] +
            self.institutional_holdings_score * weights['institutional_holdings'] +
            self.fdv_ratio_score * weights['fdv_ratio'] +
            self.supply_inflation_score * weights['supply_inflation'] +
            (100 if self.has_main_chain else 0) * weights['has_main_chain']
        )

        return self.overall_score