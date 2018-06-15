import pymongo
import requests
from bs4 import BeautifulSoup

#思路
#1.获取格言的首页（人生格言的首页）
#2.在首页当中获取每一个二级页面的链接（所以需要for循环）
#3.在进入二级页面之后，获取想要的东西（标题，内容）
#4.保存到mongo
#5.主函数，主函数内要进行翻页（for循环）
#6.id __name__=="__main__"
MONGO_URL='localhost'
MONGO_DB='geyan'
MONGO_TABLE='geyangeyan'
client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]


url='https://www.geyanw.com/html/renshenggeyan/list_4_1.html'

headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'

}


def get_first_page(url):#获取首页并且响应
    response=requests.get(url,headers=headers)
    html=response.text
    #html=response.text
    #print(html)
    return html



def into_page_two(html):#选择进入二级页面的所有链接，for循环，BS4
    # print(type(html))
    soup=BeautifulSoup(html,'lxml')
    href=soup.select('.newlist h2 a')
    href_list=[]
    for i in href:
        href_list.append('https://www.geyanw.com'+i.attrs['href'])
    return href_list


def text_intro(href_list):#在进入二级页面之后，获取想要的东西（标题，内容）
    all_url_list=[]
    for i in href_list:
        response=requests.get(i,headers=headers)
        html=response.content.decode("gb18030")
        soup=BeautifulSoup(html,'lxml')
        ev_title= soup.select('.viewbox .title h2')
        content=soup.select('.content p')
        all_url_list.append(ev_title)
        all_url_list.append(content)

        # print(all_url_list)
    save_to_mong(all_url_list)
    return (all_url_list)

def save_to_mong(all_info):
    # print(type(all_info))
    if db['geyan'].insert(all_info):
        print('保存成功',all_info)
    else:
        print('保存失败',all_info)


# def save(info):
#     for list in info:
#         print(list)
#         with open('brigeyanb.txt','a',encoding='utf8',errors='strict') as f:
#             f.write(str(list))



def main():#主函数，调用所有步骤，并且进行翻页
    i=''
    for i in range(6):
        url= 'https://www.geyanw.com/html/renshenggeyan/list_4_'+str(i)+'.html'
        text=get_first_page(url)
        wenben = into_page_two(text)
        all_text_con=text_intro(wenben)
        save_to_mong(all_text_con)
        # save(all_text_con)




if  __name__=="__main__":
    main()