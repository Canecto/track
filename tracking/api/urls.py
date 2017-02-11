from django.conf.urls import url
#from django.contrib import admin

from .views import save_data

urlpatterns = [
    url(r'^$', save_data, name="save_data"),
]
