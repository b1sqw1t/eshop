from django.urls                import re_path
from account                    import views
from django.urls                import reverse_lazy
from django.contrib.auth.views  import login,logout,PasswordChangeView,PasswordChangeDoneView,\
                                        PasswordResetView,PasswordResetDoneView,\
                                        PasswordResetConfirmView,PasswordResetCompleteView


app_name = 'account'

urlpatterns = [
    re_path('^test',                        views.post_share,                   name='post_share'),
    re_path('^reg',                        views.Reg.as_view(),                   name='reg'),
    re_path('^index/',                      views.test,                         name='test'),
    re_path('^profile/(?P<id>[0-9]+)/$',    views.view_profile,                 name='view_profile'),
    re_path('^profile/edit/$',              views.edit,                         name='edit_profile'),
    re_path('^profile/$',                   views.my_account,                   name='my_account'),
    re_path('^login/$',                     login,                              name='login'),
    re_path('^logout/$',                    logout, {'next_page' : reverse_lazy('index:home_page')},                            name='logout'),
    re_path('^create_account/$',            views.register,                     name='registration'),
    re_path('^history/$',                   views.view_history,                 name='view_history'),

    re_path('^password-reset/$',      PasswordResetView.as_view(
                                    success_url=reverse_lazy('account:password_reset_done'),
                                    template_name='registration/password_reset_form.html',
                                    email_template_name='registration/password_reset_email.html',
                                    html_email_template_name='registration/password_reset_email.html',
                                    from_email = 'bisqwit@yandex.ru'),
                                    name='password_reset'),

    re_path('^password-reset/done/$', PasswordResetDoneView.as_view(
                                    template_name='registration/password_reset_done.html'),
                                    name='password_reset_done'),

    re_path('^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
                    PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',
                                                     success_url=reverse_lazy('account:password_reset_complete')),
                                    name='password_reset_confirm'),

    re_path('^password-reset/complete/$',   PasswordResetCompleteView.as_view(
                                    template_name='registration/password_reset_complete.html'),
                                    name='password_reset_complete'),

    re_path('^password-change/$', PasswordChangeView.as_view(
                                    success_url=reverse_lazy('account:password_change_done')),
                                    name='password_change'),
    re_path('^password-change/done/$', PasswordChangeDoneView.as_view(), name='password_change_done'),

]