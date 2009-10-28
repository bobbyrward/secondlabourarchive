from django.shortcuts import get_object_or_404
from comicsarchive.archive.models import DownloadLink
from comicsarchive.archive.models import DownloadTopics
from django.contrib.auth.decorators import login_required
from comicsarchive.archive.templates import render_response
from django.core.paginator import QuerySetPaginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.utils import simplejson
from comicsarchive.archive.json import json_paginator_response, json_response


@login_required
def browse(request, page_number=1):
    links = DownloadLink.objects.filter(hidden=False)

    paginator = QuerySetPaginator(links, 25)
    page = paginator.page(page_number)

    return render_response(request, 'style2/link_browse.html', '',
        {
        'page': page,
        'paginator': paginator,
        })


@login_required
def browse2(request, page_number=1):
    links = DownloadLink.objects.filter(hidden=False)

    paginator = QuerySetPaginator(links, 25)
    page = paginator.page(page_number)

    return render_response(request, 'style2/link_browse_json.html', '',
        {
        'page': page,
        'paginator': paginator,
        })


@login_required
def json_browse(request, page_number=1):
    paginator = QuerySetPaginator(DownloadLink.objects.filter(hidden=False), 4)
    page = paginator.page(page_number)
    from time import sleep

    return json_paginator_response(page)


@login_required
def name_search_json(request):
    if 'terms' not in request.GET:
        raise Http404()

    links = DownloadLink.objects.filter(hidden=False)

    for term in request.GET['terms'].split():
        links = links.filter(name__icontains=term)

    return json_response(links)



@login_required
def change_name(request, link_id):
    link = get_object_or_404(DownloadLink, pk=link_id)

    if not request.POST:
        raise Http404()

    link.name = request.POST['name']
    link.save()

    return HttpResponseRedirect(reverse('comicsarchive.archive.link.link_listing', args=(link_id,)))


@login_required
def link_listing(request, link_id):
    link = get_object_or_404(DownloadLink, pk=link_id)

    if link.name.find('(') != -1:
        sliced = link.name[:link.name.find('(')].strip()
    else:
        sliced = link.name

    return render_response(request, 'style2/link_view.html', '',  {'link': link, 'sliced': sliced})


@login_required
def link_topic(request, topic_id, page_number=1):
    topic = get_object_or_404(DownloadTopics, pk=topic_id)
    links = DownloadLink.objects.filter(hidden=False, from_topic=topic)

    paginator = QuerySetPaginator(links, 26)
    page = paginator.page(page_number)

    return render_response(request, 'style2/link_topic.html', '',
        {
        'topic': topic,
        'page': page,
        'paginator': paginator,
        })


