### Pixiv画师图片爬虫
---
**简介：**
该程序主要用来爬取 **pixiv** `https://www.pixiv.net/` 画师的图片

**使用方法：**
1. 前置准备
```python
# 请确保你拥有一些最基本的web知识
# 填写pixiv_reptile.py下面的 User-Agent 和 Cookie
headers = {
    'User-Agent':'...',
    'Referer':'https://www.pixiv.net/',
    'Cookie':'...'
}
```
2. 运行程序
```python
python pixiv_reptile.py
# 程序会提示你输入画师的uid，选择你喜欢的画师uid填入即可
```
3. 等待结果
```python
# 程序会提示下载进度
# 完成以后在当前文件夹的image文件夹内可以找到你要的图片
```
<br>

**前置库**
若缺失请使用 `pip install` 指令进行安装
```python
from bs4 import BeautifulSoup
import requests
import json
import os
```
<br>

**作者的话：**
这只是一次小尝试，算是我第一次学python做的东西了，如果发现问题(BUG)，或者有更好的改进方法，都可以和我联系。

**联系方式：**
GitHub: **https://github.com/Anainoyume**
QQ邮箱: **1684221962@qq.com**

### 更新记录
---
**2023.10.17**
解决了下载不了图册的问题，之前只能下载封面，现在可以下载里面全部的内容了

**2023.10.26**
修复了一些请求的图片里不包含Content-Length，导致下载进度计算错误的问题，现在对于没有Content-Length的图片下载，将直接显示 `Downloading...` 不会进行计算下载进度。