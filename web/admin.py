# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from web import models
admin.site.register(models.UserProfile)
admin.site.register(models.SecretDB)
