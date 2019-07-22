####明星网图片下载###
====================

啥也不说，先亮出网页的页面
------------------------
![image](https://github.com/1jone/Spider-StarPicter/blob/master/images/start1.PNG)

这个网站收录了很多明星的照片，写真、生活、影视照（请绝对放心，照片完全`社会主义核心价值观`）
----------------------

###下面开始我写的简单爬虫代码

####所使用的扩展包
```Python
import requests
import chardet
import urllib
import os
import threading
from multiprocessing import Queue
from bs4 import BeautifulSoup
```
我使用的是Python3环境，使用requests来进行url请求，然后使用BeautifulSoup来设置响应内容的格式。接下根据响应的源码内容来提取需要的图片链接，之后使用threading多线程来进行图片的下载


####Url链接提取
```Python
def get_src(page_num):
	global name
	lists=[]
	for num in range(1,page_num+1):  #range(1,101)代表要爬取的页面页数，最高为500页
		print("-------当前页面%-3d-------"%num)
		try:
			soup=get_soup('http://www.mingxing.com/tuku/index?type=mxxz&p='+str(num))
		except Exception as e:
			print("页面%d获取失败！"%num)
			continue
		else:
			for inn in soup.find_all(class_="inn"):
				for a in inn.ul.find_all('a'):
					if name in a.get('title'):
						href=r'http://www.mingxing.com'+a.get('href')
						soup2=get_soup(href)
						for imgbox in soup2.find_all(class_="img-box"):
							img=imgbox.find('img')
							src=img.get('src')
							if src not in lists:
								lists.append(src)
	return lists
```
Url链接提取的基本思想是：先获取URL响应源码->查看源码->找出所需要的图片链接所在的标签->使用beautifulSoup自带的解析方法，根据图片链接所在的标签位置一级一级提取图片URL->将获取到的url存入list中

还有很多中提取URL链接的方法：比如利用正则表达式来提取；利用xpath提取；利用css来提取

####如何下载图片
```Python
def download(que):
	global num
	global local
                
	while True:
		if que.empty():
			print("图片已全部下载完成！")
			break
		try:
			url=que.get()
			num+=1
			print("第%-3d张 "%num,end="")
			urllib.request.urlretrieve(url,local+name+str(num)+'.jpg',Schedule)
		except Exception as e:
			print("！！！第%-3d条链接出错，已经跳过！！！"%i)
			continue
```
这个里面使用urllib包来下载图片，使用schedule调度器来显示下载的进度

另一种下载的方法是使用request.get()方法请求图片的url，然后将获取到的响应内容利用write()方法写入一个空白图片文件中。如：

```Python
def download(urls):
	global local
	i=1
	for url in urls:
		r = requests.get(url)
		with open(local+str(i)+'.jpg','wb') as pic:
			pic.write(r.content)
		i+= 1
	print("图片下载完成")
```

最后来看一下执行的效果吧
-----------------
下面爬一些 `林允儿` `女神` 的图片

![image](https://github.com/1jone/Spider-StarPicter/blob/master/images/lyr1.PNG)

![image](https://github.com/1jone/Spider-StarPicter/blob/master/images/lyr2.PNG)


提示：不要过高频率爬取该网站（一是对网站服务器有影响；另外过度爬取但是不是用IP代理池的话会被记录IP地址，限制访问）
---------------






















