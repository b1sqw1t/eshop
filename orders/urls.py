from django.urls import re_path
from . import views

app_name='orders'

urlpatterns = [
    re_path('^create/$',        views.order_create,                 name='order_create'),

]