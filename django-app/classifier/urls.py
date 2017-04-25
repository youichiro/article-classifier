from django.conf.urls import url
from . import views

app_name = 'classifier'
urlpatterns = [
    url(r'^$', views.form, name='form'),
]
