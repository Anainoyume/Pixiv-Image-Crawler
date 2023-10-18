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
    'User-Agent':'...',
    'Referer':'https://www.pixiv.net/',
    'Cookie':'...'
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

