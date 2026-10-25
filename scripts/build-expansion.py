"""Render the authored expansion without regenerating or rewriting old articles."""
import csv
import io
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from expansion_content import all_pages, SERVICES, WORKFLOWS, SAMPLES, p, ul

DOMAIN = 'https://www.elixirconsultinggroup.com'
RELEASE_DATE = '2026-10-24'
PAGES = all_pages()
GROUPS = [('/guides/', 'Business Consulting Buying Guides & Industry Workflows',
           'Compare consulting options and work through specific delivery problems with scope guides, decision tables, and industry workflows.',
           ['Buying guide', 'Industry workflow']),
          ('/playbooks/', 'Business Implementation Playbooks',
           'Plan CRM rollout, SOP adoption, management transitions, location expansion, acquisition integration, and sales handover with clear acceptance gates.',
           ['Implementation playbook']),
          ('/examples/', 'Sample Business Operations Reports, Maps & Dashboards',
           'Inspect fictional worked examples of assessment findings, process maps, and weekly dashboards. Download the sample tables and adapt the definitions.',
           ['Sample deliverable']),
          ('/tools/', 'Small Business Operations Calculators',
           'Estimate service capacity, project contribution margin, and rework cost with transparent formulas, editable assumptions, and downloadable results.',
           ['Calculator']),
          ('/compare/', 'Business Consulting & Software Comparisons',
           'Compare operating support, process projects, automation approaches, and CRM or documentation products using practical selection tests.',
           ['Comparison']),
          ('/alternatives/', 'Business Consulting & Software Alternatives',
           'Explore alternatives to executive hires, coaching, operating frameworks, CRM migration, and software choices by the work your team needs.',
           ['Alternatives']),
          ('/pricing/', 'Consulting Pricing & Software Cost Guides',
           'Elixir consulting starts at $5,000 per month. Compare implementation cost drivers, reviewed vendor software prices, billing conditions, and quote requirements.',
           ['Pricing guide']),
          ('/lists/', 'Business Operations Checklists & Curated Shortlists',
           'Use practical lists to evaluate consultants, proposals, CRM trials, documentation tools, operating measures, automation, and location readiness.',
           ['Curated list'])]


def link_list(items):
    return '<ul class="resource-list">' + ''.join('<li><a href="' + escape(x['path']) + '">' + escape(x['title']) + '</a><p>' + escape(x['description']) + '</p></li>' for x in items) + '</ul>'


def hubs():
    pages = []
    for path, title, intro, kinds in GROUPS:
        sections = []
        for kind in kinds:
            label = 'Alternatives guides' if kind == 'Alternatives' else kind + 's'
            sections.append((label, link_list([x for x in PAGES if x['kind'] == kind])))
        sections.append(('Choose one operating problem first', p('Begin with the workflow that is causing missed commitments, repeated approvals, or unreliable reporting. Use the guide to define the decision, the worksheet or example to prepare evidence, and the related service page to understand implementation scope. Test one change before introducing a larger system.')))
        sections.append(('What these resources represent', p('The worked examples are illustrative and the calculators are planning models. They are not client outcomes or industry benchmarks. Service pages explain potential scope and acceptance criteria; specific responsibilities, timing, and fees are agreed in a written proposal.')))
        if path == '/pricing/':
            sections.insert(0, ('How Elixir consulting is priced', p('Elixir scopes consulting fees around the workflow, systems, data, participating teams, pilot, and handover required. Elixir consulting starts at $5,000 per month, with final pricing based on scope. Bring a recent operating example to a consultation and ask for a written scope separating diagnostic work, implementation, ongoing support, and third-party costs. Vendor subscription amounts in the guides below are separate from Elixir fees.')))
            sections.insert(1, ('Existing consulting cost guides', '<ul><li><a href="/guides/operations-consulting-cost/">Operations consulting cost</a></li><li><a href="/guides/sop-documentation-cost/">SOP documentation cost</a></li><li><a href="/guides/crm-implementation-cost-small-business/">CRM implementation cost</a></li><li><a href="/guides/consulting-project-vs-retainer/">Project versus retainer</a></li></ul>'))
        pages.append(dict(path=path, title=title, description=intro, intro=intro, sections=sections,
                          links=['/services/', '/blog/small-business-operations-templates-checklists/'] + [g[0] for g in GROUPS if g[0] != path],
                          kind='Resource hub', parent='/', modified='2026-10-25' if path in ('/compare/', '/alternatives/', '/pricing/', '/lists/') else RELEASE_DATE,
                          listed_items=[dict(name=x['title'], url=x['path']) for x in PAGES if x['kind'] in kinds]))
    return pages


def target(path):
    return ROOT / path.strip('/') / 'index.html'


def patch_section(path, name, content):
    file = target(path)
    if not file.exists():
        raise RuntimeError('Missing contextual linking page: ' + path)
    text = file.read_text()
    if 'href="/expansion.css"' not in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="/expansion.css"></head>')
    start, end = '<!-- expansion:' + name + ':start -->', '<!-- expansion:' + name + ':end -->'
    section = start + '<section class="section expansion-related"><div class="container">' + content + '</div></section>' + end
    if start in text:
        text = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda _: section, text, flags=re.S)
    else:
        assert '</main>' in text, path
        text = text.replace('</main>', section + '</main>', 1)
    file.write_text(text)


def footer_links(text):
    marker = '<!-- expansion:navigation:start -->'
    block = marker + '<li><a href="/guides/">Buying Guides &amp; Workflows</a></li><li><a href="/tools/">Operations Calculators</a></li><li><a href="/playbooks/">Implementation Playbooks</a></li><li><a href="/examples/">Sample Deliverables</a></li><li><a href="/compare/">Comparisons</a></li><li><a href="/alternatives/">Alternatives</a></li><li><a href="/pricing/">Pricing &amp; Costs</a></li><li><a href="/lists/">Checklists &amp; Shortlists</a></li><!-- expansion:navigation:end -->'
    text = re.sub(re.escape(marker) + r'.*?<!-- expansion:navigation:end -->', '', text, flags=re.S)
    needle = '<li><a href="/blog/">Blog</a></li>'
    return re.sub(r'<footer\b.*?</footer>', lambda m: m.group(0).replace(needle, needle + block), text, flags=re.S)


def page_html(page, shell, global_schema, lookup):
    title = page.get('seo_title', page['title']) + ' | Elixir'
    desc = page['description']
    if len(desc) > 158:
        desc = desc[:155].rsplit(' ', 1)[0].rstrip('.,;') + '…'
    path = page['path']
    head = shell
    head = head.replace('<link rel="stylesheet" href="/expansion.css">', '')
    head = re.sub(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + '</title>', head, flags=re.S)
    values = {'description': desc, 'og:title': title, 'og:description': desc, 'og:url': DOMAIN + path,
              'og:type': 'website', 'twitter:title': title, 'twitter:description': desc,
              'twitter:url': DOMAIN + path}

    def meta(match):
        tag = match.group(0)
        key = re.search(r'(?:name|property)=["\']([^"\']+)', tag)
        if key and key.group(1) in values:
            tag = re.sub(r'content=(["\']).*?\1', lambda _: 'content="' + escape(values[key.group(1)], quote=True) + '"', tag)
        return tag

    head = re.sub(r'<meta\b[^>]*>', meta, head)
    head = re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>', '<link rel="canonical" href="' + DOMAIN + path + '">', head)
    if not path.startswith('/services/'):
        head = head.replace(' style="color:#002E5B;font-weight:700" aria-current="page"', '')
    head = re.sub(r'\saria-current="page"', '', head)
    parent = page['parent']
    crumbs = [('/', 'Home')]
    if parent != '/':
        label = lookup.get(parent, {}).get('title', parent.strip('/').replace('-', ' ').title())
        crumbs.append((parent, label))
    crumbs.append((path, page['title']))
    breadcrumb = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': label, 'item': DOMAIN + url}
        for i, (url, label) in enumerate(crumbs)]}
    web = {'@context': 'https://schema.org', '@type': 'WebPage', '@id': DOMAIN + path,
           'url': DOMAIN + path, 'name': page['title'], 'description': desc,
           'isPartOf': {'@id': DOMAIN + '/#website'}, 'inLanguage': 'en-US'}
    schemas = [global_schema, breadcrumb, web]
    if page.get('listed_items'):
        schemas.append({'@context': 'https://schema.org', '@type': 'ItemList', 'name': page['title'],
                        'numberOfItems': len(page['listed_items']), 'itemListElement': [
                            {'@type': 'ListItem', 'position': i + 1, 'name': item['name'], 'url': DOMAIN + item['url']}
                            for i, item in enumerate(page['listed_items'])]})
    if page['kind'] == 'Service':
        schemas.append({'@context': 'https://schema.org', '@type': 'Service', 'name': page['title'],
                        'url': DOMAIN + path, 'description': desc, 'provider': {'@id': DOMAIN + '/#organization'}})
    schemas_html = ''.join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False).replace('<', '\\u003c') + '</script>' for s in schemas)
    asset = '<link rel="stylesheet" href="/expansion.css">'
    if page['kind'] == 'Calculator':
        asset += '<script src="/operations-calculators.js" defer></script>'
    head = head.replace('</head>', asset + schemas_html + '</head>')
    sections = ''.join('<section id="section-' + str(i) + '" aria-labelledby="heading-' + str(i) + '"><h2 id="heading-' + str(i) + '">' + escape(h) + '</h2>' + body + '</section>' for i, (h, body) in enumerate(page['sections']))
    related = []
    for link in page['links']:
        label = lookup[link]['title'] if link in lookup else link.strip('/').split('/')[-1].replace('-', ' ').capitalize()
        related.append('<li><a href="' + link + '">' + escape(label) + '</a></li>')
    sample_slug = path.strip('/').split('/')[-1]
    download = ''
    if sample_slug in SAMPLES:
        download = '<p><a class="btn btn-outline" href="/downloads/' + sample_slug + '-sample.csv" download>Download the illustrative sample CSV</a></p>'
    toc = '<nav class="resource-toc" aria-label="On this page"><h2>On this page</h2><ul>' + ''.join('<li><a href="#section-' + str(i) + '">' + escape(h) + '</a></li>' for i, (h, _) in enumerate(page['sections'])) + '</ul></nav>'
    breadcrumb_html = '<nav class="resource-crumb" aria-label="Breadcrumb"><ol>' + ''.join('<li><a href="' + url + '">' + escape(label) + '</a></li>' if url != path else '<li aria-current="page">' + escape(label) + '</li>' for url, label in crumbs) + '</ol></nav>'
    main = ('<main class="site-main" id="main-content">' + breadcrumb_html
            + '<section class="page-hero"><div class="container"><p class="resource-kicker">' + escape(page['kind']) + '</p><h1>' + escape(page['title']) + '</h1><p>' + escape(page['intro']) + '</p></div></section>'
            + '<div class="container resource-layout">' + toc + '<article class="resource-content">' + download + sections
            + '<section><h2>Related implementation resources</h2><ul>' + ''.join(related) + '</ul></section>'
            + '<section class="resource-cta"><h2>Discuss the operating problem</h2><p>Elixir consulting starts at $5,000 per month, with final pricing based on scope. Bring a recent example, the current workflow, and the person who owns the result to define the appropriate implementation scope.</p><p><a class="btn btn-primary" href="/contact/">Book a consult</a> <a href="/about/">About Elixir and Dr. Connor Robertson</a></p></section>'
            + '</article></div></main>')
    return footer_links(re.sub(r'<main\b.*?</main>', lambda _: main, head, count=1, flags=re.S))


def build():
    pages = PAGES + hubs()
    lookup = {x['path']: x for x in pages}
    assert len(lookup) == len(pages), 'Duplicate expansion paths'
    shell = target('/services/operations/').read_text()
    global_schema = next(json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', shell, re.S) if '"@graph"' in s)
    for page in pages:
        file = target(page['path'])
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(page_html(page, shell, global_schema, lookup))
    for slug, sample in SAMPLES.items():
        stream = io.StringIO(newline='')
        writer = csv.writer(stream)
        writer.writerow(['ILLUSTRATIVE SAMPLE — NOT CLIENT RESULTS'])
        writer.writerow(sample['headings'])
        writer.writerows(sample['rows'])
        (ROOT / 'downloads').mkdir(exist_ok=True)
        (ROOT / 'downloads' / (slug + '-sample.csv')).write_text(stream.getvalue())
    # Add discovery paths while preserving every existing article and page body.
    for file in ROOT.rglob('*.html'):
        if '.git' in file.parts:
            continue
        original = file.read_text()
        updated = footer_links(original)
        if updated != original:
            file.write_text(updated)
    featured = '<h2>Tools, guides, comparisons, and pricing</h2>' + link_list([lookup[group[0]] for group in GROUPS])
    patch_section('/', 'resource-hubs', featured)
    patch_section('/blog/', 'resource-hubs', featured)
    patch_section('/services/', 'specific-services', '<h2>Implementation services by operating problem</h2>' + link_list([x for x in pages if x['kind'] == 'Service']))
    for parent in {s['parent'] for s in SERVICES}:
        children = [lookup['/services/' + s['slug'] + '/'] for s in SERVICES if s['parent'] == parent]
        patch_section('/services/' + parent + '/', 'specific-services', '<h2>Define the implementation you need</h2>' + link_list(children))
    for industry in {w['industry'] for w in WORKFLOWS}:
        children = [lookup['/guides/' + w['slug'] + '/'] for w in WORKFLOWS if w['industry'] == industry]
        patch_section('/industries/' + industry + '/', 'industry-workflows', '<h2>Practical industry workflows</h2>' + link_list(children))
    contexts = {
        '/blog/how-to-write-sops-your-team-will-actually-use/': ['/services/sop-documentation/', '/playbooks/sop-rollout/'],
        '/blog/how-to-map-your-business-processes-from-start-to-finish/': ['/services/business-process-mapping/', '/examples/business-process-map/'],
        '/blog/how-to-build-a-sales-pipeline-that-runs-without-you/': ['/services/sales-process-implementation/', '/playbooks/founder-sales-handoff/'],
        '/blog/the-crm-setup-that-makes-sales-follow-up-automatic/': ['/services/crm-implementation/', '/playbooks/crm-rollout/'],
        '/blog/building-an-operational-dashboard-that-tells-you-what-matters/': ['/services/kpi-dashboard-setup/', '/examples/weekly-operations-dashboard/'],
        '/blog/how-to-reduce-owner-dependency-in-your-business/': ['/services/owner-dependency-reduction/', '/playbooks/operations-manager-first-90-days/'],
        '/blog/when-to-hire-a-fractional-coo-pittsburgh-owner-guide/': ['/guides/fractional-coo-vs-operations-consultant/', '/guides/consultant-vs-operations-manager/'],
        '/blog/roi-of-hiring-business-consultant-real-numbers/': ['/guides/operations-consulting-cost/', '/guides/consulting-project-vs-retainer/'],
        '/blog/ai-implementation-small-business-step-by-step-guide/': ['/services/ai-workflow-implementation/', '/blog/ai-pilot-success-criteria-template/'],
        '/blog/service-business-capacity-planning-template/': ['/tools/service-capacity-calculator/'],
        '/blog/project-margin-review-template-service-firms/': ['/tools/project-margin-calculator/'],
        '/case-studies/construction-operating-cadence/': ['/guides/construction-estimating-to-production-handoff/', '/guides/construction-crew-capacity-planning/'],
        '/case-studies/professional-services-close-rate/': ['/guides/professional-services-scope-to-invoice/', '/services/sales-process-implementation/'],
        '/case-studies/manufacturing-delivery-delays/': ['/guides/manufacturing-production-scheduling-handoff/', '/guides/manufacturing-late-order-recovery/'],
    }
    for path, links in contexts.items():
        resources = [lookup[x] if x in lookup else dict(path=x, title='AI Pilot Success Criteria Template', description='Define output requirements and a controlled pilot before rollout.') for x in links]
        patch_section(path, 'contextual-resources', '<h2>Put the workflow into practice</h2>' + link_list(resources))
    commercial_contexts = {
        '/services/': ['/compare/', '/pricing/', '/lists/questions-before-hiring-operations-consultant/'],
        '/services/operations/': ['/compare/operations-consultant-vs-business-coach/', '/lists/operations-consulting-deliverables/'],
        '/services/sales-strategy/': ['/compare/hubspot-vs-pipedrive/', '/compare/zoho-crm-vs-monday-crm/', '/lists/crm-selection-criteria/'],
        '/services/leadership/': ['/alternatives/full-time-coo/', '/alternatives/eos-small-business/', '/alternatives/business-coaching/'],
        '/services/ai-consulting/': ['/compare/ai-vs-rule-based-automation/', '/pricing/ai-workflow-implementation/', '/lists/workflows-to-automate-first/'],
        '/services/business-strategy/': ['/compare/in-house-vs-outsourced-operations/', '/lists/consulting-engagement-models/'],
        '/services/crm-implementation/': ['/pricing/hubspot-sales-hub/', '/pricing/pipedrive/', '/pricing/zoho-crm/', '/pricing/monday-crm/', '/lists/crm-migration-acceptance-tests/'],
        '/services/crm-cleanup/': ['/compare/crm-cleanup-vs-crm-migration/', '/alternatives/crm-migration/'],
        '/services/sop-documentation/': ['/compare/sop-documentation-vs-process-mapping/', '/lists/sop-documentation-tools/', '/pricing/trainual/'],
        '/services/business-process-mapping/': ['/compare/sop-documentation-vs-process-mapping/', '/lists/handoff-failures-to-check/', '/pricing/process-street/'],
        '/services/kpi-dashboard-setup/': ['/compare/kpi-dashboard-vs-business-intelligence/', '/pricing/kpi-dashboard-implementation/', '/lists/service-business-operating-metrics/'],
        '/services/client-onboarding-systems/': ['/lists/handoff-failures-to-check/', '/compare/trainual-vs-process-street/'],
        '/services/owner-dependency-reduction/': ['/alternatives/full-time-coo/', '/compare/in-house-vs-outsourced-operations/'],
        '/services/multi-location-operations/': ['/lists/systems-before-second-location/'],
        '/guides/operations-consulting-cost/': ['/pricing/', '/lists/consulting-engagement-models/', '/lists/operations-consulting-deliverables/'],
        '/guides/crm-implementation-cost-small-business/': ['/pricing/hubspot-sales-hub/', '/pricing/pipedrive/', '/pricing/zoho-crm/', '/pricing/monday-crm/'],
        '/guides/sop-documentation-cost/': ['/pricing/trainual/', '/pricing/process-street/', '/lists/sop-documentation-tools/'],
        '/guides/fractional-coo-vs-operations-consultant/': ['/alternatives/full-time-coo/', '/compare/in-house-vs-outsourced-operations/'],
        '/blog/how-to-choose-the-right-franchise-for-your-market/': ['/lists/systems-before-second-location/'],
    }
    for path, links in commercial_contexts.items():
        patch_section(path, 'commercial-resources', '<h2>Compare options and plan the cost</h2>' + link_list([lookup[x] for x in links]))
    # Merge our entries; preserve all existing search descriptions and kinds.
    index_file = ROOT / 'search-index.json'
    search = json.loads(index_file.read_text())
    search = [entry for entry in search if entry['u'] not in lookup]
    for page in pages:
        search.append(dict(t=page['title'], u=page['path'], d=page['description'][:150], k=page['kind'],
                           s=' '.join([page['title'], page['description'], page['kind']]).lower()))
    index_file.write_text(json.dumps(search, separators=(',', ':'), ensure_ascii=False))
    urls = ''.join('<url><loc>' + DOMAIN + x['path'] + '</loc><lastmod>' + x.get('modified', RELEASE_DATE) + '</lastmod></url>\n' for x in pages)
    (ROOT / 'sitemap-expansion.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    sitemap_file = ROOT / 'sitemap.xml'
    sitemap = sitemap_file.read_text()
    sitemap = re.sub(r'\s*<sitemap>\s*<loc>' + re.escape(DOMAIN + '/sitemap-expansion.xml') + r'</loc>.*?</sitemap>', '', sitemap, flags=re.S)
    sitemap_file.write_text(sitemap.replace('</sitemapindex>', '<sitemap><loc>' + DOMAIN + '/sitemap-expansion.xml</loc><lastmod>' + RELEASE_DATE + '</lastmod></sitemap>\n</sitemapindex>'))
    manifest = [dict(path=x['path'], title=x['title'], kind=x['kind'], parent=x['parent'], related=x['links'], sources=x.get('sources', [])) for x in pages]
    (ROOT / 'scripts/expansion-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Built {len(pages)} expansion pages, 3 illustrative CSVs, contextual links, search entries, and sitemap.')


if __name__ == '__main__':
    build()
