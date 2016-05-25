#!/usr/bin/python
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
f = open('links.txt','w')
global count_search
def visited_function(visited,r,tell):
	if r in visited:
		return 0
	else:
		return 1
def main_func(q, url,count,visited):
	#if urllib.request.urlopen(url):
	try:
		global count_search
		convo_photo = "iitg.ernet.in/convoPhoto"
		statphys = "iitg.ernet.in/statphys"
		if convo_photo in url or statphys in url:
			return count
		visited.append(url)
		r = urllib.request.urlopen(url)
		exe = ".exe"
		dat = ".dat"
		zippe = ".zip"
		doc = ".doc"
		bmp = ".bmp"
		jpg = ".jpg"
		pdf = ".pdf"
		alist = [exe,pdf,dat,zippe,doc,bmp,jpg]
		soup =  BeautifulSoup(r.read())
		links = soup.find_all("a")
		new2 = "http://www.iitg.ernet.in/www.iitg.ernet.in"
		var = "iitg.ernet.in"

		for link in links:
	#queue(link)
			href = link.get("href")
			search_in = link.contents[0]
			if search_in is not None:
				search_in = search_in.lower()
			p = str(href)
			p = urllib.parse.urljoin(url,href)
			newstring = p[-4:]
			one_more = "@"
			pdf = ".pdf"
			if var in p and p not in visited and p not in q and one_more not in p and new2 not in p:
				count += 1
				f.write(p)
				f.write("\n")
				if newstring not in alist:
					q.append(p)
	except :
			return count
	return count
url = "http://intranet.iitg.ernet.in/"
count=0
q=deque([])
visited = deque([])
q.append(url)
flag=1
search_text = "Saswata"
count_search = 0
new_one = "http://jatinga.iitg.ernet.in/~dppc"
while len(q) > 0 and flag == 1:
	tell = 0
	while(tell==0):
		if len(q) > 0:
			r = q.popleft()
			tell = visited_function(visited,r,tell)
	if new_one not in r:
		count = main_func(q,r,count,visited)

	