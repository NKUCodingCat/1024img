import requests
import re
import cl_spider
import time
import urllib
import urlparse
import web_parse
import db_handler

import gevent 
from gevent import coros 
from gevent import monkey 

from gevent.queue import Queue



monkey.patch_all()
Lock = coros.Semaphore()

def forum_page_fetch(db, P_que, F_que, sleep_len, sess):
	time.sleep(sleep_len)
	while not P_que.empty():
		#========================
		if F_que.qsize() > 60:
			gevent.sleep()		
			continue
		#========================
		
		url = P_que.get()
		print "Forum Queue len = %s, Page Queue len = %s"%(F_que.qsize(), P_que.qsize())
		Base = urlparse.urlsplit(url)
		print "Start Catch %s"%url
		FL = cl_spider.scan_forum(db, url, sess)
		if not FL:
			while not P_que.empty():
				P_que.get()
			print "P_que is empty!"
			return
		for i in FL:
			i['link'] = (urlparse.urlunparse(urlparse.ParseResult(
					scheme = Base.scheme,
					netloc = Base.netloc,
					path = i["link"],
					params = '',
					query = '',
					fragment = ''
				))
			)
			F_que.put(i)
		gevent.sleep(1)
	return
	
def Image_fetcher(db, P_que, F_que, sleep_len, sess):
	time.sleep(sleep_len)
	while ((not F_que.empty()) or (not P_que.empty())) :
		try:
			dic = F_que.get(timeout = 2)
		except:
			continue
		print "Catch %s, last %s"%(dic["link"] , F_que.qsize())
		try:
			con = sess.get(dic["link"]).content
		except:
			continue
		lst = web_parse.img_list(con)
		Lock.acquire()
		try:
			db.data_in(lst, dic["name"], web_parse.url_to_Mark(urlparse.urlsplit(dic["link"]).path[1:]), dic["tag"])
		except:
			raise
			print "Insert Data Failed @ %s"%dic["link"]
			print lst, dic["name"], web_parse.url_to_Mark(urlparse.urlsplit(dic["link"]).path[1:]), dic["tag"]
		finally:
			Lock.release()
	return

	
def Pre_fetch(HomePage_url, sess):
	query_dict = dict([(k,v[0]) for k,v in urlparse.parse_qs( urlparse.urlsplit(HomePage_url).query ).items()])
	Base = urlparse.urlsplit(HomePage_url)
	for i in range(1, (1+  web_parse.max_page_index(sess.get(HomePage_url).content))):
		query_dict["page"] = i
		yield urlparse.urlunparse(urlparse.ParseResult(
			scheme = Base.scheme,
			netloc = Base.netloc,
			path = Base.path,
			params = "",
			query = urllib.urlencode(query_dict),
			fragment = ""
		))
		
		
if __name__ == "__main__":
	
	Page_list = Queue()
	Forum_list = Queue()
	DB = db_handler.db_proc()
	Sess = requests.session()
	
	for i in Pre_fetch("https://www.t66y.com/thread0806.php?fid=8&search=&page=1", Sess):
		Page_list.put(i)
	print "Catch First Page Complete"
	gevent.joinall([gevent.spawn(forum_page_fetch, DB, Page_list, Forum_list, 0.5*i, Sess) for i in range(5)]+[gevent.spawn(Image_fetcher, DB, Page_list, Forum_list, 0.5*i, Sess) for i in range(20)])
