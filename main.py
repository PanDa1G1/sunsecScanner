from src.scan import path_scan
from src._print import _print
import argparse
from src.finger_scan import FingerScan
from src.PortScan import myThread
from src.fuzz import Fuzz
import time
from src.Ipscan import Ipscan
from sql_injection.union import ScanUnion
from sql_injection.error_inject import error_inject
from sql_injection.Boolen_scan import Boolen_Scan
from sql_injection.time_scan import Time_scan
from xss.xss_scan import xss_Scanner
from ssrf.ssrf import ssrfScan
import sys


class menu():

	def __init__(self):

		self._print = _print()

	def get_input(self):

		parser = argparse.ArgumentParser()
		parser.add_argument('-u', '--url', dest="scan_url", help="url for scanning", type=str)
		parser.add_argument('-n', '--num', dest="coroutine_num", help="coroutines num you want to use default:10", type=str,default = 10)
		parser.add_argument('-d', '--dictory', dest="dictory", help="dictory you want to use", type=str,default = 'directroy/dirList.txt')
		parser.add_argument('-s', '--sqlit',dest="sqlite_file", help="datebase file you want to use", type=str,default = 'database/web.db')
		parser.add_argument('-p', '--path_scan',dest="path_scan", help="scan the path eg: -u [url] -p 1 [-d directroy -n num]", type=str,default = False)
		parser.add_argument('-f', '--finger_scan',dest="finger_scan", help="scan the finger eg: -u [url] -f 1 [-s xx.db]", type=str,default = False)
		parser.add_argument('-P', '--port_scan',dest="port_scan", help="scan port \n\r eg: -u [host] -P [1-65535] or [22,33,88,77] or 22 [-t]", type=str,default = False)
		parser.add_argument('-t', '--thread_num',dest="thread_num", help="the number of thread  default:100", type=int,default = 100)
		parser.add_argument('-F', '--fuzz',dest="fuzz", help="http://url?fuzz=fuzz or http://url?file=fuzz", type=str,default = False)
		parser.add_argument('-sP', '--Ipscan',dest="Ipscan", help="xxx.xxx.xxx.0/24 or /16 or /8", type=str,default = False)
		parser.add_argument('--method', '--method',dest="sql_method", help="method to request", type=str,default = "GET")
		parser.add_argument('-r', '--headerFile',dest="header_file", help="header file,post request", type=str,default = False)
		parser.add_argument('--sql', '--sql',dest="sql_scan", help="whether to scan sqlinjection ", type=str,default = False)
		parser.add_argument('--union', '--union',dest="union_scan", help="union scan ", type=str,default = False)
		parser.add_argument('--error', '--error',dest="error_scan", help="error scan ", type=str,default = False)
		parser.add_argument('--Boolen', '--Boolen',dest="Boolen_scan", help="Boolen scan ", type=str,default = False)
		parser.add_argument('--true_string', '--true_string', dest="true_string", help="if payload is true,the string that will in page", type=str,default = "")
		parser.add_argument('--false_string', '--false_string', dest="false_string", help="tif payload is False,the string that will in page", type=str,default = "")
		parser.add_argument('--time', '--time',dest="time_scan", help="Boolen scan ", type=str,default = False)
		parser.add_argument('--wait_time', '--wait_time',dest="wait_time", help="wait_time ", type=int,default = 5)
		parser.add_argument('--payload_num', '--payload_num',dest="payload_num", help="the num of payload you want to print. default 10(used for error,boolen,time inject)", type=int,default = 10)
		parser.add_argument('-x', '--xss',dest="xss_scan", help="xss scan", type=str,default = False)
		parser.add_argument('--param_file', '--param_file', dest="param_file", help="LFi fuzz param_file", type=str,default = 'directroy/123.txt')
		parser.add_argument('--value_file', '--value_file', dest="value_file", help="LFi fuzz value_file", type=str,default = 'directroy/pathtotest_huge.txt')
		parser.add_argument('--ssrf', '--ssrf', dest="ssrf_scan", help="whether start ssrf scan", type=str,default = False)
		parser.add_argument('--redirect_file', '--redirect_file', dest="redirect_file", help="the path of 302 file if not will not try 302", type=str,default = None)
		

		self.args = parser.parse_args()
	
	def start(self):
		
		try :
			self.get_input()
			#路径扫描
			if self.args.path_scan:
				time0 = time.time()
				scan_path = path_scan(self.args.scan_url,self.args.coroutine_num,self.args.dictory)
				scan_path.start()
				time1 = time.time()
				self._print.print_end(time1 - time0,'path scan')

			#指纹扫描
			if self.args.finger_scan:
				time0 = time.time()
				finger_scan = FingerScan(self.args.scan_url,self.args.sqlite_file)
				finger_scan.run()
				time1 = time.time()
				self._print.print_end(time1 - time0,'finger scan')

			#端口扫描
			if self.args.port_scan:
				thread = myThread(self.args.scan_url,self.args.port_scan)
				thread.in_queue()
				thread.scan_start()	

			if self.args.fuzz:
				fuzz = Fuzz(self.args.scan_url,num = self.args.coroutine_num,param_file=self.args.param_file,value_file=self.args.value_file)
				fuzz.start()
			
			# ip扫描
			if self.args.Ipscan:
				scan = Ipscan(self.args.scan_url)
				scan.ip_queue()
				scan.scan_start()

			if self.args.sql_scan:
				if 	self.args.union_scan:
					#self._print.start_scan("union",time0)
					union_scan = ScanUnion(self.args.scan_url,self.args.sql_method,self.args.header_file)
					union_scan.union_inject()
					self._print.sql_stop()
				if self.args.error_scan:
					time0 = time.time()
					self._print.start_scan("error")
					error_scan = error_inject(self.args.scan_url,self.args.sql_method,self.args.header_file,payload_num=self.args.payload_num)
					error_scan.start()
					time1 = time.time()
					self._print.print_end(time1 - time0,'SQL_Error scan')
				if self.args.Boolen_scan:
					time0 = time.time()
					self._print.start_scan("Boolen")
					Boolen_scan = Boolen_Scan(self.args.scan_url,method = self.args.sql_method,file = self.args.header_file,thread_num = self.args.thread_num,payload_num=self.args.payload_num, string=self.args.true_string, not_string=self.args.false_string)
					Boolen_scan.start()
					time1 = time.time()
					self._print.print_end(time1 - time0,'SQL_Boolen scan')
				if self.args.time_scan:
					time0 = time.time()
					self._print.start_scan("time")
					Time = Time_scan(self.args.scan_url,method = self.args.sql_method,file = self.args.header_file,thread_num = self.args.thread_num,payload_num=self.args.payload_num,wait_time=self.args.wait_time)
					Time.start()
					time1 = time.time()
					self._print.print_end(time1 - time0,'SQL_time scan')
				if not self.args.union_scan and not self.args.error_scan and not self.args.Boolen_scan and not self.args.time_scan:
					time0 = time.time()
					self._print.start_scan("union")
					union_scan = ScanUnion(self.args.scan_url,method = self.args.sql_method,file = self.args.header_file)
					union_scan.union_inject()
					self._print.start_scan("error")
					error_scan = error_inject(self.args.scan_url,self.args.sql_method,self.args.header_file,payload_num=self.args.payload_num)
					error_scan.start()
					self._print.sql_stop()
					self._print.start_scan("Boolen")
					Boolen_scan = Boolen_Scan(self.args.scan_url,method = self.args.sql_method,file = self.args.header_file,thread_num = self.args.thread_num,payload_num=self.args.payload_num,string=self.args.true_string,not_string=self.args.false_string)
					Boolen_scan.start()
					self._print.start_scan("time")
					time_scan = time_scan(self.args.scan_url,method = self.args.sql_method,file = self.args.header_file,thread_num = self.args.thread_num,payload_num=self.args.payload_num,wait_time = self.args.wait_time)
					time_scan.start()
					time1 = time.time()
					self._print.print_end(time1 - time0,'SQL scan')
				
			if self.args.xss_scan:
				self._print.start_scan("xss")
				xssScanner=xss_Scanner(self.args.scan_url,thread_num = self.args.thread_num,payload_num=self.args.payload_num)
				xssScanner.run()
			
			if self.args.ssrf_scan:
				self._print.start_scan("ssrf")
				if self.args.redirect_file:
					time0 = time.time()
					ssrfScan_ = ssrfScan(self.args.scan_url,self.args.scan_url)
					ssrfScan_.FileScan()
					ssrfScan_.dictScan()
					ssrfScan_.redirectScan()
					ssrfScan_.url_in_queue()
					ssrfScan_.start()
					time1 = time.time()
					self._print.print_end(time1 - time0,'SSRF scan')
				else:
					time0 = time.time()
					ssrfScan_ = ssrfScan(self.args.scan_url)
					ssrfScan_.FileScan()
					ssrfScan_.dictScan()
					ssrfScan_.url_in_queue()
					ssrfScan_.start()
					time1 = time.time()
					self._print.print_end(time1 - time0,'SSRF scan')

		except OSError as e:
			pass
	def banner(self):
		banner = '''
 ____                            ____                  
/ ___| _   _ _ __  ___  ___  ___/ ___|  ___ __ _ _ __  
\___ \| | | | '_ \/ __|/ _ \/ __\___ \ / __/ _` | '_ \ 
 ___) | |_| | | | \__ \  __/ (__ ___) | (_| (_| | | | |
|____/ \__,_|_| |_|___/\___|\___|____/ \___\__,_|_| |_|
                                                      
	'''
		print(banner)

if __name__ == "__main__":

	pro = menu()
	pro.banner()
	pro.start()

