from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from expenses import settings
from app import views, views_auth

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('register/', views_auth.registration, name='register'),
    path('login/', views_auth.login_view, name='login'),
    path('logout/', views_auth.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path('create/', views.create_view, name='create'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
