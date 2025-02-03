import os
from project.sparta_75433bcd57.sparta_4707cc0e48.qube_2b3fffb380 import qube_2b3fffb380
from project.sparta_75433bcd57.sparta_4707cc0e48.qube_816168dd74 import qube_816168dd74
from project.sparta_75433bcd57.sparta_4707cc0e48.qube_65f50127f9 import qube_65f50127f9
from project.sparta_75433bcd57.sparta_4707cc0e48.qube_c4fbd00356 import qube_c4fbd00356
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_2b3fffb380()
		elif A.dbType==1:A.dbCon=qube_816168dd74()
		elif A.dbType==2:A.dbCon=qube_65f50127f9()
		elif A.dbType==4:A.dbCon=qube_c4fbd00356()
		return A.dbCon