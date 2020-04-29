# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from cookies_pool.settings import CHROME_DRIVER_PATH


class YouYuanCookies(object):
    """
    YouYuanCookies class
    """
    def __init__(self, username, password, browser):
        """
        init instance
        :param username: login of account
        :param password: login of password
        :param browser:  browser instance objects
        """
        self.url = "http://www.youyuan.com/login.html"
        self.browser = browser
        self.username = username
        self.password = password
        self.wait = WebDriverWait(self.browser, 20)

    def get_elements(self) -> tuple:
        """
        get username and password and click of elements for login
        :return: username_elem, password_elem, submit_elem
        ----------------------------------------------------------------------------------------------------
        ### selenium click input elem antiSpider
        # click before
        <li><label>登录密码：</label>
            <input id="loginPassText" title="登录密码" type="text" value="登录密码">
            <input style="display: none;" id="loginPass" title="登录密码" type="password">
        </li>

        # click after
        <li><label>登录密码：</label>
            <input id="loginPassText" title="登录密码" type="text" value="登录密码" style="display: none;">
            <input style="display: block;" id="loginPass" title="登录密码" type="password" class="input_out">
        </li>
        -----------------------------------------------------------------------------------------------------
        """
        username_elem = self.wait.until(
            EC.presence_of_element_located((By.ID, 'loginUserId'))
        )
        password1_elem = self.wait.until(
            EC.presence_of_element_located((By.ID, 'loginPassText'))
        )
        password2_elem = self.wait.until(
            EC.presence_of_element_located((By.ID, 'loginPass'))
        )
        submit_elem = self.wait.until(
            EC.presence_of_element_located((By.ID, 'loginSubmit'))
        )

        return username_elem, password1_elem, password2_elem, submit_elem

    def open(self):
        """
        open the page and enter your username and password then click
        :return: None
        """
        # delete all cookies in the scope of the session.
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        username_elem, password1_elem, password2_elem, submit_elem = self.get_elements()
        username_elem.send_keys(self.username)
        password1_elem.click()
        password2_elem.send_keys(self.password)
        time.sleep(1)
        submit_elem.click()

    def password_error(self):
        """
        determine if the password is incorrect
        :return:
        """
        try:
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.ID, 'loginMsg'), '*登录失败，帐号或密码错误！')
            )
        except TimeoutException:
            return False

    def login_successfully(self):
        """
        determine if the login was successful
        :return:
        """
        try:
            return bool(self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="blue"]'))
            ))
        except TimeoutException:
            return False

    def get_cookies(self):
        """
        get cookies
        :return: cookies
        """
        return self.browser.get_cookies()

    def main(self):
        """
        break the entrance
        :return:
        """
        self.open()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
            # res = {
            #     'status': 2,
            #     'content': '用户名或密码错误'
            # }
            # print(res)

        # if you do not need verification code directly login successfully
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
            # res = {
            #     'status': 1,
            #     'content': cookies
            # }
            # print(res)
        else:
            # other reason
            return {
                'status': 3,
                'content': '登录失败'
            }
            # res = {
            #     'status': 3,
            #     'content': '登录失败'
            # }
            # print(res)


if __name__ == '__main__':
    browser_ = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    y = YouYuanCookies('username', 'password', browser_)
    y.main()


