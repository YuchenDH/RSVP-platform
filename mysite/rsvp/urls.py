from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('signup', views.signup, name = 'signup'),
    path('create_event', views.create_event, name = 'create_event'),
    path('event/<id>', views.event, name='event'),
    path('create_question', views.create_question, name='create_question'),
    path('event/<id>/add_owner', views.add_owner, name='add_owner'),
    path('event/<id>/add_vendor', views.add_vendor, {'role':'vendor'}, name='add_vendor'),
    path('event/<id>/add_guest', views.add_vendor,  {'role':'guest'}, name='add_guest'),
    path('event/<id>/update', views.event_update, name='event_update'),
    path('event/<id>/add_question', views.add_question, name='add_question'),
    path('event/<id>/<qid>/add_option', views.add_option, name='add_option'),
    path('event/<id>/<qid>/finalize', views.question_finalize, name='finalize'),
]
