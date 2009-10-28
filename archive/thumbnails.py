from django.shortcuts import get_object_or_404
from comicsarchive.archive.models import DownloadLink
from comicsarchive.archive.models import TroubleTicket
from comicsarchive.archive.models import TroubleTicketType
from django.contrib.auth.decorators import login_required
from comicsarchive.archive.templates import render_response
from django.core.paginator import QuerySetPaginator
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.http import HttpResponse, Http404



@user_passes_test(lambda u: u.is_superuser)
def thumbnail_search(request):
    if request.GET:
        pass
    else:
        return render_response(request, 'style2/thumbnail_search_form.html', '')


@user_passes_test(lambda u: u.is_superuser)
def copy_thumbnail(request, dest_link_id):
    if not request.POST:
        raise Http404()

    src_link = get_object_or_404(DownloadLink, pk=request.POST['src_link_id'])
    dest_link = get_object_or_404(DownloadLink, pk=dest_link_id)

    dest_link.thumbnail = src_link.thumbnail
    dest_link.save()

    return HttpResponse('', mimetype='text/plain')


@user_passes_test(lambda u: u.is_superuser)
def thumbnail_search_json(request):
    links = DownloadLink.objects.all()

    if 'terms' in request.GET:
        for term in request.GET['terms'].split():
            links = links.filter(name__icontains=term)
    else:
        raise Http404()

    data = serializers.serialize('json', links[:8], fields=('id','thumbnail'))

    return HttpResponse(data, mimetype='text/plain')


@user_passes_test(lambda u: u.is_superuser)
def thumbnail_search_ajax(request):
    pass


