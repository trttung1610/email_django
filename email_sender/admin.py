from django.contrib import admin
from .models import CustomUser, UploadedFile

admin.site.register(CustomUser)

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('uploaded_at', 'uploaded_by', 'file')
