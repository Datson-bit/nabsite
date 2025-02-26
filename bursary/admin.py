from django.contrib import admin
from .models import BursaryApplication, ApplicationComment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import openpyxl
from django.http import HttpResponse
from django.contrib import admin


@admin.action(description="Export Qualified Applicants as Excel")
def export_qualified_applicants(modeladmin, request, queryset):
    # Create an Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Qualified Applicants"

    # Add header row
    headers = ["Reference Code", "Full Name", "Email", "Status"]
    sheet.append(headers)

    # Add data rows
    for application in queryset.filter(status="qualified"):
        sheet.append([
            application.reference_code,
            application.full_name,
            application.email,
            application.status
        ])

    # Prepare the response
    response = HttpResponse(content_type="application/vnd.openpyxl")
    response["Content-Disposition"] = 'attachment; filename="qualified_applicants.xlsx"'
    workbook.save(response)
    return response

@admin.register(BursaryApplication)
class BursaryApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'status', 'submitted_at')
    list_filter = ["status"]
    actions= [export_qualified_applicants]
@admin.register(ApplicationComment)
class ApplicationCommentAdmin(admin.ModelAdmin):
    list_display = ('application', 'stage', 'author', 'created_at')

# Unregister the default User admin and re-register with the default UserAdmin,
# which already includes groups.
admin.site.register(User, BaseUserAdmin)
