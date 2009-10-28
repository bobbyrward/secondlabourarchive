from django.contrib.auth.decorators import login_required
from comicsarchive.archive.templates import render_response
from comicsarchive.archive.models import DownloadLink


@login_required
def index(request):
    links = DownloadLink.objects.filter(hidden=False)[:25]
    #return render_response(request, 'home.html', '/', {'links': links})
    return render_response(request, 'style2/home.html', '/', {'links': links})

@login_required
def profile(request):
    return render_response(request, 'style2/profile.html', '')


