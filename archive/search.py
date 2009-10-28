from django.shortcuts import get_object_or_404
from comicsarchive.archive.models import DownloadLink, DownloadService
from django.core.paginator import QuerySetPaginator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from comicsarchive.archive.templates import render_response
from django.db import models


@login_required
def search_results(request, service_id, search_terms, page_number=1):
    results = DownloadLink.objects.filter(hidden=False)

    term_list = search_terms.split('+')

    for term in term_list:
        results = results.filter(name__icontains=term)

    try:
        service = DownloadService.objects.get(id=service_id)
        results = results.filter(service=service)
    except:
        service = None

    paginator = QuerySetPaginator(results, 25)
    page = paginator.page(page_number)

    return render_response(request, 'style2/search_results.html', '', {
        'search_terms': search_terms,
        'service': service,
        'page': page,
        'paginator': paginator,
        'term_list': term_list,
        })


@login_required
def search_form(request):
    if 's' in request.GET:
        results = DownloadLink.objects.filter(hidden=False)
        terms = request.GET['search_terms'].strip()

        if terms:
            terms = '+'.join(terms.split())

        return HttpResponseRedirect(reverse('comicsarchive.archive.search.search_results',
            args=(request.GET['service'], terms,)))
    else:
        return render_response(request, 'style2/search_form.html', '')




