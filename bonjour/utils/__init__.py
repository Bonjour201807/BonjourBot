from .log_helper import *
from .utils import *
from .db_helper import *

LogHelper.initialize('bonjour.log')
# 设置级别（可选，默认DEBUG）
LogHelper.set_level('DEBUG')
# 获取句柄
logger = LogHelper.get('app')