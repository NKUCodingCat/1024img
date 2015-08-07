#coding=utf-8
from lxml import etree
import re
import os
import urlparse
import posixpath

def max_page_index(content):
	print len(content)
	SRC = public_par(content)
	#Max_url = [i.attrib["href"] for i in SRC.xpath(u"//div[@class='t3']/table/tr/td/div[@class='pages']/a") if i.text == u"\uff1e"][0]
	Max_url = SRC.xpath(u"//a[@id='last']")[0].attrib["href"]
	return int(dict([(k,v[0]) for k,v in urlparse.parse_qs( urlparse.urlsplit(Max_url).query ).items()])['page'])
	
def url_build(base, url):
	url1 = urlparse.urljoin(base, url)
	arr = urlparse.urlparse(url1)
	path = posixpath.normpath(arr[2])
	return urlparse.urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))


def public_par(content):
	try:
		Page = etree.HTML(content.lower().decode('GBK', 'ignore'))
	except:
		raise
	else:
		return Page
		
def forum_list(content):
	SRC = public_par(content)
	F_list = [i.xpath(u"td[@style='text-align:left;padding-left:8px']") for i in SRC.xpath(u"//tr[@class='tr3 t_one']")]
	F_list = [i[0] for i in F_list if i]
	return [
		{
			"tag" :re.sub("\s","",td.text),
			"link":td.xpath("h3/a")[0].attrib["href"], 
			"name":td.xpath("h3/a")[0].text
		} 
		for td in F_list
	]
	
def img_list(content):
	SRC = public_par(content)
	I_List = [i.attrib["src"] for i in SRC.xpath(u"//input[@type='image']")]
	return I_List
	
def url_to_Mark(url):
	return "-".join(re.split("/",os.path.splitext(url)[0])[1:])


if __name__ == '__main__':
	import os
	root = os.path.split(os.path.realpath(__file__))[0]+"/"
	# print forum_list(open(root+"test.html").read())
	# print img_list(open(root+"img.html").read())
	# print url_to_Mark('htm_data/8/1508/1585767.html')
	# print url_build("https://www.t66y.com/", 'htm_data/8/1508/1585767.html')
	print max_page_index(open(root+"test.html").read())
	