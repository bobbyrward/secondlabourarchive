from django.core import serializers
from django.utils import simplejson
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder


def json_response(objects, fields=None):
    return HttpResponse(serializers.serialize('json', objects, fields=fields), mimetype='text/plain')


def json_paginator_response(page, fields=None):
    d = {}
    d['end_index'] = page.end_index()
    d['has_next'] = page.has_next()
    d['has_other_pages'] = page.has_other_pages()
    d['has_previous'] = page.has_previous()
    d['next_page_number'] = page.next_page_number()
    d['number'] = page.number
    d['previous_page_number'] = page.previous_page_number()
    d['start_index'] = page.start_index()
    d['total'] = page.paginator.count
    d['object_list'] = serializers.serialize('python', page.object_list, fields=fields)

    return HttpResponse(simplejson.dumps(d, cls=DjangoJSONEncoder, separators=(',',':')), mimetype='text/plain')

