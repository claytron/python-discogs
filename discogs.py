#!/usr/bin/env python

"""Python interface to the Discogs music information database."""

import urllib, urllib2, gzip, cStringIO
import xml.etree.ElementTree as ET
from scriptutils.options import Options

DISCOGS_API_KEY = 'f1e79f104f'
MULTI_DELIMITER = ' / '

def urlopen_gzip(url): #{{{1
    req = urllib2.Request(url)
    req.add_header('Accept-Encoding', 'gzip')
    data = urllib2.urlopen(req).read()
    return gzip.GzipFile(fileobj=cStringIO.StringIO(data))

def get_options(): #{{{1
    opts = Options()
    opts.add_option('-v', '--verbose', action='store_true', default=False, help='Be verbose.')
    opts.add_option('-r', '--release', help='Set release.')
    opts.add_option('-q', '--query', help='Display a specific attribute.')
    return opts.parse_args()

def main(): #{{{1
    opts, args = get_options()
    d = Discogs(DISCOGS_API_KEY)
    if opts.release:
        release = d.release(opts.release)
        if opts.query:
            query = getattr(release, opts.query)
            if type(query) in (tuple, list):
                print MULTI_DELIMITER.join(query)
            else:
                print query

#}}}1

class Discogs(object): #{{{1

    def __init__(self, api_key):
        self.api_key = api_key
        self.url_base = 'http://www.discogs.com'

    def url(self, operation, operand):
        return '%s/%s/%s?%s' % (
                self.url_base,
                operation,
                urllib.quote_plus(str(operand)),
                urllib.urlencode({'api_key': self.api_key, 'f': 'xml',})
                )

    def root(self, name, value):
        url = self.url(name, value)
        return ET.parse(urlopen_gzip(url)).getroot().find(name)

    def artist(self, artist):
        return Artist(self.root('artist', artist))

    def release(self, release):
        return Release(self.root('release', release))



class DiscogsXML(object): #{{{1

    def __init__(self, root):
        self.root = root
        self.load()

    def load(self):
        pass



class Artist(DiscogsXML): #{{{1

    def load(self):
        self.name = self.root.find('name').text
        self.releases = {}
        for element in self.root.findall('releases/release'):
            if element.get('type') != 'Main': continue
            self.releases[int(element.get('id'))] = element.find('title').text



class Image(DiscogsXML): #{{{1

    def load(self):
        self.height = int(self.root.get('height'))
        self.width = int(self.root.get('width'))
        self.type = self.root.get('type')
        self.url = self.root.get('uri')
        self.url_small = self.root.get('uri150')



class Release(DiscogsXML): #{{{1

    def load(self):
        self.id = int(self.root.get('id'))
        self.genres = []
        self.genres.extend(e.text for e in self.root.findall('genres/genre'))
        self.genres.extend(e.text for e in self.root.findall('styles/style'))
        self.images = [Image(e) for e in self.root.findall('images/image')]

#}}}1

if __name__ == '__main__': main()
