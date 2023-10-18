# bs4 与 requests 的结合使用
'''
    requests的作用是模拟请求网页,而bs4的作用便是解析我们获得的html代码
'''
from bs4 import BeautifulSoup
import requests
import json
import os

# 下载函数 mika uid:1039353
def download_img(downloadURL,uid):
    download = requests.get(downloadURL,headers=headers,stream=True)
    if (download.status_code != 200):
        downloadURL = downloadURL[:downloadURL.find('_p0')] + '_p0.png'
        download = requests.get(downloadURL,headers=headers,stream=True)

    Total = int(download.headers.get("Content-Length"))    #获取文件内容长度
    with open(f'./image/{uid}.png','wb') as img:
        cur = 0
        for chunk in download.iter_content(chunk_size=100):
            cur += img.write(chunk)    # 返回的是读入的长度
            print(f'\r{uid}.png --> ' + 'Download: %02.2f%%' % (100 * cur / Total), end='')

# 记录画师作品uid的网页，根据实际情况修改
print('请输入画师uid: ')
author_id = input()

url = f'https://www.pixiv.net/ajax/user/{author_id}/profile/all?lang=zh&version=7707a7b6e474a4d07889017bf5b6707451f95ba9'

# 进入pixiv首页的标头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Referer':'https://www.pixiv.net/',
    'Cookie':'first_visit_datetime_pc=2023-10-15%2020%3A54%3A16; p_ab_id=1; p_ab_id_2=2; p_ab_d_id=1092508805; yuid_b=FDIVY5Y; _fbp=fb.1.1697370859567.1977225397; privacy_policy_agreement=6; PHPSESSID=81229234_JVzsc9gd1Q3BFufKiCp1bmE7jjqj6nqF; device_token=d537e90ebd7097b9e383a50c3866c1cd; c_type=19; privacy_policy_notification=0; a_type=0; b_type=0; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _im_vid=01HCSK1FNSTZZE2Y951XBGTM2B; _gid=GA1.2.1505717847.1697467294; cf_clearance=pwjudnwkuolopnXJZoHOaspY5yw5m84ik6LBrlRuV0w-1697467314-0-1-818fea4a.eb2a95da.d68eb5aa-0.2.1697467314; _im_uid.3929=b.0ad740c8178a4940; __cf_bm=HQCqlg3WDKYne6MsOqtccwhYw7Sxit3.GkUGNB4H78w-1697519203-0-AcRBmNM+SY9qOqjytpTF/PExRKRcWe4ewvrCrVWq0TopdZ8F04atuNGWVpbM4vJb3eI/DvG6aqRDS5DMpx9DWTgyxmjfzyjoSShlzLz3g5cz; cto_bundle=ws9J1F9uR2pXUFpJRVdQTmVpJTJGcDMwWHc2NW5vWGVWMWMxRUFCUmNoZiUyRnI3WVlwV2lQVzNhTW50SHVUNENESVpmM001WjFselElMkJBVHNXYlNqJTJCNkpxc0JiRzNZb2tiMEclMkJYazBDWmpiTUgwUlY2cEg4bFVXSlBsNzNzdFdDU0RqRGVrQ0I; _gat_UA-1830249-3=1; _ga_75BBYNYN9J=GS1.1.1697517392.4.1.1697519311.0.0.0; _ga=GA1.2.349102705.1697370858'
}

r = requests.get(url,headers=headers)

data = json.loads(r.text)

uids = list(data['body']['illusts'].keys())

img_count = 0

try:
    for uid in uids:
        work_url = 'https://www.pixiv.net/artworks/' + uid
        artwork = requests.get(url=work_url,headers=headers)
        # 这里的artwork就是每一个我们访问的网页了，我们使用bs进行解析
        soup = BeautifulSoup(artwork.text, 'html.parser')
        date = json.loads(soup.find("meta",attrs={"name":"preload-data","id":"meta-preload-data"})["content"])
        str = date['illust'][uid]['userIllusts'][uid]['url']

        download_url = 'https://i.pximg.net/img-original/img/' + str[str.find('/img/')+5:str.find('_p0')] + '_p0.jpg'
        
        # 新建文件夹
        if not os.path.exists('image'):
            os.makedirs('image')

        download_img(download_url,uid)
        print('')
        img_count += 1
except:
    print(f'下载结束! 共计下载 {img_count} 张图片!')

