from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
       path('admin/',           admin.site.urls),
    re_path('^cart/',           include('cart.urls',            namespace='cart')),
    re_path('^account/',        include('account.urls',         namespace='account')),
    re_path('^orders/',         include('orders.urls',          namespace='orders')),
    re_path('^comments/',       include('comments.urls',        namespace='comments')),
    re_path('',                 include('index.urls',           namespace='index')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
 + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)