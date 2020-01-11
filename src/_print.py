import colorama
from colorama import Fore, Style, Back
import platform
import sys
import os

class _print():

	def __init__(self):

		self.terminal_size = os.get_terminal_size().columns
		self.system = platform.system()
		self.lastInLine = False

	def inLine(self, string):
		self.lastInLine = True
		if len(string) > self.terminal_size:
			string = "\r" + string[:self.terminal_size - 8] + "..." + Style.RESET_ALL + "\r"
		string = ("\r" + string + Style.RESET_ALL) + "\r"
		sys.stdout.write(string)
		sys.stdout.flush()

	def new_line(self, message, nowrap=False):
		if self.lastInLine:
			self.erase()

		if self.system == 'Windows':
			sys.stdout.write(message)
			sys.stdout.flush()

		else:
			sys.stdout.write(message)

		if not nowrap:
			sys.stdout.write('\n')

		sys.stdout.flush()
		self.lastInLine = False

	def print_process(self,present,url):

		self.inLine(
                Fore.LIGHTYELLOW_EX + '[~] {:2.1f}% [{:<50}] {}'.format(present if present < 100 else 99.9,
                                                                        "=" * int(present // 2) + (
                                                                            ">" if present < 100 else ""), url).ljust(
                        self.terminal_size - 5, " "))

	def print_forbidden(self,url):

		self.new_line(Fore.LIGHTRED_EX + '[-] 403\t\t{}'.format(url))

	def print_401(self,url):

		self.new_line(Fore.LIGHTBLUE_EX + '[-] 401\t\t{}'.format(url))
    
	def print_succ(self,url):
		self.new_line(Fore.LIGHTGREEN_EX + '[*] 200\t\t{}'.format(url))
	

	def print_info(self, message, **kwargs):
		if self.system == "Windows":
			self.new_line(Fore.LIGHTYELLOW_EX + Style.NORMAL + "[~] {0}".format(message) + Style.RESET_ALL, **kwargs)
		else:
			self.new_line(Fore.LIGHTGREEN_EX + Style.NORMAL + "[~] {0}".format(message) + Style.RESET_ALL, **kwargs)

	def erase(self):
		if self.system == 'Windows':
			sys.stdout.write(Style.RESET_ALL + '\r' + ' ' * (self.terminal_size - 2) + '\r')
			sys.stdout.flush()

		else:
			sys.stdout.write('\033[1K')
			sys.stdout.write('\033[0G')
			sys.stdout.flush()

	def print_end(self,time,issue):
		self.new_line(Fore.LIGHTYELLOW_EX + "[~] {} finished! time spent {}s {} {}".format(issue,time,' '*50,'\n'))
	def check_sess(self,url,name):
		self.new_line(Fore.LIGHTGREEN_EX + '[*] ' + Fore.LIGHTGREEN_EX + '{}'.format(name) + Fore.LIGHTGREEN_EX +' is existed in'+ Fore.LIGHTGREEN_EX +' {}'.format(url))
	def port_end(self,time):
		self.new_line(Fore.LIGHTYELLOW_EX + '[~] finshed! time spent {}s'.format(time))
	def port_fail(self,port,state):
		sys.stdout.write(Fore.LIGHTGREEN_EX + '[*] port: {}\t\tstate: '.format(port) + Fore.LIGHTRED_EX + '{} {}'.format(state,'\n'))
	def port_sess(self,port,state):
		sys.stdout.write(Fore.LIGHTGREEN_EX + '[*] port: {}\t\tstate: {} {}'.format(port,state,'\n'))
	def port_res(self,port,state,service):
		sys.stdout.write(Fore.LIGHTGREEN_EX + '[*] port: {}\t\tstate: {}\tservice: {}\n'.format(port,state,service))
	def fuzz_res(self,param,value):
		sys.stdout.write(Fore.LIGHTGREEN_EX + '[*] param:{}\t\tvlaue:{}\n'.format(param,value))
	def ip_res(self,ip):
		sys.stdout.write(Fore.LIGHTGREEN_EX + '[*] ip: {}\t\tstate:up\n'.format(ip))
	def start_scan(self,type):
		sys.stdout.write(Fore.LIGHTGREEN_EX + "[~]start checking {} inject......\n".format(type))
	def sql_stop(self):
		sys.stdout.write(Fore.LIGHTYELLOW_EX + "[*]scan finished\n")
	