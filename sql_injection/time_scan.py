import requests
from colorama import Fore, Style, Back
from urllib import parse
import threading
import queue
import time
import sys

class Time_scan():

    def __init__(self,url,method = "GET",file = "sql_injection/payload/header.txt",thread_num = 50,payload_num = 10,wait_time=5):

        self.url = url
        self.method = method
        self.header_file = file
        self.paylaodFile = "sql_injection/payload/time.txt"
        self.headers =  {
		'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
		'Accept-Language': 'Zh-CN, zh;q=0.8, en-gb;q=0.8, en-us;q=0.8',
		'Accept-Encoding': 'identity',
		'Keep-Alive': '300',
		'Connection': 'close',
		'Cache-Control': 'max-age=0',
		}
        self.queue_ = queue.Queue()
        self.thread_num = thread_num
        self.flag = 0
        self.data = {}
        self.postHeaders = {}
        self.payload_final_num = payload_num
        self.payload_temp_num = 0
        self.wait_time = wait_time
    
    def payload_in_queue(self):
        with open(self.paylaodFile,"r") as f:
            for payload in f:
                TruePayload = payload.split("\n")[0]
                self.queue_.put(TruePayload)
    
    def get_time(self,payload):
        if self.method == "GET":
            payload = parse.quote(payload.encode("utf-8"))
            url = self.url.replace("*",payload)
            time1 = time.time()
            requests.get(url,headers = self.headers)
            time2 = time.time()
            return time2 - time1
        else:
            self.prepare_post(payload)
            time1 = time.time()
            requests.post(self.url,headers = self.postHeaders,data = self.data)
            time2 = time.time()
            return time2 - time1
    
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
    
    def scan(self):
        while not self.queue_.empty():
            payload = self.queue_.get().replace('[wait_time]',str(self.wait_time))
            #print(payload)
            time_ = self.get_time(payload)
            if time_ > self.wait_time - 1:
                self.payload_temp_num += 1
                self.flag +=1
                sys.stdout.write(Fore.LIGHTGREEN_EX + "[*]available payload {}\n".format(payload))
                if self.payload_temp_num == self.payload_final_num:
                    sys.stdout.write(Fore.LIGHTYELLOW_EX + "[*]scan finished\n")
                    sys.exit(0)
    
    def start(self):
        self.payload_in_queue()
        thread_ = []
        for i in range(self.thread_num):
            t = threading.Thread(target = self.scan())
            thread_.append(t)
            t.start()
        for t in thread_: 
            t.join()
        
        if not self.flag:
            sys.stdout.write(Fore.LIGHTRED_EX + "[-]can't Boolen inject\n")

if __name__ == "__main__":
    a = Time_scan("http://127.0.0.1/sqli-labs-master/Less-9/?id=*")
    a.start()