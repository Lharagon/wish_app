from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main, name = 'login'),
    url(r'^dashboard$', views.dashboard, name = 'home'),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^log_out$', views.log_out, name = "log_out"),
    url(r'^add_page$', views.add_page, name = "add_page"),
    url(r'^add_product/(?P<id>\d+)$', views.add_product, name = "add_product"),
    url(r'^wish_items/(?P<id>\d+)$', views.item_profile, name = "item_profile"),
    url(r'^delete/(?P<id>\d+)$', views.delete, name = "delete_item"),
    url(r'^add_wish/(?P<id>\d+)$', views.add_wish, name = "add_wish"),
    url(r'^remove_wish/(?P<id>\d+)$', views.remove_wish, name = "remove_wish")
]