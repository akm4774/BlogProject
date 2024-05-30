from django.urls import path
from . import views
from .views import SignUpView, LoginView, DashboardView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('add-blog/', views.add_blog, name='add_blog'),
    path('edit-blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete-blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('profile/', views.profile_view, name='profile'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
