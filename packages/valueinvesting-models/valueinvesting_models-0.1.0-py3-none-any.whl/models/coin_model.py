from . import db

# 中间表，用于关联 Coin 和 CoinType
coin_types_association = db.Table(
    'coin_types_association',
    db.Column('coin_id', db.Integer, db.ForeignKey('coin.id'), primary_key=True),
    db.Column('coin_type_id', db.Integer, db.ForeignKey('coin_type.id'), primary_key=True)
)

# 中间表,用于关联 Coin 和 Founder
coin_founder_association = db.Table(
    'coin_founder_association',
    db.Column('coin_id', db.Integer, db.ForeignKey('coin.id'), primary_key=True),
    db.Column('founder_id', db.Integer, db.ForeignKey('founder.id'), primary_key=True)
)

# 中间表，用于关联 Coin 和 Ecosystem
coin_ecosystem_association = db.Table(
    'coin_ecosystem_association',
    db.Column('coin_id', db.Integer, db.ForeignKey('coin.id'), primary_key=True),
    db.Column('ecosystem_id', db.Integer, db.ForeignKey('ecosystem.id'), primary_key=True)
)

# 币表，存储币种的详细信息
class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(80), unique=True, nullable=False)  # 币种名称
    symbol = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(500), nullable=True)  # 币种介绍
    issuance_date = db.Column(db.Date, nullable=True)  # 发行时间
    is_active = db.Column(db.Boolean, default=True)  # 是否为活跃币种
    address = db.Column(db.String(200), nullable=True)
    rank = db.Column(db.Integer, default=0)
    coinmarketid = db.Column(db.Integer,nullable=True) #bnb CoinmarketGap id
    # 多对多关系，关联 Ecosystem
    ecosystems = db.relationship('Ecosystem', secondary=coin_ecosystem_association, back_populates='coins')

    # 多对多关系，关联 创始人
    founder = db.relationship('Founder', secondary=coin_founder_association, back_populates='coins')

    # 多对多关系，关联 投资机构
    investments = db.relationship('CoinInvestment', backref='coin', cascade="all, delete-orphan")

    # 多对多关系，关联 CoinType
    coin_type = db.relationship('CoinType', secondary=coin_types_association, back_populates='coins')


# 生态链表，存储不同生态链的信息
class Ecosystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # 生态链名称
    description = db.Column(db.String(100), nullable=True)  # 生态链描述
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # 创建时间

    # 多对多关系，关联 Coin
    coins = db.relationship('Coin', secondary=coin_ecosystem_association, back_populates='ecosystems')


# 币种类型表，分类不同类型的币 多对多
class CoinType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), nullable=False)  # 币种类型（主流币、山寨币、新型币、生态币）
    description = db.Column(db.String(200), nullable=True)  # 类型描述
    coins = db.relationship('Coin', secondary=coin_types_association, back_populates='coin_type')


# 创始人表，记录币种创始人和团队的信息 多对多
class Founder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 创始人姓名
    team_name = db.Column(db.String(100), nullable=True)  # 团队名称
    reputation_score = db.Column(db.Integer, nullable=True)  # 知名度评分（1-100）
    coins = db.relationship('Coin', secondary=coin_founder_association, back_populates='founder')


# 投资机构表，用于存储机构的基本信息 多对多
class InvestmentInstitution(db.Model):
    __tablename__ = 'investment_institution'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # 机构名称（唯一）
    description = db.Column(db.String(500), nullable=True)  # 介绍（可选）
    investments = db.relationship('CoinInvestment', backref='institution')


# 币种-投资机构中间表，用于记录每个机构对每个币种的投资情况 多对多
class CoinInvestment(db.Model):
    __tablename__ = 'coin_investment'
    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.Integer, db.ForeignKey('coin.id'), nullable=False)  # 外键，关联币种
    institution_id = db.Column(db.Integer, db.ForeignKey('investment_institution.id'), nullable=False)  # 外键，关联投资机构
    holding_amount = db.Column(db.Float, nullable=True)  # 持有量
    holding_percentage = db.Column(db.Float, nullable=True)  # 持有比例

    # coin_id 和 institution_id 唯一约束
    __table_args__ = (db.UniqueConstraint('coin_id', 'institution_id', name='_coin_institution_uc'),)
