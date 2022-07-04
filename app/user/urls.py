"""
URL Mappings for the user API.
"""
from django.urls import path

from user import views


# This is the name system will look for when using reverse(<app_name>:...)
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]