"""Check the generated release, internal discovery graph, and preserved old copy."""
import csv
import argparse
import json
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
arguments = argparse.ArgumentParser()
arguments.add_argument('--compare-ref', help='Optionally verify existing HTML copy against a Git revision.')
OPTIONS = arguments.parse_args()
DOMAIN = 'https://www.elixirconsultinggroup.com'
MANIFEST = json.loads((ROOT / 'scripts/expansion-manifest.json').read_text())


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.ids = []
        self.links = []
        self.assets = []
        self.canonicals = []
        self.metas = {}
        self.labels = []
        self.inputs = []

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == 'h1':
            self.h1 += 1
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
        if tag == 'link':
            if a.get('rel') == 'canonical':
                self.canonicals.append(a['href'])
            elif a.get('rel') == 'stylesheet':
                self.assets.append(a['href'])
        if tag == 'script' and 'src' in a:
            self.assets.append(a['src'])
        if tag == 'meta':
            self.metas[a.get('name', a.get('property', ''))] = a.get('content', '')
        if tag == 'label':
            self.labels.append(a.get('for'))
        if tag == 'input':
            self.inputs.append(a)


def file_for(path):
    t = ROOT / path.lstrip('/')
    return t if t.is_file() else t / 'index.html'


def parsed(file):
    parser = Page()
    text = file.read_text()
    parser.feed(text)
    return text, parser


ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
sitemap_urls = [x.text for x in ET.parse(ROOT / 'sitemap-expansion.xml').iter(ns + 'loc')]
assert len(sitemap_urls) == len(set(sitemap_urls)) == 43
assert DOMAIN + '/sitemap-expansion.xml' in [x.text for x in ET.parse(ROOT / 'sitemap.xml').iter(ns + 'loc')]
search = json.loads((ROOT / 'search-index.json').read_text())
search_counts = Counter(entry['u'] for entry in search)
paths = {entry['path'] for entry in MANIFEST}
assert len(paths) == 43
titles = set()
descriptions = set()
redirects = json.loads((ROOT / 'vercel.json').read_text())['redirects']
for entry in MANIFEST:
    path = entry['path']
    text, page = parsed(file_for(path))
    assert page.h1 == 1, (path, 'h1 count')
    assert len(page.ids) == len(set(page.ids)), (path, 'duplicate IDs')
    assert page.canonicals == [DOMAIN + path], (path, 'canonical')
    assert page.metas['og:url'] == DOMAIN + path, (path, 'og url')
    assert page.metas['og:type'] == 'website', path
    assert 'noindex' not in page.metas['robots'], path
    assert search_counts[path] == 1 and DOMAIN + path in sitemap_urls, (path, 'discovery')
    assert not any(r['source'] == path for r in redirects), (path, 'redirect collision')
    title = re.search(r'<title>(.*?)</title>', text, re.S).group(1)
    assert title not in titles, (path, 'duplicate title')
    titles.add(title)
    desc = page.metas['description']
    assert 50 <= len(desc) <= 158 and desc not in descriptions, (path, desc)
    descriptions.add(desc)
    assert page.metas['og:description'] == desc and page.metas['twitter:description'] == desc
    assert page.assets.count('/expansion.css') == 1, (path, 'css count')
    assert '<!-- expansion:navigation:start -->' not in text.split('<footer', 1)[0], (path, 'footer links leaked into header')
    for source in page.assets:
        if source.startswith('/'):
            assert file_for(source).is_file(), (path, source)
    for link in page.links:
        url = urlsplit(link)
        if url.netloc and url.netloc != 'www.elixirconsultinggroup.com':
            continue
        if not url.path.startswith('/') and url.path:
            continue
        destination = file_for(url.path) if url.path else file_for(path)
        assert destination.is_file(), (path, link)
        if url.fragment:
            _, dest_page = parsed(destination)
            assert unquote(url.fragment) in dest_page.ids, (path, link, 'missing fragment')
    schemas = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)]
    assert sum(s.get('@type') == 'BreadcrumbList' for s in schemas) == 1, path
    assert sum(s.get('@type') == 'WebPage' for s in schemas) == 1, path
    assert sum(s.get('@type') == 'Service' for s in schemas) == (1 if entry['kind'] == 'Service' else 0), path
    assert not any(s.get('@type') in ('FAQPage', 'BlogPosting', 'Review') for s in schemas), path
    if entry['kind'] == 'Calculator':
        assert len(page.inputs) == 5 and all(i['id'] in page.labels for i in page.inputs), path
        assert 'aria-live="polite"' in text and 'data-export disabled' in text
        assert 'data-calculate disabled' in text and '<noscript>' in text
    if entry['kind'] == 'Sample deliverable':
        assert 'fictional' in text.lower() and 'sample.csv' in text, path

# Every new URL must have an inbound link beyond sitewide footer navigation.
incoming = Counter()
for file in ROOT.rglob('index.html'):
    if '.git' in file.parts:
        continue
    text = file.read_text()
    text = re.sub(r'<!-- expansion:navigation:start -->.*?<!-- expansion:navigation:end -->', '', text, flags=re.S)
    page = Page()
    page.feed(text)
    source = '/' + file.parent.relative_to(ROOT).as_posix().strip('./') + '/'
    for link in set(page.links):
        destination = urlsplit(link).path
        if destination in paths and destination != source:
            incoming[destination] += 1
assert all(incoming[path] for path in paths), [path for path in paths if not incoming[path]]
for file in (ROOT / 'downloads').glob('*-sample.csv'):
    with file.open(newline='') as source:
        rows = list(csv.reader(source))
    assert 'ILLUSTRATIVE' in rows[0][0] and len(rows) >= 6, file
    assert all(len(row) == len(rows[1]) for row in rows[2:]), file
print(f'PASS: {len(paths)} pages; metadata, canonicals, schemas, assets, local links/fragments, calculator labels, sample disclosures, sitemap/search, and non-footer discovery links.')

if OPTIONS.compare_ref:
    files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', OPTIONS.compare_ref], cwd=ROOT, text=True).splitlines()
    checked = 0
    for name in files:
        if not name.endswith('.html') or not (ROOT / name).exists():
            continue
        old = subprocess.check_output(['git', 'show', OPTIONS.compare_ref + ':' + name], cwd=ROOT, text=True)
        current = (ROOT / name).read_text()
        current = re.sub(r'<!-- expansion:[^>]+:start -->.*?<!-- expansion:[^>]+:end -->', '', current, flags=re.S)
        current = current.replace('<link rel="stylesheet" href="/expansion.css">', '')
        assert current == old, (name, 'copy changed outside marked additions')
        checked += 1
    print(f'PASS: original copy and styles preserved on {checked} existing HTML files.')
