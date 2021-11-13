#coding:utf-8

# 数据库结构体
class DataBase:
	
    url = ""
    port = 3306
    username = ""
    password = ""
    database = ""
    charset = ""

# 测试用例信息结构体
class CaseInfo:
    
    path = ""
    case_list = []

# 测试用例结构体
class Case:
    
    url = ""
    db_table = ""
    case_id = ""
    method = ""
    data = {}
    check_item = {}
    status = ""
    db_key = {}
    check_result = ""