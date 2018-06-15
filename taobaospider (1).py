from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import pymongo

MONGO_URL='localhost'
MONGO_DB='Taobao'
MONGO_TABLE='Food'

KEYWORD='美食'

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

browser=webdriver.Chrome()
wait=WebDriverWait(browser,10)

#搜索
def search():
    try:
        browser.get('https://www.taobao.com/')
    except TimeoutException:
        return search()
    try:
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
        button=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)
        button.click()
        page=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total'))).text
        get_information(browser.page_source)
        return page
    except NoSuchElementException:
        return search()

def next_page(num_page):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(num_page)
        button.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'.items .item.active'),str(num_page)))
        print('翻页：',num_page)
        get_information(browser.page_source)
    except TimeoutException:
        next_page(num_page)

def get_information(html):
    soup=BeautifulSoup(html,'lxml')
    imgs = soup.select('.pic img.J_ItemPic')
    prices =soup.select('.price')
    counts=soup.select('.deal-cnt')
    names=soup.select('.title')
    shops=soup.select('.shop')
    locations=soup.select('.location')
    for i in range(len(imgs)):
        product={
            'img':imgs[i].attrs['src'],
            'price':prices[i].get_text().strip(),
            'count':counts[i].get_text(),
            'name':names[i].get_text().strip(),
            'location':locations[i].get_text(),
            'shop':shops[i].get_text().strip()
        }
        save_to_mongo(product)

def save_to_mongo(info):
    try:
        if db[MONGO_TABLE].insert(info):
            print('成功保存：',info)
    except Exception:
        print('保存失败：',info)

def main():
    page=search()
    pattern=re.compile('(\d+)')
    page = int(re.search(pattern,page).group(1))
    for i in range(2,page+1):
        next_page(i)

if __name__=='__main__':
    main()
