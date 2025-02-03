_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_1d1c5d5897.sparta_ee6412fa89 import qube_f55a4eac1e as qube_f55a4eac1e
from project.sparta_1d1c5d5897.sparta_ee6412fa89 import qube_f88c176225 as qube_f88c176225
from project.sparta_1d1c5d5897.sparta_7ac67607ea import qube_f56d10f0cf as qube_f56d10f0cf
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_2975e084e6,sparta_51069271d4
@csrf_exempt
def sparta_85b415e7d4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_85b415e7d4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_d2d6c3f4a6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_d2d6c3f4a6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_23b8fab6c1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_23b8fab6c1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_6d5940bda6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_6d5940bda6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_5f9c683a77(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_5f9c683a77(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_f53b032321(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_f53b032321(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_f1a9b738d6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_f1a9b738d6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_b5f587d122(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_b5f587d122(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_7e9b5a0440(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_7e9b5a0440(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_29f3ef4d25(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.sparta_29f3ef4d25(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_3a783773a4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f55a4eac1e.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_d6fdc04245(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_f55a4eac1e.sparta_d6fdc04245(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_43b64383e9(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_6a72537440(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_2975e084e6
def sparta_90081509d4(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_6a72537440(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_f55a4eac1e.sparta_9aef548623(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_2975e084e6
def sparta_0a545a4436(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_f55a4eac1e.sparta_2f8df244ff(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_9b010516b1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_9b010516b1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_e838aff462(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_e838aff462(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_2f7beded0f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_2f7beded0f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_2c888ade5c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_2c888ade5c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_45b25d7dcf(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_45b25d7dcf(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_d3d59c449c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_d3d59c449c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_8abe456522(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_8abe456522(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_f1ab03db29(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_f1ab03db29(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_cd98fa75b1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_cd98fa75b1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_e665265714(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_e665265714(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_11867367a9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_11867367a9(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_e0e77fd383(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_e0e77fd383(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_76a7e46498(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_76a7e46498(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
@sparta_51069271d4
def sparta_3e20a3b0a1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f88c176225.sparta_3e20a3b0a1(C,A.user);E=json.dumps(D);return HttpResponse(E)