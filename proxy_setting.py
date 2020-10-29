# 满分为可用，检测器会定时循环检测每个 IP 的可用情况，
# 一旦检测到有可用的 IP 就立即置为满分，检测到不可用就将分数减 1，减至 0 后移除。
# 新获取的代理添加时将分数置为 10，当测试可行立即置 30，不可行分数减 1，减至 0 后移除
HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'
SQL_NAME = 'ip_pool'

# 代理等级
MAX_SCORE = 30
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 1000

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 30