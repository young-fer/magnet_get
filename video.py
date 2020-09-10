from urllib import request
from bs4 import BeautifulSoup
from retrying import retry
import requests

start_page = 1
end_page = 100
num = 1
url = 'https://www.dygod.net/html/gndy/dyzz/index.html'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    # 此处改为自己的headers
}


@retry(stop_max_attempt_number=3, wait_fixed=1000)
def down_link(video_url):

    global num
    video_res = requests.get(video_url, headers=headers, timeout=0.5)
    video_res.encoding = video_res.apparent_encoding
    html = BeautifulSoup(video_res.text, "html.parser")
    video_down = html.find("td", {"style": "WORD-WRAP: break-word"})
    video_magnet = video_down.find("a")["href"]
    with open("magnet01.txt", 'a') as f:
        f.write(video_magnet + "\n")
    print(str(num) + ".  " + video_magnet)
    num = num + 1


for i in range(start_page, end_page + 1):

    num = 1
    if i == 1:
        url = 'https://www.dygod.net/html/gndy/dyzz/index.html'
    else:
        url = 'https://www.dygod.net/html/gndy/dyzz/index_' + str(i) + '.html'

    res = requests.get(url, headers=headers, timeout=5)
    res.encoding = res.apparent_encoding
    html = BeautifulSoup(res.text, "html.parser")

    list = html.find("div", {"class": "co_content8"}).ul

    video_list = list.find_all("a")
    print("第", i, "页开始采集")
    start_info = "第" + str(i) + "页磁力连接采集：" + "\n"
    with open("magnet01.txt", 'a') as f:
        f.write(start_info)
    for each_video in video_list:
        video_url = "https://www.dygod.net/" + each_video["href"]

        try:
            down_link(video_url)
        except Exception as e:
            print("<此视频链接下载失败>" + str(e))

    finish_info = "完成进度" + str(num - 1) + "/25" + "\n\n\n"
    print(finish_info)
    with open("magnet01.txt", 'a') as f:
        f.write(finish_info)