#coding=utf-8
import sqlite3
import os
import json

db_path = os.path.split(os.path.realpath(__file__))[0]+"/1024.db"

class db_proc(object):
	def __init__(self, dbPATH = db_path):
		self.cx = sqlite3.connect(dbPATH)
		#=========================================
		cu = self.cx.cursor()
		cu.execute("CREATE TABLE IF NOT EXISTS CL(id BIGINT(20),imglist TEXT,title VARCHAR(255), mark varchar(255),tag varchar(31))")
		cu.close()
	
	def is_exist_forum(self, forum_mark):
		cu = self.cx.cursor()
		cu.execute("select 1 from CL where mark=? limit 1;", (forum_mark, ))
		if cu.fetchall():
			cu.close()
			return True
		else:
			return False
			
	def MAXID(self):
		cu = self.cx.cursor()
		cu.execute("SELECT MAX(id) from CL;")
		MAXID = cu.fetchall()[0][0]
		return MAXID
			
	def data_in(self, imglist, title, mark, tag):
		cu = self.cx.cursor()
		MAXID = self.MAXID()
		ID = MAXID+1 if MAXID else 1
		try:
			cu.execute("INSERT INTO CL VALUES (?, ?, ?, ?, ?);", (ID, json.dumps(imglist), title, mark, tag))
		except:
			#print "INSERT INTO CL VALUES (%s, '%s', '%s', '%s', '%s')"%(ID, json.dumps(imglist), title, mark, tag)
			raise
		self.cx.commit()
		cu.close()
		
	def list_forum(self, start, leng=20):
		cu = self.cx.cursor()
		cu.execute("select id,title from CL limit %s, %s"%(start, leng))
		return cu.fetchall()
	
	def get_title(self, id):
		cu = self.cx.cursor()
		cu.execute("select title from CL where id=?", (id, ))
		TL = cu.fetchall()
		return TL[0][0] if TL else "Nothing"
		
	def list_image(self, id):
		cu = self.cx.cursor()
		cu.execute("SELECT * from CL where id=%s;"%id)
		res = cu.fetchall()
		if res:
			return res[0]
		else:
			return []
	def leng_of_tag(self, tag):
		cu = self.cx.cursor()
		tag = unicode(tag.decode('utf-8', 'ignore') )
		cu.execute('select COUNT(id) from cl where tag=?', (tag, ))
		return cu.fetchall()[0][0]
			
	def list_forum_by_tag(self, tag, start, leng = 20):
		cu = self.cx.cursor()
		tag = unicode( tag.decode('utf-8', 'ignore') )
		cu.execute('select id, title from cl where tag=? limit ?, ?', (tag, start, leng))
		return cu.fetchall()
		
	def list_tag(self):
		cu = self.cx.cursor()
		cu.execute("select distinct tag from CL where tag <> ''")
		return [i[0] for i in cu.fetchall()]
		
	def list_photo_by_tag(self, id):
		cu = self.cx.cursor()
		data = self.list_image(id)
		if not data:
			return (-1, "没有了"),[],(-1, "没有了")
		tag = data[-1]
		cu.execute('select id, title from cl where id = (select MAX(id) from cl where id<? and tag=?)', (id, tag))
		pr = cu.fetchall()
		pr = pr[0] if pr else (-1, "没有了")
		cu.execute('select id, title from cl where id>? and tag=? limit 1', (id, tag))
		ne = cu.fetchall()
		ne = ne[0] if ne else (-1, "没有了")
		return pr, data, ne
		
if __name__  == "__main__":
	DB = db_proc()
	#print DB.data_in(["fhsufhoesf", "abfduosgdo", "wdiadhioaw"], "awdawdwf", "16-1508-1584651")
	#print DB.list_image(6)
	# print DB.list_photo_by_tag(2233)
	# print DB.list_photo_by_tag(1)
	# print DB.list_photo_by_tag(10998)
	# print DB.list_photo_by_tag(DB.MAXID())
	print DB.list_forum_by_tag('[歸美]', 40,20)