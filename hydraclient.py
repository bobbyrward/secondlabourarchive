import mechanize
from BeautifulSoup import BeautifulSoup

_0day_base = 'http://<removed>.com/viewtopic.php?f=1&t=%d'


class HydraClient(object):
    def __init__(self):
        self.b = b = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))

        b.set_handle_robots(False)

        b.open('http://<removed>.com/ucp.php?mode=login')
        b.select_form(nr=0)
        b['username'] = 'username'
        b['password'] = 'password'
        b.submit()

    def open0day(self, topic):
        url = _0day_base % topic
        self.b.open(url)


    def soup(self, isHTML=True):
        kwargs = {}

        if isHTML:
            kwargs['convertEntities'] = BeautifulSoup.HTML_ENTITIES

        return BeautifulSoup(self.b.response(), **kwargs)

    def pageLinks(self):
        soup = self.soup()

        return soup.findAll('code')


    def pages(self):
        while 1:
            try:
                yield self.b.follow_link(text='Next')
            except:
                return

    def nextPage(self):
        self.b.follow_link(text='Next')





