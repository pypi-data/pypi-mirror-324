_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_1d1c5d5897.sparta_a34306fc83 import qube_2729450391 as qube_2729450391
from project.sparta_1d1c5d5897.sparta_4ba64018ff import qube_522a884fea as qube_522a884fea
from project.sparta_1d1c5d5897.sparta_27dd4d9e88.qube_4fa258c701 import sparta_2975e084e6
@csrf_exempt
@sparta_2975e084e6
def sparta_5c6e8e38f9(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_522a884fea.sparta_ea2bc41c99(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_2729450391.sparta_5c6e8e38f9(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_2975e084e6
def sparta_e31c4136a9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2729450391.sparta_ce396f8966(C,A.user);E=json.dumps(D);return HttpResponse(E)