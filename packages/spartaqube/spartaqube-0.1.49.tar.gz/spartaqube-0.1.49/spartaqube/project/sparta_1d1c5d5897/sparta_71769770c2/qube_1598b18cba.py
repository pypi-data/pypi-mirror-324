_T='projectPath'
_S='unpicklable'
_R='kernelSize'
_Q='kernelVenv'
_P='kernel_size'
_O='main_ipynb_fullpath'
_N='kernel_manager_uuid'
_M='main.ipynb'
_L='-kernel__last_update'
_K='windows'
_J='luminoLayout'
_I='description'
_H='slug'
_G='is_static_variables'
_F=False
_E='name'
_D='kernelManagerUUID'
_C='res'
_B=True
_A=None
import os,sys,gc,json,base64,shutil,zipfile,io,uuid,subprocess,cloudpickle,platform,getpass
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
from dateutil import parser
import pytz
UTC=pytz.utc
from django.contrib.humanize.templatetags.humanize import naturalday
from project.sparta_1d1c5d5897.sparta_ed520409dc import qube_b79a99bc7e as qube_b79a99bc7e
from project.models_spartaqube import Kernel,KernelShared,ShareRights
from project.sparta_1d1c5d5897.sparta_9e2dd8c569.qube_e41a999d1e import IPythonKernel as IPythonKernel
from project.sparta_1d1c5d5897.sparta_e0f10cf586.qube_97c853e9c9 import sparta_d4809fae31,sparta_9fbb5384da
from project.sparta_1d1c5d5897.sparta_f2e5918cc6.qube_56e2b853b1 import sparta_3e964c37c3,sparta_4841534c3e,sparta_9965f613d0,sparta_3dbc449912
from project.sparta_1d1c5d5897.sparta_e0f10cf586.qube_fe2fd2db77 import sparta_d6097e5baf,sparta_37eab207ca
from project.sparta_1d1c5d5897.sparta_3863939d0b.qube_06437133ee import sparta_d5431c9725
def sparta_d6506bed7a():
	A=platform.system()
	if A=='Windows':return _K
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
def sparta_4432ad3ae5():
	A=sparta_d6506bed7a()
	if A==_K:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\kernel"
	elif A=='linux':B=os.path.expanduser('~/SpartaQube/kernel')
	elif A=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\kernel')
	return B
def sparta_fecce12a4b(user_obj):
	A=qube_b79a99bc7e.sparta_ffa29a5b8d(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_2bc546cd20(user_obj,kernel_manager_uuid):from project.sparta_1d1c5d5897.sparta_fad3ec945b import qube_1a6dfd0324 as A;B=A.sparta_f9652966ca(user_obj,kernel_manager_uuid);C,D=B.cloudpickle_kernel_variables();return cloudpickle.dumps(C),D
def sparta_01ec8525e0(user_obj):
	I='%Y-%m-%d';C=user_obj;J=sparta_4432ad3ae5();D=sparta_fecce12a4b(C)
	if len(D)>0:B=KernelShared.objects.filter(Q(is_delete=0,user_group__in=D,kernel__is_delete=0)|Q(is_delete=0,user=C,kernel__is_delete=0))
	else:B=KernelShared.objects.filter(Q(is_delete=0,user=C,kernel__is_delete=0))
	if B.count()>0:B=B.order_by(_L)
	E=[]
	for F in B:
		A=F.kernel;K=F.share_rights;G=_A
		try:G=str(A.last_update.strftime(I))
		except:pass
		H=_A
		try:H=str(A.date_created.strftime(I))
		except Exception as L:print(L)
		M=os.path.join(J,A.kernel_manager_uuid,_M);E.append({_N:A.kernel_manager_uuid,_E:A.name,_H:A.slug,_I:A.description,_O:M,_P:A.kernel_size,'has_write_rights':K.has_write_rights,'last_update':G,'date_created':H})
	return E
def sparta_76443591f4(user_obj):
	B=user_obj;C=sparta_fecce12a4b(B)
	if len(C)>0:A=KernelShared.objects.filter(Q(is_delete=0,user_group__in=C,kernel__is_delete=0)|Q(is_delete=0,user=B,kernel__is_delete=0))
	else:A=KernelShared.objects.filter(Q(is_delete=0,user=B,kernel__is_delete=0))
	if A.count()>0:A=A.order_by(_L);return[A.kernel.kernel_manager_uuid for A in A]
	return[]
def sparta_dc7829e86b(user_obj,kernel_manager_uuid):
	B=user_obj;D=Kernel.objects.filter(kernel_manager_uuid=kernel_manager_uuid).all()
	if D.count()>0:
		A=D[0];E=sparta_fecce12a4b(B)
		if len(E)>0:C=KernelShared.objects.filter(Q(is_delete=0,user_group__in=E,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=B,kernel__is_delete=0,kernel=A))
		else:C=KernelShared.objects.filter(is_delete=0,user=B,kernel__is_delete=0,kernel=A)
		F=_F
		if C.count()>0:
			H=C[0];G=H.share_rights
			if G.is_admin or G.has_write_rights:F=_B
		if F:return A
def sparta_331ca278b5(json_data,user_obj):
	D=user_obj;from project.sparta_1d1c5d5897.sparta_fad3ec945b import qube_1a6dfd0324 as I;A=json_data[_D];B=I.sparta_a0d8a851f2(D,A)
	if B is _A:return{_C:-1,'errorMsg':'Kernel not found'}
	E=sparta_4432ad3ae5();J=os.path.join(E,A,_M);K=B.venv_name;F=_A;G=_F;H=_F;C=sparta_dc7829e86b(D,A)
	if C is not _A:G=_B;F=C.lumino_layout;H=C.is_static_variables
	return{_C:1,'kernel':{'basic':{'is_kernel_saved':G,_G:H,_N:A,_E:B.name,'kernel_venv':K,'kernel_type':B.type,'project_path':E,_O:J},'lumino':{'lumino_layout':F}}}
def sparta_aea3b579d5(json_data,user_obj):
	D=user_obj;A=json_data;print('Save notebook');print(A);print(A.keys());L=A['isKernelSaved']
	if L:return sparta_173c2afd7b(A,D)
	C=datetime.now().astimezone(UTC);F=A[_D];M=A[_J];N=A[_E];O=A[_I];E=sparta_4432ad3ae5();E=sparta_d4809fae31(E);G=A[_G];P=A.get(_Q,_A);Q=A.get(_R,0);B=A.get(_H,'')
	if len(B)==0:B=A[_E]
	H=slugify(B);B=H;I=1
	while Kernel.objects.filter(slug=B).exists():B=f"{H}-{I}";I+=1
	J=_A
	if G:J,K=sparta_2bc546cd20(D,F)
	R=Kernel.objects.create(kernel_manager_uuid=F,name=N,slug=B,description=O,is_static_variables=G,lumino_layout=M,project_path=E,kernel_venv=P,kernel_variables=J,kernel_size=Q,date_created=C,last_update=C,last_date_used=C,spartaqube_version=sparta_d5431c9725());S=ShareRights.objects.create(is_admin=_B,has_write_rights=_B,has_reshare_rights=_B,last_update=C);KernelShared.objects.create(kernel=R,user=D,share_rights=S,is_owner=_B,date_created=C);print('kernel_cpkl_unpicklable');print(K);return{_C:1,_S:K}
def sparta_173c2afd7b(json_data,user_obj):
	F=user_obj;A=json_data;print('update_kernel_notebook');print(A);D=A[_D];B=sparta_dc7829e86b(F,D)
	if B is not _A:
		J=datetime.now().astimezone(UTC);D=A[_D];K=A[_J];L=A[_E];M=A[_I];E=A[_G];N=A.get(_Q,_A);O=A.get(_R,0);C=A.get(_H,'')
		if len(C)==0:C=A[_E]
		G=slugify(C);C=G;H=1
		while Kernel.objects.filter(slug=C).exists():C=f"{G}-{H}";H+=1
		E=A[_G];I=_A
		if E:I,P=sparta_2bc546cd20(F,D)
		B.name=L;B.description=M;B.slug=C;B.kernel_venv=N;B.kernel_size=O;B.is_static_variables=E;B.kernel_variables=I;B.lumino_layout=K;B.last_update=J;B.save()
	return{_C:1,_S:P}
def sparta_8385218895(json_data,user_obj):0
def sparta_67d3b62b09(json_data,user_obj):A=sparta_d4809fae31(json_data[_T]);return sparta_d6097e5baf(A)
def sparta_686470f6b7(json_data,user_obj):A=sparta_d4809fae31(json_data[_T]);return sparta_37eab207ca(A)
def sparta_93dd0d6156(json_data,user_obj):
	C=user_obj;B=json_data;print('SAVE LYUMINO LAYOUT KERNEL NOTEBOOK');print('json_data');print(B);I=B[_D];E=Kernel.objects.filter(kernel_manager_uuid=I).all()
	if E.count()>0:
		A=E[0];F=sparta_fecce12a4b(C)
		if len(F)>0:D=KernelShared.objects.filter(Q(is_delete=0,user_group__in=F,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=C,kernel__is_delete=0,kernel=A))
		else:D=KernelShared.objects.filter(is_delete=0,user=C,kernel__is_delete=0,kernel=A)
		G=_F
		if D.count()>0:
			J=D[0];H=J.share_rights
			if H.is_admin or H.has_write_rights:G=_B
		if G:K=B[_J];A.lumino_layout=K;A.save()
	return{_C:1}
def sparta_8ea82bd4e1(json_data,user_obj):
	from project.sparta_1d1c5d5897.sparta_fad3ec945b import qube_1a6dfd0324 as A;C=json_data[_D];B=A.sparta_a0d8a851f2(user_obj,C)
	if B is not _A:D=A.sparta_c883dcbeee(B);return{_C:1,_P:D}
	return{_C:-1}
def sparta_71e2dddc1a(json_data,user_obj):
	B=json_data[_D];A=sparta_dc7829e86b(user_obj,B)
	if A is not _A:A.is_delete=_B;A.save()
	return{_C:1}