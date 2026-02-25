from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, logout_view, home_view, find_user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path('facelogin/', login_view, name='facelogin'),
    path('facelogout/', logout_view, name='facelogout'),
    path('classify/', find_user_view, name='classify'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)