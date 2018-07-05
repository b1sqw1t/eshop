from django.urls import path,re_path,include
from django.conf.urls.static import static
from comments import views

app_name = 'comments'

urlpatterns = [
    re_path('^add/$',                     views.add_comment,        name='add_comment'),
    re_path('^del/(?P<id>[0-9]+)/$',      views.del_comment,        name='delete_comment'),
]


