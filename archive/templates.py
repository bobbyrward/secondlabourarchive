from django.template import RequestContext
from django.shortcuts import render_to_response
from comicsarchive.archive.models import DownloadService
from comicsarchive.archive.models import DownloadTopics


def render_response(request, name, path, args=None):
  actual_args = {
          'services': DownloadService.objects.all(),
          'topics': DownloadTopics.objects.filter(crawl=True).order_by('-date'),
          'current_path': request.path,
          'dirinfo': dir(request),
          }

  if args:
    actual_args.update(args)

  return render_to_response(name, actual_args, context_instance=RequestContext(request))


