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
		
	def data_in(self, imglist, title, mark, tag):
		cu = self.cx.cursor()
		cu.execute("SELECT MAX(id) from CL;")
		MAXID = cu.fetchall()[0][0]
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
		
		
	def list_image(self, id):
		cu = self.cx.cursor()
		cu.execute("SELECT * from CL where id=%s;"%id)
		res = cu.fetchall()
		if res:
			return res[0]
		else:
			return []
		
if __name__  == "__main__":
	DB = db_proc()
	print DB.data_in(["fhsufhoesf", "abfduosgdo", "wdiadhioaw"], "awdawdwf", "16-1508-1584651")
	print DB.list_image(6)