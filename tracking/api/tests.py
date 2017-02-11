from tracking.models import Session
from tracking.api.serializers import SessionSerializer, PageDataSerializer

session = Session.objects.all()
SessionSerializer(session[0])

data = {"page_url": "someUrl", "time_on_page": 10, "exit_to": "Exit"}
PageDataSerializer(data)