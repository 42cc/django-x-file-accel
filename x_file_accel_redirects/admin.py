# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import AccelRedirect


class AccelRedirectAdmin(admin.ModelAdmin):
    list_display = ('description', 'login_required', 'prefix', 'internal_path', 'serve_document_root')
    list_filter = ('login_required', 'filename_solver')
    search_fields = ('description', 'prefix', 'internal_path', 'serve_document_root')


admin.site.register(AccelRedirect, AccelRedirectAdmin)
