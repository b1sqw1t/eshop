from django.urls import path,re_path,include
from index import views

app_name='index'
urlpatterns = [
    re_path('^test/$',                              views.test,                      name='test'),
    re_path('^search/',                            views.search.as_view(),          name='search'),
    re_path('^test/check$',                         views.check,                     name='check'),
    re_path('^category/(?:(?P<type>[-\w]+)/)?$',    views.category_view.as_view(),   name='category_view'),
    re_path('^(?P<model>[-\w]+)/$',                 views.product_view.as_view(),    name='product_view'),
    re_path('^(?P<model>[-\w]+)/like/$',            views.product_like,              name='product_like'),
    re_path('^(?P<model>[-\w]+)/dislike/$',         views.product_dislike,           name='product_dislike'),
    re_path('^$',                                   views.home_page.as_view(),       name='home_page'),
]