from django.contrib.auth.decorators import login_required
from comicsarchive.archive.templates import render_response
from django.core.mail import send_mail


def contact_me(request):
    if not request.POST:
        return render_response(request, 'style2/contact.html', '')
    else:
        text = "From: %s\nSubject: %s\nMessage:\n%s" % (request.user.username,
                request.POST['subject'], request.POST['comment'])

        send_mail('Site Feedback', text, 'Second Labour Archive<null@secondlabourarchive.info>',
                ['bobbyrward@gmail.com'], fail_silently=False)

        return render_response(request, 'style2/contact_done.html', '')
