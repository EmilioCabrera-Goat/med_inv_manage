from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView, Index, Dashboard, InformationView,
    AddItem, EditItem, DeleteItem, login_view, detect_face_view,
    check_face_encoding, pill_detection_view, detect_pill_view,
    support_view, chatbot_view
)

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('information/', InformationView.as_view(), name='information-page'),
    path('support/', support_view, name='support-page'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('facelogin/', login_view, name='facelogin'),
    path('facelogin/detect/', detect_face_view, name='detect_face'),
    path('check-face-encoding/', check_face_encoding, name='check_face_encoding'),
    path('pill-detection/', pill_detection_view, name='pill-detection'),
    path('pill-detection/detect/', detect_pill_view, name='detect_pill'),
    path('chatbot/', chatbot_view, name='chatbot'),
]