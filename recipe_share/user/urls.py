from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('userdashboard/', views.user_profile, name='userdashboard'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('recipe/', views.view_recipe, name='recipes'),
    path('comments/', views.view_comments, name='comments'),
    path('yourrecipes/', views.view_yourrecipes, name='recipedetail'),
    path('logout/', views.logout, name='logout'),
    path('upload-recipe/', views.upload_recipe, name='upload_recipe'),
    path('delete-recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('post-comment/', views.post_comment, name='post_comment'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('adminpanel',views.admin_panel, name='adminpanel'),
    
]



