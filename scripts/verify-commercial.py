"""Editorial and structural checks specific to comparisons, prices, and lists."""
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from commercial_content import commercial_pages, RESEARCH

pages = commercial_pages()
assert Counter(x['kind'] for x in pages) == {'Comparison': 10, 'Alternatives': 8, 'Pricing guide': 8, 'Curated list': 10}
official = {source['url'] for source in RESEARCH['sources'].values()}
assert all(urlsplit(url).scheme == 'https' for url in official)
for page in pages:
    text = (ROOT / page['path'].strip('/') / 'index.html').read_text()
    body = re.search(r'<article class="resource-content">(.*?)</article>', text, re.S).group(1)
    assert len(re.sub('<[^>]+>', ' ', body).split()) >= 300, page['path']
    assert 'book a consult' in body.lower(), page['path']
    for key in page['sources']:
        assert key in RESEARCH['sources'], (page['path'], key)
        assert RESEARCH['sources'][key]['url'] in body, (page['path'], 'source missing from visible copy')
    if page['sources']:
        assert RESEARCH['checked_on'] in body and 'editorial' in body, page['path']
    schemas = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)]
    assert not any(s.get('@type') in ('Review', 'Product', 'AggregateRating', 'Offer') for s in schemas), page['path']
    if page['kind'] == 'Curated list':
        actual = page['listed_items']
        expected_count = int(page['title'].split()[0])
        assert len(actual) == expected_count, page['path']
        schema = next(s for s in schemas if s.get('@type') == 'ItemList')
        assert schema['numberOfItems'] == expected_count and len(schema['itemListElement']) == expected_count
        for i, item in enumerate(actual):
            assert 'id="section-' + str(i + 1) + '"' in body
            assert schema['itemListElement'][i]['name'] == item['name']
            assert schema['itemListElement'][i]['url'].endswith(item['url'])
    if page['kind'] == 'Pricing guide':
        assert 'Elixir' in body and ('scope' in body.lower() or 'scoped' in body.lower())

# Keep quote-only pages explicit and do not silently restore historical prices.
for slug in ('trainual', 'process-street'):
    text = (ROOT / 'pricing' / slug / 'index.html').read_text()
    article = re.search(r'<article class="resource-content">(.*?)</article>', text, re.S).group(1)
    vendor_snapshot = re.search(r'<section id="section-0".*?</section>', article, re.S).group(0)
    assert not re.search(r'\$\s*\d', vendor_snapshot), (slug, 'unverified vendor dollar figure')
    assert 'quote' in article.lower(), slug

# Independently recheck the arithmetic printed in the four subscription examples.
assert 5 * 90 * 12 + 1500 == 6900
assert 5 * 39 * 12 == 2340
assert 5 * 23 * 12 == 1380
assert 10 * 17 * 12 == 2040
for slug, annual in [('hubspot-sales-hub', '$6,900'), ('pipedrive', '$2,340'), ('zoho-crm', '$1,380'), ('monday-crm', '$2,040')]:
    assert annual in (ROOT / 'pricing' / slug / 'index.html').read_text(), slug

hub = (ROOT / 'pricing/index.html').read_text()
assert 'Elixir consulting starts at $5,000 per month' in hub
assert 'Vendor subscription amounts' in hub
print('PASS: 36 commercial pages + 4 hubs; source citations, pricing boundaries, worked budget arithmetic, quote-only handling, list counts, and truthful list markup.')
