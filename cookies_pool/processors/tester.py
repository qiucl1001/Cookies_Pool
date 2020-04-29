# encoding: utf-8
# author: QCL
# software: PyCharm Community Edition 2018.1.2
import json
import requests
from loguru import logger
from cookies_pool.storages.redisclient import RedisClient
from cookies_pool.settings import TEST_URL_MAP
from requests.exceptions import ConnectionError


class ValidTester(object):
    """
    to achieve commonality, define a detector parent class and configure some common components
    """
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class WeiboValidTester(ValidTester):
    """
    define a cookie to detect the timeliness of weibo sites
    """
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        logger.info(f'正在测试cookies, 用户名, {username}')
        try:
            cookies = json.loads(cookies)
            print("-----------1----------------")
            print(cookies, type(cookies))
        except TypeError:
            logger.info(f'cookies非法..., {username}')
            self.cookies_db.delete(username)
            logger.info(f'删除cookies..., {username}')
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(url=test_url,
                                    headers=YouYuanValidTester.headers,
                                    cookies=cookies,
                                    timeout=5,
                                    allow_redirects=False
                                    )
            if response.status_code == 200:
                logger.info(f'cookies有效..., {username}')
            else:
                logger.info(f'{response.status_code}, {response.headers}')
                logger.info(f'cookies失效..., {username}')
                self.cookies_db.delete(username)
                logger.info(f'删除cookies...., {username}')
        except ConnectionError as e:
            logger.error(f'出现异常了..., {e.args}')


class YouYuanValidTester(WeiboValidTester):
    """
    define a cookie to detect the timeliness of youyuan sites
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        # "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.youyuan.com",
        "Referer": "http://www.youyuan.com/login.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.132 Safari/537.36",
    }

    def __init__(self, website='youyuan'):
        """
        init instance
        :param website: test of website
        """
        super(YouYuanValidTester, self).__init__(website)


if __name__ == '__main__':
    y = YouYuanValidTester()
    y.run()

