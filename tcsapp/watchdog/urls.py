from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views



views.clear_stores()
views.clear_invoices()
views.clear_checks()
views.refresh_codes()
views.testStuff()

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
     url(r'^$', views.dashboard, name='dashboard'),
     url(r'^watcher/$', views.watcher, name='watcher'),
     url(r'^info/$', views.info, name='info'),
     url(r'^phone/$', views.yealink, name='phone'),
     url(r'^info/table_info/$', views.table_info, name='ajax_url'),
     url(r'^info/update/$', views.update, name='update'),
 ]
