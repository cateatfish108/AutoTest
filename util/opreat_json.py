#coding:utf-8

import json
from collections import OrderedDict
class OperetJson:

	def __init__(self,file_path=None):
		if file_path  == None:
			self.file_path = '../config/config.json'
		else:
			self.file_path = file_path

	#读json文件
	def readData(self,file_path=None):
		if file_path == None:
			file_path = self.file_path
		with open(file_path,encoding='utf-8') as fp:
			data = json.load(fp,object_pairs_hook=OrderedDict)
			return data

	#写json文件
	def writeData(self,data,file_path=None):
		# data=json.dumps(data,sort_keys=True,indent=4)
		data=json.dumps(data,indent=4)
		if file_path == None:
			file_path = self.file_path
		with open(file_path,'w') as fp:
			fp.write(data)


if __name__ == '__main__':
	opjson = OperetJson()
	data = opjson.readData()
	opjson.readData()
	print(data)