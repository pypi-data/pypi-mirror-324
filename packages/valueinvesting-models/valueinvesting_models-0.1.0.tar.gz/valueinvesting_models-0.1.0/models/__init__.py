"""
- Create by @Auther: WangWei
- @StudientID: S1034363
- @Email: S1034363@students.lsbf.edu.sg
- @ModuleCode: CN6000
- @Date 2024/11/2/18:19 
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 确保 `db` 在 Flask 和 FastAPI 项目中都可以正确使用
from .coin_model import *
from .common_model import *
from .eventnews_model import *
from .investement_model import *
from .realtimedata_model import *
from .score_model import *
from .traderecord_model import *
from .user_model import *