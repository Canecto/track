from rest_framework.serializers import ModelSerializer

from tracking.models import Session, SessionData, PageData, Page


class SessionSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'last_seen', 'ip_address', 'platform', 'cookie', 'month')
        read_only_fields = ('id', 'last_seen', 'date', 'time', 'year', 'cookie', )


class SessionDataSerializer(ModelSerializer):
    session = SessionSerializer()
    class Meta:
        model = SessionData
        fields = ('session_id', 'pageview',)

class PageSerializer(ModelSerializer):
    session = SessionSerializer()
    class Meta:
        model = Page

class PageDataSerializer(ModelSerializer):
    session = SessionSerializer()
    page = PageSerializer()
    class Meta:
        model = PageData
        fields = ('session_id', 'page_id', 'time_on_page', 'exit_to',)

    def create(self, validated_data):
        PageData.objects.create(validated_data)