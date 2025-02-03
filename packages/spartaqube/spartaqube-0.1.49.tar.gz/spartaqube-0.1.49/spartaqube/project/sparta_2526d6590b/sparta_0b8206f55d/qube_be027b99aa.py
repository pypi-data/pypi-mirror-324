from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_75433bcd57.sparta_e9edb68cbd.qube_dc67a122c8 as qube_dc67a122c8
from project.models import UserProfile
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_8197dd6d72
from project.sparta_2526d6590b.sparta_7a80b30776.qube_99bf83bd2d import sparta_52a96e441e
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_10d328a38a(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_dc67a122c8.sparta_3733b346bd(B);A.update(qube_dc67a122c8.sparta_2bfdf5ff2a(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_52a96e441e());return render(B,'dist/project/auth/settings.html',A)