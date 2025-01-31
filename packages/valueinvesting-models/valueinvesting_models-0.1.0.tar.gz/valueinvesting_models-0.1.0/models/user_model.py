from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# Association Tables
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

# Models
class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now())
    roles = db.relationship('Role', secondary=role_permissions, back_populates='permissions')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now())
    users = db.relationship('User', secondary=user_roles, back_populates='roles')
    permissions = db.relationship('Permission', secondary=role_permissions, back_populates='roles')

# 用户表，包含用户基本信息和投资偏好
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=True)  # 保持nullable=True
    roles = db.relationship('Role', secondary=user_roles, back_populates='users')
    followed_coins = db.Column(db.String(200), nullable=True)  # 关注的币（逗号分隔）
    total_investment = db.Column(db.Float, nullable=True)  # 我的投资总额
    target_amount = db.Column(db.Float, nullable=True)  # 目标达到金额
    target_date = db.Column(db.Date, nullable=True)  # 目标时间
    notifications = db.relationship('NotificationSetting', backref='user', lazy=True)  # 一对多关联
    risk_tolerance = db.Column(db.String(50), nullable=True)  # 投资风险承受能力（如：保守、中等、激进）
    simulation_wallet = db.Column(db.Float, default=0.0)  # 模拟盘钱包余额
    real_wallet = db.Column(db.Float, default=0.0)  # 实盘钱包余额
    simulation_enabled = db.Column(db.Boolean, default=True)  # 模拟盘开关
    real_trade_enabled = db.Column(db.Boolean, default=False)  # 实盘交易开关
    created_at = db.Column(db.DateTime, default=datetime.now())  # 创建时间

    def set_password(self, password):
        """Hash password"""
        print("before encode:", password)
        encode_passwd = generate_password_hash(password)
        print("after encode:", encode_passwd)
        self.password_hash = encode_passwd

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name):
        for role in self.roles:
            if permission_name in [perm.name for perm in role.permissions]:
                return True
        return False

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password_hash

            }
        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            db.session.rollback()
            return {'message': 'Something went wrong'}


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True, nullable=False)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding token to blacklist: {e}")
            raise

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
