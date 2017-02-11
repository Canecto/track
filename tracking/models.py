from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta

# Create your models here.

class SessionManager(models.Manager):
    def all(self, *args, **kwargs):
        expired_session_time = datetime.now() - timedelta(hours=1)
        return super(SessionManager, self).filter(last_seen__gt=expired_session_time)


class Session(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=True)
    time = models.TimeField(auto_now=False, auto_now_add=True)
    year = models.IntegerField(default=int(datetime.now().year))
    month = models.IntegerField(default=int(datetime.now().month))
    platform = models.CharField(max_length=100, blank=True, null=True, default=None)
    ip_address = models.GenericIPAddressField()
    last_seen = models.DateTimeField(auto_now=True, auto_now_add=False)
    cookie = models.CharField(max_length=50, blank=True, null=True, default=None)
    country_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    country_code = models.CharField(max_length=5, blank=True, null=True, default=None)
    city = models.CharField(max_length=100, blank=True, null=True, default=None)
    time_zone = models.CharField(max_length=100, blank=True, null=True, default=None)
    latitude = models.CharField(max_length=10, blank=True, null=True, default=None)
    longitude = models.CharField(max_length=10, blank=True, null=True, default=None)
    #is_mobile = models.BooleanField(default=False)
    #mobile_device_make = models.CharField(max_length=50, blank=True, null=True, default=None)
    #mobile_device_model = models.CharField(max_length=50, blank=True, null=True, default=None)

    objects = SessionManager()

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'session'
        ordering = ['id']


class SessionData(models.Model):
    session_id = models.ForeignKey(Session, db_column='session_id', on_delete=models.CASCADE)
    pageview = models.TextField(blank=False, null=False)
    pageflow = models.TextField(blank=False, null=False)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class Page(models.Model):
    page_url = models.TextField(blank=False, null=False)
    img_count = models.IntegerField(default=0)
    content = models.TextField(blank=False, null=False)
    content_text = models.TextField(blank=True, null=True, default='')
    content_html = models.TextField(blank=True, null=True, default='')
    content_size = models.IntegerField(default=0)
    lang = models.CharField(max_length=10, blank=True, null=True, default=None)
    video_count = models.IntegerField(default=0)
    login = models.BooleanField()
    kwd_count = models.IntegerField(default=0)
    title = models.CharField(max_length=255, blank=True, null=True, default=None)
    headings = models.CharField(max_length=255, blank=True, null=True, default=None)
    meta = models.TextField(blank=False, null=False)
    created = models.DateField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)

    #def save(self, *args, **kwargs):
        ## do staff
        #super(Page, self).save(*args, **kwargs)


class PageData(models.Model):
    session_id = models.ForeignKey(Session, db_column='session_id')
    page_id = models.IntegerField(default=0)
    page_url = models.TextField(blank=False, null=False)
    time_on_page = models.IntegerField(default=0)
    exit_to = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)


class MLSession(models.Model):
    PC_PLATFORM = 1
    MAC_PLATFORM = 2
    IOS_PLATFORM = 3
    ANDROID_PLATFORM = 4

    PLATFORM_CHOISE = (
        (PC_PLATFORM, 'PC'),
        (MAC_PLATFORM, 'MAC'),
        (IOS_PLATFORM, 'IOS'),
        (ANDROID_PLATFORM, 'ANDROID')
        )

    session_id = models.IntegerField(default=0)
    day = models.IntegerField(default=int(datetime.now().day))
    time = models.TimeField()
    year = models.IntegerField(default=int(datetime.now().year))
    month = models.IntegerField(default=int(datetime.now().month))
    platform = models.IntegerField(choices=PLATFORM_CHOISE)
    visitor_type = models.IntegerField(default=1)

    page_1 = models.IntegerField(default=0)
    page_time_1 = models.IntegerField(default=0)
    page_pictures_1 = models.IntegerField(default=0)

    page_2 = models.IntegerField(default=0)
    page_time_2 = models.IntegerField(default=0)
    page_pictures_2 = models.IntegerField(default=0)

    page_3 = models.IntegerField(default=0)
    page_time_3 = models.IntegerField(default=0)
    page_pictures_3 = models.IntegerField(default=0)

    page_4 = models.IntegerField(default=0)
    page_time_4 = models.IntegerField(default=0)
    page_pictures_4 = models.IntegerField(default=0)

    page_5 = models.IntegerField(default=0)
    page_time_5 = models.IntegerField(default=0)
    page_pictures_5 = models.IntegerField(default=0)

    page_6 = models.IntegerField(default=0)
    page_time_6 = models.IntegerField(default=0)
    page_pictures_6 = models.IntegerField(default=0)

    page_7 = models.IntegerField(default=0)
    page_time_7 = models.IntegerField(default=0)
    page_pictures_7 = models.IntegerField(default=0)

    page_8 = models.IntegerField(default=0)
    page_time_8 = models.IntegerField(default=0)
    page_pictures_8 = models.IntegerField(default=0)

    page_9 = models.IntegerField(default=0)
    page_time_9 = models.IntegerField(default=0)
    page_pictures_9 = models.IntegerField(default=0)

    page_10 = models.IntegerField(default=0)
    page_time_10 = models.IntegerField(default=0)
    page_pictures_10 = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.id)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['session_id']