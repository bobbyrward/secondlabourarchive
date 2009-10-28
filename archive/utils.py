from django.shortcuts import get_object_or_404
from comicsarchive.archive.models import DownloadLink
from comicsarchive.archive.models import TroubleTicket
from comicsarchive.archive.models import TroubleTicketType
from django.contrib.auth.decorators import login_required
from comicsarchive.archive.templates import render_response
from django.core.paginator import QuerySetPaginator
from django.contrib.auth.decorators import user_passes_test



@user_passes_test(lambda u: u.is_superuser)
def mislabelled(request):
    ticket_type = TroubleTicketType.objects.get(id=3)
    tickets = TroubleTicket.objects.filter(ticket_type=ticket_type)

    return render_response(request, 'style2/mislabelled.html', '', {'tickets': tickets})


@user_passes_test(lambda u: u.is_superuser)
def addthumb(request, link_id):
    link = get_object_or_404(DownloadLink, pk=link_id)

    if request.POST:
        url = request.POST['thumbnail_url']

        return render_response(request, 'style2/addthumb_complete.html', '', {'link': link})
    else:
        return render_response(request, 'style2/addthumb_form.html', '', {'link': link})





@user_passes_test(lambda u: u.is_superuser)
def blanknames(request):
    links = DownloadLink.objects.filter(name='')

    return render_response(request, 'style2/blanknames.html', '', {'links': links})


@user_passes_test(lambda u: u.is_superuser)
def blankthumbs(request):
    links = DownloadLink.objects.filter(thumbnail='')

    return render_response(request, 'style2/blanknames.html', '', {'links': links})


