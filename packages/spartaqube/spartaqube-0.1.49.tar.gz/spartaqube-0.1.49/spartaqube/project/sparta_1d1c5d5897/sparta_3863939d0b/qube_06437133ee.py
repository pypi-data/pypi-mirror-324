import re,os,json,requests
from datetime import datetime
from packaging.version import parse
from project.models import AppVersioning
import pytz
UTC=pytz.utc
def sparta_7827691053():0
def sparta_15c00ba6c9():A='name';B='https://api.github.com/repos/SpartaQube/spartaqube-version/tags';C=requests.get(B);D=json.loads(C.text);E=max(D,key=lambda t:parse(t[A]));return E[A]
def sparta_b94a75051a():
	try:A='https://pypi.org/project/spartaqube/';B=requests.get(A).text;C=re.search('<h1 class="package-header__name">(.*?)</h1>',B,re.DOTALL);D=C.group(1);E=D.strip().split('spartaqube ')[1];return E
	except:pass
def sparta_d5431c9725():
	B=os.path.dirname(__file__);C=os.path.dirname(B);D=os.path.dirname(C);E=os.path.dirname(D)
	try:
		with open(os.path.join(E,'app_version.json'),'r')as F:G=json.load(F);A=G['version']
	except:A='0.1.1'
	return A
def sparta_8156e56c23():
	G='res'
	try:
		C=sparta_d5431c9725();A=sparta_15c00ba6c9();D=AppVersioning.objects.all();E=datetime.now().astimezone(UTC)
		if D.count()==0:AppVersioning.objects.create(last_available_version_pip=A,last_check_date=E)
		else:B=D[0];B.last_available_version_pip=A;B.last_check_date=E;B.save()
		return{'current_version':C,'latest_version':A,'b_update':not C==A,'humanDate':'A moment ago',G:1}
	except Exception as F:print('Exception versioning update');print(F);return{G:-1,'errorMsg':str(F)}