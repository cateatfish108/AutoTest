#coding:utf-8

import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import time
import unittest
from util.HTMLTestRunner import HTMLTestRunner

def main():
	
	now = time.strftime("%Y-%m-%d_%H_%M_%S")
	report_dir = '../report/'
	# 创建报告文件，并以写的形式打开文件，用于写入报告内容
	fp = open(report_dir + "report" + now + ".html", 'wb')
	# 初始化一个HTMLTestRunner实例对象，用来生成报告
	runner = HTMLTestRunner(stream=fp,title="接口自动化测试报告",verbosity=2,description='环境：windows 7 浏览器：chrome',tester='tangbo')
	case = unittest.defaultTestLoader.discover("./", pattern='oms_replace_order_check_test.py')
	runner.run(case)
	fp.close()

if __name__ == '__main__':
	main()