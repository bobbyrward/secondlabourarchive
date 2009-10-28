from comicsarchive.archive.models import DownloadLink, DownloadService, TroubleTicket
import re
import mechanize
import sys
from BeautifulSoup import BeautifulSoup


b = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
b.set_handle_robots(False)


def update_mf(blank_names):
    print 'update_mf'
    for result in blank_names.filter(service=DownloadService.objects.get(id=1)):
        sys.stdout.write('.')
        sys.stdout.flush()
        try:
            b.open(result.url)
            result.name = b.title()
            result.name = result.name.strip()
            if result.name.endswith('.cbr'):
                 result.name = result.name[:-4]

            result.save()
        except KeyboardInterrupt:
            raise
        except:
            continue
    sys.stdout.write('\n')


def update_rs(blank_names):
    print 'update_rs'
    rs_re = re.compile('http://(?:www\.)?rapidshare.com/files/\d+/(.*)(?:\.cbr)?(?:\.html)?')

    for result in blank_names.filter(service=DownloadService.objects.get(id=2)):
        sys.stdout.write('.')
        sys.stdout.flush()
        try:
            result.name = rs_re.match(result.url).group(1)
            result.name = result.name.strip()
            if result.name.endswith('.cbr'):
                 result.name = result.name[:-4]
            result.save()
        except KeyboardInterrupt:
            raise
        except:
            continue
    sys.stdout.write('\n')


def update_zshare(blank_names):
    print 'update_zshare'
    for result in blank_names.filter(service=DownloadService.objects.get(id=3)):
        sys.stdout.write('.')
        sys.stdout.flush()
        try:
            b.open(result.url)
            result.name = b.title()[9:]
            result.name = result.name.strip()
            if result.name.endswith('.cbr'):
                 result.name = result.name[:-4]
            result.save()
        except KeyboardInterrupt:
            raise
        except:
            continue
    sys.stdout.write('\n')


def update_gigasize(blank_names):
    print 'update_gigasize'
    for result in blank_names.filter(service=DownloadService.objects.get(id=4)):
        sys.stdout.write('.')
        sys.stdout.flush()
        try:
            b.open(result.url)
            soup = BeautifulSoup(b.response())
            result.name = soup.find('strong', text='Name').next.next.contents[0]
            result.name = result.name.strip()
            if result.name.endswith('.cbr'):
                 result.name = result.name[:-4]
            result.save()
        except KeyboardInterrupt:
            raise
        except:
            continue
    sys.stdout.write('\n')


def update_sendspace(blank_names):
    print 'update_sendspace'
    for result in blank_names.filter(service=DownloadService.objects.get(id=5)):
        sys.stdout.write('.')
        sys.stdout.flush()
        try:
            b.open(result.url)
            soup = BeautifulSoup(b.response())
            result.name = soup.find('b', text='Name:').next
            result.name = result.name.strip()
            if result.name.endswith('.cbr'):
                 result.name = result.name[:-4]
            result.save()
        except KeyboardInterrupt:
            raise
        except:
             continue
    sys.stdout.write('\n')



def update_mu(blank_names):
    print 'update_mu'
    for result in blank_names.filter(service=DownloadService.objects.get(id=6)):
        sys.stdout.write('.')
        sys.stdout.flush()
        try:
            b.open(result.url)
            soup = BeautifulSoup(b.response())
            result.name = soup.find('b', text='Filename:').next
            result.name = result.name.strip()
            if result.name.endswith('.cbr'):
                result.name = result.name[:-4]
            result.save()
        except KeyboardInterrupt:
            raise
        except:
            continue
    sys.stdout.write('\n')


def update_fileducky(blank_names):
    pass
    # service_id=9


def do_update():
    blank_names = DownloadLink.objects.filter(name='')

    update_mf(blank_names)
    update_rs(blank_names)
    update_zshare(blank_names)
    #update_gigasize(blank_names)
    #update_sendspace(blank_names)
    update_mu(blank_names)
    update_fileducky(blank_names)





