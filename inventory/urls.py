from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import SignUpView, Index, Dashboard, InformationView, SupportView, AddItem, EditItem, DeleteItem
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('information/', InformationView.as_view(), name='information-page'),
    path('support/', SupportView.as_view(), name='support-page'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
]