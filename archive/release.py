from django.shortcuts import get_object_or_404
from comicsarchive.archive.models import DownloadLink
from comicsarchive.archive.models import Release
from django.contrib.auth.decorators import login_required
from comicsarchive.archive.templates import render_response
from django.core import serializers
from django.http import HttpResponse
from comicsarchive.archive.json import json_paginator_response, json_response


@login_required
def add_link_to_release(request, link_id):
    link = get_object_or_404(DownloadLink, pk=link_id)

    return render_response(request, 'style2/add_link_to_release.html', '',  {'link': link})


@login_required
def release_admin(request, release_id):
    release = get_object_or_404(Release, pk=release_id)

    return render_response(request, 'style2/release_admin.html', '', {'release': release})


@login_required
def json_release_children(request, release_id):
    release = get_object_or_404(Release, pk=release_id)

    return json_response(release.downloadlink_set.all(), ('name',))


@login_required
def json_release_add_link(request, release_id, link_id):
    release = get_object_or_404(Release, pk=release_id)
    link = get_object_or_404(DownloadLink, pk=link_id)

    release.downloadlink_set.add(link)

    return HttpResponse('[]', mimetype='text/plain')


@login_required
def json_release_link_search(request, release_id):
    release = get_object_or_404(Release, pk=release_id)

    if 'terms' not in request.GET:
        raise Http404()

    links = DownloadLink.objects.filter(hidden=False).exclude(release=release)

    for term in request.GET['terms'].split():
        links = links.filter(name__icontains=term)

    return json_response(links)


@login_required
def json_release_remove_link(request, release_id, link_id):
    release = get_object_or_404(Release, pk=release_id)
    link = get_object_or_404(DownloadLink, pk=link_id)

    release.downloadlink_set.remove(link)

    return HttpResponse('[]', mimetype='text/plain')


@login_required
def search_releases(request):
    results = Release.objects.all()

    if request.GET:
        for term in request.GET['terms'].split():
            results = results.filter(name__icontains=term)

    data = serializers.serialize("json", results, fields=('id', 'name'))

    return HttpResponse(data, mimetype='application/json')






