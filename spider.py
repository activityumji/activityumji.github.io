import re
import time
import random
import traceback
import requests
import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
from config import WECHAT_ACCOUNTS, DB_PATH, COVER_PATH, USER_AGENT


class Spider(object):
    """
    微信公众号文章爬虫
    """

    def __init__(self):
        # 微信公众号账号
        self.account = ""
        # 微信公众号密码
        self.pwd = ""

    def create_driver(self):
        """
        初始化 webdriver
        """
        options = webdriver.ChromeOptions()
        # 禁用gpu加速，防止出一些未知bug
        options.add_argument("--disable-gpu")

        # 这里我用 chromedriver 作为 webdriver
        # 可以去 http://chromedriver.chromium.org/downloads 下载你的chrome对应版本
        # TODO: executable_path and chrome_options are deprecated
        self.driver = webdriver.Chrome(
            executable_path=r"./chromedriver",
            chrome_options=options,
        )
        # 设置一个隐性等待 5s
        self.driver.implicitly_wait(5)

    def log(self, msg):
        """
        格式化打印
        """
        print("------ %s ------" % msg)

    def login(self):
        """
        登录拿 cookies
        """
        try:
            self.create_driver()
            # 访问微信公众平台
            self.driver.get("https://mp.weixin.qq.com/")
            # 等待网页加载完毕
            time.sleep(3)
            """WARNING: Not tested
            # 输入账号
            self.driver.find_element(By.XPATH,"./*//input[@name='account']").clear()
            self.driver.find_element(By.XPATH,"./*//input[@name='account']").clear()
            self.driver.find_element(By.XPATH,"./*//input[@name='account']").send_keys(self.account)
            # 输入密码
            self.driver.find_element(By.XPATH,"./*//input[@name='password']").clear()
            self.driver.find_element(By.XPATH,"./*//input[@name='password']").send_keys(self.pwd)
            # 点击登录
            self.driver.find_elements_by_class_name('btn_login')[0].click()
            """
            self.log("请拿手机扫码二维码登录公众号")
            # 等待手机扫描
            time.sleep(10)
            self.log("登录成功")
            # 获取cookies 然后保存到变量上，后面要用
            self.cookies = {x["name"]: x["value"] for x in self.driver.get_cookies()}
        except Exception as e:
            traceback.print_exc()
        finally:
            # 退出 chrome
            self.driver.quit()

    def get_article(self, query=""):
        try:
            url = "https://mp.weixin.qq.com"
            headers = {
                "HOST": "mp.weixin.qq.com",
                "User-Agent": USER_AGENT,
                "Connection": "close",
            }
            # 登录之后的微信公众号首页url变化为
            # https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1234567890
            response = requests.get(url=url, cookies=self.cookies)
            try:
                token = re.findall(r"token=(\d+)", str(response.url))[0]
            except IndexError:
                self.log("获取 token 失败")
                exit(1)

            time.sleep(2)
            self.log("正在查询[ %s ]相关公众号" % query)
            search_url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
            # 搜索微信公众号接口需要传入的参数，
            # 有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
            params = {
                "action": "search_biz",
                "token": token,
                "random": random.random(),  # I am not sure this is necessary
                "query": query,
                "lang": "zh_CN",
                "f": "json",
                "ajax": "1",
                "begin": "0",
                "count": "5",
            }
            # 打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
            response = requests.get(
                search_url, cookies=self.cookies, headers=headers, params=params
            )
            time.sleep(2)
            # 取搜索结果中的第一个公众号
            try:
                lists = response.json().get("list")[0]
            except IndexError:
                self.log("没有搜索到公众号[ %s ]" % query)

            # 获取这个公众号的fakeid，后面爬取公众号文章需要此字段
            fakeid = lists.get("fakeid")
            nickname = lists.get("nickname")

            # 微信公众号文章接口地址
            search_url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
            # 搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
            params = {
                "action": "list_ex",
                "token": token,
                "random": random.random(),
                "fakeid": fakeid,
                "lang": "zh_CN",
                "f": "json",
                "ajax": "1",
                "begin": "0",  # 不同页，此参数变化，变化规则为每页加5
                "count": "5",
                "query": "",
                "type": "9",
            }
            self.log("正在查询公众号[ %s ]相关文章" % nickname)
            # 打开搜索的微信公众号文章列表页
            response = requests.get(
                search_url, cookies=self.cookies, headers=headers, params=params
            )

            time.sleep(2)
            data = response.json().get("app_msg_list", [])
            self.write_db(
                [
                    (
                        article.get("aid"),
                        article.get("create_time"),
                        date.fromtimestamp(article.get("create_time")).isoformat(),
                        article.get("title"),
                        query,
                        article.get("cover"),
                        article.get("link"),
                    )
                    for article in data
                ]
            )
        except Exception as e:
            traceback.print_exc()

    def write_db(self, data):
        """Write spider output to CSV database.

        DB line structure:
        aid, UNIX timestamp, YYYY-MM-DD, article title, author account, cover URL, article URL

        where aid is a unique (or at least I'm pretty sure it is) attribute
        wechat gives to each article. If a single article is pushed to users
        in appmsgid=2651188302, its aid is 2651188302_1. If multiple articles
        are pushed in one message (album), the suffixes become _1, _2, etc.

        aid was not present in the legacy database. After the conversion,
        they are assigned aids in "legacy_{unix_timestamp}" format.

        The aid is NOT an integer and should not be parsed as such.
        """
        db_file = open(DB_PATH)
        # TODO: this gets inefficient as DB grows
        reader = csv.reader(db_file)
        articles = list(reader)
        db_file.close()

        aids = [art[0] for art in articles]
        for article in data:
            # append new article to DB, skip when exists
            if article[0] in aids:
                continue
            articles.append(article)

        # sort articles from most recent to least
        articles.sort(key=lambda art: int(art[1]), reverse=True)

        db_file = open(DB_PATH, "w")
        writer = csv.writer(db_file)
        writer.writerows(articles)
        db_file.close()

    def download_covers(self):
        """Read cover URLs from DB and save to disk."""
        headers = {"user-agent": USER_AGENT}

        db_file = open(DB_PATH)
        reader = csv.reader(db_file)
        articles = list(reader)
        aids = [art[0] for art in articles]
        urls = [art[5] for art in articles]

        for aid, url in zip(aids, urls):
            # TODO: detect jpeg/png
            fp = COVER_PATH / f"{aid}.jpg"
            try:
                with open(fp, "xb") as f:
                    self.log(f"Downloading {url} to {fp}")
                    resp = requests.get(url, headers=headers)
                    f.write(resp.content)
                    f.close()
            except FileExistsError:
                # skip saved covers
                continue
            except Exception as e:
                traceback.print_exc()


if __name__ == "__main__":
    try:
        f = open(DB_PATH, "x")
        f.close()
    except FileExistsError:
        pass

    spider = Spider()
    spider.login()
    for acct in WECHAT_ACCOUNTS:
        spider.get_article(acct)
    spider.download_covers()
