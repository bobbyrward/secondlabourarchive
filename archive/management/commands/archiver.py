#!/usr/bin/env python
from __future__ import with_statement

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

from django.core.management import setup_environ

setup_environ(settings)


import os
import re
import datetime
import sys
import logging
import urllib
import socket


import mechanize
import Image
from BeautifulSoup import BeautifulSoup


from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand


from comicsarchive.archive.models import DownloadLink
from comicsarchive.archive.models import DownloadService
from comicsarchive.archive.models import DownloadTopics
from comicsarchive.archive.models import TroubleTicket
from comicsarchive.archive.models import TroubleTicketType
from comicsarchive.hydraclient import HydraClient


# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)



client = HydraClient()

b = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
b.set_handle_robots(False)


rs_re = re.compile('http://(?:www\.)?rapidshare.com/files/\d+/(.*)(?:\.cbr)?(?:\.html)?')


unknown_service = DownloadService.objects.get(id=99)


UNABLE_TO_PARSE = TroubleTicketType.objects.get(id=1)
USER_ME = User.objects.get(id=1)


def log(message, args=()):
    logging.info(message, args)


def create_trouble_ticket(link, comment):
    log('Creating trouble ticket for %s', link.url)
    ticket = TroubleTicket(link=link, ticket_type=UNABLE_TO_PARSE, from_user=USER_ME, comments=comment)
    ticket.save()


def find_link_service(link):
    for service in DownloadService.objects.all():
        if re.match(service.url_re, link):
            log('Found service: %s', service.name)
            return service

    log('Unable to find service: %s', link)
    return unknown_service


def sanitize_name(name):
    log('Name: %s', name)
    name =  name.strip().replace('_.cbr', ')').replace('.cbr', '').replace('___', ') (').replace('__', ' (').replace('_', ' ').title()
    log('Sanitized to: %s', name)
    return name


def get_page_title(url, prefix_chars=0):
    b.open(url)

    title= b.title()

    if prefix_chars:
        title = title[prefix_char:]

    return title


def get_rs_name(url):
    return rs_re.match(url).group(1)


def get_mf_name(url):
    return get_page_title(url)


#def get_zshare_name(blank_names):
#    return get_page_title(url, 9)


#def get_gigasize_name(blank_names):
#    b.open(result.url)
#    return BeautifulSoup(b.response()).find('strong', text='Name').next.next.contents[0]


#def get_sendspace_name(blank_names):
#    b.open(result.url)
#    return BeautifulSoup(b.response()).find('b', text='Name:').next


def get_mu_name(url):
    b.open(url)
    return BeautifulSoup(b.response()).find('b', text='Filename:').next


#def get_fileducky_name(blank_names):
#    raise ValueError



service_name_funcs = { 1: get_mf_name
                     , 2: get_rs_name
                     , 6: get_mu_name
                     }


#                service = find_link_service(link_contents)


def find_name_for_link(link):
    x = link.parent.parent.previous
    i = 0

    while hasattr(x, 'name'):
        x = x.previous
        i += 1

        if i > 24:
            log('unable to find name for link: %s', link)
            return ''

    log('find_name_for_link: %s', x)

    return x


def find_image_for_link(link):
    x = link
    while 1:
        x = x.previous

        if hasattr(x, 'name') and x.name == 'img':
            log('Found thumbnail: %s', x['src'])
            return x['src']

        if not isinstance(x, basestring) and 'class' in x and x['class'] == 'content':
            log('Unable to find thumbnail')
            return ''


def create_thumbnail(url):
    try:
        urllib.urlretrieve(url, '/tmp/archive-image')
        img = Image.open('/tmp/archive-image')
        img.thumbnail((128, 128))
        img.save('/tmp/archive-image-thumbnail.jpeg', 'JPEG')
    except KeyboardInterrupt:
        raise
    except:
        return ''

    return '/tmp/archive-image-thumbnail.jpeg'


def add_link(topic, name, url, text, thumbnail):
    log('Adding link: %s', url)

    service = find_link_service(url)

    if not name and service.id in service_name_funcs:
        name = service_name_funcs[service.id](url)

    name = sanitize_name(name)

    log('Url: %s', url)
    log('Name: %s', name)
    log('Service: %s', service.name)
    log('Thumbnail: %s', thumbnail)

    link = DownloadLink(text=text, name=name, url=url, service=service,
            from_topic=topic)
    link.save()

    if thumbnail:
        filename = create_thumbnail(thumbnail)

        if filename:
            name = os.path.split(thumbnail)[1]
            link.save_thumbnail_file(name, open('/tmp/archive-image-thumbnail.jpeg', 'rb').read())


def parse_link(topic, link):
    link_contents = filter(lambda x: not hasattr(x, 'name'), link.contents)

    if not link_contents:
        log('Link contents EMPTY!')
        return

    for contents in link_contents:
        try:
            DownloadLink.objects.get(url=contents)
        except KeyboardInterrupt:
            raise
        except:
            pass
        else:
            return

    if len(link_contents) == 1:
        name = find_name_for_link(link)
        thumbnail = find_image_for_link(link)

        add_link(topic, name, link_contents[0], link.parent.parent.parent, thumbnail)
    else:
        log('Link contents size = %d', len(link_contents))

        name = find_name_for_link(link)
        thumbnail = find_image_for_link(link)

        for contents in link_contents:
            add_link(topic, name, contents, link.parent.parent.parent, thumbnail)


def do_archive(skip_topics=None):
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filename='logs/archiver-' + datetime.date.today().isoformat() + '.log',
        filemode='a')

    log('Starting crawl')

    for topic in DownloadTopics.objects.order_by('number'):
        if skip_topics and topic.number in skip_topics:
            log('Skipping topic: %s', topic.number)
            continue

        log('Opening topic: %s', topic.number)

        client.open0day(topic.number)

        while 1:
            log('Next Page')

            for link in client.pageLinks():
                parse_link(topic, link)

            try:
                client.nextPage()
            except KeyboardInterrupt:
                raise
            except:
                log('End of Pages')
                break

    log('done')


class Command(NoArgsCommand):
    help = "Runs the archiver script"

    required_model_validation = True
    can_import_settings = True

    def handle_noargs(self, **options):
        do_archive()


if __name__ == '__main__':
    do_archive()




