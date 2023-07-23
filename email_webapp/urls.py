from django.contrib import admin
from django.urls import path
from email_sender import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('send_email/', views.send_email_view, name="send_email"),  # send_email is no longer the home view
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
