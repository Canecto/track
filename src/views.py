#from django.shortcuts import render
#from django.http import HttpResponseBadRequest, HttpResponse
import django_excel as excel
from tracking.models import MLSession

# Create your views here.
def export_data(request):
    query_sets = set(MLSession.objects.all())
    for item in query_sets:
        item.time = item.time.strftime('%H:%M')
    column_names = [
        'session_id',
        'year',
        'month',
        'day',
        'time',
        'platform',
        'visitor_type',
        'page_1',
        'page_time_1',
        'page_pictures_1',
        'page_2',
        'page_time_2',
        'page_pictures_2',
        'page_3',
        'page_time_3',
        'page_pictures_3',
        'page_4',
        'page_time_4',
        'page_pictures_4',
        'page_5',
        'page_time_5',
        'page_pictures_5',
        'page_6',
        'page_time_6',
        'page_pictures_6',
        'page_7',
        'page_time_7',
        'page_pictures_7',
        'page_8',
        'page_time_8',
        'page_pictures_8',
        'page_9',
        'page_time_9',
        'page_pictures_9',
        'page_10',
        'page_time_10',
        'page_pictures_10'
        ]
    result = excel.make_response_from_query_sets(
            query_sets,
            column_names,
            'xls',
            file_name="custom"
        )

    return result
