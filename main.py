#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import subprocess
import time
import urllib.parse

VPN_HOST = "202.170.220.26"

# 构造 SAML URL
saml_url = f"https://{VPN_HOST}/+webvpn+/index.html"

# 配置 Firefox
options = Options()
options.set_preference("general.useragent.override", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0")

driver = webdriver.Firefox(options=options)

print(f"打开 SAML 登录页面: {saml_url}")
driver.get(saml_url)

print("请在浏览器中完成 Microsoft 登录...")
print("登录成功后按 Enter...")
input()

# 获取所有 cookie
cookies = driver.get_cookies()
driver.quit()

# 构造 cookie 字符串
cookie_dict = {c['name']: c['value'] for c in cookies}
cookie_str = "; ".join([f"{k}={v}" for k, v in cookie_dict.items() 
                       if k in ['acSamlV2Token', 'webvpn', 'webvpn_as', 'webvpnc']])

print(f"获取到的 Cookies: {cookie_str[:100]}...")

if cookie_str:
    print("启动 OpenConnect...")
    subprocess.run([
        "sudo", "openconnect", VPN_HOST,
        "--protocol=anyconnect",
        "--cookie=" + cookie_str,
        "--servercert", "pin-sha256:d1WgDyHpDruxoCt3tB1lov+BUmcg9tAAfQxPLcmkexE="
    ])
else:
    print("未找到有效 cookie")