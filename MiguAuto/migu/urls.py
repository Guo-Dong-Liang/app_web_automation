from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login$', views.login, name='login'),
    url(r'^home$', views.login_post),
    url(r'^logout$', views.logout),
    url(r'^youxi/(?P<tasktype>[0-9]+)', views.youxi),
    url(r'^download', views.download),
    url(r'^(?P<taskid>[0-9]+)/run', views.app_run),
    url(r'^(?P<taskid>[0-9]+)/record', views.youxi_record),
]
# urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)