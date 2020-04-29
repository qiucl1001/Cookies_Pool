# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import os
import platform
from environs import Env
from loguru import logger
from cookies_pool.utils.parse import parse_redis_connection_string

env = Env()
env.read_env()


# definition of flags
IS_WINDOWS = platform.system().lower() == "windows"


# definition of dirs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")


# definition of environments
DEV_MODE, TEST_MODE, PROD_MODE = 'dev', 'test', 'prod'
APP_ENV = env.str('APP_ENV', DEV_MODE).lower()
APP_DEBUG = env.bool('APP_DEBUG', True if APP_ENV == DEV_MODE else False)
APP_DEV = IS_DEV = APP_ENV == DEV_MODE
APP_PROD = IS_PROD = APP_ENV == PROD_MODE
APP_TEST = IS_TEST = APP_ENV == TEST_MODE


# redis host
REDIS_HOST = env.str('REDIS_HOST', '127.0.0.1')
# redis port
REDIS_PORT = env.int('REDIS_PORT', 6379)
# redis password, if no password, set it to None
REDIS_PASSWORD = env.str('REDIS_PASSWORD', None)
# redis database num, default 0
REDIS_DATABASE_NUM = env.int('REDIS_DATABASE_NUM', 12)
# redis connection string, like redis://[:password]@host:port/num or rediss://[:password]@host:port/num
REDIS_CONNECTION_STRING = env.str('REDIS_CONNECTION_STRING', None)

if REDIS_CONNECTION_STRING:
    REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DATABASE_NUM = parse_redis_connection_string(REDIS_CONNECTION_STRING)


# definition of browser
BROWSER_TYPE = env.str('BROWSER_TYPE', 'Chrome')

# definition of chrome driver path
CHROME_DRIVER_PATH = env.str('CHROME_DRIVER_PATH',
                             'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe')

# definition of api
API_HOST = env.str('API_HOST', '0.0.0.0')
API_PORT = env.int('API_PORT', 5000)
API_THREADED = env.bool('API_THREADED', True)


# definition of generator class, if extends other website, conf in this
GENERATOR_MAP = env.dict(
    'GENERATOR_MAP', {
        # 'weibo': 'WeiboCookiesGenerator',
        'youyuan': 'YouYuanCookiesGenerator'
    }
)


# definition of test class, if extends other website, conf in this
TESTER_MAP = env.dict(
    'TESTER_MAP', {
        # 'weibo': 'WeiboValidTester',
        'youyuan': 'YouYuanValidTester'
    }
)


# definition of test_url map,  if extends other website, conf in this
TEST_URL_MAP = env.dict(
    'TEST_URL_MAP', {
        # 'weibo': 'https://m.weibo.cn/',
        'youyuan': 'http://www.youyuan.com/v30/apps/today_love.html'
    }
)


# definition of generator and verifier cycles unit:second
CYCLE = env.int('CYCLE', 20)


# definition of flags enable
TESTER_ENABLED = env.bool('TESTER_ENABLED', True)
API_ENABLED = env.bool('API_ENABLED', True)
GENERATOR_ENABLED = env.bool('GENERATOR_ENABLED', True)  # 产生器开关，模拟登录添加Cookies


logger.add(env.str('LOG_RUNTIME_FILE', 'runtime.log'), level='DEBUG', rotation='1 week', retention='20 days')
logger.add(env.str('LOG_ERROR_FILE', 'error.log'), level='ERROR', rotation='1 week')









