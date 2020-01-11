import queue
import socket
import threading
import time
from src._print import _print

class Ipscan():

    def __init__(self,url,thread_num = 100):
        self.host = url
        self.thread_num = thread_num
        self.queue = queue.Queue()
        self.queue2 = queue.Queue()
        self._print = _print()
        self.port_list = [22,80,111,443,8080]
        self.threads = [threading.Thread(target = self.scan) for i in range(thread_num)]
        
    
    def ip_queue(self):
        num = self.host.split('/')[1]
        ip_list = self.host.split('/')[0].split('.')
        if int(num) == 24:
            ip = ip_list[0] + '.' + ip_list[1] + '.' + ip_list[2]
            for i in range(256):
                real_ip = ip + '.' + str(i) 
                self.queue.put(real_ip)
            self.length = self.queue.qsize()
        elif int(num) == 16:
            ip = ip_list[0] + '.' + ip_list[1]
            for i in range(256):
                for j in range(256):
                    real_ip = ip + '.' + str(i) + '.' + str(j)
                    self.queue.put(real_ip)
            self.length = self.queue.qsize()
        else:
            ip = ip_list[0]
            for i in range(256):
                for j in range(256):
                    for k in range(256):
                        real_ip = ip + '.' + str(i) + '.' + str(j) + '.' + str(k)
                        self.queue.put(real_ip)
            self.length = self.queue.qsize()

    def out_queue(self,queue):
        return queue.get()
  
    def scan(self):
        while not self.queue.empty():
            ip = self.out_queue(self.queue)
            for port in self.port_list:
                #print(ip,port)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.1)
                res = s.connect_ex((ip, port))
                s.close()
                if res ==0:
                    self._print.ip_res(ip)
                    #print(ip,port)
                    break


    def scan_start(self):
        self._print.print_info("Start Ipscan : %s" % time.strftime("%H:%M:%S"))
        time0 = time.time()
        for i in self.threads:
            i.start()

        for i in self.threads:
            i.join()
        time2 = time.time() - time0
        self._print.port_end(time2)




