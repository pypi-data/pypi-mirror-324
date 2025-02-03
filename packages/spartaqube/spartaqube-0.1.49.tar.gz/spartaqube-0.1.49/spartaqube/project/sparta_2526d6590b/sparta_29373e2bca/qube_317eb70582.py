_D='bCodeMirror'
_C='menuBar'
_B='windows'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_75433bcd57.sparta_e9edb68cbd.qube_dc67a122c8 as qube_dc67a122c8
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_8197dd6d72
from project.sparta_1d1c5d5897.sparta_6f8ac4359a import qube_2d7d6b2b69 as qube_2d7d6b2b69
from project.sparta_1d1c5d5897.sparta_7ac67607ea import qube_f56d10f0cf as qube_f56d10f0cf
def sparta_d6506bed7a():
	A=platform.system()
	if A=='Windows':return _B
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_52962c5a91(request):
	C=request;D=C.GET.get('edit')
	if D is None:D='-1'
	A=qube_dc67a122c8.sparta_3733b346bd(C);A[_C]=9;F=qube_dc67a122c8.sparta_2bfdf5ff2a(C.user);A.update(F);A[_D]=_A;A['edit_chart_id']=D
	def G(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	E=sparta_d6506bed7a()
	if E==_B:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\dashboard"
	elif E=='linux':B=os.path.expanduser('~/SpartaQube/dashboard')
	elif E=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\dashboard')
	G(B);A['default_project_path']=B;print(f"default_project_path {B}");return render(C,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_fd058a98bb(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_8ff771ea52(A,B)
def sparta_8ff771ea52(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_f56d10f0cf.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_52962c5a91(B)
	A=qube_dc67a122c8.sparta_3733b346bd(B);A[_C]=9;I=qube_dc67a122c8.sparta_2bfdf5ff2a(B.user);A.update(I);A[_D]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)