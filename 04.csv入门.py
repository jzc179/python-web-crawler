#csv操作方式1:文件操作的原始方式
#写
# with open("csv_data/01.csv","w",encoding="utf-8") as f:
#     f.write("姓名,年龄,性别,爱好\n")
#     f.write("张三,18,男,Python\n")
#     f.write("李四,19,女,Java\n")
#     f.write("王五,20,男,Go\n")

# #读
# with open("csv_data/01.csv","r",encoding="utf-8") as f:
#     for line in f:
#         print(line.strip())


#csv操作方式2:   csv库
import csv
#写
with open("csv_data/02.csv","w",encoding="utf-8",newline="") as f:#newline=""表示不换行
    writer = csv.DictWriter(f,fieldnames=["name","age","sex","hobby"])
    writer.writeheader()#写入表头
    writer.writerow({"name":"张三","age":18,"sex":"男","hobby":"Python"})
    writer.writerow({"name":"李四","age":19,"sex":"女","hobby":"Java"})
    writer.writerow({"name":"王五","age":20,"sex":"男","hobby":"Go"})

#读
with open("csv_data/02.csv","r",encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
