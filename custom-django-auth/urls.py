from django.conf.urls import patterns, include, url
from django.contrib import admin
from profiles.views import AccountRegistration, ProfileView, SearchView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ProfileView.as_view(), name='root_page'),
    url(r'^profile/$', ProfileView.as_view(), name='profile_page'),
    url(r'^search/$', SearchView.as_view()),
    
    #registration
    (r'^register/$', AccountRegistration.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'profiles/login.haml'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'profiles/password_reset_form.haml'}),    
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'profiles/password_reset_complete.haml'}),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            'django.contrib.auth.views.password_reset_confirm',
            {'template_name': 'profiles/password_reset_confirm.haml'},
            name='password_reset_confirm'),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'profiles/password_reset_done.haml'}),
    
)
