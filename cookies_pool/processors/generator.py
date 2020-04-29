# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import time
import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from cookies_pool.settings import BROWSER_TYPE, IS_WINDOWS
from cookies_pool.storages.redisclient import RedisClient
from cookies_pool.crawlers.login.weibo.cookies import WeiboCookies
from cookies_pool.crawlers.login.youyuan.cookies import YouYuanCookies
from loguru import logger


class CookiesGenerator(object):
    def __init__(self, website='default'):
        """
        父类, 初始化一些对象
        :param website: 站点名称
        :param browser: 浏览器, 若不使用浏览器则可设置为 None
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
        self.init_browser()

    # def __del__(self):
    #     self.close()

    def init_browser(self):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :return:
        """
        if BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) \
                                            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        elif BROWSER_TYPE == 'Chrome':
            if IS_WINDOWS == "windows":
                self.browser = webdriver.Chrome()
            else:
                self.browser = webdriver.Chrome()

    def new_cookies(self, username, password):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    @staticmethod
    def process_cookies(cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        dict0 = {}
        for cookie in cookies:
            dict0[cookie['name']] = cookie['value']
        return dict0

    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts_usernames = self.accounts_db.user_names()
        cookies_usernames = self.cookies_db.user_names()

        for username in accounts_usernames:
            if username not in cookies_usernames:
                password = self.accounts_db.get(username)
                logger.info(f'正在生成Cookies, 账号: {username}, 密码：{password}')
                result = self.new_cookies(username, password)
                # 成功获取
                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    logger.info(f'成功获取到Cookies：{cookies}')
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        logger.info('成功保存Cookies')
                # 密码错误，移除账号
                elif result.get('status') == 2:
                    error_info = result.get('content')
                    logger.info(f'{error_info}')
                    if self.accounts_db.delete(username):
                        logger.info(f'成功删除账号: {username}')
                else:
                    # 登录失败
                    error_info = result.get('content')
                    logger.info(f'{error_info}')
        else:
            logger.info('所有账号都已经成功获取Cookies')
            time.sleep(3)
            self.close()

    def close(self):
        """
        关闭
        :return:
        """
        try:
            logger.info('Closing BrowserClosing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            logger.error('Browser not opened')


class WeiboCookiesGenerator(CookiesGenerator):
    def __init__(self, website='weibo'):
        """
        初始化操作
        :param website: 站点名称
        :param browser: 使用的浏览器
        """
        super(WeiboCookiesGenerator, self).__init__(website)
        self.website = website

    def new_cookies(self, username, password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        return WeiboCookies(username, password, self.browser).main()


class YouYuanCookiesGenerator(CookiesGenerator):
    def __init__(self, website='youyuan'):
        """
        init instance
        :param website: website name
        """
        super(YouYuanCookiesGenerator, self).__init__(website)
        self.website = website

    def new_cookies(self, username, password):
        """
        generate cookies
        :param username: account for login
        :param password: password for login
        :return:
        """
        return YouYuanCookies(username, password, self.browser).main()


if __name__ == '__main__':
    # generator = WeiboCookiesGenerator()
    generator = YouYuanCookiesGenerator()
    generator.run()
