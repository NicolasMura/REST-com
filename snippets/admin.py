# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from snippets.models import Snippet
# Register your models here.


class SnippetAdmin(admin.ModelAdmin):
    list_display = (
            'title',
            # 'owner',
            'code',
            'created',
            'linenos',
            'language',
            'style',
            # 'highlighted',
        )

admin.site.register(Snippet, SnippetAdmin)
