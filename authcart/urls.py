from django.urls import path
from authcart import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate')
]