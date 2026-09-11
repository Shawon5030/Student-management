from django.contrib import admin
from django.utils.html import format_html
from .models import Students,env_token, LoginHistory,Additional_information

admin.site.register(env_token)

# Register Additional Information model
@admin.register(Additional_information)
class AdditionalInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'login_page_image')

admin.site.site_header = "Student Management Admin"
admin.site.register(LoginHistory)
# Students Admin
@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):

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

    search_fields = (
        'name',
        'roll',
        'reg',
        'email',
        'mobile_number',
        'father_name',
        'mother_name',
    )

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

    date_hierarchy = 'created_at'

    ordering = ('-roll', '-semester')

    list_display_links = ('roll', 'name')

    list_per_page = 25

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

    # ❌ এটা remove করা হয়েছে
    # readonly_fields = ('created_at', 'updated_at')

    actions = [
        'make_morning_shift',
        'make_day_shift',
    ]

    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" '
                'style="border-radius:50%;" />',
                obj.profile_picture.url
            )

        return "No Photo"

    display_profile_picture.short_description = 'Photo'

    def make_morning_shift(self, request, queryset):
        updated = queryset.update(shift='Morning')
        self.message_user(
            request,
            f"{updated} students shifted to Morning."
        )

    make_morning_shift.short_description = "Change shift to Morning"

    def make_day_shift(self, request, queryset):
        updated = queryset.update(shift='Day')
        self.message_user(
            request,
            f"{updated} students shifted to Day."
        )

    make_day_shift.short_description = "Change shift to Day"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if change:
            self.message_user(
                request,
                f"Student '{obj.name}' updated successfully."
            )
        else:
            self.message_user(
                request,
                f"Student '{obj.name}' added successfully."
            )

    def get_queryset(self, request):
        return super().get_queryset(request)

    def view_on_site(self, obj):
        return f"/students/{obj.id}/"