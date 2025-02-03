_H='execution_count'
_G='cell_type'
_F='code'
_E='outputs'
_D='source'
_C='cells'
_B='sqMetadata'
_A='metadata'
import os,re,uuid,json
from datetime import datetime
from nbconvert.filters import strip_ansi
from project.sparta_1d1c5d5897.sparta_9040a4dffd import qube_877d906936 as qube_877d906936
from project.sparta_1d1c5d5897.sparta_e0f10cf586.qube_97c853e9c9 import sparta_d4809fae31,sparta_9fbb5384da
def sparta_e12dd1450e(file_path):return os.path.isfile(file_path)
def sparta_42a7202d14():return qube_877d906936.sparta_bfb952d58b(json.dumps({'date':str(datetime.now())}))
def sparta_98351ff29c():B='python';A='name';C={'kernelspec':{'display_name':'Python 3 (ipykernel)','language':B,A:'python3'},'language_info':{'codemirror_mode':{A:'ipython','version':3},'file_extension':'.py','mimetype':'text/x-python',A:B,'nbconvert_exporter':B,'pygments_lexer':'ipython3'},_B:sparta_42a7202d14()};return C
def sparta_44487ced92():return{_G:_F,_D:[''],_A:{},_H:None,_E:[]}
def sparta_9aacba6ad0():return[sparta_44487ced92()]
def sparta_178cb225a3():return{'nbformat':4,'nbformat_minor':0,_A:sparta_98351ff29c(),_C:[]}
def sparta_ef98ed7c98(first_cell_code=''):A=sparta_178cb225a3();B=sparta_44487ced92();B[_D]=[first_cell_code];A[_C]=[B];return A
def sparta_2a05065979(full_path):
	A=full_path
	if sparta_e12dd1450e(A):return sparta_04e7ff21b0(A)
	else:return sparta_ef98ed7c98()
def sparta_04e7ff21b0(full_path):return sparta_adaf21f961(full_path)
def sparta_ab00484763():A=sparta_178cb225a3();B=json.loads(qube_877d906936.sparta_9b234d7d53(A[_A][_B]));A[_A][_B]=B;return A
def sparta_adaf21f961(full_path):
	with open(full_path)as C:B=C.read()
	if len(B)==0:A=sparta_178cb225a3()
	else:A=json.loads(B)
	A=sparta_54f63f1054(A);return A
def sparta_54f63f1054(ipynb_dict):
	A=ipynb_dict;C=list(A.keys())
	if _C in C:
		D=A[_C]
		for B in D:
			if _A in list(B.keys()):
				if _B in B[_A]:B[_A][_B]=qube_877d906936.sparta_9b234d7d53(B[_A][_B])
	try:A[_A][_B]=json.loads(qube_877d906936.sparta_9b234d7d53(A[_A][_B]))
	except:A[_A][_B]=json.loads(qube_877d906936.sparta_9b234d7d53(sparta_42a7202d14()))
	return A
def sparta_6816cb034c(full_path):
	B=full_path;A=dict()
	with open(B)as C:A=C.read()
	if len(A)==0:A=sparta_ab00484763();A[_A][_B]=json.dumps(A[_A][_B])
	else:
		A=json.loads(A)
		if _A in list(A.keys()):
			if _B in list(A[_A].keys()):A=sparta_54f63f1054(A);A[_A][_B]=json.dumps(A[_A][_B])
	A['fullPath']=B;return A
def save_ipnyb_from_notebook_cells(notebook_cells_arr,full_path,dashboard_id='-1'):
	R='output_type';Q='markdown';L=full_path;K='tmp_idx';B=[]
	for A in notebook_cells_arr:
		A['bIsComputing']=False;S=A['bDelete'];F=A['cellType'];M=A[_F];T=A['positionIndex'];A[_D]=[M];G=A.get('ipynbOutput',[]);C=A.get('ipynbError',[]);print('ipynb_output_list');print(G);print(type(G));print('ipynb_error_list');print(C);print(type(C))
		if int(S)==0:
			if F==0:H=_F
			elif F==1:H=Q
			elif F==2:H=Q
			elif F==3:H='raw'
			D={_A:{_B:qube_877d906936.sparta_bfb952d58b(json.dumps(A))},'id':uuid.uuid4().hex[:8],_G:H,_D:[M],_H:None,K:T,_E:[]}
			if len(G)>0:
				N=[]
				for E in G:O={};O[E['type']]=[E['output']];N.append({'data':O,R:'execute_result'})
				D[_E]=N
			elif len(C)>0:
				D[_E]=C
				try:
					J=[];U=re.compile('<ipython-input-\\d+-[0-9a-f]+>')
					for E in C:E[R]='error';J+=[re.sub(U,'<IPY-INPUT>',strip_ansi(A))for A in E['traceback']]
					if len(J)>0:D['tbErrors']='\n'.join(J)
				except Exception as V:print('Except prepare error output traceback with msg:');print(V)
			else:D[_E]=[]
			B.append(D)
	B=sorted(B,key=lambda d:d[K]);[A.pop(K,None)for A in B];I=sparta_2a05065979(L);P=I[_A][_B];P['identifier']={'dashboardId':dashboard_id};I[_A][_B]=qube_877d906936.sparta_bfb952d58b(json.dumps(P));I[_C]=B
	with open(L,'w')as W:json.dump(I,W,indent=4)
	return{'res':1}
def sparta_a4d8e02755(full_path):
	A=full_path;A=sparta_d4809fae31(A);C=dict()
	with open(A)as D:E=D.read();C=json.loads(E)
	F=C[_C];B=[]
	for G in F:B.append({_F:G[_D][0]})
	print('notebook_cells_list');print(B);return B