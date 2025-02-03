from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_2526d6590b.sparta_2e69be99ce.qube_26deccdf12.sparta_8b1a05ed03'
handler500='project.sparta_2526d6590b.sparta_2e69be99ce.qube_26deccdf12.sparta_57d2f9273b'
handler403='project.sparta_2526d6590b.sparta_2e69be99ce.qube_26deccdf12.sparta_14b6b15f81'
handler400='project.sparta_2526d6590b.sparta_2e69be99ce.qube_26deccdf12.sparta_67b9fbfcca'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]