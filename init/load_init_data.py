#!/usr/bin/env python3
# coding: utf-8

import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import pymysql
from util.opreat_database import OperetDataBase
from util.opreat_json import OperetJson
from base.config import Config

class InitDB:

    def __init__(self,db_connect,sql_init_path):
        
        self.conn = db_connect
        self.sql_file = []
        self.sql_file_path = sql_init_path
    
    # def init(self):

    def getSqlFile(self):
        data = self.OpJson.readData(self.init_config_path)
        self.sql_file=data["sql_init_file"]
        self.init_config_path=data["init_data_path"]

    def run(self):
        try:
            with open(self.sql_file_path,encoding='utf-8',mode='r') as fil:
                # 读取整个sql文件，以分号切割。[:-1]删除最后一个元素，也就是空字符串
                for sql in fil.readlines():
                    # 带#的为注释
                    if sql[0:1] == '#':
                        continue

                    # 判断包含空行的
                    if '\n' in sql:
                        # 替换空行为1个空格
                        sql = sql.replace('\n', ' ')

                    sql = sql.lstrip()
                    # 没有字符串则忽略
                    if len(sql) == 0:
                        continue

                    # 判断多个空格时
                    if '    ' in sql:
                        # 替换为空
                        sql = sql.replace('    ', '')

                    # sql语句添加分号结尾
                    res=self.conn.executeSql(sql)
                    print(res)
                    print("执行成功sql: %s"%sql)
        except Exception as e:
            print(e)
            print('执行失败sql: %s'%sql)
        finally:
            self.conn.commit()
            #self.conn.closeConn()

if __name__ == '__main__':
    
    CONFIG_PATH = "../config/config.json"
    CASE_CONFIG_PATH = "../TestCase/case_config.json"
    INIT_CONFIG_PATH = "./init_config.json"
    config = Config(CONFIG_PATH,CASE_CONFIG_PATH)
    OpDataBase = OperetDataBase(config.getDataBase())
    init_db=InitDB(OpDataBase,INIT_CONFIG_PATH)
    init_db.run()