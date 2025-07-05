from django.urls import path
from .import views
urlpatterns = [
    path('',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('home/', views.home_view, name='home'),
    path('predict/',views.predict,name='predict'),
    path('logout/',views.logout_view,name='logout')
]