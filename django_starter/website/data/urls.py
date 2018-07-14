from django.urls import path

from . import views


urlpatterns = [
    # ex: /data/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /data/5/
    path('<int:flower_id>/', views.detail, name='detail'),
]
