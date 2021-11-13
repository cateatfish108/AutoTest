#coding:utf-8
import decimal

def getFormatSymbol(value):
    if (isinstance(value,str)):
        return  "%s","string"
    elif (isinstance(value,int)):
        return "%d","int"
    elif (isinstance(value,float)):
        return "%f","float"

def formatDBReturn(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
        actual_list.append(f_tmp)
    elif isinstance(value, int):
        return int(value)
    else:
        return value
