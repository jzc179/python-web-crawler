import requests
from lxml import html
from tomlkit import document

# 第一次测试 Git 修改追踪


#定义url
target_url="https://www.tiobe.com/tiobe-index/"

#发送请求.获取数据.response就是前端的html
response = requests.get(target_url)
document=html.fromstring(response.text)

#解析表头"
th_list=document.xpath("/html/body/section/div/article/table[1]/thead/tr/th/text()")#可以去页面找到element,复制xpath路径
print(th_list)



