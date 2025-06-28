from django.shortcuts import render, redirect
from user.models import CustomUser, Recipe, Comment, ContactQuery  # add models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# from .models import CustomUser, Recipe, Comment, ContactQuery
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
def admin_panel(request):
    users = CustomUser.objects.all()
    recipes = Recipe.objects.select_related('user').all()
    comments = Comment.objects.select_related('user', 'recipe').all()
    enquiries = ContactQuery.objects.all()
    deleted_comment_count = request.session.get('deleted_comment_count', 0)
    
    context = {
        'users': users,
        'recipes': recipes,
        'comments': comments,
        'enquiries': enquiries,
        'user_count': users.count(),
        'recipe_count': recipes.count(),
        'comment_count': comments.count(),
        'unread_enquiry_count': enquiries.filter(is_resolved=False).count(),
        'read_enquiry_count': enquiries.filter(is_resolved=True).count(),
        'deleted_comment_count': deleted_comment_count,  # You can update this if you implement soft delete
    }

    return render(request, 'admin.html', context)

def logout(request):
        return render(request,'home.html')
    
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    messages.success(request, "Recipe deleted successfully.")
    return redirect('adminpanel')

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    request.session['deleted_comment_count'] = request.session.get('deleted_comment_count', 0) + 1
    messages.success(request, "Comment deleted successfully.")
    return redirect('adminpanel')   
def resolve_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(ContactQuery, id=enquiry_id)
    enquiry.is_resolved = True
    enquiry.save()
    # return HttpResponseRedirect(f"mailto:{enquiry.email}")
    return redirect('adminpanel')