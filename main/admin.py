from django.contrib import admin
from .models import Study, Samples, Spider_db, db_test

class StudyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sample', 'user_response', 'viewed')
    list_filter = ['user']
    
admin.site.register(Study, StudyAdmin)
admin.site.register(Samples)
admin.site.register(Spider_db)
admin.site.register(db_test)

