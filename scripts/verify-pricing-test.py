"""Verify the fictional pricing article, artifact and actual generator ingestion.

Run: python3 scripts/verify-pricing-test.py
Optional preservation comparison: --compare-ref <prior Git commit>
This does not run the legacy whole-site generator or contact a network service.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from decimal import Decimal
from fractions import Fraction
import argparse,csv,json,math,re,subprocess,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
SLUG='the-pricing-strategy-that-increased-our-clients-revenue-by-30-percent'
ROUTE='/blog/'+SLUG+'/'
TITLE='Test a Price Change: Revenue, Volume and Contribution'
OLD='The Pricing Strategy That Increased Our Clients’ Revenue by 30 Percent'
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.h1=0;self.ids=[];self.links=[];self.canonical=[];self.meta={};self.schemas=[];self.parts=None;self.rows=[];self.row=None;self.cell=None;self.title='';self.intitle=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h1':self.h1+=1
  if 'id'in a:self.ids.append(a['id'])
  if t=='a'and'href'in a:self.links.append(a['href'])
  if t=='link'and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if t=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
  if t=='script'and a.get('type')=='application/ld+json':self.parts=[]
  if t=='tr':self.row=[]
  if t in ['th','td']:self.cell=[]
  if t=='title':self.intitle=True
 def handle_data(self,d):
  if self.parts is not None:self.parts.append(d)
  if self.cell is not None:self.cell.append(d)
  if self.intitle:self.title+=d
 def handle_endtag(self,t):
  if t in ['th','td']and self.cell is not None:self.row.append(' '.join(''.join(self.cell).split()));self.cell=None
  if t=='tr'and self.row is not None:self.rows.append(self.row);self.row=None
  if t=='script'and self.parts is not None:self.schemas.append(json.loads(''.join(self.parts)));self.parts=None
  if t=='title':self.intitle=False

def article(text):return re.search(r'<article class="article-body" id="post-body">([\s\S]*?)</article>',text).group(1)
def visible(text):return ' '.join(unescape(re.sub('<[^>]+>',' ',text)).split())
def git(ref,file):return subprocess.check_output(['git','show',ref+':'+file],cwd=ROOT,text=True)
args=argparse.ArgumentParser();args.add_argument('--compare-ref');options=args.parse_args()
data=json.loads((ROOT/'data/pricing-test-example.json').read_text());assert data['fictional']is True
cases=data['cases'];assert len(cases)==3
results=[]
for a in cases:
 p=Decimal(a['unit_price']);n=Decimal(a['completed_jobs']);v=Decimal(a['variable_cost_per_job']);fixed=Decimal(a['listed_fixed_costs']);revenue=p*n;cost=v*n;contribution=revenue-cost;results.append((revenue,cost,contribution,contribution-fixed))
assert results==[(20000,8000,12000,4000),(19800,7200,12600,4600),(24200,8800,15400,7400)]
assert (results[1][0]/results[0][0]-1)*100==-1
assert (results[1][2]/results[0][2]-1)*100==5
assert (results[1][3]/results[0][3]-1)*100==15
assert math.ceil(Fraction(20000,110))==182 and 181*110==19910 and 182*110==20020
assert math.ceil(Fraction(12000,70))==172 and 171*70==11970 and 172*70==12040
assert data['revenue_growth_goal_percent']==30 and 20000*Decimal('1.30')==26000
assert math.ceil(Fraction(26000,110))==237 and 236*110==25960 and 237*110==26070
assert data['capacity_jobs']==220 and 237-220==17 and 26000-220*110==1800
text=(ROOT/'blog'/SLUG/'index.html').read_text();p=Page();p.feed(text);body=article(text)
assert p.h1==1 and len(p.ids)==len(set(p.ids))
assert p.canonical==['https://www.elixirconsultinggroup.com'+ROUTE]
assert TITLE in p.title
assert p.meta['og:title']==p.meta['twitter:title']==TITLE
assert p.meta['description']==p.meta['og:description']==p.meta['twitter:description']
assert p.meta['article:published_time']=='2025-08-29' and p.meta['article:modified_time']=='2026-11-21'
post=next(s for s in p.schemas if s.get('@type')=='BlogPosting')
assert post['headline']==TITLE and post['datePublished']=='2025-08-29' and post['dateModified']=='2026-11-21'
assert post['wordCount']==len(visible(body).split())
assert post['timeRequired']=='PT'+str(math.ceil(post['wordCount']/220))+'M'
expected=[['Measure','Baseline','Price-change case'],['Price per completed job','$100','$110'],['Completed jobs','200','180'],['Modeled revenue','$20,000','$19,800'],['Variable cost per job','$40','$40'],['Total variable costs','$8,000','$7,200'],['Contribution before listed fixed costs','$12,000','$12,600'],['Listed fixed costs','$8,000','$8,000'],['Remainder after those fixed costs','$4,000','$4,600']]
assert p.rows==expected,('Displayed table differs',p.rows)
for phrase in ['−1%','5%','15%','182','172','237','17 jobs','not Elixir client results','not an industry benchmark']:
 assert phrase in visible(body),phrase
for link in p.links:
 if link.startswith('#'):assert link[1:]in p.ids,link
 elif link.startswith('/'):
  from urllib.parse import urlsplit
  route=urlsplit(link).path;f=ROOT/route.lstrip('/');assert f.exists()or(f/'index.html').exists(),link
assert OLD not in text and OLD.lower()not in text
rows=list(csv.DictReader((ROOT/'downloads/fictional-pricing-test-scenarios.csv').open(newline='')));assert len(rows)==3
for a,row,result in zip(cases,rows,results):
 assert row['fictional']=='true'and row['scenario']==a['scenario']
 assert [Decimal(row[k])for k in ['price_per_completed_job','completed_jobs','variable_cost_per_job','listed_fixed_costs']]==[a[k]for k in ['unit_price','completed_jobs','variable_cost_per_job','listed_fixed_costs']]
 assert tuple(Decimal(row[k])for k in ['modeled_revenue','total_variable_costs','contribution_before_fixed','remainder_after_listed_fixed'])==result
sitemap=ET.parse(ROOT/'sitemap-blog.xml');entries=sitemap.findall('.//{*}url');entry=next(e for e in entries if e.find('{*}loc').text=='https://www.elixirconsultinggroup.com'+ROUTE);assert entry.find('{*}lastmod').text=='2026-11-21'
search=json.loads((ROOT/'search-index.json').read_text());assert len([r for r in search if r.get('u')==ROUTE])==1
item=next(r for r in search if r.get('u')==ROUTE);assert item['t']==TITLE and item['d']==p.meta['description']
# Execute definitions before the legacy MAIN block, not its whole-site writes.
sys.path.insert(0,str(ROOT));source=(ROOT/'generate_site.py').read_text();prefix=source[:source.index('\n# MAIN\n')];ns={'__file__':str(ROOT/'generate_site.py'),'__name__':'pricing_generator_check'};exec(compile(prefix,'generate_site.py','exec'),ns);ns['SITE_DIR']=str(ROOT)
parsed=ns['parse_existing_post'](SLUG,text)
assert visible(parsed['content'])==visible(body)
assert parsed['title']==TITLE and parsed['date']=='2025-08-29'and parsed['modified']=='2026-11-21'
anchored,_=ns['add_heading_anchors'](parsed['content']);assert visible(anchored)==visible(body)
# Construct only this post's actual template; use cached image dimensions so
# the preservation test cannot make remote image requests or mutate a cache.
ns['_IMAGE_DIMS']={parsed['image']:[1200,630]}
parsed.update(category='Sales & Revenue',url=ROUTE,read_min=math.ceil(len(visible(body).split())/220),excerpt=parsed['description'],og_image=parsed['image'],image_alt=TITLE)
rendered=ns['gen_blog_post'](parsed,[parsed]);assert visible(article(rendered))==visible(body)
again=ns['parse_existing_post'](SLUG,rendered);assert visible(again['content'])==visible(body)and again['modified']=='2026-11-21'
if options.compare_ref:
 oldsearch=json.loads(git(options.compare_ref,'search-index.json'));assert len(oldsearch)==len(search)
 assert sum(a!=b for a,b in zip(oldsearch,search))==1
 oldxml=ET.fromstring(git(options.compare_ref,'sitemap-blog.xml'));assert [e.text for e in oldxml.findall('.//{*}loc')]==[e.text for e in sitemap.findall('.//{*}loc')]
 oldpage=Page();oldpage.feed(git(options.compare_ref,'blog/'+SLUG+'/index.html'));oldpost=next(s for s in oldpage.schemas if s.get('@type')=='BlogPosting');assert oldpost['datePublished']==post['datePublished'] and oldpost['author']==post['author']
print(json.dumps({'pricingArithmetic':'passed','displayedTableCells':'passed','fictionalCsvRows':3,'publicationHistory':'preserved','sitemapOwners':len(entries),'searchEntry':'passed','generatorRoundTrip':'passed','networkInPreservationTest':'none','wordCount':post['wordCount']}))
