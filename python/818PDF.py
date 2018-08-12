page=1
url="https://www.qiushibaike.com"+str(page)
user_agent="Mozilla/4.0(compatitible;MSIE 5.5;Windows NT)"
headers={'user-Agent':user_agent}
try:
	request=urllib2.request(url,headers=headers)
	response=urlib2.urlopen(request)