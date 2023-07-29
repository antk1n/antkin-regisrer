from django.urls import re_path
from OsauhingAPP import views


urlpatterns = [
    re_path(r'^isik$', views.IsikAPI),
    re_path(r'^isik/([0-9]+)$', views.IsikAPI),
    re_path(r'^otsing/', views.OtsingAPI),
    re_path(r'^create$', views.createAPI),
    re_path(r'^edit$', views.muudaAPI),
]