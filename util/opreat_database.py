#coding:utf-8
import pymysql
import decimal
class OperetDataBase:

	def __init__(self, database_info=None):
		
		self.conn = pymysql.connect(host=database_info.url,
									port=database_info.port,
									user=database_info.username,
									passwd=database_info.password,
									db=database_info.database,
									charset=database_info.charset)
		#self.cur = self.conn.cursor()
	
	def executeSql(self, sql):
		cursor = self.conn.cursor()
		self.conn.sql_mode
		try:
			cursor.execute(sql)
			rows_db = cursor.fetchall()
		except pymysql.DatabaseError as e:
			cursor.close()
			return ()
		return rows_db

	def closeConn(self):
		self.conn.close()
	
	def commit(self):
		self.conn.commit()
		

if __name__ == '__main__':

	import sys,os
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(BASE_DIR)
	from base.struct_data import DataBase
	db=DataBase()
	db.url="172.19.81.78"
	db.port=8002
	db.username="root"
	db.password="OMS@10jqka"
	db.database="quickbroker"
	db.charset="utf8"
	ODB = OperetDataBase(db)
	sql="select business_balance,cancel_flag,offset_flag from entrust where stock_account='5LC05088'"
	ret=ODB.executeSql(sql)
	tmp=[]
	for r in ret[0]:
		if isinstance(r,decimal.Decimal):
		# 	pass
			print(str(r))
		print(type(type(r)))
	# print(tmp)
	# print(type(ret[0][0]))
	exit()
	list1=["client_id","client_name","branch_no"]
	list2=list(ret[0])
	dic=dict(zip(list1,list2))
	li=["hello","hhh"]
	li.append(dic['client_name'])
	print(li[2]=="")