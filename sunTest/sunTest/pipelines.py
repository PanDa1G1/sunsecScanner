# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SuntestPipeline(object):

    def process_item(self, item, spider):

    	result = dict(item)
    	#print("[6]",result,sep="")
    	with open('D:\\code\\python\\scan\\myscan\\database\\url.txt', 'a', encoding='utf-8') as file:
    		url = result.get("scanUrl")
    		#print("[7]",url,sep="")
    		file.write(url+"\n")
    	return item
