from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from tracking.models import Session, SessionData, PageData, Page
from .utils import get_or_create_session, session_expires

import json

import requests
from bs4 import BeautifulSoup as bsoup
import html2text
import babel

html2text_handle = html2text.HTML2Text()
html2text_handle.ignore_links = True
html2text_handle.ignore_images = True

HEADER = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def save_data(request):

    if request.method == 'GET':
        session = get_or_create_session(request)
        return Response({'cookie': session.cookie})

    post_data = request.data
    session = ''
    if isinstance(post_data, str):
        post_data = json.loads(post_data)

    page_url = post_data['page_url']
    try:
        page = Page.objects.get(page_url=page_url)
    except Page.MultipleObjectsReturned:
        page = Page.objects.filter(page_url=page_url).last()
    except Page.DoesNotExist:

        res = requests.get(page_url, headers=HEADER, timeout=10)
        soup = bsoup(res.content, "lxml")

        text_tmp = ' '.join( html2text.html2text(res.content.decode('utf-8')).replace('\\n','').replace('\\r','').replace('\\t','').split() )
        content = ' '.join(text_tmp[0:2000].split())
        content_size = len(text_tmp)

        just_text = html2text_handle.handle(res.content.decode('utf-8').replace('\n','').replace('\r','').replace('\t','')).replace('\"', '\\"')
        full_html = res.content.decode('utf-8')
        try:
            img_count = len([l['src'] for l in  soup.find_all('img') if l['src'].startswith('http') and l['src'].endswith('.png')])
        except:
            img_count = 0
        #
        try:
            lang_code = soup.find_all('html')[0]['lang']
            if '-' in lang_code:
                lang_code = lang_code.split('-')[0]
            lang = babel.Locale.parse(lang_code).get_display_name('en')
        except:
            lang = None
        #
        video_count = len(soup.find_all('video'))
        #
        if 'login' in str(res.content):
            login = True
        else:
            login = False
        #
        kwd_count = len(content.split(' '))
        #
        try:
            title = soup.find_all('title')[0].text
        except:
            title = None
        #
        headings = len(soup.find_all('h1'))
        #
        try:
            meta_list = [ i['content'] for i in soup.find_all('meta')]
            meta = ' '.join(meta_list)
        except:
            meta = None

        page = Page(
            page_url=page_url,
            img_count=img_count,
            content=content,
            content_text=just_text,
            content_html=full_html,
            content_size=content_size,
            lang=lang,
            video_count=video_count,
            login=login,
            kwd_count=kwd_count,
            title=title,
            headings=headings,
            meta=meta
            )
        page.save()

    time_on_page = post_data['time_on_page']

    cookie = post_data['cookie']
    if cookie:
        session = Session.objects.filter(
            cookie__exact=cookie,
            last_seen__gt=session_expires()
            ).last()

    if not session:
        session = get_or_create_session(request)


    session_data, session_data_created = SessionData.objects.get_or_create(session_id=session)

    previous_page = ''
    if session_data_created:
        session_data.pageview = page_url
    else:
        page_visited = session_data.pageview.split(',')
        previous_page = page_visited[-1]
        if not page_url in page_visited:
            session_data.pageview = ','.join([session_data.pageview, page_url])

    session_data.pageflow = page_url if session_data_created else ','.join([session_data.pageflow, page_url])

    session_data.save()

    if previous_page:
        previous_page_data = PageData.objects.filter(session_id=session, page_url__exact=previous_page).first()
        if previous_page_data:
            previous_page_data.exit_to = page_url
            previous_page_data.save()

    page_data, page_data_created = PageData.objects.get_or_create(session_id=session, page_id=page.id, page_url=page_url)

    page_data.time_on_page += int(time_on_page)
    if page_data_created:
        page_data.page_url = page_url

    page_data.save()
    return Response({'status': 'ok'})