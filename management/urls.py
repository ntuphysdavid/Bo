from django.conf.urls import url
from management import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^add_inventory/$', views.add_inventory, name='add_inventory'),
    url(r'^add_img/$', views.add_img, name='add_img'),
    url(r'^view_inventory_list/$', views.view_inventory_list, name='view_inventory_list'),
    url(r'^view_inventory/detail/$', views.detail, name='detail'),
    url(r'^view_FA_list/$', views.view_FA_list, name='view_FA_list'),
]
