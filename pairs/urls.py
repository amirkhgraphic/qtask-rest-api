from django.urls import path

from pairs import views

urlpatterns = [
    path('', views.KeyValueListCreateAPIView.as_view(), name='list-create'),
    path('<int:pk>/', views.KeyValueRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-delete'),
]
