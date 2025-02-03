_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_1d1c5d5897.sparta_ba7818ee7d import qube_15a94b80fc as qube_15a94b80fc
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_2975e084e6
@csrf_exempt
@sparta_2975e084e6
def sparta_7b3b21a38b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_15a94b80fc.sparta_7b3b21a38b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_81c2ce73ff(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_15a94b80fc.sparta_81c2ce73ff(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_2975e084e6
def sparta_bfa2b1f257(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_15a94b80fc.sparta_bfa2b1f257(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_2975e084e6
def sparta_d93f5d541f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_15a94b80fc.sparta_d93f5d541f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_3574e6b3b6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_15a94b80fc.sparta_3574e6b3b6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2975e084e6
def sparta_251933b404(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_15a94b80fc.sparta_251933b404(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_e8fbb23451(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_15a94b80fc.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_2975e084e6
def sparta_cca4fe73e7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_15a94b80fc.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_ffa9d4d51e(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_15a94b80fc.sparta_ffa9d4d51e(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_0ae2e56eeb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_15a94b80fc.sparta_0ae2e56eeb(A,C);E=json.dumps(D);return HttpResponse(E)