# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8


class PoolEmptyException(Exception):
    def __str__(self):
        """
        cookies_pool is used out
        :return:
        """
        return repr('no cookies in cookies_pool')


