#coding:utf-8

import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import unittest
from base.base_test import BaseTest
from ddt import ddt,data,unpack,file_data

@ddt
class MidOfficeTest(BaseTest):
    
    @file_data("../TestCase/midoffice_test.json")    
    def test_01_midoffice(self,case_id,url,method,data,header,check_response_item,check_item,response,db_key,check_result):
        case_file="midoffice_test.json"
        self.check(case_file,case_id,url,method,data,header,check_response_item,check_item,response,db_key,check_result)