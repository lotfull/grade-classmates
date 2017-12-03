from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'time/$', views.index, name='index'),
    url(r'dashboard', views.dashboard, name='dashboard'),

    url(r'^meeting/(?P<meeting_id>[0-9]+)/results/$', views.meeting_results, name='meeting_results'),
    url(r'^meeting/(?P<meeting_id>[0-9]+)/vote_choice/(?P<graded_id>[0-9]+)/$', views.meeting_vote_choice, name='meeting_vote_choice'),
    url(r'^meeting/(?P<meeting_id>[0-9]+)/vote_action/(?P<graded_id>[0-9]+)$', views.meeting_vote_action, name='meeting_vote_action'),
]