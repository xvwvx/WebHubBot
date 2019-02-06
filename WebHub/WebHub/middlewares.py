# encoding=utf-8
import base64
import random
import time

from scrapy.http import HtmlResponse

from WebHub.user_agents import agents
import json



class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """
    cookie = {
        'platform': 'pc',
        'ss': '367701188698225489',
        'bs': '%s',
        'RNLBSERVERID': 'ded6699',
        'FastPopSessionRequestNumber': '1',
        'FPSRN': '1',
        'performance_timing': 'home',
        'RNKEY': '40859743*68067497:1190152786:3363277230:1'
    }

    def process_request(self, request, spider):
        bs = ''
        for i in range(32):
            bs += chr(random.randint(97, 122))
        _cookie = json.dumps(self.cookie) % bs
        request.cookies = json.loads(_cookie)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:1087"

        # proxy_user_pass = "username:password"
        # encoded_user_pass = base64.b64encode(proxy_user_pass.encode('utf-8'))
        #
        # # setup basic authentication for the proxy
        # request.headers['Proxy-Authorization'] = 'Basic ' + str(encoded_user_pass, encoding="utf-8")

class PhantomJSMiddleware(object):
    def process_request(self, request, spider):
        if request.url.startswith('https://www.pornhub.com/embed/'):
            driver = webdriver.PhantomJS()
            driver.get(request.url)
            time.sleep(1)
            # driver.execute_script()

            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request, status=200)


from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChromeMiddleware(object):
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # options.add_argument('--proxy=proxy.com:8080')
        # options.binary_locaion = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        if 'Chrome' in request.meta:
            driver = self.driver
            driver.get(request.url)
            show = EC.presence_of_element_located((By.XPATH, '//*[@id="player"]/div[21]/video/source'))
            self.wait.until(show)
            # driver.execute_script()

            body = driver.page_source.encode('utf-8')
            response = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
            return response