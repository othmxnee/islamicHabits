from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('register',views.RegisterView.as_view()),
    path('login',views.LoginView.as_view()),
    path('logout',views.LogoutView.as_view()),
    path('profile', views.UserProfileView.as_view(), name='user-profile'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)