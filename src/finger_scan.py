# -*- coding: UTF-8 -*-
import sqlite3
import requests
from urllib import parse
from bs4 import BeautifulSoup
from src._print import _print
import os 
import time
import re 

class FingerScan(set):

	def __init__(self,url,db):
		self._print = _print()
		self.url = url
		self.headers = {'UserAgent':'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))'}
		self.db = db
		self.path = os.path.dirname(os.path.abspath(__file__))
		self.db_path = os.path.join(self.path,self.db)
		self.zz = '\"(.*)\"'
		self.zz_2 = '\(.*&&.*\)'

	def make_url(self):

		parts = parse.urlparse(self.url)
		scheme = parts[0]

		if scheme == '':
			self.url = 'http://' + self.url

		if self.url[-1:] != '/':
			self.url += '/'
	
	def get_message(self):

		try:
			self.make_url()
			res = requests.get(self.url,headers = self.headers,timeout=3)
			content = res.text
			headers = res.headers
			soup = BeautifulSoup(content, 'lxml')
			if soup.title:
				title = soup.title.string.strip()
				return content,headers,title
			else:
				title = 'none'
				return content,headers,title

		except Exception as e:
			pass

	def get_count(self):
		with sqlite3.connect(self.db_path) as conn:
			cur = conn.cursor()
			count = cur.execute('SELECT COUNT(id) FROM `fofa`')
			for i in count:
				return i[0]

	def get_dic(self,id_):
		with sqlite3.connect(self.db_path) as conn:
			cur = conn.cursor()
			result = cur.execute("SELECT name,keys FROM `fofa` where id = '{}'".format(id_))
			for row in result:
				return row[0],row[1]

	def check_rule(self,issue,content,header,title):
		if "header" in issue:
			str_ = re.search(self.zz,issue).group(1).lower()
			if str_ in str(header).lower():
				return True
		elif 'body' in issue:
			str_ = re.search(self.zz,issue).group(1).lower()
			if str_ in str(content).lower():
				return True
		elif 'title' in issue:
			str_ = re.search(self.zz,issue).group(1).lower()
			if str_ in str(title).lower():
				return True
		else:
			str_ = re.search(self.zz,issue).group(1).lower()
			if str_ in str(header).lower():
				return True


	def check(self,id_,count,content,header,title):
		name,keys = self.get_dic(id_)
		self._print.print_process((id_ / count)*100,id_)
		if '||' in keys and '&&' not in keys and '(' not in keys and ')' not in keys:
			for issue in keys.split('||'):
				if self.check_rule(issue,content,header,title):
					self._print.check_sess(self.url,name)
					break

		elif '||' not in keys and '&&' not in keys and '(' not in keys and ')' not in keys:
			if self.check_rule(keys,content,header,title):
				self._print.check_sess(self.url,name)

		elif '&&' in keys and '||' not in keys and '(' not in keys and ')' not in keys:
			cal = 0
			for issue in keys.split('&&'):
				if self.check_rule(issue,content,header,title):
					cal += 1
			if cal == len(keys.split('&&')):
				self._print.check_sess(self.url,name)
		else:
			
			if re.search(self.zz_2,keys):
				# a ||b||(c&&d)
				for issue in keys.split('||'):
					if '&&' not in issue:
						if self.check_rule(issue,content,header,title):
							self._print.check_sess(self.url,name)
							break
					else:
						num = 0
						issue = issue.replace('(','').replace(')','').strip()
						for i in issue.split('&&'):
							if self.check_rule(i,content,header,title):
								num += 1
						if num == len(issue.split('&&')):
							self._print.check_sess(self.url,name)
			else:
				# a && b &&(c||d)
				num = 0
				for  issue in keys.split('&&'):
					if '||' not in issue:
						if self.check_rule(issue,content,header,title):
							num += 1
					else:
						issue = issue.replace('(','').replace(')','').strip()
						for i in issue.split('||'):
							if self.check_rule(i,content,header,title):
								num += 1
								break
			if num == len(keys.split('&&')):
				self._print.check_sess(self.url,name)
					
	def run(self):

		try:
			self._print.print_info("Start scan finger: %s" % time.strftime("%H:%M:%S"))
			count = self.get_count()
			content,header,title = self.get_message()
			for i in range(1,count + 1):
				self.check(i,count,content,header,title)
		
		except Exception as e:
				print(e)








