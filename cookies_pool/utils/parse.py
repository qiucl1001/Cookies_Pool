# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import re


def parse_redis_connection_string(connection_string):
    """
    parse a redis connection string, for example:
    redis://[:password]@host:port/num
    rediss://[:password]@host:port/num
    :param connection_string:
    :return:
    """
    result = re.match('rediss?:\/\/(.*?)@(.*?):(\d+)/(.*)', connection_string)
    return result.group(2), int(result.group(3)), (result.group(1) or None), (result.group(4) or 0) if result \
        else ('localhost', 6379, None, 0)

