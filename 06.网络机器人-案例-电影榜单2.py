import requests
import csv
from lxml import html

#常量
MOVIE_LIST_FILE = "csv_data/movies.csv"
tmbd_base_url = "https://www.themoviedb.org"
tmbd_top_url_1= "https://www.themoviedb.org/movie/top-rated"#高分榜单(默认为第一页)
tmbd_top_url_2= "https://www.themoviedb.org/discover/movie/items"#通过前端页面表头查看


#定义函数,获取电影详情
def get_movie_info(url):
    #发送请求,获取电影详情数据
    response = requests.get(url,timeout=20)
    print (f"发送请求{url},获取电影详情数据...")  # 打印请求的url

    #解析数据
    document = html.fromstring(response.text)
    name=document.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")#电影名称
    year=document.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")#年份
    score=document.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')#评分
    time=document.xpath('//*[@id="original_header"]//span[contains(@class, "runtime")]/text()')#时间
    tags=document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a/text()')#标签
    slogan=document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/h3[1]/text()')#标语
    #可以把 XPath 定位理解成：先找“身份证”，再找“名字标签”，最后才按“第几个座位”找人。
    #id 就像身份证，class 像岗位名称，span[4] 就像“第四排第三个人”——网页一改布局，位置就变了。
    #这里定位的写法并不是很好,很容易有一些爬取为空



    #返回电影详情----字典
    movie_info= {
        "电影名称": name[0].strip() if name else '',#这个if可以避免有些数据没爬取到报错
        "年份": year[0].strip() if year else '',
        "评分": score[0].strip() if score else '',
        "时间": time[0].strip() if time else '',
        "标签": ",".join(tags) if tags else '',  #这个特殊,因为标签有多个;join() 的作用就是：把多个字符串拼接成一个字符串，并在它们中间插入指定的分隔符
        "标语": slogan[0].strip() if slogan else ''
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
    all_movies = []  # 存储所有电影详情信息
    #循环获取高分榜单数据,从第一页到第5页
    for page_num in range(1,6):
        #1.发送请求,获取高分榜单数据
        if page_num == 1:
            response = requests.get(tmbd_top_url_1,timeout=20)
        else:
            response = requests.post(tmbd_top_url_2, f"air_date.gte=&air_date.lte=&certification=&certification_country=US&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&vote_count.lte=&watch_region=US&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=top-rated", timeout=20)
            #这里是post请求体的源代码,只需要修改一下page对应的值就好了,改为page_num
        print (f"发送请求,访问{page_num}页获取高分榜单数据:" )

        #解析数据,获取电影列表
        document = html.fromstring(response.text)
        movie_list=document.xpath('//div[contains(@class, "media-list-results")]/div[@data-object-id]')

        #遍历电影列表,获取电影详情

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