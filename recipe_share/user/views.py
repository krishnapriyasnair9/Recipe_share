import json
from venv import logger
from django.conf import settings
from django.contrib import messages  # ✅ Correct
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render


from .models import ContactQuery, UserProfile

from .models import CustomUser
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login as auth_login
from .models import Recipe, Comment
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
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

        # ✅ Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html", {
                "email": email,
                "number": number,
            })

        # ✅ Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "register.html", {
                "username": username,
                "number": number,
            })

        # Save new user
        user = CustomUser(
            username=username,
            email=email,
            number=number,
            password=make_password(password)  # securely hashed
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

            # ✅ Check if password matches (hashed or raw fallback)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                messages.success(request, "Login successful!")
                return redirect("userdashboard")
            else:
                messages.error(request, "Invalid password.")
                return render(request, "login.html")
        except CustomUser.DoesNotExist:
            pass  # Continue to check Django superuser

        # Check for superuser/admin login
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            auth_login(request, user)
            return redirect("adminpanel")
        else:
            messages.error(request, "User not found.")

    return render(request, "login.html")
def admin_panel(request):
    return render(request, 'admin.html')
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
User = get_user_model()

def generate_otp():
    return str(random.randint(100000, 999999))

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            messages.error(request, "No user found with this email.")
            return redirect("forget_password")

        otp = str(random.randint(100000, 999999))
        request.session['reset_email'] = email
        request.session['reset_otp'] = otp

        # ✅ Directly set sender email here
        email_msg = EmailMessage(
            subject='Your OTP for Password Reset',
            body=f'Hi {user.username}, your OTP is: {otp}',
            from_email='your-custom-sender@example.com',  # ✅ Override here
            to=[email]
        )
        email_msg.send(fail_silently=False)

        print("Sending OTP to:", email)
        messages.success(request, "OTP has been sent to your email.")
        return redirect('verify_otp')

    return render(request, 'forgetpassword.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        actual_otp = request.session.get('reset_otp')

        if entered_otp == actual_otp:
            return redirect('reset_password')
        else:
            return render(request, 'verifyotp.html', {'error': 'Invalid OTP'})
    return render(request, 'verifyotp.html')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        email = request.session.get('reset_email')

        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect('forget_password')

        user = CustomUser.objects.filter(email=email).first()

        if user:
            # ✅ Manually hash the password and save it
            hashed_password = make_password(password)
            user.password = hashed_password
            user.save(update_fields=["password"])

            # ✅ Clear session
            request.session.flush()

            # ✅ Success message and redirect
            messages.success(request, "Password reset successfully. Please login.")
            return redirect('login')

        else:
            messages.error(request, "User not found.")
            return redirect('forget_password')

    return render(request, 'resetpassword.html')