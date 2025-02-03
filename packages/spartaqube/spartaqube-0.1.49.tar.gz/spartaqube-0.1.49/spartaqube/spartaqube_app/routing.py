import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_75433bcd57.sparta_f61b1e2701 import qube_e8587ffb2b,qube_55b55f67de,qube_5f86b9cadd,qube_3589f273ab,qube_c6b08cde8e,qube_616705c33e,qube_2ad3c68a12,qube_0cb74db6ca,qube_664cbe3b79
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
print('CHANNELS VERSION')
print(channels_ver)
def sparta_ba808c2107(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_ba808c2107(qube_e8587ffb2b.StatusWS)),url('ws/notebookWS',sparta_ba808c2107(qube_55b55f67de.NotebookWS)),url('ws/wssConnectorWS',sparta_ba808c2107(qube_5f86b9cadd.WssConnectorWS)),url('ws/pipInstallWS',sparta_ba808c2107(qube_3589f273ab.PipInstallWS)),url('ws/gitNotebookWS',sparta_ba808c2107(qube_c6b08cde8e.GitNotebookWS)),url('ws/xtermGitWS',sparta_ba808c2107(qube_616705c33e.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_ba808c2107(qube_2ad3c68a12.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_ba808c2107(qube_0cb74db6ca.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_ba808c2107(qube_664cbe3b79.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)