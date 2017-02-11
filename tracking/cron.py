from django_cron import CronJobBase, Schedule
from tracking.models import Session, Page, PageData, MLSession
from tracking.api.utils import session_expires

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 # every x minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        last_ml_sessions = MLSession.objects.all().last()
        last_ml_sessions_id = 0
        if last_ml_sessions:
            last_ml_sessions_id = last_ml_sessions.id

        sessions = Session.objects.filter(last_seen__lt=session_expires(), id__gt=last_ml_sessions_id)
        for session in sessions:
            platform = 0
            for indentifier, os in enumerate(['MAC', 'IOS', 'ANDROID'], 1):
                if os in session.platform.upper():
                    platform = indentifier
            platform = platform or 1

            try:
                model_layer, created = MLSession.objects.get_or_create(
                    session_id=session.id,
                    day=session.date.day,
                    time=session.time.replace(second=0, microsecond=0),
                    year=session.year,
                    month=session.month,
                    platform=platform
                )
            except MLSession.MultipleObjectsReturned:
                 model_layer = MLSession.objects.filter(
                    session_id=session.id,
                    day=session.date.day,
                    time=session.time.replace(second=0, microsecond=0),
                    year=session.year,
                    month=session.month,
                    platform=platform
                ).last()

            visitor_type = 2 if len(Session.objects.filter(cookie__exact=session.cookie)) > 1 else 1
            model_layer.visitor_type = visitor_type

            page_data = PageData.objects.filter(session_id=session.id)
            for number, page_data_item in enumerate(page_data, 1):
                if number > 10:
                    break
                page = Page.objects.get(id=page_data_item.page_id)
                setattr(model_layer, 'page_%s' % number, page.id)
                setattr(model_layer, 'page_time_%s' % number, page_data_item.time_on_page)
                setattr(model_layer, 'page_pictures_%s' % number, page.img_count)

            model_layer.save()

