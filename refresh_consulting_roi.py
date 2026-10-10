"""Apply the authored ROI workbench without regenerating unrelated pages."""
from pathlib import Path
import json, re, html
ROOT=Path(__file__).resolve().parent
slug='roi-of-hiring-business-consultant-real-numbers'
file=ROOT/'blog'/slug/'index.html'
s=file.read_text()
body=(ROOT/'data/consulting-roi-article.html').read_text()
title='Business Consulting ROI Calculator & Proposal Worksheet'
desc='Calculate consulting ROI using contribution margin, cash savings, fees, and implementation costs. Export your assumptions and compare a downside case.'
s,count=re.subn(r'(<article class="article-body" id="post-body">)[\s\S]*?(</article>)',lambda m:m[1]+body+m[2],s,count=1)
assert count==1
old_title=re.search(r'<title>(.*?)</title>',s).group(1)
s=s.replace(old_title,html.escape(title))
for key in ['description','og:description','twitter:description']:
 s=re.sub(r'(<meta (?:name|property)="'+re.escape(key)+r'" content=")[^"]*(")',lambda m:m[1]+html.escape(desc,quote=True)+m[2],s)
s=re.sub(r'(<h1[^>]*>).*?(</h1>)',lambda m:m[1]+title+m[2],s,count=1,flags=re.S)
s=re.sub(r'(article:modified_time" content=")[^"]*',r'\g<1>2026-10-09',s)
s=re.sub(r'<nav class="toc"[\s\S]*?</nav>','',s)
def schema(m):
 d=json.loads(m[1])
 for node in d.get('@graph',[d]):
  if node.get('@type') in ['BlogPosting','Article','WebPage']:
   node['description']=desc
   if 'headline' in node:node['headline']=title
   if 'name' in node:node['name']=title
   node['dateModified']='2026-10-09'
  if node.get('@type')=='FAQPage':
   node['mainEntity']=[{'@type':'Question','name':'How do you calculate consulting ROI?','acceptedAnswer':{'@type':'Answer','text':'Subtract the engagement’s total cost from incremental contribution and separate cash savings over the same period, then divide the net modeled benefit by total cost. State every assumption.'}},{'@type':'Question','name':'Is additional revenue the same as consulting profit?','acceptedAnswer':{'@type':'Answer','text':'No. Subtract the variable costs needed to deliver that revenue. Track owner capacity separately unless it produces documented contribution or cash savings.'}}]
 return '<script type="application/ld+json">'+json.dumps(d)+'</script>'
s=re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',schema,s,flags=re.S)
# Remove the old generated visible FAQ so it cannot contradict the revised article.
s=re.sub(r'<section class="post-faq[^"]*"[\s\S]*?</section>','',s)
s=re.sub(r'(<section class="page-hero">[\s\S]*?</h1>\s*<p>).*?(</p>)',lambda m:m[1]+desc+m[2],s,count=1)
s=s.replace('The ROI of Hiring a Business...', 'Consulting ROI Calculator').replace('<span>1 min read</span>', '<span>5 min read</span>')
s=re.sub(r'<section class="section">\s*<div class="container">\s*<div class="text-center"[^>]*>\s*<span class="eyebrow">Questions</span>\s*<h2>Related Questions</h2>[\s\S]*?</section>','',s,count=1)
file.write_text(s)
sm=ROOT/'sitemap-blog.xml';x=sm.read_text()
url='https://www.elixirconsultinggroup.com/blog/'+slug+'/'
def date(m):
 tail=re.sub(r'<lastmod>.*?</lastmod>','',m[2])
 return m[1]+'<lastmod>2026-10-09</lastmod>'+tail+m[3]
x,count=re.subn(r'(<url>\s*<loc>'+re.escape(url)+r'</loc>)([\s\S]*?)(</url>)',date,x)
assert count==1;sm.write_text(x)
print('Refreshed existing ROI guide and its sitemap date.')
