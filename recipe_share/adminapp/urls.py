from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin_panel, name='adminpanel'),
    path('logout/', views.logout, name='logout'),
    path('delete-recipe/<int:recipe_id>/', views.delete_recipe, name='admin_delete_recipe'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='admin_delete_comment'),
    path('resolve-enquiry/<int:enquiry_id>/', views.resolve_enquiry, name='resolve_enquiry'),  # <-- add this
]