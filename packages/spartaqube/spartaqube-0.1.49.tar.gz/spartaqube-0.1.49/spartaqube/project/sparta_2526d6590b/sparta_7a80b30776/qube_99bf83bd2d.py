_O='Please send valid data'
_N='dist/project/auth/resetPasswordChange.html'
_M='captcha'
_L='password'
_K='POST'
_J=False
_I='login'
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_75433bcd57.sparta_e9edb68cbd.qube_dc67a122c8 as qube_dc67a122c8
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_8197dd6d72
from project.sparta_1d1c5d5897.sparta_27dd4d9e88 import qube_4fa258c701 as qube_4fa258c701
from project.sparta_38a6a901a0.sparta_6f5a43f416 import qube_3540f991ef as qube_3540f991ef
from project.models import LoginLocation,UserProfile
def sparta_52a96e441e():return{'bHasCompanyEE':-1}
def sparta_ecaf75889d(request):B=request;A=qube_dc67a122c8.sparta_3733b346bd(B);A[_C]=qube_dc67a122c8.sparta_60d871905d();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_8197dd6d72
def sparta_dd91e0c66b(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_577df96ce4(C,A)
def sparta_cfda83322e(request,redirectUrl):return sparta_577df96ce4(request,redirectUrl)
def sparta_577df96ce4(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_4fa258c701.sparta_1e85c8122d(F):return sparta_ecaf75889d(A)
				login(A,F);K,L=qube_dc67a122c8.sparta_cac4d204b5();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_dc67a122c8.sparta_3733b346bd(A);B.update(qube_dc67a122c8.sparta_b6371ac09f(A));B[_C]=qube_dc67a122c8.sparta_60d871905d();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_52a96e441e());return render(A,'dist/project/auth/login.html',B)
def sparta_6a627bea4a(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_8197dd6d72
def sparta_cbdd01355e(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_4fa258c701.sparta_821d08cde7()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_4fa258c701.sparta_06a2bd1dbe(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_4fa258c701.sparta_192e637a81(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_dc67a122c8.sparta_3733b346bd(A);C.update(qube_dc67a122c8.sparta_b6371ac09f(A));C[_C]=qube_dc67a122c8.sparta_60d871905d();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_52a96e441e());return render(A,'dist/project/auth/registration.html',C)
def sparta_c1781d1d6c(request):A=request;B=qube_dc67a122c8.sparta_3733b346bd(A);B[_C]=qube_dc67a122c8.sparta_60d871905d();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_8c6a1571db(request,token):
	A=request;B=qube_4fa258c701.sparta_dcc41e44ec(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_dc67a122c8.sparta_3733b346bd(A);D[_C]=qube_dc67a122c8.sparta_60d871905d();return redirect(_I)
def sparta_32e06644a8(request):logout(request);return redirect(_I)
def sparta_3144e1e2d4(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_ff773b7e78(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_c7ce2fe034(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_4fa258c701.sparta_c7ce2fe034(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_dc67a122c8.sparta_3733b346bd(A);C.update(qube_dc67a122c8.sparta_b6371ac09f(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_dc67a122c8.sparta_60d871905d();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_dc67a122c8.sparta_3733b346bd(A);D.update(qube_dc67a122c8.sparta_b6371ac09f(A));D[_C]=qube_dc67a122c8.sparta_60d871905d();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_52a96e441e());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_a4652fbf7f(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_4fa258c701.sparta_a4652fbf7f(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_dc67a122c8.sparta_3733b346bd(D);A.update(qube_dc67a122c8.sparta_b6371ac09f(D));A[_C]=qube_dc67a122c8.sparta_60d871905d();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_52a96e441e());return render(D,_N,A)