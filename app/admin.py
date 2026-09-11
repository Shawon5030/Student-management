from django.contrib import admin
from django.utils.html import format_html
from .models import Students,env_token, LoginHistory,Additional_information








from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Students,
    env_token,
    LoginHistory,
    Additional_information,
)


# =========================================================
# Environment Token
# =========================================================

admin.site.register(env_token)


# =========================================================
# Additional Information Admin
# =========================================================

@admin.register(Additional_information)
class AdditionalInformationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'login_page_image',
    )


# =========================================================
# Login History
# =========================================================

admin.site.register(LoginHistory)
admin.site.register(Students)


# =========================================================
# Admin Site Configuration
# =========================================================

admin.site.site_header = "Student Management Admin"
admin.site.site_title = "Student Management"
admin.site.index_title = "Student Management Dashboard"


# =========================================================
# Students Admin
# =========================================================


