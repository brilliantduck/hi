#思路分析
# url和头部放在外面，方便使用
# 1.运动girl一级页面，获取响应  def get_first_page(url):
# 2.遍历循环一级页面，得到链接  def get_first_page_use_for(html):   for
# 3.得到一级页面后进入二级页面，获取到二级页面相对应的照片的链接  def get_page_two(all_url):  for*2
# 4.保存  def save(topic):  for
# 5.主函数（翻页）  def main(folder='TOPI'):   for 改变url
# 6.if __name__

import requests
from bs4 import BeautifulSoup
import os

url='http://www.meizitu.com/a/yundong.html'

headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
'Referer':'http://www.meizitu.com/',
'Cookie':'bdshare_firstime=1525924893961; UM_distinctid=1634836151a27-0b2e28e2aebf83-3e3d5f01-100200-1634836151b159; safedog-flow-item=; CNZZDATA30056528=cnzz_eid%3D1541629977-1525920268-http%253A%252F%252Fwww.meizitu.com%252F%26ntime%3D1528705377'

}

# 1.运动girl一级页面，获取响应
def get_first_page(url):
    response=requests.get(url,headers=headers)
    # html=response.content.decode=('gbk')
    html=response.content.decode('gb18030')
    print('运动girl一级页面，获取响应成功')
    return html

# 2.遍历循环一级页面，得到链接
def get_first_page_use_for(html):
    all_url=[]
    response=requests.get(url,headers=headers)
    html = response.content.decode('gbk')
    soup=BeautifulSoup(response.text,'lxml')
    src=soup.select('#maincontent .pic a')
    for i in src:
        all_url.append(i['href'])
    print('all_url 获取成功')
    return all_url


# 3.得到一级页面后进入二级页面，获取到二级页面相对应的照片的链接
def get_page_two(all_url):
    topic=[]
    for url1 in all_url:
        print(url1)
        response=requests.get(url1,headers=headers)
        html=response.text
        soup=BeautifulSoup(response.text,'lxml')
        src=soup.select('#picture img')
        for i in src:
            topic.append(i.attrs['src'])
    # print(topic)
    print("最终图片的地址获取成功")
    return topic

# 4.保存
def save(topic):
    for url in topic:
        img=requests.get(url).content
        filename='TOPIC'
        name = url.split('/')
        filename = name[-2]+'-'+name[-1]
        with open(filename,'wb') as T:
            T.write(img)
    print("图片保存完成")

def main(folder='TOPIc'):
    os.mkdir(folder)
    os.chdir(folder)
    for i in range(5):
        url='http://www.meizitu.com/a/yundong_'+str(i)+'.html'
        getfirstpage = get_first_page(url)
        pageusefor=get_first_page_use_for(getfirstpage)
        # print(pageusefor)
        getpagetwo=get_page_two(pageusefor)
        save(getpagetwo)



if __name__=="__main__":
   main()




