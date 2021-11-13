#coding:utf-8

import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from .struct_data import Case
from util.opreat_json import OperetJson
from util.opreat_database import OperetDataBase
import copy
import decimal
import pandas as pd
from .func import formatDBReturn,getFormatSymbol

class CaseManager:

    def __init__(self, config):
        # self.case_info = config.getCaseInfo()
        self.config=config
        # 接收测试用例json文件数据
        self.case_list = []
        self.case_path = ''
        # self.case_config = case_config
        self.cases_data = None
        self.case_lines = 0
        # 接收测试用例
        self.case = Case()
        self.case_dict = {}
        self.case_pre_actual_value = {}
        self.OpDataBase = OperetDataBase(self.config.getDataBase())
        self.OpJson = OperetJson()
        self.loadCaseConfig()

    def loadCaseConfig(self):
        
        data=self.config.getCaseInfo()
        self.case_list = data['case_list']
        self.case_path = data['case_path']

    def initCase(self,case_id,**kwargs):
        self.case_dict[case_id] = kwargs

    def setData(self,case_id,data):
        self.case_dict[case_id]["data"]=data

    def setCheckItem(self,case_id,check_item):

        self.case_dict[case_id]["check_item"]=check_item

    def setResponse(self,case_id,response):

        self.case_dict[case_id]["response"]=response
    
    def setCheckResult(self,case_id,check_result):

        self.case_dict[case_id]["check_result"]=check_result

    def setSetPreActualValue(self,check_item):
        if check_item:
            for check_table, check_field in check_item.items():
                for field, ecp_act_value in check_field.items():
                    if ecp_act_value.get("type") and ecp_act_value.get("type") == 'inc'\
                            and (isinstance(ecp_act_value['actual_value'],float) or isinstance(ecp_act_value['actual_value'],int)):
                        self.case_pre_actual_value[check_table + '.' + field] = ecp_act_value["actual_value"]

    def selectDBToCheckItem(self,data,check_item,response,db_key):
        chk_item = copy.deepcopy(check_item)
        for check_table,check_field in check_item.items():
            fields=""
            field_list=[]
            conditions=""
            for field,ecp_act_value in check_field.items():
                # 获取对应表的查询字段
                tmp = field+','
                fields = fields+tmp
                field_list.append(field)
            # 去除最后面的逗号
            fields=fields[0:-1]
            for condition_field,condition_value in db_key[check_table].items():
                value = self._getConditionFieldValue(data,response,db_key,condition_value)
                db_key[check_table][condition_field] = value
                tmp = condition_field+'='+"'"+str(value)+"'"+' and '
                conditions += tmp
            conditions=conditions[0:-5]
            sql = "select %s from %s where %s"%(fields,check_table,conditions)
            actual_ret = self.OpDataBase.executeSql(sql)
            self.OpDataBase.commit()
            actual_list=[]
            if len(actual_ret)==0:
                for i in field_list:
                    actual_list.append("NULL")
            else:
                for r in actual_ret[0]:
                    actual_list.append(formatDBReturn(r))
            actual_dict=dict(zip(field_list,actual_list))
            
            for field, actual_value in actual_dict.items():
                chk_item[check_table][field]["actual_value"]=actual_value
        
        return chk_item

    def _getConditionFieldValue(self,data,response,db_key,db_key_field_value):
        dic=response
        result=None
        if db_key_field_value.startswith('@db.'):
            condition_value=db_key_field_value.split("@db.")[1]
            tmp = condition_value.split(".")
            str_target_table = tmp[0] + '.' + tmp[1]
            dict_target_value = db_key[str_target_table]
            for k,v in dict_target_value.items():
                str_target_key = k
                str_target_value = v
            sql="select %s from %s where %s = '%s'"%(tmp[2],str_target_table,str_target_key,str_target_value)
            result=self.OpDataBase.executeSql(sql)[0][0]
        elif db_key_field_value.startswith('@response.'):
            db_key_field_value=db_key_field_value.split("@response.")[1]
            tmp = db_key_field_value.split(".")
            for p in tmp:
                if p.startswith('$'):
                    p=int(p.split("$")[1])
                dic=dic[p]
                if dic == None:
                    break
            result=dic
        elif db_key_field_value.startswith('@data.'):
            tmp=db_key_field_value.split("@data.")[1]
            result=data[tmp]
            # elif db_key_field_value.startswith('@SQL.'):
            #     db_key_field_value=db_key_field_value.split("@SQL.")[1]
            #     tmp=db_key_field_value.split("$$")
            #     sql=""
            #     for p in tmp:
            #         if p.startswith('@RESPONSE.'):
            #             p=p.split("@RESPONSE.")[1]
            #             p=p.split(".")
            #             for q in p:
            #                 if q.startswith('$'):
            #                     q=int(q.split("$")[1])
            #                 dic=dic[q]
            #             p="'%s'"%(dic)
            #         sql=sql+p
                # result=str(self.OpDataBase.executeSql(sql)[0][0])
        else:
            result = db_key_field_value
        return result
    
    def selectResponseCheckItem(self,check_response_item,response):
        chk_response_item = copy.deepcopy(check_response_item)
        res = copy.deepcopy(response)
        for chk_response_item_name,chk_response_item_value in res.items():
            if chk_response_item.get(chk_response_item_name):
                chk_response_item[chk_response_item_name]["actual_value"]=chk_response_item_value

        return chk_response_item

    def setResponseCheckItem(self,case_id,check_response_item):
        self.case_dict[case_id]["check_response_item"]=check_response_item

    def getCheckList(self,case_id, check_response_item, check_item):
        except_list=[case_id]
        actual_list=[case_id]
        if check_response_item != None:
            for check_response_item_name,check_response_item_value in check_response_item.items():
                except_list.append(check_response_item_name)
                except_list.append(check_response_item_value["expect_value"])
                actual_list.append(check_response_item_name)
                actual_list.append(check_response_item_value["actual_value"])

        if check_item != None:
            for check_table,check_field in check_item.items():
                except_list.append(check_table)
                actual_list.append(check_table)
                for field,ecp_act_value in check_field.items():
                    except_list.append(field)
                    except_list.append(ecp_act_value["expect_value"])

                    #如果字段类型为增量且为数字类型，则每次统计的实际值为增量的数值
                    if ecp_act_value.get("type") and ecp_act_value.get("type") == 'inc' \
                            and (isinstance(ecp_act_value['actual_value'],float) or isinstance(ecp_act_value['actual_value'],int)):
                        actual_list.append(field)
                        if isinstance(ecp_act_value['actual_value'],float):
                            actual_list.append(round(ecp_act_value["actual_value"] -
                            self.case_pre_actual_value.get(check_table + '.' +field,0),4))
                        else:
                            actual_list.append(ecp_act_value["actual_value"] -
                                  self.case_pre_actual_value.get(check_table + '.' + field, 0))
                    else:
                        actual_list.append(field)
                        actual_list.append(ecp_act_value["actual_value"])
        
        return except_list,actual_list
        
    def allCaseToJson(self):
        for flie_name,data in self.case_dict.items():
            file_path = self.case_path + flie_name
            data=dict(data)
            self.OpJson.writeData(data,file_path)
    
    def closeConn(self):
        self.OpDataBase.closeConn()

    def checkResponse(self,response,test_system):
        if test_system.upper()=="OMS" and int(response["FID_CODE"])>=0:
            return True
        elif test_system.upper()=="MIDOFFICE":
            return True        

    # 设置依赖数据
    def setRelyItem(self,data,rely_item):
        for item_name,item_value in rely_item.items():
            item_name=item_name.split("$")
            item_value=item_value.split("%")
            if item_name[0].upper()=='DATA':
                index=item_name[1]
                dic=copy.deepcopy(self.case_dict)
                for p in item_value:
                    if p.startswith('$'):
                        p=int(p.split("$")[1])
                    dic=dic[p]
                data[index]=dic
                return data

    def writeToCsv(self,except_list,actual_list,case_id):
        
        df = pd.DataFrame({'实际值':actual_list,'理论值':except_list})
        df.to_csv('%s.csv'%(self.config.report_path+'_'+case_id),index = None,encoding = 'gbk')

    def message(self,actual_list,except_list):
        actual_=[]
        except_=[]
        for i in range(len(actual_list)):
            if actual_list[i]!=except_list[i]:
                actual_.append('**'+actual_list[i]+'**')
                except_.append('**'+except_list[i]+'**')
            else:
                actual_.append(actual_list[i])
                except_.append(except_list[i])

        msg="\n实际值与理论值不符!!!\n实际值:%s\n理论值:%s"%(actual_,except_)

        return msg