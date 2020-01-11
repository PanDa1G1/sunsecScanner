import asyncio
import time
import aiohttp
from aiohttp import ClientSession
from urllib import parse
from src._print import _print

class path_scan(object):

	def __init__(self,url,max_num,dictory):
		
		self.url = url
		self.dictory = dictory
		self.count = 0;
		self.loop = asyncio.get_event_loop()
		self.tasks = []
		self.coroutine_num = int(max_num)
		self.queue = asyncio.Queue()
		self._print = _print()
		self.session = ClientSession(loop=self.loop)
		self.headers =  {
        'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
        'Accept-Language': 'Zh-CN, zh;q=0.8, en-gb;q=0.8, en-us;q=0.8',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    	}

	def make_url(self,url):

		parts = parse.urlparse(self.url)
		scheme = parts[0]

		if scheme == '':
			self.url = 'http://' + self.url

		if self.url[-1:] != '/':
			self.url += '/'

		full_url = str(self.url) + str(url)
		return full_url

	async def get_response(self,url,allow_redirects=True):
		return await self.session.get(url,headers = self.headers,allow_redirects=allow_redirects)

	async def scan(self):

		while True:

			if not self.queue.empty():
				url = await self.queue.get()
				full_url = self.make_url(url)
				self.count += 1
				try:

					response = await self.get_response(full_url)
					self._print.print_process((self.count / self.length)*100,url)
					code = response.status
					if code == 200:
						self._print.print_succ(url)
						continue
					if code == 404:
						continue
					if code == 403:
						#self._print.print_forbidden(url)
						continue
					if code == 401:
						self._print.print_401(url)
						continue
					if code == 302 or code == 301:
						#jump_url = response.location
						#self._print.print_forbidden(url,jump_url,code)
						continue
				except:
					await self.session.close()
					pass
			else:
				await self.session.close()
				break



	def make_cor(self):

		self.tasks = [self.scan() for i in range(self.coroutine_num)]
		return self.loop.run_until_complete(asyncio.wait(self.tasks))

	def get_dir(self):
		with open(self.dictory,'r') as f:

			while True:
				url = f.readline().strip()
				if url:
					self.queue.put_nowait(url)

				else:
					break
		self.length = self.queue.qsize()

	def start(self):

		self._print.print_info("Start scan path : %s" % time.strftime("%H:%M:%S"))
		self.get_dir()
		self.make_cor()






