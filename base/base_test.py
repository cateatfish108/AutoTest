#coding:utf-8

import unittest
from .config import Config
from util.opreat_database import OperetDataBase
from util.opreat_json import OperetJson
from .case_manager import CaseManager
from util.process_http import ProcessHttp
import copy
import time
import pandas as pd
from .func import getFormatSymbol

class BaseTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        # 相对路径起点为整个程序入口出
        CONFIG_PATH = "../config/config.json"
        CASE_CONFIG_PATH = "../TestCase/case_config.json"
        self.config = Config(CONFIG_PATH,CASE_CONFIG_PATH)
        # self.operet_database = OperetDataBase(self.config.getDataBase())
        self.case_manage = CaseManager(self.config)
        self.pro_http = ProcessHttp()

    @classmethod
    def tearDownClass(self):
        self.case_manage.closeConn()
        #self.case_manage.allCaseToJson()

    def check(self,**kwargs):
        # 1.向待测系统发送HTTP请求
        res = self.pro_http.sendHttp(kwargs.get('url'),kwargs.get('method'),kwargs.get('data'),kwargs.get('header'))
        i = self.__class__
        self.case_manage.initCase(kwargs.get('case_id'))
        self.case_manage.setResponse(kwargs.get('case_id'),res)
        check_response_item = None
        check_item = None
        if kwargs.get('check_response_item') != None:
            check_response_item=self.case_manage.selectResponseCheckItem(kwargs.get('check_response_item'),res)
            self.case_manage.setResponseCheckItem(kwargs.get('case_id'),kwargs.get('check_response_item'))
        # 2.数据库查询实际值并回写
        # 等待后端写入数据库
        if kwargs.get('check_item') != None:
            time.sleep(1)
            check_item = self.case_manage.selectDBToCheckItem(kwargs.get('data'),kwargs.get('check_item'),res,kwargs.get('db_key'))
            self.case_manage.setCheckItem(kwargs.get('case_id'),kwargs.get('check_item'))
        # 3.实际值与理论值校对,并回写校对结果
        if (check_response_item != None) or (check_item != None):
            #except_list,actual_list = self.case_manage.getCheckList(kwargs.get('case_id'),check_response_item,check_item)
            #self.case_manage.writeToCsv(except_list,actual_list,kwargs.get('case_id'))
            try:
                if check_response_item:
                    msg = ''
                    b_check_result = True
                    for str_check_key, dict_check_value in check_response_item.items():
                        str_msg_symbol_e,str_msg_e = getFormatSymbol(dict_check_value.get("expect_value"))
                        str_msg_symbol_a,str_msg_a = getFormatSymbol(dict_check_value.get("actual_value"))

                        if str_msg_e != str_msg_a:
                            b_check_result = False
                            msg = msg + ("\n字段：%s 理论值(%s)：" + str_msg_symbol_e + " -> 实际值(%s)：" + str_msg_symbol_a + " 类型不匹配")  \
                                % (str_check_key,str_msg_e,
                                    dict_check_value.get("expect_value"),
                                    str_msg_a,
                                    dict_check_value.get("actual_value"))
                        elif dict_check_value.get("expect_value") != dict_check_value.get("actual_value"):
                            b_check_result = False
                            msg = msg + ("\n字段：%s 理论值：" + str_msg_e + "%s -> 实际值：" + str_msg_a + "%s 值不匹配")  \
                                % (str_check_key,dict_check_value.get("expect_value"),dict_check_value.get("actual_value"))
                    if b_check_result == False:
                        self.assertEqual(1, 0, msg)

                if check_item:
                    msg = ''
                    b_check_result = True
                    for str_db_table_name, dict_db_table_value in check_item.items():
                        msg = msg + '\n表：%s：' % str_db_table_name
                        for str_check_key,dict_check_value in dict_db_table_value.items():
                            str_msg_symbol_e,str_msg_e = getFormatSymbol(dict_check_value.get("expect_value"))
                            str_msg_symbol_a,str_msg_a = getFormatSymbol(dict_check_value.get("actual_value"))

                            if str_msg_e != str_msg_a:
                                b_check_result = False
                                msg = msg + ("\n 字段：%s 理论值(%s)：" + str_msg_symbol_e + " -> 实际值(%s)：" + str_msg_symbol_a + " 类型不匹配") \
                                    % (str_check_key, str_msg_e,
                                        dict_check_value.get("expect_value"),
                                        str_msg_a,
                                        dict_check_value.get("actual_value"))
                            elif dict_check_value.get("type") == "inc" and (str_msg_e == 'int' or str_msg_e == 'float'):
                                v_actual_value_fix = dict_check_value.get("actual_value") \
                                                    - self.case_manage.case_pre_actual_value.get(str_db_table_name + '.' + str_check_key,0)
                                if dict_check_value.get("expect_value") != v_actual_value_fix:
                                    b_check_result = False
                                    msg = msg + ("\n 字段：%s 理论值：" + str_msg_symbol_e + " -> 实际值：" + str_msg_symbol_a + " 值不匹配") \
                                        % (str_check_key, dict_check_value.get("expect_value"),v_actual_value_fix)

                            elif dict_check_value.get("expect_value") != dict_check_value.get("actual_value"):

                                b_check_result = False
                                msg = msg + ("\n 字段：%s 理论值：" + str_msg_symbol_e + " -> 实际值：" + str_msg_symbol_a + " 值不匹配") \
                                % (str_check_key,dict_check_value.get("expect_value"),dict_check_value.get("actual_value"))

                    if b_check_result == False:
                        self.assertEqual(1, 0, msg)

                    check_result = 1
                    self.case_manage.setCheckResult(kwargs.get('case_id'),check_result)
                    self.case_manage.setSetPreActualValue(check_item)
            except AssertionError as e:
                check_result=0
                self.case_manage.setCheckResult(kwargs.get('case_id'),check_result)
                self.case_manage.setSetPreActualValue(check_item)
                raise e
    
if __name__ == '__main__':

    case = unittest.defaultTestLoader.discover("./", pattern='run_test.py')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(case)