from django.contrib import admin
from django.utils.html import format_html
from .models import Students, Additional_information


# Register Additional Information model
@admin.register(Additional_information)
class AdditionalInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'login_page_image')


# Students Admin
@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):

    # Columns in list view
    list_display = (
        'roll',
        'name',
        'semester',
        'section',
        'shift',
        'session',
        'mobile_number',
        'email',
        'display_profile_picture',
    )

    # Search
    search_fields = (
        'name',
        'roll',
        'reg',
        'email',
        'mobile_number',
        'father_name',
        'mother_name',
    )

    # Filters
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

    # Date navigation
    date_hierarchy = 'created_at'

    # Ordering
    ordering = ('-roll', '-semester')

    # Clickable fields
    list_display_links = ('roll', 'name')

    # Pagination
    list_per_page = 25

    # Editable in list
    list_editable = ('semester', 'section', 'shift')

    # Form layout
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'name',
                'father_name',
                'mother_name',
                'date_of_birth',
                'gender',
                'blood_group',
                'profile_picture',
            )
        }),
        ('Academic Information', {
            'fields': (
                'semester',
                'roll',
                'reg',
                'session',
                'shift',
                'section',
            ),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': (
                'mobile_number',
                'alternate_mobile',
                'email',
                'present_address',
                'permanent_address',
            )
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name',
                'emergency_contact_number',
            ),
            'classes': ('wide',)
        }),
        ('Other Information', {
            'fields': (
                'nationality',
                'religion',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )

    # Readonly
    readonly_fields = ('created_at', 'updated_at')

    # ✅ FIXED method (no more TypeError)
    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;" />',
                obj.profile_picture.url
            )
        return "No Photo"

    display_profile_picture.short_description = 'Photo'

    # Bulk actions
    actions = ['make_morning_shift', 'make_day_shift']

    def make_morning_shift(self, request, queryset):
        updated = queryset.update(shift='Morning')
        self.message_user(request, f"{updated} students shifted to Morning.")

    make_morning_shift.short_description = "Change shift to Morning"

    def make_day_shift(self, request, queryset):
        updated = queryset.update(shift='Day')
        self.message_user(request, f"{updated} students shifted to Day.")

    make_day_shift.short_description = "Change shift to Day"

    # Save message
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            self.message_user(request, f"Student '{obj.name}' updated successfully.")
        else:
            self.message_user(request, f"Student '{obj.name}' added successfully.")

    # Optimize query
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs  # no select_related needed unless FK exists

    # Optional: View on site
    def view_on_site(self, obj):
        return f"/students/{obj.id}/"
