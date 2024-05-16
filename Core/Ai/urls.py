
''''
from django.urls import path
from . import views

urlpatterns = [
    path('find_similar_images/', views.find_similar_images_api, name='find_similar_images_api'),
]
'''
from django.urls import path
from .views import ModelAPIView

urlpatterns = [
    path('api/model/', ModelAPIView.as_view(), name='model_api'),
]
