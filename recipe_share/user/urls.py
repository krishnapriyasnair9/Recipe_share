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
    
    path('password_reset/', views.custom_password_reset_request, name='password_reset'),
    path('password_reset_done/', views.password_reset_done_view, name='password_reset_done'),
]



