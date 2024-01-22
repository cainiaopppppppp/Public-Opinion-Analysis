import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def getURL(url):
    datalist = []
    driver = webdriver.Edge()
    driver.minimize_window()
    count = 1
    driver.get(url)
    while count <= 50:
        time.sleep(3)
        pagenum = len(driver.find_elements(By.XPATH, '//*[@id="rmw-search"]/div/div[2]/div[3]/div/span'))
        nextBtn = driver.find_element(By.XPATH, '//*[@id="rmw-search"]/div/div[2]/div[3]/div/span[' + str(pagenum) + ']')
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select("li > div.content > div.ttl > a")
        for link in links:
            datalist.append(link['href'])
        count += 1
        nextBtn.click()
        if count % 5 == 0:
            with open("URL.txt", encoding='utf-8', mode='a+', newline='') as file:
                for data in datalist:
                    file.write(data + '\n')
            datalist = []
    driver.close()


def main():
    url1 = "http://search.people.cn/s?keyword=%E4%BA%9A%E5%A4%AA%E7%BB%84%E7%BB%87%E6%96%B0%E4%BA%9A%E5%A4%AA%E8%81%94%E7%9B%9F&st=0&_=1701172388626"
    getURL(url1)
    url2 = "http://search.people.cn/s?keyword=%E4%BA%9A%E5%A4%AA%E7%BB%84%E7%BB%87%E7%BE%8E%E6%97%A5%E5%8D%B0%E6%BE%B3&st=0&_=1701172408013"
    getURL(url2)
    url3 = "http://search.people.cn/s?keyword=%E4%BA%9A%E5%A4%AA%E7%BB%84%E7%BB%87%E7%BE%8E%E6%97%A5%E8%81%94%E7%9B%9F&st=0&_=1701172427870"
    getURL(url3)
    url4 = "http://search.people.cn/s?keyword=%E4%BA%9A%E5%A4%AA%E7%BB%84%E7%BB%87%E4%BA%94%E7%9C%BC%E8%81%94%E7%9B%9F&st=0&_=1701172442405"
    getURL(url4)
    url5 = "http://search.people.cn/s?keyword=%E4%BA%9A%E5%A4%AA%E7%BB%84%E7%BB%87%E7%BE%8E%E6%97%A5%E9%9F%A9&st=0&_=1701172457060"
    getURL(url5)
    url6 = "http://search.people.cn/s?keyword=%E4%BA%9A%E5%A4%AA%E7%BB%84%E7%BB%87%E4%B8%9C%E5%8D%97%E4%BA%9A%E8%81%94%E7%9B%9F&st=0&_=1701172471978"
    getURL(url6)
    url7 = "http://search.people.cn/s?keyword=%E4%BA%9A%E5%A4%AA%E7%BB%84%E7%BB%87%E4%B8%9C%E7%9B%9F&st=0&_=1701172491080"
    getURL(url7)


if __name__ == "__main__":
    main()
