from django.contrib import admin
from .models import Job,Result


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("user","created","since","until","limit","language","credits_required")



@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("job","created","result_file")
