# bs4 与 requests 的结合使用
'''
    requests的作用是模拟请求网页,而bs4的作用便是解析我们获得的html代码
'''
from bs4 import BeautifulSoup
import requests
import json
import os

# 记录画师作品uid的网页，根据实际情况修改
print('请输入画师uid: ')
author_id = input()

url = f'https://www.pixiv.net/ajax/user/{author_id}/profile/all?lang=zh&version=7707a7b6e474a4d07889017bf5b6707451f95ba9'

# 进入pixiv首页的标头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Referer':'https://www.pixiv.net/',
    'Sec-Fetch-Site':'cross-site',
    'Cookie':'first_visit_datetime_pc=2023-10-15%2020%3A54%3A16; p_ab_id=1; p_ab_id_2=2; p_ab_d_id=1092508805; yuid_b=FDIVY5Y; _fbp=fb.1.1697370859567.1977225397; privacy_policy_agreement=6; device_token=d537e90ebd7097b9e383a50c3866c1cd; privacy_policy_notification=0; a_type=0; b_type=0; _im_vid=01HCSK1FNSTZZE2Y951XBGTM2B; _im_uid.3929=b.0ad740c8178a4940; _gcl_au=1.1.254438710.1697637384; login_ever=yes; howto_recent_view_history=101954965%2C59452194; __cf_bm=lqi2ehZdKnCMbYFOZeJCA0AFKUAw.iirn7HDKGOSXgg-1698311014-0-AaTKoCVPj4QObFzh48Vu5Xd7MIQXql5rnNA21n2ARs0knoM+/A30Nct1jEhjF4W4QijDxO/MQEkGUFVWbi25PJdOKzKu5Dv5lHE5UN7RDOXJ; cf_clearance=C87.Tf0w6uTVSJppuewoWmvlWIoZ_mqHjTChaocMO8k-1698311019-0-1-818fea4a.eb2a95da.d68eb5aa-0.2.1698311019; _gid=GA1.2.1808724708.1698311021; PHPSESSID=81229234_0vg93tqU3iECmBjS4oPFs1lBkyQRA4qY; c_type=20; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; cto_bundle=LiMapV9uR2pXUFpJRVdQTmVpJTJGcDMwWHc2NXM4aWFJWEFyJTJGdUtzWFJrTDN5OUZRVEklMkJBWHZPOEc3QkNOZiUyQlhaTUVNVDdJblR2NGVhTlFaM21sOFlscUdya3ZRZnZtaEtZRnJhVEtrMmxlNUp2RVJwTXhPOG1zJTJGRFF3TEtTMzRWNWFXSzU; _gat_UA-1830249-3=1; _ga=GA1.1.349102705.1697370858; _ga_75BBYNYN9J=GS1.1.1698311017.11.1.1698312741.0.0.0'
}

# 下载函数 mika uid:1039353
def download_img(downloadURL,pageCount,uid):
    download = requests.get(downloadURL,headers=headers,stream=True)
    if (download.status_code != 200):
        downloadURL = downloadURL[:downloadURL.find(f'_p{pageCount}')] + f'_p{pageCount}.png'
        download = requests.get(downloadURL,headers=headers,stream=True)

    # 有些请求不会记录content-length信息
    if (download.headers.get("Content-Length") is not None):
        Total = int(download.headers.get("Content-Length"))    #获取文件内容长度
    else:
        Total = -1
    with open(f'./image/{uid}_p{pageCount}.png','wb') as img:
        cur = 0
        for chunk in download.iter_content(chunk_size=100):
            cur += img.write(chunk)    # 返回的是读入的长度
            if (Total != -1):
                print(f'\r{uid}_p{pageCount}.png --> ' + 'Download: %02.2f%%' % (100 * cur / Total), end='')
            else:
                print(f'\r{uid}_p{pageCount}.png --> ' + 'is downloading...', end='')

r = requests.get(url,headers=headers)

data = json.loads(r.text)

uids = list(data['body']['illusts'].keys())

with open('debug_uid.txt','w',encoding='utf-8') as tmp:
    for uid in uids:
        tmp.write(uid+'\n')

img_count = 0

try:
    for uid in uids:
        work_url = 'https://www.pixiv.net/artworks/' + uid
        artwork = requests.get(url=work_url,headers=headers)
        # 这里的artwork就是每一个我们访问的网页了，我们使用bs进行解析
        soup = BeautifulSoup(artwork.text, 'html.parser')
        date = json.loads(soup.find("meta",attrs={"name":"preload-data","id":"meta-preload-data"})["content"])
        str = date['illust'][uid]['userIllusts'][uid]['url']
        pageCount = int(date['illust'][uid]['userIllusts'][uid]['pageCount'])

        # 新建文件夹
        if not os.path.exists('image'):
            os.makedirs('image')

        for curPage in range(pageCount):
            download_url = 'https://i.pximg.net/img-original/img/' + str[str.find('/img/')+5:str.find('_p')] + f'_p{curPage}.jpg'
            # print(download_url)
            download_img(download_url,curPage,uid)
            print('')
            img_count += 1
except:
    print(f'下载结束! 共计下载 {img_count} 张图片!')

