from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('update-user/', views.update_user, name='update-user'),
    path('update-password/', views.update_password, name='update-password'),
    path('update-info/', views.update_info, name='update-info'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<product_id>', views.product, name='product'),
    path('category/<str:cat_egory>', views.category, name='category'),
    path('category-summary/', views.category_summary, name='category-summary'),
    path('search', views.search, name='search'),
]

