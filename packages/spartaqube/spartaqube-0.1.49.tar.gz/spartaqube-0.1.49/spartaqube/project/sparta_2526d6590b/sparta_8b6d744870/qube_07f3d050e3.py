_M='bPublicUser'
_L='developer_name'
_K='developer_id'
_J='b_require_password'
_I='developer_obj'
_H='windows'
_G='default_project_path'
_F='bCodeMirror'
_E='menuBar'
_D='dist/project/homepage/homepage.html'
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
from django.conf import settings as conf_settings
import project.sparta_75433bcd57.sparta_e9edb68cbd.qube_dc67a122c8 as qube_dc67a122c8
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_8197dd6d72
from project.sparta_1d1c5d5897.sparta_e3abbda9fb import qube_aea23cbe5a as qube_aea23cbe5a
def sparta_d6506bed7a():
	A=platform.system()
	if A=='Windows':return _H
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_bb9e206a97(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_dc67a122c8.sparta_3733b346bd(B);return render(B,_D,A)
	qube_aea23cbe5a.sparta_6917be7256();A=qube_dc67a122c8.sparta_3733b346bd(B);A[_E]=12;E=qube_dc67a122c8.sparta_2bfdf5ff2a(B.user);A.update(E);A[_F]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_d6506bed7a()
	if D==_H:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\developer"
	elif D=='linux':C=os.path.expanduser('~/SpartaQube/developer')
	elif D=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\developer')
	F(C);A[_G]=C;print(f"default_project_path {C}");return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_43cd7457f9(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_dc67a122c8.sparta_3733b346bd(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_aea23cbe5a.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_bb9e206a97(B)
	A=qube_dc67a122c8.sparta_3733b346bd(B);A[_E]=12;H=qube_dc67a122c8.sparta_2bfdf5ff2a(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_3142bf6513(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_dc67a122c8.sparta_3733b346bd(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_aea23cbe5a.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_bb9e206a97(B)
	A=qube_dc67a122c8.sparta_3733b346bd(B);A[_E]=12;H=qube_dc67a122c8.sparta_2bfdf5ff2a(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_ea8fd6bd39(request,project_path,file_name):C=file_name;B=request;A=project_path;print('request DEBUG');print(B);A=unquote(A);print(f"Serve {C} on project_path {A}");return serve(B,C,document_root=A)