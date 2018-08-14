from .log_utils import *
from .common_utils import *
from .db_utils import *

LogHelper.initialize('bonjour.log')
# 设置级别（可选，默认DEBUG）
LogHelper.set_level('DEBUG')
# 获取句柄
logger = LogHelper.get('app')