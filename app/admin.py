from django.contrib import admin
from .models import Students,Additional_information
from django.utils.html import format_html

admin.site.register(Additional_information)

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    # List display - shows these columns in the admin list view
    list_display = (
        'roll', 
        'name', 
        'semester', 
        'section', 
        'shift', 
        'session',
        'mobile_number', 
        'email',
        'display_profile_picture'
    )
    
    # Search fields - allows searching by these fields
    search_fields = (
        'name', 
        'roll', 
        'reg', 
        'email', 
        'mobile_number',
        'father_name',
        'mother_name'
    )
    
    # Filters - adds filter sidebar
    list_filter = (
        'semester',
        'section',
        'shift',
        'gender',
        'blood_group',
        'session',
        'nationality',
        'religion',
        'created_at',
    )
    
    # Date hierarchy - adds date-based drill-down navigation
    date_hierarchy = 'created_at'
    
    # Default ordering
    ordering = ('-roll', '-semester')
    
    # Fields to make clickable in list display
    list_display_links = ('roll', 'name')
    
    # Number of items per page
    list_per_page = 25
    
    # Editable fields directly in list view
    list_editable = ('semester', 'section', 'shift')
    
    # Fields to show in the detail form
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'name', 
                'father_name', 
                'mother_name', 
                'date_of_birth', 
                'gender', 
                'blood_group',
                'profile_picture'
            )
        }),
        ('Academic Information', {
            'fields': (
                'semester', 
                'roll', 
                'reg', 
                'session', 
                'shift', 
                'section'
            ),
            'classes': ('collapse',)  # Collapsible section
        }),
        ('Contact Information', {
            'fields': (
                'mobile_number', 
                'alternate_mobile', 
                'email', 
                'present_address', 
                'permanent_address'
            )
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name', 
                'emergency_contact_number'
            ),
            'classes': ('wide',)  # Wider layout
        }),
        ('Other Information', {
            'fields': (
                'nationality', 
                'religion'
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at', 
                'updated_at'
            ),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
    
    # Readonly fields
    readonly_fields = ('created_at', 'updated_at')
    
    # Custom method to display profile picture thumbnail
    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_picture.url)
        return format_html('<span style="color: gray;">No Photo</span>')
    
    display_profile_picture.short_description = 'Photo'
    
    # Bulk actions (default actions are already there, you can add custom ones)
    actions = ['make_morning_shift', 'make_day_shift']
    
    def make_morning_shift(self, request, queryset):
        queryset.update(shift='Morning')
        self.message_user(request, f"{queryset.count()} students shifted to Morning shift.")
    
    make_morning_shift.short_description = "Change shift to Morning"
    
    def make_day_shift(self, request, queryset):
        queryset.update(shift='Day')
        self.message_user(request, f"{queryset.count()} students shifted to Day shift.")
    
    make_day_shift.short_description = "Change shift to Day"
    
    # Save model and show success message
    def save_model(self, request, obj, form, change):
        if change:
            self.message_user(request, f"Student {obj.name} updated successfully.")
        else:
            self.message_user(request, f"Student {obj.name} added successfully.")
        super().save_model(request, obj, form, change)
    
    # Quick filter for recent students
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related()  # Optimize queries
    
    # Add custom buttons or links
    def view_on_site(self, obj):
        return f"/students/{obj.id}/"