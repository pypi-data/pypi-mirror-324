import os,sys,json,importlib,traceback,asyncio,subprocess,platform
from pathlib import Path
from channels.generic.websocket import WebsocketConsumer
from project.sparta_1d1c5d5897.sparta_e0f10cf586.qube_97c853e9c9 import sparta_d4809fae31
class OutputRedirector:
	def __init__(A,websocket,filepath):A.websocket=websocket;A.filepath=filepath;A.original_stdout=sys.stdout;A.original_stderr=sys.stderr;A.file=None
	def __enter__(A):
		os.makedirs(os.path.dirname(A.filepath),exist_ok=True);A.file=open(A.filepath,'w')
		class B:
			def __init__(A,file,websocket):A.file=file;A.websocket=websocket
			def write(A,message):
				B=message
				if A.file:A.file.write(B)
				if A.websocket:
					try:A.websocket.send(json.dumps({'res':1000,'msg':B}))
					except Exception as C:print(f"WebSocket send error: {C}",file=A.file)
			def flush(A):
				if A.file:A.file.flush()
		A.custom_stream=B(A.file,A.websocket);sys.stdout=A.custom_stream;sys.stderr=A.custom_stream
	def __exit__(A,exc_type,exc_val,exc_tb):
		sys.stdout=A.original_stdout;sys.stderr=A.original_stderr
		if A.file:A.file.close()
class ApiWebsocketWS(WebsocketConsumer):
	def connect(A):print('Connect Now');A.user=A.scope['user'];A.accept()
	def disconnect(A,close_code=None):print('Disconnect')
	def receive(A,text_data):
		I='baseProjectPath';E=text_data
		if len(E)>0:
			B=json.loads(E);J=B.get('isRunMode',False);K=sparta_d4809fae31(B[I]);F=os.path.join(os.path.dirname(K),'backend');sys.path.insert(0,F);import websockets as C;importlib.reload(C);G=B['service'];H=B.copy();del B[I];L=os.path.join(F,'logs','output.log')
			if J:D=C.sparta_9756ec7860(G,H,A.user);A.send(json.dumps(D))
			else:
				with OutputRedirector(A,L):
					try:D=C.sparta_9756ec7860(G,H,A.user);A.send(json.dumps(D))
					except Exception as M:print(traceback.format_exc());A.send(json.dumps({'res':-1,'errorMsg':str(M)}))