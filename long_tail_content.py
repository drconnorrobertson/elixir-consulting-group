"""Authored long-tail guides and downloadable worksheets, retained on rebuild."""
import csv
import io
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOPICS = json.loads((ROOT / 'data/long-tail/topics.json').read_text())
HUB_SLUG = 'small-business-operations-templates-checklists'
SERVICE_NAMES = {'operations': 'operations consulting', 'leadership': 'leadership consulting',
                 'sales-strategy': 'sales systems consulting', 'ai-consulting': 'AI implementation consulting',
                 'business-strategy': 'business strategy consulting'}


def authored_posts():
    posts = []
    for topic in TOPICS:
        slug = topic['slug']
        stream = io.StringIO(newline='')
        writer = csv.writer(stream)
        writer.writerow(['Field', 'Instructions', 'Your entry', 'Owner', 'Due date', 'Status / evidence'])
        writer.writerows([field, instruction, '', '', '', ''] for field, instruction in topic['fields'])
        download = ROOT / 'downloads' / (slug + '.csv')
        download.parent.mkdir(exist_ok=True)
        download.write_text(stream.getvalue(), encoding='utf-8')
        rows = ''.join(f'<tr><th scope="row">{escape(field)}</th><td>{escape(instruction)}</td></tr>'
                       for field, instruction in topic['fields'])
        steps = ''.join(f'<li><p>{escape(step)}</p></li>' for step in topic['steps'])
        related = [p for p in TOPICS if p['service'] == topic['service'] and p['slug'] != slug][:3]
        links = ''.join(f'<li><a href="/blog/{p["slug"]}/">{escape(p["title"])}</a></li>' for p in related)
        body = f'''<p>{escape(topic['intro'])}</p>
<p><a href="/downloads/{slug}.csv" download>Download the editable CSV worksheet</a>. Open it in your spreadsheet application, keep the instructions, and complete the blank entry, owner, due date, and evidence columns. This is a blank planning tool; the example below is illustrative.</p>
<h2>When to use this worksheet</h2><p>Use it with the manager who owns this workflow and one person who performs the work. Bring a recent completed case and a recent exception. Compare the worksheet with those records before adopting it as a team standard. If an existing system already stores these details, use its fields rather than maintaining two competing records.</p>
<h2>Template fields and completion checklist</h2><div style="overflow-x:auto"><table><caption>{escape(topic['title'])}: field guide</caption><thead><tr><th scope="col">Field</th><th scope="col">What to record</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>How to put the process into practice</h2><ol>{steps}</ol>
<h2>Worked example</h2><p>{escape(topic['example'])}</p>
<h2>Common mistake to avoid</h2><p>{escape(topic['failure'])}</p>
<h2>What to measure after implementation</h2><p>{escape(topic['measure'])}</p>
<h2>Review the first completed worksheet</h2><p>Before expanding this process, have the responsible manager check one completed record against the original evidence. Confirm that another team member can understand the next action without asking the author to explain it. Record any missing information as a revision to the worksheet. Choose a review date based on how often the workflow runs; a weekly process gives feedback sooner than a quarterly one.</p>
<h2>Related templates and implementation support</h2><ul>{links}<li><a href="/blog/{HUB_SLUG}/">Browse all business templates and checklists</a></li></ul>
<p>Elixir Consulting Group helps owner-led businesses install practical systems. Explore <a href="/services/{topic['service']}/">{SERVICE_NAMES[topic['service']]}</a> or <a href="/contact/">book a consult</a> to discuss the workflow your team needs to improve.</p>'''
        posts.append(make_post(slug, topic['title'], topic['intro'], body))
    groups = ''
    for service, name in SERVICE_NAMES.items():
        links = ''.join(f'<li><a href="/blog/{t["slug"]}/">{escape(t["title"])}</a><p>{escape(t["intro"])}</p></li>'
                        for t in TOPICS if t['service'] == service)
        groups += f'<h2>{escape(name.capitalize())} templates</h2><ul>{links}</ul>'
    posts.append(make_post(HUB_SLUG, 'Small Business Templates & Operations Checklists',
        'Free business worksheets for capacity planning, sales handoffs, leadership, AI pilots, and project delivery. Includes editable CSV templates and examples.',
        '<p>Choose a practical worksheet for the operating problem in front of your team. Each guide includes field definitions, implementation steps, an illustrative example, a common failure to avoid, and an editable CSV download.</p>'
        '<h2>Choose the right starting point</h2><p>If deadlines keep slipping, start with capacity planning and handoffs. If every decision returns to the owner, use decision rights and coverage planning. If sales reports are unreliable, begin with CRM cleanup and pipeline aging. If automation creates hidden work, define exception handling and pilot acceptance criteria first.</p>'
        '<p>Use one worksheet with real work before introducing several at once. Agree on the responsible manager, the source of evidence, and the first review date. These are adaptable operating tools, not mandatory standards or promises of business results.</p>' + groups +
        '<h2>Need help installing the process?</h2><p>Elixir Consulting Group works with owners and leadership teams on implementation. <a href="/services/">Explore consulting services</a> or <a href="/contact/">discuss your current operating constraint</a>.</p>'))
    return posts


def make_post(slug, title, description, content):
    return dict(slug=slug, title=title, description=description[:157], date='2026-10-24',
                modified='2026-10-24', image='', image_alt='', content=content)
