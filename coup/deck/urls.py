from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_card', views.new_card, name='new_card'),
    path('reveal_card', views.reveal_card, name='reveal_card'),
    path('replace_card', views.replace_card, name='replace_card')
]
