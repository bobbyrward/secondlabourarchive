from django.shortcuts import get_object_or_404
from comicsarchive.archive.models import DownloadService
from django.contrib.auth.decorators import login_required
from comicsarchive.archive.templates import render_response
from django.core.paginator import QuerySetPaginator


@login_required
def service_index(request):
    return render_response(request, 'style2/service_index.html', '/service/')


@login_required
def service_listing(request, service_id, page_number=1):
    service = get_object_or_404(DownloadService, pk=service_id)

    links = service.downloadlink_set.filter(hidden=False)

    paginator = QuerySetPaginator(links, 25)
    page = paginator.page(page_number)

    return render_response(request, 'style2/service_view.html', '/service/%s/' % service_id,
        {
        'service': service,
        'page': page,
        'paginator': paginator,
        })




