import requests
from lxml import html
# 第一次测试 Git 修改追踪


#定义url
target_url="https://www.tiobe.com/tiobe-index/"

#发送请求.获取数据
response = requests.get(target_url)
data = response.text

#输出数据
print(data)
