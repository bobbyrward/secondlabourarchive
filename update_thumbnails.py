from comicsarchive.archive.models import DownloadLink, DownloadService, TroubleTicket
import re
import mechanize
import sys
from BeautifulSoup import BeautifulSoup


def update_link_thumbnail(link):
    soup = BeautifulSoup(link.text)

    imgs = soup.findAll('img')

    if len(imgs) == 1:
        link.thumbnail_url = imgs[0]['src']
        link.save()


def do_update():
    for link in DownloadLink.objects.filter(thumbnail_url=''):
        update_link_thumbnail(link)


