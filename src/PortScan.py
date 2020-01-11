import queue
import threading
from src._print import _print
import socket
import time 

class myThread():

	def __init__(self,host,port,thread_num = 100):

		self.host = host
		self._print = _print()
		self.port = port
		self.q = queue.Queue()
		self.timeout = 0.1
		self.threads = [threading.Thread(target = self.thread_work) for i in range(thread_num)]
		self.thread_num = thread_num
		self.flag = False
	
	def in_queue(self):

		if '-' in self.port:
			hport = int(self.port.split('-')[1])
			lport = int(self.port.split('-')[0])
			for i in range(lport,hport + 1):
				self.q.put(i)
			self.flag = True

		elif ',' in self.port:
			ports = self.port.split(',')
			for port in ports:
				self.q.put(int(port))
		else:
			self.q.put(int(self.port))


	def out_queue(self):

		return self.q.get()

	def thread_work(self):

		while not self.q.empty():
			port = self.out_queue()
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket.setdefaulttimeout(0.1)
			res = s.connect_ex((self.host, port))
			s.close()
			if self.flag:
				if res == 0:
					try:
						service = socket.getservbyport(port)
					except:
						service = 'unknown'
					self._print.port_res(port,'open',service)
			else:
				if res == 0:
					self._print.port_sess(port,'open')
				else:
					self._print.port_fail(port,'close')

	def scan_start(self):

		self._print.print_info("Start scan port : %s" % time.strftime("%H:%M:%S"))
		time0 = time.time()
		for i in self.threads:
			i.start()

		for i in self.threads:
			i.join()
		time2 = time.time() - time0
		self._print.port_end(time2)





		









