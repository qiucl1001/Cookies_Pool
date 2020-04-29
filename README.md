# Cookies_Pool

![](https://img.shields.io/badge/python-3.7%2B-brightgreen)

可扩展的Cookies池，目前对接了新浪微博、有缘网，[m.weibo.cn](https://m.weibo.cn)、[youyuan.com](http://www.youyuan.com)
可自行扩展其他站点

简易高效可扩张的cookies池，提供如下功能：

* 定时抓取需要登录的特定网站cookies，简易可扩展。
* 使用 Redis的散列表做二级分类(Hash name: [accounts:website]、[cookies:website])对cookies进行存储
* 定时测试和筛选，剔除过期cookies，留下可用cookies。
* 提供cookies API，随机取用测试通过的cookies。

## 账号购买

账号可在淘宝购买


## 导入账号
```
python3 importer.py
```

## 使用要求

### 常规方式

常规方式要求有 Python 环境、Redis 环境，具体要求如下：

* Python Versions: >=3.7
* Redis

### 安装和配置 Redis

本地安装Redis, 启动Redis、远程 Redis 都是可以的，只要能正常连接使用即可。

首先需要配置一下环境变量，代理池会通过环境变量读取这些值。

设置 Redis 的环境变量有两种方式，一种是分别设置 host、port、password，另一种是设置连接字符串，设置方法分别如下：

设置 host、port、password，如果 password 为空可以设置为空字符串，示例如下：

```shell script
export REDIS_HOST='localhost'
export REDIS_PORT=6379
export REDIS_PASSWORD=''
export REDIS_DATABASE_NUM=12  # default redis_database_num=0 
```

或者只设置连接字符串：

```shell script
export REDIS_CONNECTION_STRING='redis://[:password]@host:port/num'
```
这里连接字符串的格式需要符合 `redis://[password]@host:port/num` 的格式。

以上两种设置任选其一即可。

### 安装依赖包

这里强烈推荐使用 [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) 
或 [virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html) 创建虚拟环境，Python 版本不低于 3.7。

然后 pip 安装依赖即可：

```shell script
pip3 install -r requirements.txt
```

### 运行代理池

*请先导入一部分账号之后再运行，运行命令：

两种方式运行代理池，一种是 Tester、Generator、Server 全部运行，另一种是按需分别运行。

一般来说可以选择全部运行，命令如下：

```
python3 importer.py
```

```shell script
python3 run.py
```

运行之后会启动 Tester、Generator、Server，
这时访问 [http://localhost:5000/<weibste>/random/cookies](http://localhost:5000/<website>/random/cookies) 
即可获取一个随机可用代理。
* 注意：这里<website>是指定要获取cookies所在的网站，e.g:<weibo>-->获取[https://m.weibo.cn]该网站对应的cookies

## 使用

成功运行之后可以通过 [http://localhost:5000/<weibste>/random/cookies](http://localhost:5555/random) 获取一个随机可用代理。

可以用程序对接实现，下面的示例展示了获取代理并爬取网页的过程：

```python
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
    print({"status_code": response.status_code})


if __name__ == '__main__':
    main()
```
运行结果如下：
```
 get random cookies from cookies_pool: {'1028305008_showTodayLove': 'true', 'visitedMsg1028305008': '3', 'Hm_lpvt_c50069af1fd1adc2cb066a862bd83f1c': '1588123587', 'radomUserId': '1588123580862_RO4AMKXNOO2UKPMS', 'today_love_key': 'space', '__auc': 'db0a2c58171c38abe21bead391d', 'UYYU': 'XLBIHBYYIB67P3UM7KRYSRGB2XLHGAL7LYS3AUJXO343DI5T5DUR2RCI74FEUQKAXR7HVYJSSWKVO===', '__asc': 'db0a2c58171c38abe21bead391d', 'JSESSIONID': 'aaaQIF6gRq6Znas1OAahx', 'Hm_lvt_c50069af1fd1adc2cb066a862bd83f1c': '1588123581', 'cckShow': 'false', '__cdnuid_h': 'f7685a80080d2b0c14fb61ff0795f1cc', 'out_url': 'N'}
{"status_code": 200}
```

可以看到成功获取了cookies，并请求 http://www.youyuan.com/v30/apps/today_love.html 返回了响应状态码200，验证了cookies的可用性。

## 可配置项

代理池可以通过设置环境变量来配置一些参数。

### 开关

* ENABLE_TESTER：允许 Tester 启动，默认 true
* ENABLE_GETTER：允许 Getter 启动，默认 true
* ENABLE_SERVER：运行 Server 启动，默认 true

### 环境

* APP_ENV：运行环境，可以设置 dev、test、prod，即开发、测试、生产环境，默认 dev
* APP_DEBUG：调试模式，可以设置 true 或 false，默认 true

### Redis 连接

* REDIS_HOST：Redis 的 Host
* REDIS_PORT：Redis 的端口
* REDIS_PASSWORD：Redis 的密码
* REDIS_CONNECTION_STRING：Redis 连接字符串

### 处理器

* CYCLE：Tester、Generator 运行周期，即间隔多久运行一次测试，默认 20 秒
* TEST_URL_MAP：测试 URL映射，不同网站对应测试地址
* API_HOST：代理 Server 运行 Host，默认 0.0.0.0
* API_PORT：代理 Server 运行端口，默认 5000
* API_THREADED：代理 Server 是否使用多线程，默认 true

### 日志

* LOG_DIR：日志相对路径
* LOG_RUNTIME_FILE：运行日志文件名称
* LOG_ERROR_FILE：错误日志文件名称
