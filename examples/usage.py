# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import requests

# cookies_pool_url format: http://127.0.0.1:5000/<website>/random/cookies
# <website>: generate cookies of website domain flag
COOKIES_POOL_URL = 'http://127.0.0.1:5000/youyuan/random/cookies'
TARGET_URL = 'http://www.youyuan.com/v30/apps/today_love.html'


def get_random_cookies():
    """
    get random cookies from cookies_pool
    :return: cookies
    """
    return requests.get(COOKIES_POOL_URL).text.strip()


def get_page(url, cookies):
    """
    use cookies to crawl page
    :param url: page url
    :param cookies: cookies, such as {"name1": "value1", "name2": "value2", ...}
    :return: response
    """

    return requests.get(
        url=url,
        cookies=cookies,
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.youyuan.com",
            "Referer": "http://www.youyuan.com/login.html",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/80.0.3987.132 Safari/537.36",
        }
    )


def main():
    """
    main method, entry point
    if you run this model, please sure run server of cookies_pool before
    :return: none
    """
    cookies = get_random_cookies()
    print('get random cookies', cookies)
    response = get_page(TARGET_URL, cookies)
    print(response.status_code, response.text[:50])


if __name__ == '__main__':
    main()
