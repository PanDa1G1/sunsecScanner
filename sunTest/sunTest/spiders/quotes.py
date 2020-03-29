# -*- coding: utf-8 -*-
import scrapy
import re
from sunTest.items import SuntestItem
from bloom_filter import BloomFilter

class QuotesSpider(scrapy.Spider):

	name = 'quotes'
	allowed_domains = []
	start_urls = ['http://127.0.0.1/php/1.php']

	def __init__(self):
	
		self.spiderUlrs=[]
		self.whiteList=["php","asp"]
		self.bloom = BloomFilter(max_elements=1000000, error_rate=0.1)

	def getFormList(self,response):
		forms = response.css("form")
		result = []
		for form in forms:
			tempUrl = form.css("::attr(action)").get()+"?"
			#print("[8]"+tempUrl)
			method = form.css("::attr(method)").get()
			names = form.css("input::attr(name)").getall()
			if method.lower() == "get":
				for name in names:
					if name.lower() == "submit":
						tempUrl += "submit=submit"
					else:
						tempUrl = tempUrl + name + "=*&"
			
			finalUrl=tempUrl.strip("&")
			#print("[9]"+finalUrl)
			result.append(finalUrl)

		return result

	def getMode(self,url):
		url_ = url.split("?")
		if len(url_) ==1:
			mode = url
		else:
			attr =  re.sub("=[a-zA-Z0-9_-]+","=*",url_[1])
			mode = url_[0] + "?" + attr
		return mode

	def parse(self, response):
		hrefList=[]
		srcList=[]
		formList=[]
		redirList=[]
		items = SuntestItem()
		hrefList = response.css("a::attr(href)").getall()
		linkList = response.css("link::attr(href)").getall()
		srcList = [i.css("*::attr(src)").get() for i in response.css("[src]")]
		formList = self.getFormList(response)
		redirtext=response.css(".redir::text").get()
		if redirtext:
			redirList=redirtext.split(",")
			#print("[3]",redirList,sep="")
		UrlList = hrefList+srcList+formList+redirList+linkList
		#print("[3]{}".format(formList))
		for url in UrlList:
			if not re.match("http",url):
				finalUrl = response.urljoin(url)
				urlmode = response.urljoin(self.getMode(url))
			else:
				finalUrl = url
				urlmode = self.getMode(url)
			#print("[2]{}".format(urlmode))
			if urlmode not in self.bloom:
				if finalUrl.split(".")[-1] in self.whiteList or finalUrl.split("?")[0].split("/")[-1].split(".")[-1] in self.whiteList:
					self.bloom.add(urlmode)
					items["scanUrl"] = urlmode
					self.spiderUlrs.append(finalUrl)
					yield items

		#print("[1] spiderUlrs{}".format(self.spiderUlrs))
		
		for url in self.spiderUlrs:
			temp = scrapy.Request(url=url,callback = self.parse)
			self.spiderUlrs.remove(url)
			yield temp
