_B='menuBar'
_A='windows'
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.http import FileResponse,Http404
from urllib.parse import unquote
import project.sparta_75433bcd57.sparta_e9edb68cbd.qube_dc67a122c8 as qube_dc67a122c8
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_8197dd6d72
from project.sparta_1d1c5d5897.sparta_fad3ec945b import qube_1a6dfd0324 as qube_1a6dfd0324
from project.sparta_1d1c5d5897.sparta_ee6412fa89 import qube_52cd691e01 as qube_52cd691e01
def sparta_d6506bed7a():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_a4cd1ff3de(request):A=request;B=qube_dc67a122c8.sparta_3733b346bd(A);B[_B]=-1;C=qube_dc67a122c8.sparta_2bfdf5ff2a(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_4e6cd7e08e(request,kernel_manager_uuid):
	E=kernel_manager_uuid;D=True;B=request;F=False
	if E is None:F=D
	else:
		G=qube_1a6dfd0324.sparta_a0d8a851f2(B.user,E)
		if G is None:F=D
	if F:return sparta_a4cd1ff3de(B)
	def I(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=D)
	H=sparta_d6506bed7a()
	if H==_A:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\kernel"
	elif H=='linux':C=os.path.expanduser('~/SpartaQube/kernel')
	elif H=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\kernel')
	I(C);J=os.path.join(C,E);I(J);K=os.path.join(J,'main.ipynb')
	if not os.path.exists(K):
		L=qube_52cd691e01.sparta_ef98ed7c98()
		with open(K,'w')as M:M.write(json.dumps(L))
	A=qube_dc67a122c8.sparta_3733b346bd(B);A['default_project_path']=C;A[_B]=-1;N=qube_dc67a122c8.sparta_2bfdf5ff2a(B.user);A.update(N);A['kernel_name']=G.name;A['kernelManagerUUID']=G.kernel_manager_uuid;A['bCodeMirror']=D;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)