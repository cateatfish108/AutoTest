import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import unittest
from base.base_test import BaseTest
from ddt import ddt,data,unpack,file_data
from init.load_init_data import InitDB
import time

@ddt
class OmsTest(BaseTest):
    
    @classmethod
    def setUpClass(self):
        BaseTest.setUpClass()
        init_db = InitDB(self.case_manage.OpDataBase, "../TestCase/测试用例-订单检查-初始化脚本.sql")
        init_db.run()
    
    @file_data("../TestCase/测试用例-订单校验.json")
    def test_order_check(self,**kwargs):
        self.case_file="测试用例-订单校验.json"
        self._testMethodDoc = kwargs.get('case_note')
        self.check(**kwargs)