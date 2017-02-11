from django.contrib import admin

# Register your models here.
from .models import Session, SessionData, PageData, Page, MLSession

class SessionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'platform', 'time', 'ip_address', 'country_name', 'city', 'time_zone', 'latitude', 'longitude']
    list_filter = ['date', 'year', 'platform']
    search_fields = ['platform']
    class Meta:
        model = Session

class SessionDataModelAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'pageview', 'pageflow']
    class Meta:
        model = SessionData

class PageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_html', 'page_url', 'img_count', 'content_size', 'lang', 'video_count', 'login', 'kwd_count', 'title', 'headings']
    class Meta:
        model = Page

class PageDataModelAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'page_id', 'page_url', 'time_on_page', 'exit_to']
    class Meta:
        model = PageData

class MLSessionModelAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'visitor_type', 'day', 'time', 'year', 'month', 'platform', 'page_1', 'page_time_1', 'page_pictures_1']
    class Meta:
        model = MLSession

admin.site.register(Session, SessionModelAdmin)
admin.site.register(SessionData, SessionDataModelAdmin)
admin.site.register(PageData, PageDataModelAdmin)
admin.site.register(Page, PageModelAdmin)
admin.site.register(MLSession, MLSessionModelAdmin)