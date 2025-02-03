_L='bPublicUser'
_K='notebook_name'
_J='notebook_id'
_I='b_require_password'
_H='notebook_obj'
_G='windows'
_F='default_project_path'
_E='bCodeMirror'
_D='menuBar'
_C='res'
_B=None
_A=True
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
from project.sparta_1d1c5d5897.sparta_1adcf7c763 import qube_bf9ee34003 as qube_bf9ee34003
def sparta_d6506bed7a():
	A=platform.system()
	if A=='Windows':return _G
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_e1866b8e60(request):
	C=request;A=qube_dc67a122c8.sparta_3733b346bd(C);A[_D]=13;E=qube_dc67a122c8.sparta_2bfdf5ff2a(C.user);A.update(E);A[_E]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_d6506bed7a()
	if D==_G:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\notebook"
	elif D=='linux':B=os.path.expanduser('~/SpartaQube/notebook')
	elif D=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\notebook')
	F(B);A[_F]=B;print(f"default_project_path {B}");return render(C,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_de301bd525(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_bf9ee34003.sparta_099fc5f6a6(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_e1866b8e60(B)
	A=qube_dc67a122c8.sparta_3733b346bd(B);A[_D]=12;H=qube_dc67a122c8.sparta_2bfdf5ff2a(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_f07a954a83(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_bf9ee34003.sparta_099fc5f6a6(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_e1866b8e60(B)
	A=qube_dc67a122c8.sparta_3733b346bd(B);A[_D]=12;H=qube_dc67a122c8.sparta_2bfdf5ff2a(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)