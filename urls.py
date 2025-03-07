from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from analysis.views import signup
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
   # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('', views.home, name='home'),  # Page d'accueil
    path('upload/', views.upload_image, name='upload_image'),  # Page pour l'upload
    path('results/', views.view_results, name='view_results'),  # Page pour les résultats
]
