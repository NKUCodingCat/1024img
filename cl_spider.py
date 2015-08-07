import requests
import db_handler
import web_parse

def scan_forum(db, url, sess):
	try:
		con = sess.get(url).content
	except:
		print "Get Page %s Failed!"%url
		return []
	lst = web_parse.forum_list(con)
	return [i for i in lst if not (db.is_exist_forum(web_parse.url_to_Mark(i["link"])) or not i["name"]) ]

"""	
def scan_img(db, base_url, dic):
	con = requests.get(web_parse.url_build(base_url, dic["link"])).content
	lst = web_parse.img_list(con)
	db.data_in(lst, dic["name"], web_parse.url_to_Mark(i["link"]), dic["tag"])
"""	
	
	
if __name__ == "__main__":
	DB = db_handler.db_proc()
	for i in scan_forum(DB, "http://cl.hkcl.pw/thread0806.php?fid=8&search=&page=4", requests.session()):
		print i