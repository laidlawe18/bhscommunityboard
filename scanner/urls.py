from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^checkin$', views.checkin, name="checkin"),
    url(r'^scan/([0-9]{2,6})$', views.scan, name="scan"),
    url(r'^checkout/([0-9]{2,6})/([0-9]{5})$', views.checkout, name="checkout"),
    url(r'^schedule$', views.schedule, name="schedule"),
    url(r'^schedule/([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})/([A-Z])$', views.schedule_period, name="schedule period"),
    url(r'^schedule/class/([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})/([A-Z])$', views.schedule_period_class, name="schedule period class"),
    url(r'^admin$', views.admin, name="admin"),
    url(r'^admin/login$', views.admin_login, name="admin login"),
    url(r'^admin/editinfo$', views.admin_edit_info, name="admin edit info"),
    url(r'^admin/addleadership$', views.admin_add_leadership, name="admin add leadership"),
    url(r'^admin/changepermissions$', views.admin_change_permissions, name="admin change permissions"),
    url(r'^admin/changepermissions/([0-9]{2,4})$', views.admin_change_user_permissions, name="admin change user permissions"),
]