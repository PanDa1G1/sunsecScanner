import asyncio
from aiohttp import ClientSession
import requests
import hashlib
import aiohttp
from src._print import _print
import time
import io
from difflib import SequenceMatcher 

class Fuzz(set):

	def __init__(self,url):

		self.url = url.split('?')[0]
		self.queue1 = asyncio.Queue()
		self.queue2 = asyncio.Queue()
		self.loop = asyncio.get_event_loop()
		self.num =  100
		self.list = []
		self.headers =  {
        'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
        'Accept-Language': 'Zh-CN, zh;q=0.8, en-gb;q=0.8, en-us;q=0.8',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    	}
		self.param = url.split('?')[1].split('=')[0]
		self._print = _print()
		self.high_ratio = 0.70
		self.low_ratio = 0.02

	def str_in_queue(self):

		with open('directroy/pathtotest_huge.txt','rb') as f:
			while True:
				string = f.readline().decode('utf-8').strip()
				if string:
					self.queue1.put_nowait(string)
				else:
					break
		self.length1 = self.queue1.qsize()
    
	def get_param(self):	
		with open('directroy/123.txt','r') as f1:
			while True:
				param = f1.readline().strip()
				if param:
					self.list.append(param)
				else:
					break
		self.length2 = len(self.list)

	def origin_md5(self):
		text = requests.get(self.url,headers = self.headers).text
		m = hashlib.md5()
		m.update(bytes(text,encoding = 'utf-8'))
		self.hex = m.hexdigest()

	def get_ratio(self,res_text):
		seqm = SequenceMatcher()
		text = requests.get(self.url,headers = self.headers).text
		seqm.set_seq1(text)
		seqm.set_seq2(res_text)
		return seqm.ratio()


	async def fuzz(self,param):
		session = ClientSession()
		while True:
			if not self.queue1.empty():
				string = await self.queue1.get()
				url = self.url + '?' + str(param) + '=' +  str(string)
				try:
					text = await self.get_response(url,session)
					#print(text)
					ratio = self.get_ratio(text)
					#print(url,ratio)
					if ratio > self.low_ratio and ratio < self.high_ratio:
						self._print.fuzz_res(param,string)
					if ratio == 0:
						self._print.fuzz_res(param,string)
				except:
					pass
			else:
				#print(param)
				await session.close()
				break

	async def get_response(self,url,session):
		
		s = await session.get(url,headers = self.headers)
		return await s.text() 

	def make_cor(self):

		if self.length2 == 1:

			self.tasks = [self.fuzz(self.param) for i in range(self.num)]
			self.loop.run_until_complete(asyncio.wait(self.tasks))
		else:
			for param in self.list:
				self.tasks = [self.fuzz(param) for i in range(self.num)]
				self.loop.run_until_complete(asyncio.wait(self.tasks))
				self.str_in_queue()

	def start(self):

		self._print.print_info("Start fuzz : %s" % time.strftime("%H:%M:%S"))
		time0 = time.time()
		if self.param == 'fuzz':
			self.get_param()
			self.str_in_queue()

		else:
			self.str_in_queue()
			self.length2 = 1

		self.make_cor()
		time2 = time.time() - time0
		self._print.port_end(time2)







