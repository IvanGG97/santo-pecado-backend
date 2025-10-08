from django.urls import path
from .views import RegisterView, LoginView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]



# from django.urls import path
# from . import views
# from rest_framework_simplejwt.views import TokenRefreshView

# urlpatterns = [
#     path('registro/', views.registro_usuario, name='registro'),
#     path('login/', views.login_usuario, name='login'),
#     path('perfil/', views.perfil_usuario, name='perfil'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]