from django.contrib import admin
from .models import ContactQuery, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'number','masked_password']
    search_fields = ['username', 'email']
    def masked_password(self, obj):
        return '********'
    masked_password.short_description = 'Password'
from django.contrib import admin
from .models import UserProfile
from .models import Recipe
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name',  'address','profile_photo')
    search_fields = ('user__username', 'name',)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at','ingredients','description','image']
    search_fields = ['title', 'user__username']
    readonly_fields = ['created_at']

admin.site.register(Recipe, RecipeAdmin)
@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_resolved',)