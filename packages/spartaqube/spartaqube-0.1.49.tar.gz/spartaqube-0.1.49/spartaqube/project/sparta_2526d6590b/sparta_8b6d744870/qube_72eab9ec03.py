import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_75433bcd57.sparta_e9edb68cbd.qube_dc67a122c8 as qube_dc67a122c8
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_8197dd6d72
from project.sparta_1d1c5d5897.sparta_6f8ac4359a import qube_2d7d6b2b69 as qube_2d7d6b2b69
from project.sparta_1d1c5d5897.sparta_7ac67607ea import qube_f56d10f0cf as qube_f56d10f0cf
def sparta_d6506bed7a():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_158ba4ffdb(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_dc67a122c8.sparta_3733b346bd(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_dc67a122c8.sparta_3733b346bd(B);A['menuBar']=12;F=qube_dc67a122c8.sparta_2bfdf5ff2a(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)