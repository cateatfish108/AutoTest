#coding:utf-8

import sys ,os
#__file__的是打印当前被执行的模块.py文件相对路径，注意是相对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from .struct_data import *
from util.opreat_json import OperetJson 
class Config:

    def __init__(self,config_path,case_config_path):
        self.database = DataBase()
        self.test_system = ""
        self.report_path = ""
        self.log_path = ""
        self.config_path = config_path
        self.case_config_path = case_config_path
        self.config = None
        self.db_congfig = None
        self.init()
        
    def init(self):
        self._loadConfigData()
        self.setDataBase()
        self.setTestSystem()
        self.setReportPath()
        self.setLogPath()

    def _loadConfigData(self):
        self.opjson = OperetJson()
        self.config = self.opjson.readData(self.config_path)
        self.case_congfig = self.opjson.readData(self.case_config_path)

    def setDataBase(self):
        self.database.url = self.case_congfig['database']['url']
        self.database.port = self.case_congfig['database']['port']
        self.database.username = self.case_congfig['database']['username']
        self.database.password = self.case_congfig['database']['password']
        self.database.database = self.case_congfig['database']['database']
        self.database.charset = self.case_congfig['database']['charset']

    def getDataBase(self):
        
        return self.database

    def getCaseInfo(self):
        
        return self.case_congfig

    def setTestSystem(self):
        self.test_system = self.config['test_system']

    def getTestSystem(self):

        return self.test_system

    def setReportPath(self):
        self.report_path = self.config['report_path']

    def getReportPath(self):

        return self.report_path

    def setLogPath(self):
        self.log_path = self.config['log_path']

    def getLogPath(self):

        return self.report_path

if __name__ == '__main__':
	CONFIG_FILE = "../config/config.json"
	CASE_CONFIG_PATH = "../TestCase/case_config.json"
	config = Config(CONFIG_FILE,CASE_CONFIG_PATH)
	print(config.database.url)

           