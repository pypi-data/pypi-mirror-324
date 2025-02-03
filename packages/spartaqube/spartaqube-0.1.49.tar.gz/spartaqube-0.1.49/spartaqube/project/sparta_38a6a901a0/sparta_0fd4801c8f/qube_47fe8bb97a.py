_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='Content-Disposition'
_C='res'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_1d1c5d5897.sparta_090c10c15f import qube_625df6a9df as qube_625df6a9df
from project.sparta_1d1c5d5897.sparta_090c10c15f import qube_a520d48e30 as qube_a520d48e30
from project.sparta_1d1c5d5897.sparta_e0f10cf586 import qube_97c853e9c9 as qube_97c853e9c9
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_2975e084e6
@csrf_exempt
@sparta_2975e084e6
def sparta_26e9798a6e(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_625df6a9df.sparta_e5c680008f(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_2975e084e6
def sparta_4617a3f802(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_625df6a9df.sparta_47a914be50(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_dc24c58ac7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_625df6a9df.sparta_35f48a8d54(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_f50227d9a0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_625df6a9df.sparta_fad30687b1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_261ebe56d4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a520d48e30.sparta_5cfd06473f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_0bef16ea15(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_625df6a9df.sparta_45ffc9eade(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_cfd23e1f15(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_625df6a9df.sparta_a7f9f48ab4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_1e516b27b7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_625df6a9df.sparta_5c352ddca7(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_f14775e1d0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_625df6a9df.sparta_d6ee7d922d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_6d927e438e(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_625df6a9df.sparta_9aef548623(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_2975e084e6
def sparta_bcbee40d05(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_625df6a9df.sparta_e17da1217d(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_2975e084e6
def sparta_25cb5edc4e(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_625df6a9df.sparta_2f8df244ff(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A