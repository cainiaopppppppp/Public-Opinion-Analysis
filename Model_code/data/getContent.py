import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


def getHTML(url, retry_count=0):
    if retry_count >= 2:
        print("bad link")
        return "error"
    headers = {
        # 将爬虫请求伪装成浏览器请求
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0"
                      "Safari/537.36",
        "Cookie": 'Hm_lvt_8599a277a3d6cd905c4c8049e95b1b10=1698286350; '
                  '__yjs_duid=1_2318cb2d089cacf7e0554708027c545c1698286350160; _ga=GA1.1.305747913.1698286351; '
                  'Hm_lpvt_8599a277a3d6cd905c4c8049e95b1b10=1698306727; '
                  '_ga_TMDYMXLY7K=GS1.1.1698303472.2.1.1698306730.0.0.0'
    }
    try:
        response = requests.get(url=url, headers=headers, params=None, timeout=5)
        try:
            html = response.content.decode("gbk")
        except Exception as e:
            html = response.content.decode("utf-8")
        return html
    except Exception as e:
        print("Error occured when fetching URL:", str(e))
        print("Trying reconnected")
        time.sleep(5)
        return getHTML(url, retry_count + 1)


def main():
    links = []
    datalist = []
    badlinks = []
    with open("URL.txt", mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace("\n", '')
            links.append(line)
    total = len(links)
    with tqdm(total=total) as t:
        for i, link in enumerate(links):
            t.update(1)
            html = getHTML(link)
            if html == "error":
                badlinks.append(link)
                continue
            soup = BeautifulSoup(html, "html.parser")
            contents = soup.select("div.rm_txt_con.cf p[style]")
            for content in contents:
                content = content.text
                datalist.append(content)
    total = len(datalist)
    with open("content.txt", mode='a+', encoding='utf-8', newline='') as file, tqdm(total=total) as t:
        for data in datalist:
            file.write(data + '\n')
            t.update(1)


if __name__ == "__main__":
    main()
