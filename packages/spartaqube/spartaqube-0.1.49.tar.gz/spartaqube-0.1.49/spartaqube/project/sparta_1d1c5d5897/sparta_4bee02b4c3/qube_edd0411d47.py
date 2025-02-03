import json,base64,asyncio,subprocess,uuid,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_1d1c5d5897.sparta_ed520409dc import qube_b79a99bc7e as qube_b79a99bc7e
from project.sparta_1d1c5d5897.sparta_05a0d11676 import qube_0aceed85a3
from project.sparta_1d1c5d5897.sparta_6f8ac4359a import qube_cb1850bb26 as qube_cb1850bb26
from project.sparta_1d1c5d5897.sparta_05a0d11676.qube_fad15a25c0 import Connector as Connector
def sparta_13d6315eee(json_data,user_obj):
	D='key';A=json_data;print('Call autocompelte api');print(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_b292ee994b(B)
	return{'res':1,'output':C,D:B}
def sparta_b292ee994b(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";C=requests.get(G)
	try:
		if int(C.status_code)==200:
			H=json.loads(C.text);D=H['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]