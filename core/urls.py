from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<int:key_id>/', views.PageDetail.as_view(), name='detail')
]

