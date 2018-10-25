#encoding:utf-8
import requests
import chardet
import urllib
import os
import threading
from multiprocessing import Queue
from bs4 import BeautifulSoup


num=0   #全局变量，用于表示下载的图片数量
name='' #查询的人的姓名
local=''#图片存储路径


#显示当前下载进度
def Schedule(blocknum, blocksize,totalsize):
	'''''
	blocknum:已经下载的数据块
	blocksize:数据块的大小
	totalsize:远程文件的大小
	'''
	per = 100.0 * blocknum*blocksize/totalsize
	if per>100:
		per = 100
		print('下载进度：%d'%per)


#使用request获取网页
def get_soup(href):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = {'User-Agent':user_agent}
	r=requests.get(href,headers=headers)
	r.encode=chardet.detect(r.content)['encoding']
	soup=BeautifulSoup(r.text,'html.parser')
	return(soup)


#获取图片链接
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


#下载图片
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


#创建目录
def mk_dir():
	global name
	global local
	local=os.getcwd()
	try:
		os.mkdir(local+'\\'+'123')
		print("123目录创建完成！")   
	except:
		print("123目录已经存在！")

	local=local+'\\'+'123'+'\\'

	try:
		os.mkdir(local+name)  #图片的绝对存储地址
		print("%s目录创建完成!"%name)
	except:
		print("%s目录已经存在"%name)
	finally:
		local+=name+'\\'


#主函数方法
def main():
	global name
	global local
	name=input("输入想喜欢的明星姓名：")
	page_num=input("输入想要查询的页数(<=500)：")
	mk_dir()
	d=get_src(int(page_num))
	if d:
		threadNum=5
		que=Queue()
		print("*****************************")
		print("当前共找到%d张%s的图片"%(len(d),name))
		for i in d:
			que.put(i)
		for i in range(threadNum):
			t1=threading.Thread(target=download,args=(que,))
			t1.start()

	else:
		print("抱歉！暂时未找到您所需要的明星图片")


#代码执行体
if __name__ == '__main__':
	main()


