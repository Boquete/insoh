from django.urls import path

from . import views

urlpatterns = [
    path('', views.VehicleListView.as_view(), name='index'),
    path('create/', views.VehicleCreate.as_view(), name='vehicle_create'),
    path('<int:pk>/edit/', views.VehicleUpdate.as_view(), name='vehicle_update'),
]
