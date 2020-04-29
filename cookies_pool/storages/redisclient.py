# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import redis
import random
from loguru import logger
from cookies_pool.exceptions.empty import PoolEmptyException
from cookies_pool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DATABASE_NUM


class RedisClient(object):
    """
    redis connection client of cookies_pool
    """
    def __init__(self,
                 type,
                 website,
                 host=REDIS_HOST,
                 port=REDIS_PORT,
                 password=REDIS_PASSWORD,
                 database=REDIS_DATABASE_NUM
                 ):
        """
        init redis connection
        :param type: accounts or cookies
        :param website: website for spider
        :param host: redis host
        :param port: redis port
        :param password: redis password
        :param database: redis database num
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=database, decode_responses=True)
        self.type = type
        self.website = website

    def name(self) -> str:
        """
        get redis hash name
        :return: hash name
        """
        return f"{self.type}:{self.website}"

    def set(self, username, value) -> int:
        """
        set key-value
        :param username:username
        :param value: password or cookies
        :return: add nums for key-value
        """
        return self.db.hset(self.name(), username, value)

    def get(self, username) -> str:
        """
        Gets the corresponding key value based on the key name
        :param username:username
        :return: username mapping for password or cookies
        """
        return self.db.hget(self.name(), username)

    def delete(self, username) -> int:
        """
        Delete the corresponding key value according to the key name
        :param username:username
        :return: username mapping for password or cookies
        """
        return self.db.hdel(self.name(), username)

    def count(self) -> int:
        """
        get count of cookies_pool
        :return: count, int
        """
        return self.db.hlen(self.name())

    def random(self) -> str:
        """
        get random password or cookies
        :return: password or cookies
        """
        if self.count():
            cookies = random.choice(self.db.hvals(self.name()))
            logger.info(f'get random cookies success from cookies_pool: {cookies}')
            return cookies
        else:
            raise PoolEmptyException

    def user_names(self) -> list:
        """
        get all accounts of cookies_pool
        :return: ['account1', 'account2', ...]
        """
        return self.db.hkeys(self.name())

    def all(self) -> dict:
        """
        get all key value of cookies_pool
        :return: {'accounts1': 'password1', 'account2': 'password2', ...} or
                {'accounts1': '{"HOME1": "1", "delPer1": 0}', 'account2': '{"HOME2": "2", "delPer2": 0}', ...}
        """
        return self.db.hgetall(self.name())


if __name__ == '__main__':
    conn = RedisClient('accounts', 'youyuan')
    conn1 = RedisClient('cookies', 'youyuan')
    res = conn.set('13082808996', '226028')
    res1 = conn1.set('888888', '{"name": "value"}')
    print(res, type(res))
    print(res1, type(res1))
    res2 = conn1.random()
    print(res2, type(res2))
    # res = conn1.delete('13082808996')
    # print(res)
