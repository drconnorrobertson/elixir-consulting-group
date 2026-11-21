"""Check the authored support guide and preservation through the real rebuild."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,csv,importlib.util,json,re,shutil,subprocess,sys,tempfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from owner_support_content import business_coach_alternatives,BRIEF_ROWS,brief_csv
ROUTE='/alternatives/business-coaching/';EXTRA='/blog/test-ai-intake-classifier/'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.excluded=[];self.article=False;self.article_text=[];self.excluded_text=[];self.ids=[];self.h1=0;self.meta={};self.canonical=[];self.schemas=[];self.parts=None;self.exclusion_tags=[];self.scope_error=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h1':self.h1+=1
  if 'id'in a:self.ids.append(a['id'])
  if t=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
  if t=='link'and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if 'data-nosnippet'in a:self.exclusion_tags.append(t)
  parent=any(self.excluded);excluded=parent or 'data-nosnippet'in a
  if t=='article'and a.get('class')=='resource-content':self.article=True;self.scope_error|=excluded
  if t=='script'and a.get('type')=='application/ld+json':self.parts=[]
  if t not in ['meta','link','img','input','br','hr','source','area','base','embed','param','track','wbr']:
   self.stack.append(t);self.excluded.append(excluded)
 def handle_data(self,d):
  if self.parts is not None:self.parts.append(d)
  if self.article:self.article_text.append(d);self.scope_error|=any(self.excluded)
  if any(self.excluded):self.excluded_text.append(d)
 def handle_endtag(self,t):
  if t=='script'and self.parts is not None:self.schemas.append(json.loads(''.join(self.parts)));self.parts=None
  if t=='article':self.article=False
  if t in self.stack:
   i=len(self.stack)-1-self.stack[::-1].index(t);self.stack=self.stack[:i];self.excluded=self.excluded[:i]

def check_page(html):
 p=Page();p.feed(html)
 assert p.h1==1 and len(p.ids)==len(set(p.ids))
 assert p.exclusion_tags==['div'] and not p.scope_error,'Article entered excluded snippet scope'
 excluded=' '.join(p.excluded_text);assert 'On this page'in excluded and 'Experienced mentor'not in excluded and 'SCORE'not in excluded
 body=' '.join(p.article_text);assert all(term in body for term in ['SCORE','SBDC','Peer group','Specialist adviser','Implementation consultant','Fractional operating leader','Internal operations manager'])
 assert 'fictional operating example'in body and 'editorial analysis'in body
 assert p.canonical==['https://www.elixirconsultinggroup.com'+ROUTE]
 assert not any(term in p.meta.get('robots','').lower()for term in ['noindex','nosnippet','max-snippet:0'])
 assert p.meta['og:title']==p.meta['twitter:title']==business_coach_alternatives()['seo_title']+' | Elixir'
 assert p.meta['description']==p.meta['og:description']==p.meta['twitter:description']==business_coach_alternatives()['description']
 web=next(s for s in p.schemas if s.get('@type')=='WebPage');assert web['dateModified']=='2026-11-21'
 assert 'https://www.sba.gov/counseling/local-assistance/resource-partners/'in html
 return p

parser=argparse.ArgumentParser();parser.add_argument('--rebuild',action='store_true');args=parser.parse_args()
page=business_coach_alternatives();assert page['modified']==page['revision_date']==page['source_checked_on']=='2026-11-21'
p=check_page((ROOT/ROUTE.lstrip('/')/'index.html').read_text());assert (ROOT/'downloads/owner-support-brief.csv').read_text()==brief_csv()
rows=list(csv.reader((ROOT/'downloads/owner-support-brief.csv').open(newline='')));assert len(rows)==len(BRIEF_ROWS)+1==9 and all(len(row)==3 for row in rows)and all(row[2]==''for row in rows[1:])
spec=importlib.util.spec_from_file_location('builder',ROOT/'scripts/build-expansion.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);pages=m.PAGES+m.hubs();selected=next(p for p in pages if p['path']==ROUTE);assert selected['modified']=='2026-11-21'
xml=(ROOT/'sitemap-expansion.xml').read_text();generated,latest=m.expansion_sitemap(pages,xml);before=ET.fromstring(xml);after=ET.fromstring(generated)
def entries(tree):return {e.find('{*}loc').text:e for e in tree.findall('{*}url')}
a=entries(before);b=entries(after);assert set(a)==set(b)and len(b)==84 and latest=='2026-11-21'
extra='https://www.elixirconsultinggroup.com'+EXTRA;assert ET.tostring(a[extra])==ET.tostring(b[extra])
assert b['https://www.elixirconsultinggroup.com'+ROUTE].find('{*}lastmod').text=='2026-11-21'
# Unknown independently-authored owners must fail review rather than disappear.
bad=xml.replace('</urlset>','<url><loc>https://www.elixirconsultinggroup.com/unreviewed-owner/</loc></url></urlset>')
try:m.expansion_sitemap(pages,bad)
except RuntimeError:pass
else:raise AssertionError('Unknown existing owner was silently discarded')
# An unclosed exclusion wrapper must be detected before it hides the body.
html=(ROOT/ROUTE.lstrip('/')/'index.html').read_text();bad=html.replace('</nav></div><article class="resource-content">','</nav><article class="resource-content">',1);assert bad!=html
try:check_page(bad)
except AssertionError:pass
else:raise AssertionError('Unclosed snippet exclusion was accepted')
rebuilt=False
if args.rebuild:
 with tempfile.TemporaryDirectory(prefix='elixir-owner-support-rebuild-')as directory:
  out=Path(directory);shutil.copytree(ROOT,out,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','__pycache__'))
  kept=(out/EXTRA.lstrip('/')/'index.html').read_bytes();pricing='blog/the-pricing-strategy-that-increased-our-clients-revenue-by-30-percent/index.html';pricing_before=(out/pricing).read_bytes()
  result=subprocess.run([sys.executable,str(out/'scripts/build-expansion.py')],cwd=out,capture_output=True,text=True);assert result.returncode==0,result.stdout+result.stderr
  check_page((out/ROUTE.lstrip('/')/'index.html').read_text())
  rebuilt_map=entries(ET.parse(out/'sitemap-expansion.xml').getroot());assert set(rebuilt_map)==set(a)and ET.tostring(rebuilt_map[extra])==ET.tostring(a[extra])
  assert (out/EXTRA.lstrip('/')/'index.html').read_bytes()==kept
  assert (out/pricing).read_bytes()==pricing_before,'Separate authored pricing guide changed'
  search=json.loads((out/'search-index.json').read_text());assert sum(x['u']==EXTRA for x in search)==1
  root=ET.parse(out/'sitemap.xml');entry=next(e for e in root.findall('.//{*}sitemap')if e.find('{*}loc').text.endswith('/sitemap-expansion.xml'));assert entry.find('{*}lastmod').text=='2026-11-21'
  rebuilt=True
print(json.dumps({'snippetExclusion':'navigation only','allSevenSupportRoutes':'present','briefRows':8,'tableOfContentsAndArticleScope':'passed','sourceRevisionPreserved':'2026-11-21','sitemapOwners':84,'independentOwnerAndDate':'preserved','unknownOwnerNegativeControl':'rejected','unclosedWrapperNegativeControl':'rejected','actualFullRebuild':rebuilt}))
