_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_1d1c5d5897.sparta_27dd4d9e88 import qube_4fa258c701 as qube_4fa258c701
from project.sparta_75433bcd57.sparta_e9edb68cbd.qube_dc67a122c8 import sparta_d5b054f52a
@csrf_exempt
def sparta_192e637a81(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_4fa258c701.sparta_192e637a81(B)
@csrf_exempt
def sparta_5c53ff5fc3(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_8d091f253d(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_99e825ebd5(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)