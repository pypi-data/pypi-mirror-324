_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_1d1c5d5897.sparta_05a0d11676.qube_0aceed85a3 as qube_0aceed85a3
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_47dcb4d44a.qube_346f336121 import AerospikeConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_4dc20785ca.qube_ed18f43fc7 import CassandraConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_babf9ea126.qube_565ac0d974 import ClickhouseConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_0a23d91a28.qube_9fddb2f728 import CouchdbConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_d4f6d027d9.qube_7d159a9efc import CsvConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_33a7c69999.qube_e7495d6df2 import DuckDBConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_b9421c43ec.qube_9ff9528b7b import JsonApiConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_0c22549603.qube_a4a5d5a904 import InfluxdbConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_934d81bea8.qube_79059e7bce import MariadbConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_6513abbc37.qube_641bcb88dd import MongoConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_fa50e6ab72.qube_9822d3c8a8 import MssqlConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_8ea6d42ef8.qube_1763cdfaf1 import MysqlConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_9067a5935f.qube_cce41b520e import OracleConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_1412ab40ad.qube_36a0c45c6e import ParquetConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_0373b260a7.qube_ebbb5cbbd3 import PostgresConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_f516ba715d.qube_b048b41d27 import PythonConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_079643c9a9.qube_a8a6b472f3 import QuestDBConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_8d38b3efaf.qube_a095a853a6 import RedisConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_4bb2188437.qube_24099773cd import ScylladbConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_bd1ed653dc.qube_8bb9992aeb import SqliteConnector
from project.sparta_1d1c5d5897.sparta_05a0d11676.sparta_c0ec718a82.qube_a437672b2e import WssConnector
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_0aceed85a3.sparta_389785be68(H)
		except:C=_A
		I=A.database;J=A.oracle_service_name;K=A.keyspace;L=A.library_arctic;M=A.database_path;N=A.read_only;O=A.json_url;P=A.socket_url;Q=A.db_engine;R=A.csv_path;S=A.csv_delimiter;T=A.token;U=A.organization;V=A.lib_dir;W=A.driver;X=A.trusted_connection;D=[]
		if A.dynamic_inputs is not _A:
			try:D=json.loads(A.dynamic_inputs)
			except:pass
		Y=A.py_code_processing;B.db_engine=Q;B.init_with_params(host=E,port=F,user=G,password=C,database=I,oracle_service_name=J,csv_path=R,csv_delimiter=S,keyspace=K,library_arctic=L,database_path=M,read_only=N,json_url=O,socket_url=P,dynamic_inputs=D,py_code_processing=Y,token=T,organization=U,lib_dir=V,driver=W,trusted_connection=X)
	def init_with_params(A,host,port,user=_A,password=_A,database=_A,oracle_service_name='orcl',csv_path=_A,csv_delimiter=_A,keyspace=_A,library_arctic=_A,database_path=_A,read_only=False,json_url=_A,socket_url=_A,redis_db=0,token=_A,organization=_A,lib_dir=_A,driver=_A,trusted_connection=True,dynamic_inputs=_A,py_code_processing=_A):
		J=keyspace;I=py_code_processing;H=dynamic_inputs;G=database_path;F=database;E=password;D=user;C=port;B=host
		if A.db_engine=='aerospike':A.db_connector=AerospikeConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='cassandra':A.db_connector=CassandraConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='clickhouse':A.db_connector=ClickhouseConnector(host=B,port=C,database=F,user=D,password=E)
		if A.db_engine=='couchdb':A.db_connector=CouchdbConnector(host=B,port=C,user=D,password=E)
		if A.db_engine=='csv':A.db_connector=CsvConnector(csv_path=csv_path,csv_delimiter=csv_delimiter)
		if A.db_engine=='duckdb':A.db_connector=DuckDBConnector(database_path=G,read_only=read_only)
		if A.db_engine=='influxdb':A.db_connector=InfluxdbConnector(host=B,port=C,token=token,organization=organization,bucket=F,user=D,password=E)
		if A.db_engine==_C:A.db_connector=JsonApiConnector(json_url=json_url,dynamic_inputs=H,py_code_processing=I)
		if A.db_engine=='mariadb':A.db_connector=MariadbConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mongo':A.db_connector=MongoConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mssql':A.db_connector=MssqlConnector(host=B,port=C,trusted_connection=trusted_connection,driver=driver,user=D,password=E,database=F)
		if A.db_engine=='mysql':A.db_connector=MysqlConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='oracle':A.db_connector=OracleConnector(host=B,port=C,user=D,password=E,database=F,lib_dir=lib_dir,oracle_service_name=oracle_service_name)
		if A.db_engine=='parquet':A.db_connector=ParquetConnector(database_path=G)
		if A.db_engine==_B:A.db_connector=PostgresConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='python':A.db_connector=PythonConnector(py_code_processing=I,dynamic_inputs=H)
		if A.db_engine=='questdb':A.db_connector=QuestDBConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='redis':A.db_connector=RedisConnector(host=B,port=C,user=D,password=E,db=redis_db)
		if A.db_engine=='scylladb':A.db_connector=ScylladbConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='sqlite':A.db_connector=SqliteConnector(database_path=G)
		if A.db_engine=='wss':A.db_connector=WssConnector(socket_url=socket_url,dynamic_inputs=H,py_code_processing=I)
	def get_db_connector(A):return A.db_connector
	def test_connection(A):return A.db_connector.test_connection()
	def sparta_c3f89605e0(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)