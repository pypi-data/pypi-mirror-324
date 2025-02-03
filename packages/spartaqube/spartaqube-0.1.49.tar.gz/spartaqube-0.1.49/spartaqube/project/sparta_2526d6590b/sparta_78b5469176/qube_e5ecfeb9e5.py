from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_8197dd6d72
from project.sparta_1d1c5d5897.sparta_4ba64018ff import qube_522a884fea as qube_522a884fea
from project.models import UserProfile
import project.sparta_75433bcd57.sparta_e9edb68cbd.qube_dc67a122c8 as qube_dc67a122c8
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_1de6c5f544(request):
	E='avatarImg';B=request;A=qube_dc67a122c8.sparta_3733b346bd(B);A['menuBar']=-1;F=qube_dc67a122c8.sparta_2bfdf5ff2a(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_8197dd6d72
@login_required(redirect_field_name='login')
def sparta_aace6026c1(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_1de6c5f544(A)