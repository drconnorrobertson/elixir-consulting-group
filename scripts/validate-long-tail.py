"""Validate published long-tail artifacts without dependencies or network calls."""
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from long_tail_content import TOPICS, HUB_SLUG


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.h1 = 0
        self.canonical = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'h1':
            self.h1 += 1
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs['href'])


slugs = [t['slug'] for t in TOPICS] + [HUB_SLUG]
search = json.loads((ROOT / 'search-index.json').read_text())
urls = {e['u'] for e in search}
sitemap = ET.parse(ROOT / 'sitemap-blog.xml')
locs = {e.text for e in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
titles = set()
for slug in slugs:
    text = (ROOT / 'blog' / slug / 'index.html').read_text()
    page = Page()
    page.feed(text)
    assert page.h1 == 1, (slug, 'h1 count')
    expected = 'https://www.elixirconsultinggroup.com/blog/' + slug + '/'
    assert page.canonical == [expected], (slug, 'canonical')
    assert expected in locs and '/blog/' + slug + '/' in urls, (slug, 'discovery')
    title = re.search(r'<title>(.*?)</title>', text).group(1)
    assert title not in titles, (slug, 'duplicate title')
    titles.add(title)
    for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        json.loads(data)
    for href in page.links:
        if not href.startswith('/') or href.startswith('//'):
            continue
        target = ROOT / href.split('#')[0].split('?')[0].lstrip('/')
        assert target.is_file() or (target / 'index.html').is_file(), (slug, href)
for topic in TOPICS:
    with (ROOT / 'downloads' / (topic['slug'] + '.csv')).open(newline='') as source:
        rows = list(csv.reader(source))
    assert len(rows) == 7 and all(len(row) == 6 for row in rows), topic['slug']
    page = (ROOT / 'blog' / topic['slug'] / 'index.html').read_text()
    assert '/downloads/' + topic['slug'] + '.csv' in page
print(f'PASS: {len(slugs)} pages; unique titles, canonicals, headings, JSON-LD, local links, sitemap/search inclusion; {len(TOPICS)} CSV worksheets.')
