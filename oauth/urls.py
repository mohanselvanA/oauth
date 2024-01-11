# urls.py

from django.urls import path
from .views import LoginView, UserListView, GetAllInstancesAPIView

urlpatterns = [
    
    path('login/', LoginView.as_view(), name='login'),
    path('message/', UserListView.as_view(), name='message'),
    path('get_all_instances/', GetAllInstancesAPIView.as_view(), name='get_all_instances'),


   
]
