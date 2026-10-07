from lxml import html

#读取html文件
with open("resources./仙逆人物志.html","r",encoding="utf-8") as f:
    html_text = f.read()

    #解析html文件,并将其转换为一个文档对象
    document = html.fromstring(html_text)

    #解析表头
    th_list=document.xpath("//table/thead/tr/th/text()")#从table定位就可以
    print(th_list)
    #.xpath是一种查询html/xml文件的语法

    # #解析表内容
    # td_list=document.xpath("//table/tbody/tr//td/text()")
    # print(td_list)

    #解析表内容
    tr_list=document.xpath("//table/tbody/tr")#获取tr元素列表
    for tr in tr_list:
        td_list=tr.xpath("./td/text()")#从当前目录下获取td元素列表
        print(td_list)
