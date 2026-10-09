import requests
import csv
from lxml import html

#常量
MOVIE_LIST_FILE = "csv_data/movies.csv"
tmbd_base_url = "https://www.themoviedb.org"
tmbd_top_url = "https://www.themoviedb.org/movie/top-rated"#高分榜单(默认为第一页)


#定义函数,获取电影详情
def get_movie_info(url):
    #发送请求,获取电影详情数据
    response = requests.get(url,timeout=20)
    print (f"发送请求{url},获取电影详情数据...")  # 打印请求的url

    #解析数据
    document = html.fromstring(response.text)
    name=document.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")[0]#电影名称
    year=document.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")[0]#年份
    score=document.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')[0]#评分
    time=document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]/text()')[0]#时间
    tags=document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a/text()')#标签
    slogan=document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/h3[1]/text()')[0]#标语
    # print("电影名称:", name)
    # print("年份:", year)
    # print("评分:", score)
    # print("标签:", tags)
    # print("标语:", slogans)
    # print("-------------\n")

    #返回电影详情----字典
    movie_info= {
        "电影名称": name.strip(),
        "年份": year.strip(),
        "评分": score.strip(),
        "时间": time.strip(),
        "标签": ",".join(tags),  #这个特殊,因为标签有多个;join() 的作用就是：把多个字符串拼接成一个字符串，并在它们中间插入指定的分隔符
        "标语": slogan.strip()
    }
    # print(movie_info)
    return movie_info



#定义函数,保存所有电影数据
def save_all_movies(all_movies):
    with open(MOVIE_LIST_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["电影名称", "年份", "评分", "时间", "标签", "标语"])#fieldnames告诉 CSV：我要哪几列，以及列的顺序是什么;csv.dictWriter 是 CSV 模块中的一个类，用于将字典写入 CSV 文件
        writer.writeheader()
        writer.writerows(all_movies)


def main():
    #发送请求,获取高分榜单数据
    response = requests.get(tmbd_top_url,timeout=20)
    print ("发送请求,获取高分榜单数据:", tmbd_top_url)

    #解析数据,获取电影列表
    document = html.fromstring(response.text)
    movie_list=document.xpath('//div[contains(@class, "media-list-results")]/div[@data-object-id]')

    #遍历电影列表,获取电影详情
    all_movies=[]#存储所有电影详情信息
    for movie in movie_list:
        movie_urls=movie.xpath("./div/div/a/@href")
        if movie_urls:
            # 拼接电影详情页url
            movie_info_url=tmbd_base_url+movie_urls[0]
            #发送请求,获得电影详情数据
            movie_info=get_movie_info(movie_info_url)

            all_movies.append(movie_info)#将获取的电影详情添加到列表中

    #保存数据csv形式
    print("保存获取到的电影数据csv形式...")
    save_all_movies(all_movies)

if __name__ == "__main__":#如果直接执行当前文件,该条件就会成立
    main()