from django.urls import path
from . import views


urlpatterns = [
    # path('', views.head),
    path('code/', views.index),
]
