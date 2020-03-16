# -*- coding: UTF-8 -*-
import requests
import re
import threading
import queue
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.alert import Alert
import time
from urllib.parse import quote
import sys
from colorama import Fore, Style, Back
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains

class xss_Scanner():
	
	def __init__(self,url,payload_num = 3,thread_num=50):
		self.url = url
		self.headers =  {
		'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
		'Accept-Language': 'Zh-CN, zh;q=0.8, en-gb;q=0.8, en-us;q=0.8',
		'Accept-Encoding': 'identity',
		'Keep-Alive': '300',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		}
		self.payload_num=payload_num
		self.if_tags=0
		self.if_attribute=0
		self.if_dom=0
		self.if_click_dom = 0
		self.if_mouse_dom =0
		self.tem_payload = "~88868666~"
		self.firefox_options=Options()
		self.firefox_options.headless = True
		self.queue_ = queue.Queue()
		self.thread_num = thread_num
		self.tem_payload_num=0
		self.dom_arr=[]

	def judge_tag(self):
		payload = "<test0>"+ self.tem_payload + "</test0>"
		url = self.url.replace("*",payload)
		result = requests.get(url,headers = self.headers).text
		#print("[1]" + result)
		m = re.search(r"(<.*>)*[^\"]<test0>.*</test0>",result)
		if m:
			tag = m.group(1)
			if tag:
				#print("[3]"+tag)
				self.if_tags=1
				sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]tags can be injected\n")
				return tag
			else:
				self.if_tags=1
				sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]tags can be injected\n")
				return 0
		else:
			return 0

	def judge_attribute(self):
		payload =self.tem_payload + "\">"
		url = self.url.replace("*",payload)
		result = requests.get(url,headers = self.headers).text
		#print("[2]" + result)
		m = re.search(r"<[a-z]+ ([a-z]*)=\"~88868666~\">",result)
		if m:
			attribute = m.group(1)
			#print("[4]"+attribute)
			self.if_attribute=1
			sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]attribute can be injected\n")
			return attribute
		else:
			return 0

	def judge_dom(self):
		url = self.url.replace("*",self.tem_payload)
		browser = webdriver.Firefox(options=self.firefox_options)
		browser.get(url)
		result = browser.page_source
		#print("[7]" + result)
		if self.tem_payload in result and ("location.search" in result or "document.location.href" in result) and ("document.write" in result or "appendChild" in result or "innerHTML" in result):
			sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]dom can be injected\n")
			self.if_dom=1
			return 1
		clickList = browser.find_elements_by_xpath("//*[@onclick]")
		mouseList = browser.find_elements_by_xpath("//*[@onmousemove]")
		if clickList:
			for tag in clickList:
				ActionChains(browser).move_to_element(tag).click(tag).perform()#模拟点击
				result = browser.page_source
				if self.tem_payload in result:
					sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]dom can be injected\n")
					self.if_click_dom = 1
					return 1
		if mouseList:
			for tag in mouseList:
				ActionChains(browser).move_to_element(tag).perform()#模拟鼠标移动
				result = browser.page_source
				if self.tem_payload in result:
					sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]dom can be injected\n")
					self.if_mouse_dom = 1
					return 1

	def payload_in_queue(self):
		self.tag_pre = self.judge_tag();
		self.pre_attribute = self.judge_attribute();
		if_dom = self.judge_dom()

		if(self.if_tags == 1):
			tag_dict = "xss/tag_payload.txt"
			with open(tag_dict,"r") as f:
				for payload in f:
					self.queue_.put(payload.split("\n")[0])

		if(self.if_attribute == 1):
			tag_dict = "xss/attr_payload.txt"
			with open(tag_dict,"r") as f:
				for payload in f:
					self.queue_.put(payload.split("\n")[0])

		if(self.if_dom == 1 or self.if_click_dom == 1 or self.if_mouse_dom == 1):
			tag_dict = "xss/dom_dict.txt"
			with open(tag_dict,"r") as f:
				for payload in f:
					self.queue_.put(payload.split("\n")[0])


	def tag_scan(self):
		while not self.queue_.empty():
			payload = self.queue_.get()
			payload_ = quote(payload,"utf-8")
			if self.tag_pre == 0:
				url = self.url.replace("*",payload_) 
			elif re.match(r"title|textarea|math|iframe|xmp|plaintext",self.tag_pre[1:len(self.tag_pre)-1]):#闭合特殊标签
				payload = self.tag_pre[0] + "/" + self.tag_pre[1:] + payload 
				url = self.url.replace("*",payload_)
			else:
				url = self.url.replace("*",payload_)
			browser = webdriver.Firefox(options=self.firefox_options)#options=self.firefox_options
			try:
				browser.get(url)
				result = browser.switch_to.alert.text
				if result == "668868":
					sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]available payload {}\n".format(payload))
					self.tem_payload_num +=1
					#browser.close()
					if self.tem_payload_num == self.payload_num:
						sys.stdout.write(Fore.LIGHTYELLOW_EX + "[~]scan finished\n")
						browser.quit()
						sys.exit(0)
				else:
					continue

			except NoAlertPresentException as e:
				if self.tem_payload_num == self.payload_num:
					sys.stdout.write(Fore.LIGHTYELLOW_EX + "[~]scan finished\n")
					browser.quit()
					sys.exit(0)
				continue

	def attribute_scan(self):
		while not self.queue_.empty():
			payload_ = self.queue_.get()
			#payload_ = quote(payload,"utf-8")
			url = self.url.replace("*",payload_)
			#print("[8] {}".format(url))
			browser = webdriver.Firefox(options=self.firefox_options)
			try:
				browser.get(url)
				result = browser.switch_to.alert.text
				if result == "668868":
					sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]available payload {}\n".format(payload_))
					self.tem_payload_num +=1
					#browser.close()
					if self.tem_payload_num == self.payload_num:
						sys.stdout.write(Fore.LIGHTYELLOW_EX + "[~]scan finished\n")
						browser.quit()
						sys.exit(0)
				else:
					continue
			except NoAlertPresentException as e:
				if self.tem_payload_num == self.payload_num:
					sys.stdout.write(Fore.LIGHTYELLOW_EX + "[~]scan finished\n")
					browser.quit()
					sys.exit(0)
				continue

	def dom_scan(self):
		while not self.queue_.empty():
			payload = self.queue_.get()
			url = self.url.replace("*",payload)
			browser = webdriver.Firefox(options=self.firefox_options)
			try:
				browser.get(url)
				if self.if_click_dom:
					tags = browser.find_elements_by_xpath("//*[@onclick]")
					for tag in tags:
						ActionChains(browser).move_to_element(tag).click(tag).perform()
						result = browser.switch_to.alert.text
						if result == "668868":
							sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]available payload {}\n".format(payload))
							self.tem_payload_num +=1
							if self.tem_payload_num == self.payload_num:
								sys.stdout.write(Fore.LIGHTYELLOW_EX + "[~]scan finished\n")
								browser.quit()
								sys.exit(0)
				elif self.if_mouse_dom:
					tags = browser.find_elements_by_xpath("//*[@onmousemove]")
					for tag in tags:
						ActionChains(browser).move_to_element(tag).perform()
						result = browser.switch_to.alert.text
						if result == "668868":
							sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]available payload {}\n".format(payload))
							self.tem_payload_num +=1
							if self.tem_payload_num == self.payload_num:
								sys.stdout.write(Fore.LIGHTYELLOW_EX + "[~]scan finished\n")
								browser.quit()
								sys.exit(0)
				else:
					result = browser.switch_to.alert.text
					if result == "668868":
						sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]available payload {}\n".format(payload))
						self.tem_payload_num +=1
						if self.tem_payload_num == self.payload_num:
							sys.stdout.write(Fore.LIGHTYELLOW_EX + "[~]scan finished\n")
							browser.quit()
							sys.exit(0)
					else:
						continue
			except NoAlertPresentException as e:
				if self.tem_payload_num == self.payload_num:
					sys.stdout.write(Fore.LIGHTYELLOW_EX + "[~]scan finished\n")
					browser.quit()
					sys.exit(0)
				continue

	def run(self):
		self.payload_in_queue()
		#print("[5]%d" % self.if_attribute)
		#print("[6]%d" % self.if_tags)
		if self.if_attribute:
			thread_ = []
			for i in range(self.thread_num):
				t = threading.Thread(target = self.attribute_scan())
				thread_.append(t)
				t.start()
			for t in thread_: 
				t.join()
		if self.if_tags:
			thread_ = []
			for i in range(self.thread_num):
				t = threading.Thread(target = self.tag_scan())
				thread_.append(t)
				t.start()
			for t in thread_: 
				t.join()
		if self.if_dom or self.if_click_dom or self.if_mouse_dom:
			thread_ = []
			for i in range(self.thread_num):
				t = threading.Thread(target = self.dom_scan())
				thread_.append(t)
				t.start()
			for t in thread_: 
				t.join()



