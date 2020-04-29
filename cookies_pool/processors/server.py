# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import json
from loguru import logger
from flask import Flask, g
from cookies_pool.settings import GENERATOR_MAP
from cookies_pool.storages.redisclient import RedisClient
from cookies_pool.settings import API_HOST, API_PORT, API_THREADED

__all__ = ['app']

app = Flask(__name__)


@app.route("/")
def index():
    """Create a home page for index access"""
    return "<h3>Welcome To Cookies Pool System</h3>"


def get_conn():
    """
    get redis client object
    :return:
    """
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, website + "_cookies", eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + "_accounts", eval('RedisClient' + '("accounts", "' + website + '")'))
    return g


@app.route("/<website>/random/cookies")
def random_cookies(website):
    """
    get random cookie, e.g:/weibo/random/cookies
    :param website: website
    :return: random of cookie
    """
    g = get_conn()
    cookies = getattr(g, website + "_cookies").random()
    return cookies


@app.route("/<website>/random/password")
def random_password(website):
    """
    get random password, e.g:/weibo/random/passwords
    :param website: website
    :return: random of password
    """
    g = get_conn()
    password = getattr(g, website + "_accounts").random()
    return password


@app.route("/<website>/count")
def count(website) -> int:
    """
    get all cookies total numbers
    :param website: website
    :return:cookies total numbers
    """
    g = get_conn()
    count = getattr(g, website + "_cookies").count()
    return json.dumps({"status": "1", "count": count})


@app.route("/<website>/add/<username>/<password>")
def add(website, username, password):
    """
    add accounts e.g:/weibo/add/user/password
    :param website:website
    :param username: account
    :param password:password
    :return:
    """
    g = get_conn()
    logger.info(f'success add accounts: {username}:{password}')
    getattr(g, website + "_accounts").set(username, password)
    return json.dumps({"status": "1"})


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
