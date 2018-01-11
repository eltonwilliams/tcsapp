from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views



# views.clear_stores()
# views.clear_invoices()
# views.refresh_codes()
views.testStuff()

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
     url(r'^$', views.watcher, name='watcher'),
     url(r'^info/$', views.info, name='info'),
     url(r'^phone/$', views.yealink, name='phone'),
     url(r'^info/table_info/$', views.table_info, name='ajax_url'),
 ]
