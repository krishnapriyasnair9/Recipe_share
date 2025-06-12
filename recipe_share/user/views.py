import json
from venv import logger
from django.contrib import messages  # ✅ Correct

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password

from .models import UserProfile

from .models import CustomUser
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.decorators import login_required


from .models import Recipe, Comment
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def upload_recipe(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "Please login first.")
            return redirect('login')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('login')

        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        edit_id = request.GET.get('edit_id')

        if not (title and ingredients and description):
            messages.error(request, "All fields are required.")
            return redirect('userdashboard')

        if edit_id:
            try:
                recipe = Recipe.objects.get(id=edit_id, user=user)
                recipe.title = title
                recipe.ingredients = ingredients
                recipe.description = description
                if image:
                    recipe.image = image
                recipe.save()
                messages.success(request, "Recipe updated successfully!")
                return redirect('/userdashboard/?updated=1')
            except Recipe.DoesNotExist:
                messages.error(request, "Recipe not found or permission denied.")
                return redirect('userdashboard')

        # Create new recipe
        if not image:
            messages.error(request, "Image is required.")
            return redirect('userdashboard')

        Recipe.objects.create(
            user=user,
            title=title,
            ingredients=ingredients,
            description=description,
            image=image
        )
        messages.success(request, "Recipe uploaded successfully!")
        return redirect('userdashboard')

    return redirect('userdashboard')
def home(request):
    # return render(request, 'home.html')
    if request.method == 'POST':
        # Get form data directly from request.POST
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Basic validation
        if not all([name, email, subject, message]):
            messages.error(request, 'All fields are required!')
        else:
            # Save to database
            ContactQuery.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Your query has been submitted successfully!')
            return redirect('home')
    
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        number = request.POST.get("number")
        password = request.POST.get("password")

        # Email already exists?
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Save user
        user = CustomUser(
            username=username,
            email=email,
            number=number,
            password=make_password(password)
        )
        user.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')
    
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                messages.success(request, "Login successful!")
                return redirect("userdashboard")  # Replace with your dashboard URL
            else:
                messages.error(request, "Invalid password.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, "login.html")

def user_profile(request):
        # username = request.session.get('username', 'User')
        # return render(request, 'userdashboard.html',{'username': username})
    user_id = request.session.get('user_id')
    username = request.session.get('username', 'User')

    try:
        user = CustomUser.objects.get(id=user_id)
        profile = UserProfile.objects.filter(user=user).first()
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    edit_id = request.GET.get('edit_id')
    edit_recipe = None
    if edit_id:
        try:
            edit_recipe = Recipe.objects.get(id=edit_id, user=user)
        except Recipe.DoesNotExist:
            messages.error(request, "Recipe not found or permission denied.")
            return redirect('userdashboard')

    # Get 8 most recent recipes to feature on dashboard
    featured_recipes = Recipe.objects.order_by('-created_at')[:8]

    return render(request, 'userdashboard.html', {
        'user': user,
        'profile': profile,
        'edit_recipe': edit_recipe,
        'featured_recipes': featured_recipes
    })
def create_profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('login')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found. Please login again.")
        return redirect('login')

    # Now user is a valid CustomUser instance
    profile = UserProfile.objects.filter(user=user).first()
    is_edit = True if profile else False

    if request.method == 'POST':
        name = request.POST.get('name')
        
        address = request.POST.get('address')
        photo = request.FILES.get('profilePhoto')

        if not all([name,  address]):
            messages.error(request, "All fields except photo are required.")
            return render(request, 'create-profile.html', {'profile': profile, 'is_edit': is_edit})

        if profile:
            profile.name = name
            
            profile.address = address
            if photo:
                profile.profile_photo = photo
                profile.save()
            messages.success(request, "Profile updated successfully.")
        else:
            UserProfile.objects.create(
                user=user,
                name=name,
                address=address,
                profile_photo=photo
            )
            messages.success(request, "Profile created successfully.")
        
        return redirect('userdashboard')

    return render(request, 'create-profile.html', {'profile': profile, 'is_edit': is_edit,'user': user})
    
def view_recipe(request):
    user = None
    profile = None
    search_query = request.GET.get('q', '')

    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = CustomUser.objects.get(id=user_id)
            profile = UserProfile.objects.filter(user=user).first()
        except CustomUser.DoesNotExist:
            pass

    # Fetch all recipes with related user to avoid extra queries
    recipes = Recipe.objects.all().select_related('user')
    
    # Apply search filter if query exists
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__icontains=search_query)
        )

    context = {
        'user': user,
        'profile': profile,
        'recipes': recipes,
        'search_query': search_query,
    }
    return render(request, 'recipes.html', context)
def view_comments(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('login')

    try:
        user = CustomUser.objects.get(id=user_id)
        profile = UserProfile.objects.filter(user=user).first()
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    # Get recipes of the user and their comments
    recipes = Recipe.objects.filter(user=user).prefetch_related('comments')

    return render(request, 'comments.html', {
        'user': user,
        'profile': profile,
        'recipes': recipes,
    })
def view_yourrecipes(request):
    
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('login')

    try:
        user = CustomUser.objects.get(id=user_id)
        profile = UserProfile.objects.filter(user=user).first()
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    recipes = Recipe.objects.filter(user=user)
    return render(request, 'recipedetail.html', {
        'recipes': recipes,
        'user': user,
        'profile': profile,
    })
def logout(request):
    return render(request, 'home.html')


def delete_recipe(request, recipe_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('login')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    recipe = get_object_or_404(Recipe, id=recipe_id, user=user)
    recipe.delete()
    messages.success(request, "Recipe deleted successfully!")
    return redirect('userdashboard')
@csrf_exempt
def post_comment(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User not logged in'})

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})

        data = json.loads(request.body)
        recipe_title = data.get('title')
        comment_text = data.get('text')

        if not comment_text:
            return JsonResponse({'status': 'error', 'message': 'Empty comment'})

        recipe = Recipe.objects.filter(title=recipe_title).first()
        if not recipe:
            return JsonResponse({'status': 'error', 'message': 'Recipe not found'})

        Comment.objects.create(user=user, recipe=recipe, text=comment_text)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
def custom_password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)

        if associated_users.exists():
            user = associated_users[0]
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            subject = "Reset your password"
            message = render_to_string('forgetpassword/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, "Password reset link sent to your email.")
            return redirect('password_reset_done')
        else:
            messages.error(request, "No user is associated with this email.")
            return redirect('password_reset')

    return render(request, 'forgetpassword/forgetpassword.html')
def password_reset_done_view(request):
    return render(request, 'forgetpassword/password_reset_done.html')