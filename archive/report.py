from django.shortcuts import get_object_or_404
from comicsarchive.archive.models import DownloadLink, TroubleTicketType, TroubleTicket
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from comicsarchive.archive.templates import render_response
from django.core.mail import send_mail

def report_link(request, link_id):
    link = get_object_or_404(DownloadLink, pk=link_id)

    if request.POST:
        ticket_type = get_object_or_404(TroubleTicketType, pk=request.POST['type'])

        ticket = TroubleTicket(link=link, ticket_type=ticket_type, from_user=request.user, comments=request.POST['comment'])
        ticket.save()

        email_text = render_to_string('report_email.txt', {'ticket': ticket})

        send_mail('New Trouble Ticket', email_text, 'Second Labour Archive<null@secondlabourarchive.info>',
                ['bobbyrward@gmail.com'], fail_silently=False)

        return render_response(request, 'style2/report_done.html', '')
    else:
        return render_response(request, 'style2/report.html', '', {
            'link': link,
            'ticket_types': TroubleTicketType.objects.filter(id__gt=1)
            })





