_Z='stderr'
_Y='<IPY-INPUT>'
_X='<ipython-input-\\d+-[0-9a-f]+>'
_W='TRACEBACK RAISE EXCEPTION NOW'
_V='windows'
_U='stdout'
_T='errorMsg'
_S='traceback'
_R='/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/'
_Q=True
_P='text'
_O='\n'
_N='idle'
_M='busy'
_L='type'
_K='data'
_J='cell_id'
_I='exec'
_H='service'
_G=False
_F='execution_state'
_E='output'
_D='content'
_C='name'
_B='res'
_A=None
import os,gc,re,json,time,websocket,cloudpickle,base64,getpass,platform,asyncio
from pathlib import Path
from pprint import pprint
from jupyter_client import KernelManager
from IPython.display import display,Javascript
from IPython.core.magics.namespace import NamespaceMagics
from nbconvert.filters import strip_ansi
from django.conf import settings as conf_settings
from spartaqube_app.path_mapper_obf import sparta_fd02dc10b1
from project.sparta_75433bcd57.qube_4bf0315a6e import timeout
from project.sparta_1d1c5d5897.sparta_e0f10cf586.qube_97c853e9c9 import convert_to_dataframe,sparta_d4809fae31
B_DEBUG=_G
SEND_INTERVAL=.8
def sparta_27ec8d68df():return conf_settings.DEFAULT_TIMEOUT
def sparta_d6506bed7a():
	A=platform.system()
	if A=='Windows':return _V
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
class KernelException(Exception):
	def __init__(B,message):
		A=message;super().__init__(A)
		if B_DEBUG:print('KernelException message');print(A)
		B.traceback_msg=A
	def get_traceback_errors(A):return A.traceback_msg
class IPythonKernel:
	def __init__(A,api_key=_A,django_settings_module=_A,project_folder=_A):A.api_key=api_key;A.workspaceVarNameArr=[];A.django_settings_module=django_settings_module;A.project_folder=project_folder;A.output_queue=[];A.last_send_time=time.time();A.kernel_manager=KernelManager();A.startup_kernel()
	def startup_kernel(A):
		if A.django_settings_module is not _A:B=os.environ.copy();B['DJANGO_ALLOW_ASYNC_UNSAFE']='true';A.kernel_manager.start_kernel(env=B)
		else:A.kernel_manager.start_kernel()
		A.kernel_client=A.kernel_manager.client();A.kernel_client.start_channels()
		try:A.kernel_client.wait_for_ready();C=time.time();print('Ready, initialize with Django');A.initialize_kernel();print('--- %s seconds ---'%(time.time()-C))
		except RuntimeError:A.kernel_client.stop_channels();A.kernel_manager.shutdown_kernel()
	def send_sync(A,websocket,data):
		A.output_queue.append(data)
		if time.time()-A.last_send_time>=SEND_INTERVAL:
			if B_DEBUG:print(f"Send batch now Interval diff: {time.time()-A.last_send_time}")
			A.send_batch(websocket)
	def send_batch(A,websocket):
		B=websocket
		if len(A.output_queue)>0:
			if B is not _A:C={_B:1,_H:_I,'batch_output':A.output_queue};B.send(json.dumps(C));A.output_queue=[];A.last_send_time=time.time()
	def get_kernel_manager(A):return A.kernel_manager
	def get_kernel_client(A):return A.kernel_client
	def initialize_kernel(B):
		A='import os, sys\n';A+='import django\n';A+='os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"\n'
		if B.project_folder is not _A:C=f'user_app_db_path = r"{os.path.join(B.project_folder,"app","db.sqlite3")}"\n';C+='from django.conf import settings\n';C+='user_app_name = "notebook_app"\n';C+='settings.DATABASES[user_app_name] = {"ENGINE": "django.db.backends.sqlite3", "NAME": user_app_db_path}\n';A+=C
		A+='django.setup()\n';D=sparta_fd02dc10b1()['project'];E=sparta_fd02dc10b1()['project/core/api'];A+=f'sys.path.insert(0, r"{str(D)}")\n';A+=f'sys.path.insert(0, r"{str(E)}")\n';A+=f'os.environ["api_key"] = "{B.api_key}"\n'
		if B.project_folder is not _A:A+=f'os.chdir(r"{B.project_folder}")\n'
		B.execute(A,b_debug=_G);B.backup_venv_at_startup()
	def backup_venv_at_startup(A):B=f'import sys, os, json\nos.environ["PATH_BK"] = os.environ["PATH"]\nos.environ["VIRTUAL_ENV_BK"] = os.environ["VIRTUAL_ENV"]\nos.environ["SYS_PATH_BK"] = json.dumps(sys.path)\n';A.execute(B)
	def activate_venv(C,venv_name):
		def D():
			B=sparta_d6506bed7a()
			if B==_V:A=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\sq_venv"
			elif B=='linux':A=os.path.expanduser('~/SpartaQube/sq_venv')
			elif B=='mac':A=os.path.expanduser('~/Library/Application Support\\SpartaQube\\sq_venv')
			A=os.path.normpath(A);os.makedirs(A,exist_ok=_Q);return A
		def A():return os.path.normpath(os.path.join(D(),venv_name))
		def E():
			if os.name=='nt':B=os.path.join(A(),'Scripts')
			else:B=os.path.join(A(),'bin')
			return os.path.normpath(B)
		def F():
			C='site-packages'
			if os.name=='nt':B=os.path.join(A(),'Lib',C)
			else:D=f"python{sys.version_info.major}.{sys.version_info.minor}";B=os.path.join(A(),'lib',D,C)
			return os.path.normpath(B)
		G=f'import sys, os\nos.environ["PATH"] = os.environ["PATH_BK"]\nos.environ["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV_BK"]\n';H=f'os.environ["PATH"] = r"{E()};" + os.environ["PATH"] \nsite_packages_path = r"{F()}"\nsys.path = [elem for elem in sys.path if "site-packages" not in elem] \nsys.path.insert(0, site_packages_path)\n';B=G+H;print('+'*100);print('cmd_to_execute activate VENV');print(B);print('+'*100);C.execute(B)
	def deactivate_venv(A):B=f'import sys, os, json\nos.environ["PATH"] = os.environ["PATH_BK"]\nos.environ["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV_BK"]\nsys.path = json.loads(os.environ["SYS_PATH_BK"])\n';A.execute(B)
	def stop_kernel(A):A.kernel_client.stop_channels();A.kernel_manager.interrupt_kernel();A.kernel_manager.shutdown_kernel(now=_Q)
	def cd_to_notebook_folder(C,notebook_path,websocket=_A):B=notebook_path;A=f"import os, sys\n";A+=f"os.chdir('{B}')\n";A+=f"sys.path.insert(0, '{B}')";C.execute(A,websocket)
	def escape_ansi(C,line):A=re.compile('\\x1B(?:[@-Z\\\\-_]|\\[[0-?]*[ -/]*[@-~])');A=re.compile('(?:\\x1B[@-_]|[\\x80-\\x9F])[0-?]*[ -/]*[@-~]');A=re.compile('(\\x9B|\\x1B\\[)[0-?]*[ -/]*[@-~]');B='\\x1b((\\[\\??\\d+[hl])|([=<>a-kzNM78])|([\\(\\)][a-b0-2])|(\\[\\d{0,2}[ma-dgkjqi])|(\\[\\d+;\\d+[hfy]?)|(\\[;?[hf])|(#[3-68])|([01356]n)|(O[mlnp-z]?)|(/Z)|(\\d+)|(\\[\\?\\d;\\d0c)|(\\d;\\dR))';A=re.compile(B,flags=re.IGNORECASE);return A.sub('',line)
	def execute(B,cmd,websocket=_A,cell_id=_A,b_debug=_G):
		H=b_debug;F=cell_id;E=websocket;B.last_send_time=time.time();N=B.kernel_client.execute(cmd);I=_M;C=_A
		while I!=_N and B.kernel_client.is_alive():
			try:
				J=B.kernel_client.get_iopub_msg()
				if not _D in J:continue
				A=J[_D]
				if B_DEBUG or H:print(_R);print(type(A));print(A);print(A.keys());print(_R)
				if _S in A:
					if B_DEBUG or H:print(_W);print(A)
					L=re.compile(_X);K=[re.sub(L,_Y,strip_ansi(A))for A in A[_S]];C=KernelException(_O.join(K))
					if E is not _A:D=json.dumps({_B:-1,_J:F,_H:_I,_T:_O.join(K),'errorMsgRaw':A});B.send_sync(E,D)
				if _C in A:
					if A[_C]==_U:C=A[_P];G=B.format_output(C);D=json.dumps({_B:1,_H:_I,_E:G,_J:F});B.send_sync(E,D)
					if A[_C]==_Z:C=A[_P];D=json.dumps({_B:-1,_J:F,_H:_I,_T:C});B.send_sync(E,D)
				if _K in A:C=A[_K];G=B.format_output(C);D=json.dumps({_B:1,_H:_I,_E:G,_J:F});B.send_sync(E,D)
				if _F in A:I=A[_F]
			except Exception as M:print('Execute exception EXECUTION');print(M)
		B.send_batch(E);return C
	def execute_shell(B,cmd,websocket=_A,cell_id=_A,b_debug=_G):
		P='Custom signal term detected. Breaking loop name.';K=b_debug;J='custom_sig_term';G=cmd;F=cell_id;E=websocket;G=f'{G} && echo "custom_sig_term"';B.last_send_time=time.time();T=B.kernel_client.execute(G);H=_M;C=_A;L=_G;M=_A;Q=2
		while B.kernel_client.is_alive():
			if L:
				if time.time()-M>Q:break
			try:
				N=B.kernel_client.get_iopub_msg(timeout=2)
				if not _D in N:continue
				A=N[_D]
				if B_DEBUG or K:print(_R);print(type(A));print(A);print(A.keys());print(_R)
				if _S in A:
					if B_DEBUG or K:print(_W);print(A)
					R=re.compile(_X);O=[re.sub(R,_Y,strip_ansi(A))for A in A[_S]];C=KernelException(_O.join(O))
					if E is not _A:D=json.dumps({_B:-1,_J:F,_H:_I,_T:_O.join(O)});B.send_sync(E,D)
				if _C in A:
					if A[_C]==_U:
						C=A[_P]
						if J in C:print(P);break
						I=B.format_output(C);D=json.dumps({_B:1,_H:_I,_E:I,_J:F});B.send_sync(E,D)
					if A[_C]==_Z:
						C=A[_P]
						if J in C:print(P);break
						D=json.dumps({_B:-1,_J:F,_H:_I,_T:C});B.send_sync(E,D)
				if _K in A:
					C=A[_K]
					if J in str(C):print('Custom signal term detected. Breaking loop data.');break
					I=B.format_output(C);D=json.dumps({_B:1,_H:_I,_E:I,_J:F});B.send_sync(E,D)
				if _F in A:
					H=A[_F];print(f"STATE STATE STATE {H}")
					if H==_N:L=_Q;M=time.time()
			except Exception as S:print('Execute exception shell EXECUTION');print(S)
		B.send_batch(E);return C
	def list_workspace_variables(C):
		N='df_columns';M='is_df';L='preview'
		def O(data,trunc_size):B=trunc_size;A=data;A=A[:B]+'...'if len(A)>B else A;return A
		P='%whos';U=C.kernel_client.execute(P);H=_M;A=[]
		while H!=_N and C.kernel_client.is_alive():
			try:
				I=C.kernel_client.get_iopub_msg()
				if not _D in I:continue
				D=I[_D]
				if _C in D:
					if D[_C]==_U:A.append(D[_P])
				if _F in D:H=D[_F]
			except Exception as F:print(F);pass
		G=C.get_kernel_variables_memory_dict()
		if G is _A:G=dict()
		try:
			A=''.join(A).split(_O);A=A[2:-1];J=[]
			for Q in A:
				E=re.split('\\s{2,}',Q.strip())
				if len(E)>=2:K=E[0];R=E[1];S=' '.join(E[2:])if len(E)>2 else'';J.append({_C:K,_L:R,L:S,'size':G.get(K,0)})
			A=J
			for B in A:
				B['preview_display']=O(B[L],30);B[M]=_G;B[N]=json.dumps([])
				if B[_L]=='DataFrame':
					try:T=convert_to_dataframe(C.get_workspace_variable(B[_C]),B[_C]);B[N]=json.dumps(list(T.columns));B[M]=_Q
					except:pass
		except Exception as F:print('Except list workspace var');print(F)
		return A
	def get_kernel_variables_memory_dict(A):B='size_in_bytes_variables_dict';C='\nimport os, sys\ndef get_size_bytes_variables_dict():\n    # Exclude the function itself and common IPython artifacts\n    excluded_vars = {"get_size_mb", "_", "__builtins__", "__file__", "__name__", "__doc__"}\n    all_vars = {k: v for k, v in globals().items() if k not in excluded_vars and not callable(v) and not k.startswith("__")}\n    \n    variables_mem_dict = dict()\n    for var_name, obj in all_vars.items():\n        variables_mem_dict[var_name] = sys.getsizeof(obj)\n    \n    return variables_mem_dict\nsize_in_bytes_variables_dict = get_size_bytes_variables_dict()    \n';A.execute(C,b_debug=_G);D=A.get_workspace_variable(B);A.remove_variable_from_kernel(B);return D
	def get_kernel_memory_size(A):B='size_in_bytes';C='\ndef get_size_bytes():\n    # Exclude the function itself and common IPython artifacts\n    excluded_vars = {"get_size_mb", "_", "__builtins__", "__file__", "__name__", "__doc__"}\n    all_vars = {k: v for k, v in globals().items() if k not in excluded_vars and not callable(v) and not k.startswith("__")}\n    \n    size_in_bytes = 0\n    for var_name, obj in all_vars.items():\n        size_in_bytes += sys.getsizeof(obj)\n    \n    return size_in_bytes\nsize_in_bytes = get_size_bytes()    \n';A.execute(C,b_debug=_G);D=A.get_workspace_variable(B);A.remove_variable_from_kernel(B);return D
	def get_kernel_variable_repr(A,kernel_variable):
		F=f"{kernel_variable}";J=A.kernel_client.execute(F);C=_M;D=json.dumps({_B:-1})
		while C!=_N and A.kernel_client.is_alive():
			try:
				E=A.kernel_client.get_iopub_msg()
				if not _D in E:continue
				B=E[_D]
				if _K in B:G=B[_K];H=A.format_output(G);D=json.dumps({_B:1,_E:H})
				if _F in B:C=B[_F]
			except Exception as I:print('Exception get_kernel_variable_repr');print(I);pass
		return D
	def format_output(E,output):
		D='image/png';C='text/html';B='text/plain';A=output
		if isinstance(A,dict):
			if C in A:return{_E:A[C],_L:C}
			if D in A:return{_E:A[D],_L:D}
			if B in A:return{_E:A[B],_L:B}
		return{_E:A,_L:B}
	def get_workspace_variable(A,kernel_variable):
		D=_A
		try:
			G=f"import cloudpickle\nimport base64\ntmp_sq_ans = _\nbase64.b64encode(cloudpickle.dumps({kernel_variable})).decode()";J=A.kernel_client.execute(G);E=_M
			while E!=_N and A.kernel_client.is_alive():
				try:
					F=A.kernel_client.get_iopub_msg()
					if not _D in F:continue
					B=F[_D]
					if _K in B:H=B[_K];I=A.format_output(H);D=cloudpickle.loads(base64.b64decode(I[_E]))
					if _F in B:E=B[_F]
				except Exception as C:print(C);pass
		except Exception as C:print('Exception get_workspace_variable');print(C)
		A.execute(f"del tmp_sq_ans");A.execute(f"del cloudpickle");A.execute(f"del base64");return D
	def set_workspace_variables(A,variables_dict,websocket=_A):
		for(B,C)in variables_dict.items():A.set_workspace_variable(B,C,websocket=websocket)
	def set_workspace_variable(A,name,value,websocket=_A):
		try:B=f'import cloudpickle\nimport base64\n{name} = cloudpickle.loads(base64.b64decode("{base64.b64encode(cloudpickle.dumps(value)).decode()}"))';A.execute(B,websocket)
		except Exception as C:print('Exception setWorkspaceVariable');print(C)
		A.execute(f"del cloudpickle");A.execute(f"del base64")
	def reset_kernel_workspace(A):B='%reset -f';A.execute(B)
	def remove_variable_from_kernel(A,kernel_variable):B="del globals()['"+str(kernel_variable)+"']";A.execute(B)
	def cloudpickle_kernel_variables(A):C='kernel_cpkl_unpicklable';B='kernel_cpkl_picklable';A.execute('import cloudpickle');A.execute('\nimport io\nimport cloudpickle\ndef test_picklability():\n    variables = {k: v for k, v in globals().items() if not k.startswith(\'_\')}\n    picklable = {}\n    unpicklable = {}\n    var_not_to_pickle = [\'In\', \'Out\', \'test_picklability\', \'get_ipython\']\n    var_type_not_to_pickle = [\'ZMQExitAutocall\']\n    \n    for var_name, var_value in variables.items():\n        var_type = type(var_value)\n        if var_name in var_not_to_pickle:\n            continue\n        if var_type.__name__ in var_type_not_to_pickle:\n            continue\n        try:\n            # Attempt to serialize the variable\n            buffer = io.BytesIO()\n            cloudpickle.dump(var_value, buffer)\n            picklable[var_name] = buffer.getvalue()\n        except Exception as e:\n            unpicklable[var_name] = {\n                "type_name": var_type.__name__,\n                "module": var_type.__module__,\n                "repr": repr(var_value),\n                "error": str(e),\n            }\n    \n    return picklable, unpicklable\n\nkernel_cpkl_picklable, kernel_cpkl_unpicklable = test_picklability()\ndel test_picklability\n');D=A.get_workspace_variable(B);E=A.get_workspace_variable(C);A.remove_variable_from_kernel(B);A.remove_variable_from_kernel(C);return D,E
	def execute_code(A,cmd,websocket=_A,cell_id=_A,bTimeout=_G):
		C=cell_id;B=websocket
		if bTimeout:return A.execute_code_timeout(cmd,websocket=B,cell_id=C)
		else:return A.execute_code_no_timeout(cmd,websocket=B,cell_id=C)
	@timeout(sparta_27ec8d68df())
	def execute_code_timeout(self,cmd,websocket=_A,cell_id=_A):return self.execute(cmd,websocket=websocket,cell_id=cell_id)
	def execute_code_no_timeout(A,cmd,websocket=_A,cell_id=_A):return A.execute(cmd,websocket=websocket,cell_id=cell_id)
	def getLastExecutedVariable(A,websocket):
		try:B=f"import cloudpickle\nimport base64\ntmp_sq_ans = _\nbase64.b64encode(cloudpickle.dumps(tmp_sq_ans)).decode()";return cloudpickle.loads(base64.b64decode(A.format_output(A.execute(B,websocket))))
		except Exception as C:print('Excep last exec val');raise C
	def sparta_e9a79df26e(A,nameVar):
		try:B=f"import cloudpickle\nimport base64\ntmp_sq_ans = _\nbase64.b64encode(cloudpickle.dumps({nameVar})).decode()";return cloudpickle.loads(base64.b64decode(A.format_output(A.execute(B))))
		except Exception as C:print('Exception get_kernel_variable');print(C);return
	def removeWorkspaceVariable(A,name):
		try:del A.workspaceVarNameArr[name]
		except Exception as B:print('Exception removeWorkspaceVariable');print(B)
	def getWorkspaceVariables(A):return[]