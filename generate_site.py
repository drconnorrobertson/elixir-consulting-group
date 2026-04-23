#!/usr/bin/env python3
"""
Elixir Consulting Group - Static Site Generator
Generates all HTML pages, sitemap.xml, robots.txt, and vercel.json
"""

import os
import json
from datetime import datetime

DOMAIN = "https://elixirconsultinggroup.com"
YEAR = "2026"
DATE_NOW = "2026-04-23"
ADDRESS = "429 Fourth Ave. Suite 300, Pittsburgh, PA 15219"

# ─── Brand Colors & Design Tokens ──────────────────────────────────────
COLORS = {
    "navy": "#002E5B",
    "navy_dark": "#001F3F",
    "navy_light": "#003D7A",
    "gold": "#C9A84C",
    "gold_light": "#D4B96A",
    "white": "#FFFFFF",
    "off_white": "#F8F9FA",
    "light_gray": "#F0F1F0",
    "mid_gray": "#6C757D",
    "dark_gray": "#343A40",
    "text": "#1A1A2E",
    "text_light": "#555555",
    "border": "#E2E8F0",
    "success": "#28A745",
}

# ─── Shared CSS ────────────────────────────────────────────────────────
SHARED_CSS = f"""
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}
body{{font-family:'Inter',system-ui,-apple-system,sans-serif;color:{COLORS['text']};line-height:1.7;background:{COLORS['white']}}}
img{{max-width:100%;height:auto;display:block}}
a{{color:{COLORS['navy']};text-decoration:none;transition:color .2s}}
a:hover{{color:{COLORS['gold']}}}
h1,h2,h3,h4,h5,h6{{font-family:'Inter',system-ui,sans-serif;font-weight:700;line-height:1.2;color:{COLORS['navy']}}}
h1{{font-size:clamp(2rem,5vw,3.2rem);margin-bottom:1rem}}
h2{{font-size:clamp(1.6rem,4vw,2.4rem);margin-bottom:.75rem}}
h3{{font-size:clamp(1.2rem,3vw,1.6rem);margin-bottom:.5rem}}
p{{margin-bottom:1rem;color:{COLORS['text_light']}}}
.container{{max-width:1200px;margin:0 auto;padding:0 24px}}
.btn{{display:inline-block;padding:14px 32px;border-radius:6px;font-weight:600;font-size:1rem;transition:all .3s;cursor:pointer;border:none;text-align:center}}
.btn-primary{{background:{COLORS['navy']};color:{COLORS['white']}}}
.btn-primary:hover{{background:{COLORS['navy_light']};color:{COLORS['white']};transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,46,91,.3)}}
.btn-gold{{background:{COLORS['gold']};color:{COLORS['navy_dark']}}}
.btn-gold:hover{{background:{COLORS['gold_light']};color:{COLORS['navy_dark']};transform:translateY(-2px)}}
.btn-outline{{border:2px solid {COLORS['navy']};color:{COLORS['navy']};background:transparent}}
.btn-outline:hover{{background:{COLORS['navy']};color:{COLORS['white']}}}
.section{{padding:80px 0}}
.section-sm{{padding:50px 0}}
.section-gray{{background:{COLORS['off_white']}}}
.section-navy{{background:{COLORS['navy']};color:{COLORS['white']}}}
.section-navy h2,.section-navy h3,.section-navy p{{color:{COLORS['white']}}}
.text-center{{text-align:center}}
.text-gold{{color:{COLORS['gold']}}}
.eyebrow{{text-transform:uppercase;letter-spacing:2px;font-size:.85rem;font-weight:600;color:{COLORS['gold']};margin-bottom:.5rem;display:block}}
.grid{{display:grid;gap:32px}}
.grid-2{{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}}
.grid-3{{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}}
.grid-4{{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.card{{background:{COLORS['white']};border-radius:12px;padding:32px;box-shadow:0 2px 12px rgba(0,0,0,.06);transition:transform .3s,box-shadow .3s}}
.card:hover{{transform:translateY(-4px);box-shadow:0 8px 30px rgba(0,0,0,.1)}}
.card h3{{margin-bottom:.5rem}}
.card p{{font-size:.95rem}}
.card-icon{{width:56px;height:56px;background:{COLORS['off_white']};border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:16px;font-size:1.5rem}}
.stat-card{{text-align:center;padding:32px 24px}}
.stat-num{{font-size:2.5rem;font-weight:800;color:{COLORS['navy']};display:block}}
.stat-label{{color:{COLORS['mid_gray']};font-size:.9rem}}
.testimonial-card{{border-left:4px solid {COLORS['gold']};padding:28px 32px;background:{COLORS['white']};border-radius:0 12px 12px 0}}
.testimonial-card .quote{{font-style:italic;font-size:1.05rem;color:{COLORS['text']};margin-bottom:12px}}
.testimonial-card .author{{font-weight:600;color:{COLORS['navy']}}}
.testimonial-card .role{{font-size:.85rem;color:{COLORS['mid_gray']}}}
.hero{{position:relative;padding:120px 0 100px;background:linear-gradient(135deg,{COLORS['navy']} 0%,{COLORS['navy_dark']} 100%);color:{COLORS['white']};overflow:hidden}}
.hero::before{{content:'';position:absolute;top:-50%;right:-20%;width:600px;height:600px;background:radial-gradient(circle,rgba(201,168,76,.1) 0%,transparent 70%);border-radius:50%}}
.hero h1{{color:{COLORS['white']};max-width:700px}}
.hero p{{color:rgba(255,255,255,.85);max-width:600px;font-size:1.15rem}}
.hero .btn{{margin-top:24px;margin-right:12px}}
.page-hero{{padding:80px 0 60px;background:linear-gradient(135deg,{COLORS['navy']} 0%,{COLORS['navy_dark']} 100%);color:{COLORS['white']};text-align:center}}
.page-hero h1{{color:{COLORS['white']}}}
.page-hero p{{color:rgba(255,255,255,.8);max-width:600px;margin:0 auto}}
.breadcrumb{{font-size:.85rem;color:rgba(255,255,255,.6);margin-bottom:16px}}
.breadcrumb a{{color:rgba(255,255,255,.7)}}
.breadcrumb a:hover{{color:{COLORS['gold']}}}

/* Header */
.header{{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(255,255,255,.97);backdrop-filter:blur(10px);box-shadow:0 1px 3px rgba(0,0,0,.08);transition:all .3s}}
.header-inner{{display:flex;align-items:center;justify-content:space-between;height:72px;max-width:1200px;margin:0 auto;padding:0 24px}}
.logo{{font-family:'Inter',sans-serif;font-size:1.35rem;font-weight:800;color:{COLORS['navy']};letter-spacing:-.5px}}
.logo span{{color:{COLORS['gold']}}}
nav ul{{display:flex;list-style:none;gap:8px;align-items:center}}
nav a{{padding:8px 16px;font-size:.9rem;font-weight:500;color:{COLORS['text']};border-radius:6px;transition:all .2s}}
nav a:hover{{color:{COLORS['navy']};background:{COLORS['off_white']}}}
nav .btn-primary{{color:{COLORS['white']};padding:10px 24px;font-size:.85rem}}
nav .btn-primary:hover{{background:{COLORS['navy_light']};color:{COLORS['white']}}}
.nav-toggle{{display:none;background:none;border:none;cursor:pointer;padding:8px}}
.nav-toggle span{{display:block;width:24px;height:2px;background:{COLORS['navy']};margin:5px 0;transition:all .3s}}

/* Footer */
.footer{{background:{COLORS['navy_dark']};color:rgba(255,255,255,.7);padding:60px 0 0}}
.footer h4{{color:{COLORS['white']};margin-bottom:16px;font-size:1.1rem}}
.footer a{{color:rgba(255,255,255,.7)}}
.footer a:hover{{color:{COLORS['gold']}}}
.footer ul{{list-style:none}}
.footer li{{margin-bottom:8px}}
.footer-grid{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:32px}}
.footer-bottom{{border-top:1px solid rgba(255,255,255,.1);margin-top:40px;padding:20px 0;text-align:center;font-size:.85rem}}
.footer-desc{{max-width:300px;font-size:.9rem;line-height:1.6}}

/* Blog */
.blog-card{{overflow:hidden;border-radius:12px}}
.blog-card .blog-img{{height:200px;background:{COLORS['navy']};display:flex;align-items:center;justify-content:center;color:{COLORS['gold']};font-size:2.5rem}}
.blog-card .blog-content{{padding:24px}}
.blog-card .blog-date{{font-size:.8rem;color:{COLORS['mid_gray']};margin-bottom:8px}}
.blog-card h3 a{{color:{COLORS['navy']}}}
.blog-card h3 a:hover{{color:{COLORS['gold']}}}

/* FAQ */
.faq-item{{border:1px solid {COLORS['border']};border-radius:8px;margin-bottom:12px;overflow:hidden}}
.faq-q{{padding:20px 24px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;background:{COLORS['white']};transition:background .2s}}
.faq-q:hover{{background:{COLORS['off_white']}}}
.faq-q::after{{content:'+';font-size:1.4rem;color:{COLORS['gold']};font-weight:300;transition:transform .3s}}
.faq-item.active .faq-q::after{{transform:rotate(45deg)}}
.faq-a{{padding:0 24px;max-height:0;overflow:hidden;transition:all .3s ease}}
.faq-item.active .faq-a{{max-height:300px;padding:0 24px 20px}}

/* Process Steps */
.process-step{{display:flex;gap:20px;padding:24px 0;border-bottom:1px solid {COLORS['border']}}}
.process-step:last-child{{border-bottom:none}}
.step-num{{flex-shrink:0;width:48px;height:48px;background:{COLORS['navy']};color:{COLORS['gold']};border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1.1rem}}
.step-content h3{{margin-bottom:4px;font-size:1.1rem}}
.step-content p{{margin-bottom:0;font-size:.95rem}}

/* CTA Banner */
.cta-banner{{background:linear-gradient(135deg,{COLORS['navy']} 0%,{COLORS['navy_dark']} 100%);padding:60px 0;text-align:center;color:{COLORS['white']}}}
.cta-banner h2{{color:{COLORS['white']};margin-bottom:12px}}
.cta-banner p{{color:rgba(255,255,255,.8);margin-bottom:24px;max-width:500px;margin-left:auto;margin-right:auto}}

/* Contact Form */
.form-group{{margin-bottom:20px}}
.form-group label{{display:block;font-weight:600;margin-bottom:6px;font-size:.9rem;color:{COLORS['navy']}}}
.form-group input,.form-group textarea,.form-group select{{width:100%;padding:12px 16px;border:1px solid {COLORS['border']};border-radius:8px;font-size:1rem;font-family:inherit;transition:border-color .2s}}
.form-group input:focus,.form-group textarea:focus{{outline:none;border-color:{COLORS['navy']};box-shadow:0 0 0 3px rgba(0,46,91,.1)}}
.form-group textarea{{resize:vertical;min-height:120px}}
.contact-info-card{{background:{COLORS['off_white']};border-radius:12px;padding:32px;margin-bottom:16px}}
.contact-info-card h3{{font-size:1rem;margin-bottom:4px}}
.contact-info-card p{{margin-bottom:0;color:{COLORS['text_light']}}}

/* Industries */
.industry-card{{position:relative;padding:32px;border-radius:12px;background:{COLORS['white']};border:1px solid {COLORS['border']};transition:all .3s}}
.industry-card:hover{{border-color:{COLORS['gold']};box-shadow:0 4px 20px rgba(0,0,0,.08)}}
.industry-card .ind-icon{{font-size:2rem;margin-bottom:12px}}

/* Responsive */
@media(max-width:968px){{
.footer-grid{{grid-template-columns:1fr 1fr}}
.grid-3{{grid-template-columns:1fr}}
}}
@media(max-width:768px){{
.header-inner{{height:64px}}
.nav-menu{{position:fixed;top:0;right:-100%;width:280px;height:100vh;background:{COLORS['white']};flex-direction:column;padding:80px 32px 32px;box-shadow:-4px 0 20px rgba(0,0,0,.1);transition:right .3s;z-index:999}}
.nav-menu.active{{right:0}}
nav ul{{flex-direction:column;gap:4px;width:100%}}
nav a{{padding:12px 16px;width:100%;display:block}}
.nav-toggle{{display:block;z-index:1000}}
.hero{{padding:80px 0 60px}}
.section{{padding:50px 0}}
.grid-2,.grid-4{{grid-template-columns:1fr}}
.footer-grid{{grid-template-columns:1fr}}
.process-step{{flex-direction:column;text-align:center;align-items:center}}
}}
"""

NAV_ITEMS = [
    ("Home", "/"),
    ("About", "/about/"),
    ("Services", "/services/"),
    ("Industries", "/industries/"),
    ("Case Studies", "/case-studies/"),
    ("Blog", "/blog/"),
    ("FAQ", "/faq/"),
    ("Contact", "/contact/"),
]

# ─── Testimonials ──────────────────────────────────────────────────────
TESTIMONIALS = [
    {"name": "Maria K.", "role": "Operations Director", "text": "Partnering with Elixir Consulting Group was a turning point for our company. They introduced clear workflows and accountability structures that immediately reduced confusion and improved our delivery timelines."},
    {"name": "Tyler S.", "role": "VP of Sales", "text": "Elixir helped us completely rebuild our sales process. Pipeline visibility went from guesswork to structured weekly reviews, and our close rate improved within the first quarter."},
    {"name": "Rachel T.", "role": "Founder & Managing Partner", "text": "Our experience with Elixir exceeded expectations. They implemented systems that broke down silos between departments and gave our leadership team real visibility into what was working and what was not."},
    {"name": "Javed H.", "role": "President", "text": "Working with Elixir reshaped our business foundation. Their approach simplified our operations without stripping away what made us unique. We now run on a weekly cadence that keeps everyone aligned."},
    {"name": "Samantha L.", "role": "COO", "text": "Choosing Elixir was one of our best decisions. They delivered structured systems for onboarding, client communication, and internal reporting that our team adopted quickly and still uses daily."},
    {"name": "Alex J.", "role": "CEO", "text": "Working with Elixir completely changed how we run our business. Their systems created predictability where there was chaos and gave me the ability to step back from day-to-day firefighting."},
    {"name": "David R.", "role": "Managing Director", "text": "The clarity Elixir brought to our operations was remarkable. Within weeks, we had defined roles, clear handoffs, and a meeting rhythm that actually produced decisions instead of more meetings."},
    {"name": "Catherine M.", "role": "VP of Operations", "text": "Elixir did not just give us advice. They sat alongside our team and built the systems with us. The result is a business that runs more smoothly and scales without adding unnecessary complexity."},
]

# ─── FAQ Items ──────────────────────────────────────────────────────────
FAQ_ITEMS = [
    ("What types of businesses does Elixir Consulting Group work with?", "We work with small to mid-sized businesses, typically between $1M and $30M in revenue, across a wide range of industries. Our clients tend to be owner-operated or have small leadership teams that are ready to install more structure and improve execution."),
    ("How is Elixir different from other consulting firms?", "We focus on implementation, not just strategy. Many firms deliver a report and move on. We work alongside your team to build and install the systems, then stay involved to make sure they stick. Our goal is to leave your business running better, not just give you a binder."),
    ("What does the initial engagement look like?", "Every engagement starts with a consult where we learn about your business, goals, and current constraints. From there, we conduct a structured assessment to identify the highest-impact changes. Then we move into implementation where we build the systems with you."),
    ("Do you work with businesses outside of Pittsburgh?", "Yes. While we are proudly based in Pittsburgh, PA, we work with clients remotely across the United States. Our virtual consulting process is structured to be just as effective as in-person work."),
    ("How long does a typical engagement last?", "Most engagements run between 90 days and 6 months depending on the scope. Some clients continue with ongoing advisory support after the initial implementation phase is complete."),
    ("What industries do you specialize in?", "We work across industries including professional services, construction, healthcare, manufacturing, technology, real estate, and retail. Our frameworks are designed to be industry-agnostic because the core operational challenges tend to be universal."),
    ("How much does it cost to work with Elixir Consulting Group?", "Pricing depends on the scope of the engagement and the size of your business. We offer both project-based and retainer-based arrangements. The first step is a consult where we determine if there is a fit before discussing pricing."),
    ("Can you help with AI and technology adoption?", "Yes. We help businesses evaluate and adopt AI tools and digital systems that improve efficiency. This includes AI-powered automation, CRM implementation, workflow digitization, and helping teams integrate technology without disrupting operations."),
    ("What results can I expect?", "Clients typically see improved operational consistency, better sales follow-through, clearer accountability across their teams, and reduced stress for the owner. Specific outcomes depend on where your business is starting from and which systems we install."),
    ("Do you replace our existing team or processes?", "No. We work with your existing team and build on what is already working. Our goal is to strengthen your operations, not replace your people. We help teams become more effective by giving them clearer processes and better cadence."),
    ("How do I get started?", "The first step is to book a consult. You can do that through our contact page or by reaching out directly. During the consult, we will discuss your business and determine if there is a fit for an engagement."),
    ("What is a leadership cadence?", "A leadership cadence is a structured weekly rhythm of meetings, reporting, and priorities that keeps the leadership team aligned and focused on execution. It replaces ad hoc meetings and firefighting with a predictable operating system."),
    ("Do you offer ongoing advisory after the engagement ends?", "Yes. Many clients transition to a monthly advisory arrangement after the initial implementation. This provides continued access to strategic guidance and ensures the systems we built continue to evolve with the business."),
    ("What makes Dr. Connor Robertson qualified to lead Elixir Consulting Group?", "Dr. Connor Robertson brings extensive experience in business strategy, operational growth, and organizational development. He has worked with dozens of businesses to install systems that improve execution and drive measurable results. Learn more at drconnorrobertson.com."),
    ("Can you help us prepare our business for a sale or exit?", "Yes. We help business owners build the systems and documentation needed to increase business value and make the company attractive to buyers. This includes operational cleanup, financial clarity, and reducing owner dependence."),
]

# ─── Blog Posts ─────────────────────────────────────────────────────────
BLOG_POSTS = [
    {
        "slug": "how-ai-is-transforming-small-business-operations-2026",
        "title": "How AI Is Transforming Small Business Operations in 2026",
        "date": "2026-04-15",
        "excerpt": "AI is no longer just for enterprise companies. In 2026, small businesses are leveraging artificial intelligence to automate workflows, improve decision-making, and compete at scale without adding headcount.",
        "content": """<p>The landscape of small business operations has shifted significantly over the past two years. What was once the domain of large enterprises with dedicated IT departments is now accessible to businesses with five employees and a willingness to adopt new tools.</p>
<h2>Where AI Is Making the Biggest Impact</h2>
<p>For most small businesses, the highest-value AI applications fall into three categories: automating repetitive tasks, improving customer communication, and generating actionable insights from existing data.</p>
<p>Repetitive tasks like data entry, invoice processing, appointment scheduling, and email sorting are being handled by AI tools that cost a fraction of what manual labor would. This frees up team members to focus on higher-value activities like client relationships and strategic planning.</p>
<h2>Practical Applications for 2026</h2>
<p>Customer communication is another area seeing rapid improvement. AI-powered chatbots and response systems can handle first-contact inquiries, qualify leads, and route requests to the right team member without human intervention. For businesses that struggle with response time, this alone can improve conversion rates.</p>
<p>Data analysis tools powered by AI can now process financial records, sales data, and operational metrics to surface trends that would take a human analyst hours to identify. Small business owners are using these insights to make better decisions about pricing, inventory, staffing, and marketing spend.</p>
<h2>Getting Started Without Overcomplicating Things</h2>
<p>The biggest mistake businesses make with AI adoption is trying to do too much at once. The most successful implementations start with one specific pain point, implement a solution, measure results, and then expand. At Elixir Consulting Group, we help businesses identify the right starting point and build from there.</p>
<p>The key is not to chase every new tool but to find the ones that solve real problems in your business. When AI is implemented thoughtfully, it becomes a force multiplier that helps small businesses operate with the efficiency of much larger organizations.</p>"""
    },
    {
        "slug": "5-signs-your-business-needs-a-strategy-consultant",
        "title": "5 Signs Your Business Needs a Strategy Consultant",
        "date": "2026-04-08",
        "excerpt": "Not every business needs a consultant, but there are clear signals that indicate when outside expertise could save time, money, and frustration. Here are five signs it is time to bring in help.",
        "content": """<p>Many business owners resist the idea of hiring a consultant because they believe they should be able to figure everything out on their own. That mindset is understandable but often counterproductive. Sometimes the best investment is bringing in someone who has solved the same problems before.</p>
<h2>1. You Are the Bottleneck</h2>
<p>If every decision, approval, or problem resolution runs through you, your business has a structural problem. You have become the single point of failure, and your growth is capped by your personal capacity. A good consultant will help you install systems that distribute decision-making and reduce your involvement in day-to-day operations.</p>
<h2>2. Revenue Is Growing but Profits Are Flat</h2>
<p>This is one of the most common signals. You are closing more deals and taking on more clients, but the bottom line is not improving. This usually points to operational inefficiency, pricing issues, or delivery costs that scale faster than revenue. A strategic review can identify where the margin is leaking.</p>
<h2>3. Your Team Is Busy but Not Productive</h2>
<p>Everyone is working hard, but outcomes are inconsistent. Projects slip, communication breaks down, and the same mistakes keep happening. This is almost always a systems problem, not a people problem. The right consultant will map your workflows and install processes that create consistent execution.</p>
<h2>4. You Cannot Clearly Describe How Your Business Operates</h2>
<p>If someone asked you to explain your sales process, delivery workflow, or client onboarding steps, could you do it clearly and concisely? If not, your business is running on tribal knowledge and improvisation. This makes hiring harder, training slower, and quality inconsistent.</p>
<h2>5. You Know What to Do but Cannot Get It Done</h2>
<p>Many business owners already know what needs to change. The problem is not insight. It is execution. A consultant provides accountability, structure, and the bandwidth to actually implement the changes you have been putting off.</p>
<p>If you recognize yourself in any of these situations, a consult is a low-risk way to start. The goal is not to hand over control but to get the support you need to build a business that runs without depending entirely on you.</p>"""
    },
    {
        "slug": "roi-of-hiring-business-consultant-real-numbers",
        "title": "The ROI of Hiring a Business Consultant: Real Numbers",
        "date": "2026-03-25",
        "excerpt": "Business owners want to know whether hiring a consultant is worth the investment. Here is how to think about ROI in consulting engagements, with real-world benchmarks.",
        "content": """<p>The question every business owner asks before hiring a consultant is simple: will I get my money back? It is a fair question. Consulting engagements are a significant investment, and the return should be measurable.</p>
<h2>How to Measure Consulting ROI</h2>
<p>The ROI of a consulting engagement depends on what you are solving for. The most common areas where businesses see measurable returns include operational cost reduction, revenue acceleration, employee retention improvement, and owner time recaptured.</p>
<p>Operational improvements typically show returns within the first 90 days. When you eliminate redundant processes, reduce errors, and improve handoffs, the savings are direct and quantifiable. Businesses commonly see 15-30% improvement in operational efficiency within the first engagement.</p>
<h2>Revenue Impact</h2>
<p>Sales process improvements often produce the fastest visible ROI. When pipeline visibility improves, follow-up becomes consistent, and close rates increase, the revenue impact compounds quickly. A 10% improvement in close rate on an existing pipeline can generate significant additional revenue without any increase in marketing spend.</p>
<h2>The Hidden ROI: Owner Time</h2>
<p>One of the most undervalued returns is owner time. When a business owner reclaims 10-15 hours per week by delegating decisions to structured systems, that time can be redirected toward growth activities, strategic planning, or personal priorities. The dollar value of that time is substantial.</p>
<p>The businesses that see the highest ROI from consulting are those that implement fully and maintain the systems after the engagement ends. The value compounds over time as teams internalize better habits and processes become second nature.</p>"""
    },
    {
        "slug": "digital-transformation-for-traditional-businesses",
        "title": "Digital Transformation for Traditional Businesses",
        "date": "2026-03-18",
        "excerpt": "Digital transformation does not have to mean a complete technology overhaul. For traditional businesses, the most effective approach is incremental and practical.",
        "content": """<p>Digital transformation has become a buzzword that intimidates many traditional business owners. The phrase conjures images of massive software implementations, expensive consultants, and months of disruption. In reality, effective digital transformation for most businesses is much simpler than that.</p>
<h2>Start with What Hurts Most</h2>
<p>The best digital transformations begin with identifying the biggest operational pain points and solving them with technology. This might mean moving from spreadsheets to a proper CRM, digitizing paper-based workflows, or automating manual reporting processes.</p>
<p>For a construction company, this might look like moving job scheduling from whiteboards to a digital platform. For a professional services firm, it might mean automating time tracking and invoicing. The technology is secondary to the problem being solved.</p>
<h2>Common Wins for Traditional Businesses</h2>
<p>The most impactful digital improvements for traditional businesses tend to be straightforward. Centralized customer data instead of scattered files and spreadsheets. Automated follow-up sequences instead of manual reminders. Digital dashboards instead of end-of-month reports that arrive too late to act on.</p>
<p>These changes do not require a massive budget or a dedicated IT team. They require clarity about what needs to improve and the willingness to adopt better tools.</p>
<h2>Avoiding the Common Mistakes</h2>
<p>The biggest mistake traditional businesses make is buying technology before defining the process it needs to support. Software does not fix broken workflows. It amplifies them. Before investing in any tool, map out what you want the process to look like, then find the technology that fits.</p>
<p>At Elixir Consulting Group, we help businesses navigate this transition without overcomplicating it. The goal is always practical improvement, not technology for its own sake.</p>"""
    },
    {
        "slug": "how-to-scale-your-business-from-1m-to-10m",
        "title": "How to Scale Your Business From $1M to $10M",
        "date": "2026-03-10",
        "excerpt": "The journey from $1M to $10M in revenue requires a different operating system than what got you to your first million. Here is what changes and how to prepare.",
        "content": """<p>Getting a business to $1M in revenue is an achievement that proves the market wants what you offer. But the skills and systems that got you to $1M will not get you to $10M. The transition requires fundamental changes in how the business operates.</p>
<h2>What Changes at $1M</h2>
<p>At $1M, most businesses are still heavily dependent on the founder. The owner is often the top salesperson, the primary relationship manager, and the final decision-maker on everything. This works at smaller scale but becomes the ceiling for growth.</p>
<p>The shift from $1M to $10M requires the owner to move from doing the work to building the systems that allow others to do the work. This is the hardest transition most entrepreneurs face because it requires letting go of control in areas where they have historically excelled.</p>
<h2>The Three Systems You Need</h2>
<p>Three systems need to be in place before you can scale beyond a few million in revenue. First, a repeatable sales process that does not depend on the owner. Second, a delivery system that produces consistent quality without the owner involved in every project. Third, a leadership cadence that creates accountability and visibility across the organization.</p>
<p>Without these three systems, growth creates chaos. Revenue goes up, but so do mistakes, client complaints, and employee turnover. The business becomes harder to run, not easier.</p>
<h2>Building the Team That Scales</h2>
<p>Scaling also requires honest assessment of your team. The people who helped you reach $1M may not be the right people for the next stage. This does not mean they need to leave, but their roles may need to evolve. Investing in leadership development and clear role definitions is critical during this phase.</p>
<p>The businesses that successfully scale from $1M to $10M are the ones that invest in structure before they desperately need it. If you wait until things are breaking, the cost of fixing them is much higher.</p>"""
    },
    {
        "slug": "why-pittsburgh-best-city-business-innovation",
        "title": "Why Pittsburgh Is the Best City for Business Innovation",
        "date": "2026-03-01",
        "excerpt": "Pittsburgh has transformed from a steel town into a hub of innovation, technology, and entrepreneurship. Here is why it is one of the best cities in America to build a business.",
        "content": """<p>Pittsburgh's transformation over the past two decades has been remarkable. What was once defined entirely by its steel industry has become a thriving center for technology, healthcare, robotics, and entrepreneurship. For business owners, the city offers a unique combination of talent, affordability, and infrastructure.</p>
<h2>Talent and Education</h2>
<p>Pittsburgh is home to Carnegie Mellon University and the University of Pittsburgh, two world-class institutions that produce a steady pipeline of skilled graduates in engineering, computer science, business, and healthcare. This talent pool gives local businesses access to qualified candidates that would be harder to attract in more expensive markets.</p>
<h2>Cost Advantage</h2>
<p>Compared to major coastal cities, Pittsburgh offers significantly lower costs for office space, housing, and general business operations. This cost advantage means businesses can invest more in growth and less in overhead. For startups and scaling businesses, this difference can be the margin between survival and success.</p>
<h2>Innovation Ecosystem</h2>
<p>The city's innovation ecosystem continues to expand with accelerators, incubators, and investment groups focused on supporting local businesses. Organizations throughout the region provide mentorship, funding, and networking opportunities that help businesses at every stage.</p>
<p>Pittsburgh's renaissance is not just a story about technology companies. It is about a city that has reinvented itself and created an environment where businesses of all types can thrive. At Elixir Consulting Group, we are proud to be part of this ecosystem and to help Pittsburgh businesses build the systems they need to grow.</p>
<p>For more on Pittsburgh's business landscape, check out <a href="https://thepittsburghwire.com">The Pittsburgh Wire</a> for the latest local business news and development updates.</p>"""
    },
    {
        "slug": "small-business-guide-operational-efficiency",
        "title": "The Small Business Guide to Operational Efficiency",
        "date": "2026-02-20",
        "excerpt": "Operational efficiency is not about working harder. It is about building systems that produce consistent results with less wasted effort. Here is how small businesses can start.",
        "content": """<p>Operational efficiency is one of those terms that sounds corporate and abstract, but for small business owners, it is deeply practical. It means getting more done with the same resources, reducing mistakes, and making your business less dependent on any single person.</p>
<h2>Where to Start</h2>
<p>The first step is understanding where time and effort are being wasted. Most businesses have never mapped their actual workflows. They know what the end result should be, but the steps in between are inconsistent and often depend on whoever happens to be handling the task.</p>
<p>Start by documenting your three most important workflows: how you acquire customers, how you deliver your product or service, and how you handle client communication. Just the act of writing these down often reveals redundancies and gaps.</p>
<h2>The 80/20 of Operations</h2>
<p>Not every process needs to be optimized. Focus on the 20% of your workflows that create 80% of the friction. These are usually the handoff points between team members, the steps that require manual data entry, and the communication gaps that lead to errors.</p>
<p>Simple changes like standardized templates, clear assignment protocols, and weekly check-ins can eliminate a surprising amount of operational friction without requiring any new technology.</p>
<h2>Building a Culture of Consistency</h2>
<p>The hardest part of operational efficiency is not designing the systems. It is getting people to use them consistently. This requires leadership commitment, clear expectations, and regular reinforcement. When the leadership team models disciplined execution, the rest of the organization follows.</p>
<p>At Elixir Consulting Group, we help businesses install operational systems that are simple enough to actually be used and robust enough to scale. The goal is never perfection. It is consistent, reliable execution.</p>"""
    },
    {
        "slug": "ai-tools-every-business-owner-should-use-2026",
        "title": "AI Tools Every Business Owner Should Be Using in 2026",
        "date": "2026-02-10",
        "excerpt": "The AI tool landscape has matured significantly. Here are the categories of AI tools that are delivering real value for business owners right now.",
        "content": """<p>Two years ago, AI tools were mostly experimental for small businesses. Today, several categories of AI applications have matured to the point where they deliver reliable, measurable value. If you are not using at least some of these, you are likely leaving efficiency gains on the table.</p>
<h2>Communication and Content</h2>
<p>AI writing assistants have evolved beyond basic text generation. Modern tools can draft client communications, create proposals from templates, generate meeting summaries, and maintain consistent brand voice across all touchpoints. The time savings for businesses that produce regular content or maintain frequent client communication is substantial.</p>
<h2>Data Analysis and Reporting</h2>
<p>AI-powered analytics tools can now process your financial data, CRM records, and operational metrics to surface insights automatically. Instead of spending hours building reports, business owners can ask questions in natural language and get answers with supporting data. This democratizes data analysis in a way that was not possible even two years ago.</p>
<h2>Customer Service and Communication</h2>
<p>Intelligent chatbots and response systems have reached a level of sophistication where they can handle a significant portion of customer inquiries without human intervention. For businesses that struggle with response time or after-hours support, these tools can improve customer satisfaction while reducing workload.</p>
<h2>Workflow Automation</h2>
<p>AI-enhanced automation platforms can now handle complex, multi-step workflows that previously required manual coordination. From invoice processing to employee onboarding to project management, these tools reduce the administrative burden on small teams.</p>
<p>The key to successful AI adoption is starting with your biggest pain points and implementing tools that solve specific problems. Technology should serve the business, not the other way around.</p>"""
    },
    {
        "slug": "how-to-build-systems-that-scale-without-you",
        "title": "How to Build Systems That Scale Without You",
        "date": "2026-01-28",
        "excerpt": "The ultimate goal of business systems is to make the owner optional for daily operations. Here is how to build processes that work whether you are there or not.",
        "content": """<p>Most business owners started their company because they were good at something. Over time, they became the center of everything. Every question gets directed to them. Every problem lands on their desk. Every decision waits for their approval. This is not a business. It is a job with extra liability.</p>
<h2>The Owner Dependency Problem</h2>
<p>Owner dependency is the single biggest barrier to scaling, selling, or simply enjoying the business you built. When the business cannot function without you for more than a few days, you do not own a company. You own a position that you cannot leave.</p>
<p>Breaking this dependency requires systematically transferring knowledge, decision-making authority, and accountability from the owner to the team and the processes.</p>
<h2>Document Everything Worth Repeating</h2>
<p>If a task happens more than twice, it should have a documented process. This does not mean creating a 50-page manual. It means writing down the essential steps, decision criteria, and quality standards for your core workflows. Keep it simple enough that a new hire could follow it with minimal supervision.</p>
<h2>Build Decision Frameworks, Not Approval Chains</h2>
<p>Instead of requiring your approval for every decision, create frameworks that guide your team. Define the criteria for common decisions, set spending thresholds, and establish escalation rules. When people know the boundaries, they can make good decisions without asking you.</p>
<h2>Install a Weekly Operating Rhythm</h2>
<p>A structured weekly cadence replaces the need for constant check-ins. When every team member knows what they are accountable for, when they report progress, and how issues get escalated, the business runs on rhythm instead of reaction.</p>
<p>Building these systems takes effort upfront, but the payoff is a business that generates value whether you are in the building or on vacation. That is the real definition of a scalable business.</p>"""
    },
    {
        "slug": "business-exit-planning-preparing-profitable-sale",
        "title": "Business Exit Planning: Preparing for a Profitable Sale",
        "date": "2026-01-15",
        "excerpt": "Whether you plan to sell in two years or ten, the work you do now to prepare your business for exit will determine how much it is worth and how smoothly the transition goes.",
        "content": """<p>Exit planning is something most business owners think about eventually but rarely act on early enough. The irony is that the work required to prepare a business for sale is the same work that makes it better to own and operate right now.</p>
<h2>What Buyers Are Looking For</h2>
<p>Buyers want businesses that can operate without the current owner. They want predictable revenue, documented processes, a capable team, and clean financial records. Every one of these factors directly impacts the valuation multiple your business commands.</p>
<p>A business that depends entirely on the owner might sell for 2-3x earnings. A business with strong systems, recurring revenue, and an independent management team might sell for 5-8x or more. The difference in exit value can be millions of dollars.</p>
<h2>Start With Operations</h2>
<p>The first area to address is operational documentation. Can your business run for 30 days without you? If not, that is the gap buyers will see and discount. Build SOPs for every critical function, train your team to manage without you, and create reporting systems that provide visibility without your involvement.</p>
<h2>Financial Clarity</h2>
<p>Clean financials are non-negotiable for a successful exit. This means separating personal expenses from business expenses, maintaining accurate books, and being able to clearly articulate your revenue streams, margins, and growth trajectory.</p>
<h2>Building Transferable Value</h2>
<p>Transferable value means the business holds its worth regardless of who owns it. This comes from systems, brand reputation, customer relationships that belong to the company rather than an individual, and a team that is motivated and capable.</p>
<p>At Elixir Consulting Group, we help business owners build the systems and structure that increase business value whether you plan to sell or not. The result is a more valuable, more enjoyable business to own.</p>"""
    },
    {
        "slug": "how-to-scale-business-500k-to-5m-revenue",
        "title": "How to Scale Your Business From $500K to $5M in Revenue",
        "date": "2026-04-22",
        "excerpt": "Scaling from $500K to $5M is the most dangerous growth phase for any business. Here is the playbook for making that leap without breaking what already works.",
        "content": """<p>The jump from $500K to $5M in revenue is where most businesses either transform or collapse. At $500K, the founder is still doing most of the work. At $5M, the business needs to run on systems, not heroics. The transition between those two points is where the real work happens.</p>
<h2>Why $500K to $5M Is the Hardest Phase</h2>
<p>At half a million in revenue, you have proven the concept. Customers want what you sell. But the infrastructure that got you here, which is usually the founder doing everything, cannot stretch to $5M. You need to hire, delegate, and build repeatable processes before the cracks become crises.</p>
<p>The founder's role must shift from doing the work to designing the systems that allow others to do the work. This is psychologically difficult because the founder's identity is often tied to being the best at the thing the company does.</p>
<h2>The Four Pillars of Scaling to $5M</h2>
<p>First, you need a <strong>repeatable sales engine</strong>. If revenue depends on the founder's relationships and hustle, growth will always be capped. Build a pipeline with defined stages, follow-up cadence, and clear metrics. Your <a href="/services/sales-strategy/">sales strategy</a> needs to work without you in every conversation.</p>
<p>Second, you need <strong>delivery systems that scale</strong>. Document your core service delivery so that quality stays consistent as you add team members. This means SOPs, checklists, and quality gates that do not depend on any single person. Our <a href="/services/operations/">operations consulting</a> is built for exactly this challenge.</p>
<p>Third, you need a <strong>leadership layer</strong>. Somewhere between $1M and $3M, you need people who can make decisions without you. Invest in <a href="/services/leadership/">leadership development</a> early so you are not scrambling to build it when you desperately need it.</p>
<p>Fourth, you need <strong>financial clarity</strong>. At $5M, you cannot afford to guess about margins, cash flow, or profitability by service line. Build dashboards and reporting that give you real-time visibility into the numbers that matter.</p>
<h2>Common Mistakes During This Phase</h2>
<p>The most common mistake is hiring ahead of systems. Adding headcount without clear processes just multiplies chaos. The second most common mistake is the founder refusing to let go of tasks they enjoy but that no longer require their attention. Every hour the founder spends on $20-per-hour tasks is an hour not spent on $500-per-hour activities.</p>
<p>The businesses that successfully scale through this phase are the ones that invest in <a href="/services/business-strategy/">strategic planning</a> and operational structure before the growth forces their hand. If you are approaching this transition, <a href="/contact/">book a consult</a> and let us help you build the foundation for your next stage of growth.</p>"""
    },
    {
        "slug": "ai-implementation-small-business-step-by-step-guide",
        "title": "AI Implementation for Small Business: A Step-by-Step Guide",
        "date": "2026-04-20",
        "excerpt": "AI adoption does not have to be overwhelming. This step-by-step guide shows small business owners how to implement AI tools that deliver real ROI without disrupting operations.",
        "content": """<p>Most small business owners know they should be using AI but feel overwhelmed by the options and unsure where to start. The good news is that effective AI implementation does not require a massive budget, a technical team, or a complete overhaul of your operations. It requires a structured approach and clarity about what problems you are solving.</p>
<h2>Step 1: Identify Your Biggest Time Drains</h2>
<p>Before looking at any tools, list the tasks that consume the most time in your business without producing proportional value. Common culprits include manual data entry, scheduling, email sorting, report generation, and first-response customer communication. These are your highest-ROI automation targets.</p>
<h2>Step 2: Evaluate AI Tools for Your Specific Needs</h2>
<p>The AI tool landscape is massive, but most small businesses only need tools in three or four categories: communication automation, data analysis, workflow automation, and content generation. Do not try to adopt everything at once. Pick the category that addresses your biggest pain point from Step 1.</p>
<p>Our <a href="/services/ai-consulting/">AI consulting</a> team helps businesses navigate this evaluation process so you invest in tools that actually fit your workflow rather than chasing the latest trend.</p>
<h2>Step 3: Start With a Pilot Project</h2>
<p>Choose one workflow and implement AI for that specific process. Measure the results over 30 days before expanding. This approach reduces risk, builds team confidence, and gives you real data about what works in your specific environment.</p>
<h2>Step 4: Train Your Team</h2>
<p>The most common reason AI implementations fail is not the technology. It is adoption. Your team needs to understand why the tool is being introduced, how to use it, and what is expected of them. Structured training and a clear transition plan make the difference between tools that get used and tools that get abandoned.</p>
<h2>Step 5: Scale What Works</h2>
<p>Once your pilot project shows results, expand to the next highest-impact area. Build on what you have learned about your team's adoption patterns and your business's specific needs. Each new implementation gets easier because you have built the change management muscle.</p>
<h2>When to Bring in Expert Help</h2>
<p>If you are not sure where to start, or if previous AI attempts have stalled, working with an experienced <a href="/services/ai-consulting/">AI consulting partner</a> can save months of trial and error. At Elixir Consulting Group, we help businesses implement AI tools that solve real problems and deliver measurable returns. <a href="/contact/">Get in touch</a> to discuss your situation.</p>
<p>As featured on <a href="https://thepittsburghwire.com" target="_blank" rel="noopener">The Pittsburgh Wire</a>, Pittsburgh businesses are leading the way in practical AI adoption for small and mid-sized companies.</p>"""
    },
    {
        "slug": "true-cost-of-not-having-business-strategy",
        "title": "The True Cost of Not Having a Business Strategy",
        "date": "2026-04-17",
        "excerpt": "Operating without a clear business strategy costs more than most owners realize. Here is how to calculate what strategic drift is actually costing your business.",
        "content": """<p>Many business owners operate without a formal strategy. They react to opportunities, fight fires, and rely on instinct to make decisions. This works for a while, especially in the early stages when agility matters more than structure. But as the business grows, the absence of strategy becomes increasingly expensive.</p>
<h2>The Hidden Costs of Strategic Drift</h2>
<p>Without a clear strategy, every decision is made in isolation. Should you hire that person? Should you invest in that tool? Should you pursue that market? Without strategic context, these decisions are based on gut feel, and gut feel does not scale.</p>
<p>The costs show up in several ways. First, <strong>wasted resources</strong>. Without priorities, everything feels urgent, and resources get spread thin across too many initiatives. Second, <strong>missed opportunities</strong>. When you do not know what you are building toward, you cannot recognize the opportunities that matter most. Third, <strong>team confusion</strong>. Without clear direction, your team makes assumptions about what matters, and those assumptions are often wrong.</p>
<h2>What Strategy Actually Looks Like</h2>
<p>Effective <a href="/services/business-strategy/">business strategy</a> is not a 50-page document that sits in a drawer. It is a clear set of priorities, a defined competitive position, and a practical roadmap that connects long-term vision to weekly execution. It should fit on one page and be understood by every member of your leadership team.</p>
<h2>Calculating Your Strategy Gap</h2>
<p>Consider how many hours per week your leadership team spends debating priorities, revisiting decisions, or working on initiatives that do not move the needle. Multiply those hours by their loaded cost. Now add the revenue from deals lost because your team was too scattered to execute well. That number is the cost of not having a strategy.</p>
<p>For most businesses in the $1M to $10M range, this cost runs between $200K and $500K per year in lost productivity, missed opportunities, and inefficient resource allocation. A structured <a href="/services/business-strategy/">strategic planning engagement</a> typically costs a fraction of that and pays for itself within the first quarter.</p>
<p>If your business feels busy but unfocused, a strategy consult is the best investment you can make. <a href="/contact/">Book a conversation</a> with our team and let us help you build the clarity your business needs. Learn more about the founder, <a href="https://drconnorrobertson.com" target="_blank" rel="noopener">Dr. Connor Robertson</a>, and his approach to strategic consulting.</p>"""
    },
    {
        "slug": "pittsburgh-businesses-using-ai-outperform-competitors",
        "title": "How Pittsburgh Businesses Are Using AI to Outperform Competitors",
        "date": "2026-04-14",
        "excerpt": "Pittsburgh has become a national leader in practical AI adoption for small and mid-sized businesses. Here is how local companies are gaining an edge with artificial intelligence.",
        "content": """<p>Pittsburgh's unique combination of world-class research institutions, affordable business costs, and a growing tech ecosystem has created an environment where small and mid-sized businesses are adopting AI faster and more effectively than their counterparts in many larger markets.</p>
<h2>Pittsburgh's AI Advantage</h2>
<p>With Carnegie Mellon University's AI research program consistently ranked among the best in the world and the University of Pittsburgh's strong data science programs, Pittsburgh businesses have access to talent and expertise that would be prohibitively expensive in Silicon Valley or New York. This talent pool means local businesses can implement sophisticated AI solutions at a fraction of the cost.</p>
<p>As reported by <a href="https://thepittsburghwire.com" target="_blank" rel="noopener">The Pittsburgh Wire</a>, the city's AI ecosystem continues to expand, with new startups and established companies alike investing in practical AI applications for businesses of all sizes.</p>
<h2>Real Examples of AI in Pittsburgh Businesses</h2>
<p>A Pittsburgh-based professional services firm implemented AI-powered client communication tools that reduced response time by 60% and improved client satisfaction scores. The system handles initial inquiries, routes complex questions to the right team member, and maintains consistent follow-up without manual intervention.</p>
<p>A regional manufacturer adopted AI-driven quality control that catches defects earlier in the production process, reducing waste by 25% and improving delivery reliability. The system learned from historical data to predict which production runs were most likely to have issues.</p>
<p>A local healthcare practice used AI to streamline patient scheduling and reduce no-shows by 40%. The system analyzes patterns in patient behavior and sends personalized reminders at the optimal time.</p>
<h2>Getting Started With AI in Pittsburgh</h2>
<p>The key to successful AI adoption is starting with a clear problem and a practical solution. Pittsburgh businesses have an advantage because the local ecosystem provides access to experienced <a href="/services/ai-consulting/">AI consultants</a> who understand both the technology and the operational realities of running a business.</p>
<p>At Elixir Consulting Group, we help Pittsburgh businesses evaluate, implement, and optimize AI tools that deliver real returns. Our approach starts with understanding your <a href="/services/operations/">operations</a> and identifying where AI can make the biggest impact with the least disruption. <a href="/contact/">Book a consult</a> to explore how AI can give your business a competitive edge.</p>
<p>Dr. Connor Robertson has also discussed AI adoption strategies for small businesses on <a href="https://www.youtube.com/@TheProspectingShow" target="_blank" rel="noopener">The Prospecting Show</a>, sharing practical frameworks that business owners can apply immediately.</p>"""
    },
    {
        "slug": "when-to-hire-business-consultant-vs-doing-it-yourself",
        "title": "When to Hire a Business Consultant vs. Doing It Yourself",
        "date": "2026-04-10",
        "excerpt": "Not every problem requires outside help. Here is a practical framework for deciding when to hire a consultant and when to handle it internally.",
        "content": """<p>The decision to hire a business consultant is not always straightforward. Some problems are best solved internally, while others benefit enormously from outside expertise. The key is knowing the difference and being honest about where your business stands.</p>
<h2>When to Handle It Yourself</h2>
<p>If the problem is within your existing expertise and you have the bandwidth to solve it, doing it yourself is often the right call. Minor process tweaks, tool adjustments, and incremental improvements to things you already understand well are usually better handled internally. You know your business better than anyone, and small adjustments often just need time and attention.</p>
<h2>When to Hire a Consultant</h2>
<p>There are several situations where outside help pays for itself many times over.</p>
<p><strong>When you lack the expertise.</strong> If you need to build systems you have never built before, such as a structured sales process, an operational cadence, or an AI implementation plan, a consultant who has done it dozens of times will get you there faster and with fewer expensive mistakes. Our <a href="/services/operations/">operations consulting</a> and <a href="/services/sales-strategy/">sales strategy</a> services are built for exactly these situations.</p>
<p><strong>When you are too close to the problem.</strong> Business owners often cannot see the patterns in their own business because they are living inside them every day. An outside perspective can identify issues and opportunities that are invisible from the inside.</p>
<p><strong>When speed matters.</strong> If the cost of delay is high, such as lost revenue, client churn, or a market window closing, a consultant can compress months of learning into weeks of implementation.</p>
<p><strong>When you have tried and failed.</strong> If you have attempted to solve the problem internally and it keeps coming back, the issue is usually structural, not effort-based. A consultant can diagnose the root cause and build a more durable solution.</p>
<h2>How to Choose the Right Consultant</h2>
<p>Look for consultants who focus on implementation, not just advice. Ask for specific examples of results they have delivered. Make sure their approach matches your business size and stage. A framework designed for Fortune 500 companies will not work for a $3M business.</p>
<p>At Elixir Consulting Group, we specialize in working with businesses between $500K and $30M in revenue. We focus on <a href="/services/business-strategy/">practical strategy</a> and hands-on implementation because we know that advice without execution is worthless. <a href="/contact/">Book a consult</a> to discuss whether outside help makes sense for your situation.</p>"""
    },
    {
        "slug": "building-recession-proof-business-strategies",
        "title": "Building a Recession-Proof Business: Strategies That Work",
        "date": "2026-04-07",
        "excerpt": "Economic downturns expose the weaknesses in your business model. Here are the strategies that help businesses not just survive recessions but come out stronger.",
        "content": """<p>No business is completely recession-proof, but some are far more resilient than others. The difference usually comes down to operational discipline, financial clarity, and the ability to adapt quickly. The time to build recession resilience is before you need it.</p>
<h2>Diversify Your Revenue Streams</h2>
<p>Businesses that depend on a single revenue stream or a small number of clients are the most vulnerable in a downturn. If your top three clients represent more than 40% of revenue, you have a concentration risk that needs to be addressed. Building multiple service lines, expanding your client base, and developing recurring revenue models all reduce this vulnerability.</p>
<h2>Build Operational Efficiency Now</h2>
<p>The businesses that struggle most in recessions are the ones running with bloated operations during good times. When revenue drops, they have no margin to absorb the impact. Building <a href="/services/operations/">lean, efficient operations</a> during growth periods gives you the financial cushion to weather downturns without panic layoffs or quality cuts.</p>
<p>This means documenting processes, eliminating waste, and running regular efficiency reviews. It also means investing in automation and <a href="/services/ai-consulting/">AI tools</a> that reduce the labor cost of routine tasks.</p>
<h2>Maintain Financial Reserves</h2>
<p>Businesses should maintain 3 to 6 months of operating expenses in reserve. This is not conservative advice. It is survival strategy. Cash reserves give you the ability to make strategic decisions during a downturn rather than reactive ones.</p>
<h2>Invest in Client Relationships</h2>
<p>During a recession, clients scrutinize every vendor relationship. The businesses that retain clients are the ones that have built genuine relationships and demonstrated consistent value. Your <a href="/services/sales-strategy/">sales and retention systems</a> should be creating touchpoints that reinforce your value long before economic pressure forces clients to make cuts.</p>
<h2>Develop Strategic Agility</h2>
<p>The ability to pivot quickly, whether that means adjusting service offerings, entering new markets, or restructuring operations, separates the businesses that thrive in downturns from those that merely survive. <a href="/services/business-strategy/">Strategic planning</a> should include scenario planning for economic shifts so your leadership team knows what levers to pull when conditions change.</p>
<p>Building recession resilience is not about fear. It is about building a fundamentally stronger business that performs well in any economic environment. <a href="/contact/">Book a consult</a> to discuss how to strengthen your business for whatever comes next.</p>"""
    },
    {
        "slug": "reduce-operating-costs-30-percent-without-cutting-quality",
        "title": "How to Reduce Operating Costs by 30% Without Cutting Quality",
        "date": "2026-04-03",
        "excerpt": "Cutting costs does not have to mean cutting corners. Here is a systematic approach to reducing operating expenses while maintaining or improving service quality.",
        "content": """<p>Most businesses have significant operational waste hidden in their workflows, tool stack, and team structure. The challenge is finding and eliminating that waste without degrading the quality your customers expect. It requires a systematic approach, not across-the-board cuts.</p>
<h2>Start With Process Mapping</h2>
<p>You cannot optimize what you cannot see. The first step is mapping your core workflows end-to-end and identifying where time, money, and effort are being wasted. Common sources of waste include redundant approval steps, manual tasks that could be automated, tools that overlap in functionality, and communication bottlenecks that cause rework.</p>
<p>Our <a href="/services/operations/">operations consulting</a> engagements always start with process mapping because it reveals the specific areas where cost reduction will have the highest impact without affecting quality.</p>
<h2>Automate Repetitive Tasks</h2>
<p>If your team is spending time on tasks that follow the same steps every time, those tasks are candidates for automation. Invoice processing, appointment reminders, data entry, report generation, and routine customer communications can often be automated with <a href="/services/ai-consulting/">AI tools</a> that cost far less than the labor they replace.</p>
<h2>Optimize Your Tool Stack</h2>
<p>Most businesses accumulate software subscriptions over time without regularly evaluating whether each tool is still needed or being used effectively. Conduct a quarterly audit of every tool and subscription. Cancel what is not being used, consolidate tools with overlapping functionality, and negotiate better rates on the tools you keep.</p>
<h2>Restructure Around Outcomes, Not Hours</h2>
<p>Many businesses are structured around keeping people busy rather than producing specific outcomes. When you define clear deliverables and measure output rather than activity, you often find that the same results can be achieved with less effort and fewer resources.</p>
<h2>Invest in Training</h2>
<p>This sounds counterintuitive when you are trying to cut costs, but undertrained employees make more mistakes, work more slowly, and require more supervision. A one-time investment in training often pays for itself within weeks through reduced errors and improved efficiency.</p>
<p>The goal is not to run your business on the cheapest possible budget. It is to eliminate waste so that every dollar you spend is producing value. When done correctly, cost reduction actually improves quality because it forces you to focus on what matters. <a href="/contact/">Get in touch</a> to discuss how we can help you find and eliminate the waste in your operations.</p>"""
    },
    {
        "slug": "executives-guide-digital-transformation-2026",
        "title": "The Executive's Guide to Digital Transformation in 2026",
        "date": "2026-03-28",
        "excerpt": "Digital transformation in 2026 looks different than it did five years ago. Here is what executives need to know to lead their organizations through technology change effectively.",
        "content": """<p>Digital transformation has matured from a buzzword into a business necessity. In 2026, the question is no longer whether to digitize your operations but how to do it in a way that delivers ROI without creating disruption. For executives leading this charge, the approach matters as much as the technology.</p>
<h2>What Digital Transformation Means in 2026</h2>
<p>Five years ago, digital transformation meant moving from paper to digital, adopting cloud software, and building a website. Today, it means integrating AI into core workflows, using data to drive decisions, and building technology infrastructure that scales with your business. The bar has moved, and businesses that are still operating on 2020-era technology are falling behind.</p>
<h2>The Executive's Role</h2>
<p>Digital transformation fails when it is treated as an IT project. It is a business strategy initiative that requires executive sponsorship, clear vision, and organizational change management. The executive's job is not to select the technology but to define the outcomes, allocate the resources, and remove the organizational barriers to adoption.</p>
<p>This is where <a href="/services/leadership/">leadership consulting</a> intersects with technology strategy. The most successful digital transformations are led by executives who understand that technology is a tool for achieving business objectives, not an objective in itself.</p>
<h2>A Practical Framework for 2026</h2>
<p>Start with a technology audit. What tools are you using today, what problems are they solving, and where are the gaps? This audit should include both the formal tech stack and the informal workarounds your team has built, such as spreadsheets, manual processes, and tribal knowledge that should be digitized.</p>
<p>Next, prioritize based on business impact. Not every process needs to be digitized at once. Focus on the workflows that, if improved, would have the biggest impact on revenue, customer experience, or operational efficiency. Our <a href="/services/ai-consulting/">AI consulting</a> team helps executives identify and prioritize these opportunities.</p>
<p>Finally, plan for adoption. The best technology in the world is useless if your team does not use it. Build training programs, set adoption milestones, and create accountability for the transition. <a href="/services/operations/">Operational systems</a> should be redesigned around the new tools, not bolted on top of old processes.</p>
<p>For a deeper dive into how Pittsburgh businesses are approaching digital transformation, check out <a href="https://thepittsburghwire.com" target="_blank" rel="noopener">The Pittsburgh Wire</a> for local business technology coverage. Ready to start your transformation? <a href="/contact/">Book a consult</a> with Elixir Consulting Group.</p>"""
    },
    {
        "slug": "why-most-business-growth-plans-fail-and-how-to-fix",
        "title": "Why Most Business Growth Plans Fail (And How to Fix Yours)",
        "date": "2026-03-22",
        "excerpt": "Most growth plans look great on paper but fail in execution. Here are the most common reasons growth plans stall and a practical framework for building one that actually works.",
        "content": """<p>Every business owner has a growth plan, even if it is only in their head. The problem is that most growth plans fail, not because the strategy is wrong, but because the execution breaks down. Understanding why plans fail is the first step toward building one that works.</p>
<h2>Reason 1: The Plan Is Too Vague</h2>
<p>A growth plan that says "increase revenue by 50%" without specifying how, who, and by when is not a plan. It is a wish. Effective growth plans break down the goal into specific, measurable actions with clear ownership and deadlines. If you cannot describe what your team should be doing differently next week to achieve the plan, it is not specific enough.</p>
<h2>Reason 2: No Accountability Structure</h2>
<p>Plans without accountability are plans without teeth. If no one is tracking progress, reviewing results, or adjusting course, the plan will drift within weeks. Building a <a href="/services/leadership/">leadership cadence</a> with weekly check-ins on plan progress is the single most important thing you can do to keep a growth plan alive.</p>
<h2>Reason 3: Operations Cannot Support the Growth</h2>
<p>Many businesses set ambitious revenue targets without considering whether their <a href="/services/operations/">operations</a> can handle the additional volume. If your delivery systems are already strained, adding more clients will degrade quality, increase errors, and ultimately hurt retention. Operational capacity should be built ahead of growth, not after the problems start.</p>
<h2>Reason 4: The Plan Does Not Address Sales Systematically</h2>
<p>Growth requires a predictable way to generate and close new business. If your <a href="/services/sales-strategy/">sales process</a> depends on the founder's personal relationships or inconsistent outbound efforts, growth will always be lumpy and unpredictable. A systematic sales process is a prerequisite for any serious growth plan.</p>
<h2>How to Build a Growth Plan That Works</h2>
<p>Start with a clear, honest assessment of where your business is today. What is working? What is broken? Where is the ceiling? From there, define 3 to 5 priorities for the next 90 days that will move the needle. Assign ownership, set measurable targets, and build a weekly review cadence.</p>
<p>At Elixir Consulting Group, we help businesses build <a href="/services/business-strategy/">growth plans</a> that are specific, actionable, and supported by the operational infrastructure needed to execute them. The result is growth that is sustainable, not chaotic. <a href="/contact/">Book a consult</a> to start building your plan.</p>"""
    },
    {
        "slug": "how-to-build-business-that-runs-without-you",
        "title": "How to Build a Business That Runs Without You",
        "date": "2026-03-15",
        "excerpt": "The ultimate test of a well-built business is whether it can operate successfully without the owner's daily involvement. Here is how to get there.",
        "content": """<p>Most business owners dream of a business that runs without them, but few actually build one. The gap between wanting owner independence and achieving it comes down to systems, trust, and a willingness to let go of control. It is achievable, but it requires deliberate effort.</p>
<h2>Why Owner Independence Matters</h2>
<p>A business that depends on the owner for daily operations is not really a business. It is a job with overhead. Owner dependence limits your growth, destroys your quality of life, and dramatically reduces the value of your business if you ever want to sell. Buyers pay premiums for businesses that operate independently because those businesses are lower risk and easier to transfer.</p>
<h2>Step 1: Document Your Decision-Making</h2>
<p>The first step toward owner independence is understanding all the decisions you make in a typical week and determining which ones could be made by someone else with the right framework. Most owners are surprised to find that 70 to 80 percent of their decisions follow patterns that can be documented and delegated.</p>
<p>This is the foundation of effective <a href="/services/operations/">operational systems</a>. When decision criteria are documented, your team can handle situations that currently require your involvement.</p>
<h2>Step 2: Build a Leadership Team</h2>
<p>You cannot run a business without you if there is no one capable of running it in your place. Invest in developing leaders who can manage their areas independently. This means clear role definitions, decision-making authority, and <a href="/services/leadership/">accountability structures</a> that do not route everything back to you.</p>
<h2>Step 3: Install a Weekly Operating Cadence</h2>
<p>A structured weekly rhythm replaces the need for constant owner involvement. When your team knows what to report, when to report it, and how issues get escalated, the business runs on cadence instead of on you. This is the single most impactful change most businesses can make.</p>
<h2>Step 4: Remove Yourself Gradually</h2>
<p>Do not try to step back from everything at once. Choose one area of the business, build the systems and team capability to run it without you, prove it works over 30 to 60 days, then move to the next area. This gradual approach builds confidence for both you and your team.</p>
<h2>Step 5: Measure and Adjust</h2>
<p>Track the metrics that tell you whether the business is performing well without your direct involvement. Revenue, client satisfaction, delivery quality, and team retention should all be stable or improving as you step back. If they are not, the systems need adjustment, not more owner involvement.</p>
<p>Building a business that runs without you is the ultimate expression of good <a href="/services/business-strategy/">business strategy</a>. It creates freedom for the owner, value for the business, and resilience for the organization. <a href="/contact/">Book a consult</a> to start building your path to owner independence.</p>
<p>Learn more about the systems and frameworks we use from <a href="https://drconnorrobertson.com" target="_blank" rel="noopener">Dr. Connor Robertson</a>, founder of Elixir Consulting Group, who has also shared these strategies on <a href="https://www.youtube.com/@TheProspectingShow" target="_blank" rel="noopener">The Prospecting Show</a>.</p>"""
    },
]

# ─── Case Studies ───────────────────────────────────────────────────────
CASE_STUDIES = [
    {
        "title": "Manufacturing Firm Reduces Delivery Delays by 40%",
        "industry": "Manufacturing",
        "challenge": "A 45-person manufacturing company was experiencing chronic delivery delays, inconsistent quality, and growing client complaints. The owner was personally managing every production issue.",
        "solution": "We mapped the entire production workflow, identified three major bottleneck points, and installed a weekly production cadence with clear accountability. SOPs were built for quality checkpoints, and a simple dashboard gave leadership real-time visibility into order status.",
        "results": ["40% reduction in delivery delays within 90 days", "Client complaints dropped by 60%", "Owner reclaimed 12 hours per week", "Team adopted weekly scorecards for ongoing accountability"]
    },
    {
        "title": "Professional Services Firm Doubles Close Rate",
        "industry": "Professional Services",
        "challenge": "A growing consulting firm had strong inbound interest but was closing less than 20% of qualified leads. Follow-up was inconsistent, proposals took too long, and there was no structured sales process.",
        "solution": "We built a five-stage sales pipeline with clear criteria for each stage, standardized proposal templates, and installed a weekly pipeline review cadence. CRM was cleaned up and configured to support the new process.",
        "results": ["Close rate improved from 18% to 38%", "Average proposal turnaround reduced from 5 days to 1 day", "Pipeline visibility enabled better revenue forecasting", "Sales team adopted the process with minimal resistance"]
    },
    {
        "title": "Construction Company Installs Operating Cadence",
        "industry": "Construction",
        "challenge": "A regional construction company with $8M in revenue was growing fast but struggling with project coordination, subcontractor management, and internal communication. The leadership team spent most of their time in reactive mode.",
        "solution": "We installed a leadership cadence with weekly strategic meetings, daily huddles for project managers, and a scorecard system that tracked key metrics across all active projects. Role clarity was established for project handoffs.",
        "results": ["Leadership meetings went from reactive to strategic", "Project handoff errors reduced by 70%", "Subcontractor coordination improved significantly", "Owner was able to focus on business development instead of operations"]
    },
    {
        "title": "Healthcare Practice Streamlines Patient Operations",
        "industry": "Healthcare",
        "challenge": "A multi-location healthcare practice was struggling with inconsistent patient experiences across locations, high staff turnover, and operational complexity that was growing faster than revenue.",
        "solution": "We standardized patient intake and communication workflows across all locations, built onboarding systems for new staff, and created a centralized reporting dashboard. Leadership meetings were restructured around metrics instead of anecdotes.",
        "results": ["Patient satisfaction scores improved by 35%", "New staff onboarding time reduced by 50%", "Operations became consistent across all locations", "Revenue per location increased through better retention"]
    },
]

# ─── Industries ─────────────────────────────────────────────────────────
INDUSTRIES = [
    ("Professional Services", "Consulting firms, agencies, law offices, and accounting practices that need better client delivery and business development systems."),
    ("Construction & Trades", "General contractors, specialty trades, and construction companies that need project coordination, estimating systems, and operational structure."),
    ("Healthcare", "Medical practices, dental offices, therapy clinics, and healthcare organizations that need streamlined patient operations and staff management."),
    ("Manufacturing", "Production facilities and manufacturers that need process optimization, quality systems, and supply chain coordination."),
    ("Technology", "Software companies, IT services, and tech startups that need scalable operations and structured growth frameworks."),
    ("Real Estate", "Brokerages, property managers, and real estate investors that need deal flow systems and operational efficiency."),
    ("Retail & E-Commerce", "Brick-and-mortar retailers and online sellers that need inventory management, customer experience systems, and growth strategy."),
    ("Financial Services", "Wealth management firms, insurance agencies, and financial planners that need client management and compliance-friendly operations."),
]

INDUSTRY_ICONS = ["&#9881;", "&#9879;", "&#9764;", "&#9878;", "&#128187;", "&#127968;", "&#128722;", "&#128176;"]


# ─── Service Page FAQs ──────────────────────────────────────────────────
SERVICE_FAQS = {
    "business-strategy": [
        ("What does business strategy consulting include?", "Our business strategy consulting includes strategic planning, growth roadmaps, competitive analysis, execution frameworks, exit planning, and market positioning. We build practical plans that connect high-level goals to weekly action."),
        ("How long does a business strategy engagement take?", "Most business strategy engagements run 90 days to 6 months depending on complexity. We start with a structured assessment and move into implementation alongside your leadership team."),
        ("Is business strategy consulting worth the investment?", "Businesses without clear strategy typically waste $200K to $500K per year in lost productivity and missed opportunities. A structured strategy engagement typically pays for itself within the first quarter through better focus and execution."),
        ("Do you work with startups or only established businesses?", "We primarily work with businesses between $500K and $30M in revenue. Our frameworks are designed for companies that have proven market fit and are ready to scale with more structure."),
        ("What makes Elixir different from other strategy consultants?", "We focus on implementation, not just advice. Many firms deliver a report and leave. We work alongside your team to build and install the systems, then stay involved to make sure they produce results."),
    ],
    "ai-consulting": [
        ("What AI consulting services does Elixir offer?", "We provide AI readiness assessments, workflow automation, tool selection and implementation, data analysis setup, team training, and digital process design. Our focus is practical AI that solves real business problems."),
        ("How much does AI consulting cost for a small business?", "AI consulting costs vary based on scope, but most small business implementations start with a focused pilot project. The ROI typically exceeds the investment within 60 to 90 days through reduced labor costs and improved efficiency."),
        ("Do I need technical expertise to implement AI?", "No. Our AI consulting is designed for non-technical business owners. We handle the technical evaluation and implementation while training your team to use the tools effectively."),
        ("What AI tools do you recommend for small businesses?", "We do not push specific vendors. We evaluate your needs and recommend tools that fit your workflow, budget, and technical capacity. The right tool depends on what problem you are solving."),
        ("How quickly can we see results from AI implementation?", "Most businesses see measurable results within 30 to 60 days of implementing their first AI tool. We start with high-impact, low-complexity applications to build momentum and demonstrate ROI quickly."),
    ],
    "operations": [
        ("What does operations consulting involve?", "Operations consulting includes process mapping, SOP development, role clarity, tool optimization, hiring and onboarding systems, and weekly operating cadence design. We build the systems that make your business run consistently."),
        ("How do you improve operations without disrupting the business?", "We work alongside your existing team and implement changes incrementally. We do not shut down operations to rebuild them. Changes are introduced in phases so the business continues running smoothly during the transition."),
        ("What results can I expect from operations consulting?", "Clients typically see 15 to 30 percent improvement in operational efficiency, 10 to 15 hours per week reclaimed for the owner, reduced errors, faster onboarding, and more consistent delivery quality."),
        ("Do you work on-site or remotely?", "We work both on-site and remotely depending on the engagement. Our virtual consulting process is structured to be just as effective as in-person work. We serve clients in Pittsburgh and nationwide."),
        ("How do you measure operational improvement?", "We establish baseline metrics at the start of every engagement and track improvements weekly. Common metrics include cycle time, error rates, owner hours spent on operations, and team productivity measures."),
    ],
    "sales-strategy": [
        ("What does sales strategy consulting include?", "Our sales strategy consulting covers offer clarity, pipeline design, follow-up systems, CRM optimization, sales cadence and reporting, and revenue forecasting. We build repeatable sales processes your team can execute consistently."),
        ("Can you help if we already have a CRM?", "Yes. Most businesses have a CRM but are not using it effectively. We configure your existing CRM to support your actual sales process and train your team to use it properly."),
        ("How quickly will we see sales improvement?", "Most clients see measurable improvement in close rates and pipeline velocity within the first 30 to 60 days. Sales process improvements compound quickly because they affect every deal in your pipeline."),
        ("Do you train our sales team?", "Yes. We do not just design the process and hand it off. We train your team on the new systems, run practice sessions, and stay involved during the transition to make sure adoption sticks."),
        ("What size sales team do you work with?", "We work with sales teams of all sizes, from solo founders handling all sales to teams of 20 or more. Our frameworks scale to fit the size and complexity of your sales operation."),
    ],
    "leadership": [
        ("What is leadership consulting?", "Leadership consulting at Elixir focuses on installing practical systems that help leadership teams make better decisions, hold each other accountable, and run the business with clarity. This includes cadence design, scorecards, executive coaching, and succession planning."),
        ("What is a leadership cadence?", "A leadership cadence is a structured weekly rhythm of meetings, reporting, and priorities that keeps the leadership team aligned and focused on execution. It replaces ad hoc meetings and firefighting with a predictable operating system."),
        ("Do you offer executive coaching?", "Yes. We provide one-on-one coaching for owners and executives focused on leadership effectiveness, delegation, strategic thinking, and building teams that operate independently."),
        ("How do you help with accountability?", "We install clear accountability frameworks including scorecards, defined ownership for key metrics, and structured weekly reviews. Every team member knows what they own and how they are measured."),
        ("Can leadership consulting help reduce owner burnout?", "Absolutely. Most owner burnout comes from being involved in too many decisions and carrying too much operational weight. Our leadership systems distribute decision-making and create structures that reduce the daily burden on the owner."),
    ],
}

# ─── Helper Functions ───────────────────────────────────────────────────
def make_header(active_path="/"):
    nav_html = ""
    for label, path in NAV_ITEMS:
        cls = ' style="color:#002E5B;font-weight:700"' if path == active_path else ""
        nav_html += f'<li><a href="{path}"{cls}>{label}</a></li>\n'
    nav_html += f'<li><a href="/contact/" class="btn btn-primary">Book a Consult</a></li>'

    return f"""<header class="header">
<div class="header-inner">
<a href="/" class="logo">Elixir<span>.</span></a>
<nav>
<button class="nav-toggle" onclick="document.querySelector('.nav-menu').classList.toggle('active')" aria-label="Toggle menu">
<span></span><span></span><span></span>
</button>
<ul class="nav-menu">
{nav_html}
</ul>
</nav>
</div>
</header>"""


def make_footer():
    return f"""<footer class="footer">
<div class="container">
<div class="footer-grid">
<div>
<h4>Elixir Consulting Group</h4>
<p class="footer-desc">Business growth, operations, and execution support for owners who want results. Based in Pittsburgh, PA. Serving clients nationwide.</p>
<p style="margin-top:16px;font-size:.85rem">{ADDRESS}</p>
</div>
<div>
<h4>Services</h4>
<ul>
<li><a href="/services/business-strategy/">Business Strategy</a></li>
<li><a href="/services/ai-consulting/">AI Consulting</a></li>
<li><a href="/services/operations/">Operations</a></li>
<li><a href="/services/sales-strategy/">Sales Strategy</a></li>
<li><a href="/services/leadership/">Leadership</a></li>
</ul>
</div>
<div>
<h4>Company</h4>
<ul>
<li><a href="/about/">About</a></li>
<li><a href="/industries/">Industries</a></li>
<li><a href="/case-studies/">Case Studies</a></li>
<li><a href="/blog/">Blog</a></li>
<li><a href="/faq/">FAQ</a></li>
<li><a href="/testimonials/">Testimonials</a></li>
</ul>
</div>
<div>
<h4>Locations</h4>
<ul>
<li><a href="/pittsburgh-business-consultant/">Pittsburgh</a></li>
<li><a href="/pittsburgh-ai-consulting/">Pittsburgh AI</a></li>
<li><a href="/pittsburgh-operations-consulting/">Pittsburgh Ops</a></li>
<li><a href="/cranberry-township-business-consultant/">Cranberry Twp</a></li>
<li><a href="/wexford-business-consultant/">Wexford</a></li>
</ul>
</div>
<div>
<h4>Connect</h4>
<ul>
<li><a href="/contact/">Contact Us</a></li>
<li><a href="https://drconnorrobertson.com" target="_blank" rel="noopener">Dr. Connor Robertson</a></li>
<li><a href="https://thepittsburghwire.com" target="_blank" rel="noopener">The Pittsburgh Wire</a></li>
<li><a href="https://www.youtube.com/@TheProspectingShow" target="_blank" rel="noopener">The Prospecting Show</a></li>
</ul>
</div>
</div>
<div class="footer-bottom">
&copy; {YEAR} Elixir Consulting Group. All rights reserved.
</div>
</div>
</footer>"""


def make_cta():
    return """<section class="cta-banner">
<div class="container">
<span class="eyebrow">Ready to Get Started?</span>
<h2>Build the Structure Your Business Needs</h2>
<p>The first step is a consult to understand your business and determine if there is a fit.</p>
<a href="/contact/" class="btn btn-gold">Book a Consult</a>
</div>
</section>"""


def make_page(title, description, path, body, schema="", canonical=None):
    if canonical is None:
        canonical = DOMAIN + path

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Elixir Consulting Group">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="robots" content="index,follow">
<meta name="google-site-verification" content="elixir-consulting-group-gsc-verify">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{SHARED_CSS}</style>
{schema}
</head>
<body>
{make_header(path)}
<main style="margin-top:72px">
{body}
</main>
{make_footer()}
<script>
document.addEventListener('click',function(e){{if(!e.target.closest('.nav-menu')&&!e.target.closest('.nav-toggle'))document.querySelector('.nav-menu').classList.remove('active')}});
document.querySelectorAll('.faq-item').forEach(function(item){{item.querySelector('.faq-q').addEventListener('click',function(){{item.classList.toggle('active')}});}});
</script>
</body>
</html>"""


def write_page(path, content):
    """Write an HTML page to the correct file path."""
    if path.endswith("/"):
        filepath = path + "index.html"
    else:
        filepath = path

    full_path = os.path.join(SITE_DIR, filepath.lstrip("/"))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w") as f:
        f.write(content)
    print(f"  Created: {filepath}")


# ─── Page Generators ───────────────────────────────────────────────────

def gen_homepage():
    testimonials_html = ""
    for t in TESTIMONIALS[:6]:
        testimonials_html += f"""<div class="testimonial-card">
<p class="quote">"{t['text']}"</p>
<p class="author">{t['name']}</p>
<p class="role">{t['role']}</p>
</div>\n"""

    blog_cards = ""
    for post in BLOG_POSTS[:3]:
        blog_cards += f"""<div class="card blog-card">
<div class="blog-img">E</div>
<div class="blog-content">
<p class="blog-date">{post['date']}</p>
<h3><a href="/blog/{post['slug']}/">{post['title']}</a></h3>
<p>{post['excerpt'][:120]}...</p>
</div>
</div>\n"""

    schema = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Elixir Consulting Group",
  "description": "Business consulting firm specializing in operations, sales systems, AI consulting, and leadership development for business owners.",
  "url": "https://elixirconsultinggroup.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "429 Fourth Ave. Suite 300",
    "addressLocality": "Pittsburgh",
    "addressRegion": "PA",
    "postalCode": "15219",
    "addressCountry": "US"
  },
  "founder": {
    "@type": "Person",
    "name": "Dr. Connor Robertson",
    "url": "https://drconnorrobertson.com"
  },
  "areaServed": [
    {"@type": "City", "name": "Pittsburgh"},
    {"@type": "Country", "name": "United States"}
  ],
  "serviceType": [
    "Business Strategy Consulting",
    "AI Consulting",
    "Operations Consulting",
    "Sales Strategy Consulting",
    "Leadership Development"
  ]
}
</script>"""

    body = f"""
<section class="hero">
<div class="container">
<span class="eyebrow">Business Consulting | Pittsburgh, PA</span>
<h1>Build Structure That Scales Your Business</h1>
<p>Elixir Consulting Group helps business owners replace chaos with systems. We install the operations, sales processes, and leadership cadence that produce consistent execution and measurable growth.</p>
<a href="/contact/" class="btn btn-gold">Book a Consult</a>
<a href="/services/" class="btn btn-outline" style="border-color:rgba(255,255,255,.4);color:#fff">Our Services</a>
</div>
</section>

<section class="section">
<div class="container">
<div class="grid grid-4">
<div class="stat-card card"><span class="stat-num">150+</span><span class="stat-label">Businesses Served</span></div>
<div class="stat-card card"><span class="stat-num">92%</span><span class="stat-label">Client Retention</span></div>
<div class="stat-card card"><span class="stat-num">40%</span><span class="stat-label">Avg. Efficiency Gain</span></div>
<div class="stat-card card"><span class="stat-num">5x</span><span class="stat-label">Avg. ROI on Engagement</span></div>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="max-width:700px;margin:0 auto 48px">
<span class="eyebrow">What We Do</span>
<h2>Practical Systems for Real Business Problems</h2>
<p>Most companies do not fail because they lack ideas. They stall because the business is held together by memory, hero effort, and constant improvising. We replace chaos with systems.</p>
</div>
<div class="grid grid-3">
<div class="card">
<div class="card-icon">&#9881;</div>
<h3>Operations & Systems</h3>
<p>Process mapping, SOPs, workflow cleanup, role clarity, and weekly operating cadence that keeps execution consistent.</p>
<a href="/services/operations/">Learn more &rarr;</a>
</div>
<div class="card">
<div class="card-icon">&#128200;</div>
<h3>Sales & Revenue Systems</h3>
<p>Pipeline structure, follow-up standards, CRM configuration, and sales process that your team can run without guessing.</p>
<a href="/services/sales-strategy/">Learn more &rarr;</a>
</div>
<div class="card">
<div class="card-icon">&#129302;</div>
<h3>AI & Digital Transformation</h3>
<p>Evaluate and implement AI tools, automate workflows, and adopt technology that improves efficiency without disruption.</p>
<a href="/services/ai-consulting/">Learn more &rarr;</a>
</div>
<div class="card">
<div class="card-icon">&#128101;</div>
<h3>Leadership & Accountability</h3>
<p>Weekly leadership rhythms, scorecards, owner-level visibility, and accountability structures that produce decisions.</p>
<a href="/services/leadership/">Learn more &rarr;</a>
</div>
<div class="card">
<div class="card-icon">&#127919;</div>
<h3>Business Strategy</h3>
<p>Strategic planning, growth roadmaps, competitive positioning, and execution frameworks that turn strategy into results.</p>
<a href="/services/business-strategy/">Learn more &rarr;</a>
</div>
<div class="card">
<div class="card-icon">&#128640;</div>
<h3>Growth & Scaling</h3>
<p>Build the foundation to scale from $1M to $10M and beyond. Systems, team development, and infrastructure for sustainable growth.</p>
<a href="/services/">Learn more &rarr;</a>
</div>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center">
<div>
<span class="eyebrow">About the Founder</span>
<h2>Dr. Connor Robertson</h2>
<p>Dr. Connor Robertson is the founder and lead consultant at Elixir Consulting Group. With extensive experience in business strategy, operational growth, and organizational development, Dr. Robertson helps businesses identify opportunities, improve performance, and achieve sustainable success.</p>
<p>Through hands-on implementation and structured frameworks, he works directly with owners and leadership teams to install the systems that produce real results.</p>
<a href="https://drconnorrobertson.com" target="_blank" rel="noopener" class="btn btn-outline" style="margin-top:8px">Learn More About Dr. Robertson</a>
</div>
<div style="background:{COLORS['off_white']};border-radius:16px;padding:48px;text-align:center">
<div style="width:120px;height:120px;border-radius:50%;background:{COLORS['navy']};margin:0 auto 24px;display:flex;align-items:center;justify-content:center;color:{COLORS['gold']};font-size:2.5rem;font-weight:700">CR</div>
<h3 style="margin-bottom:4px">Dr. Connor Robertson</h3>
<p style="color:{COLORS['mid_gray']};margin-bottom:16px">Founder & Lead Consultant</p>
<p style="font-size:.9rem">Specializing in business strategy, operations, AI consulting, and organizational development.</p>
</div>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:48px">
<span class="eyebrow">Testimonials</span>
<h2>What Our Clients Say</h2>
</div>
<div class="grid grid-2">
{testimonials_html}
</div>
<div class="text-center" style="margin-top:32px">
<a href="/testimonials/" class="btn btn-outline">View All Testimonials</a>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:48px">
<span class="eyebrow">How We Work</span>
<h2>A Proven Process for Business Improvement</h2>
</div>
<div style="max-width:700px;margin:0 auto">
<div class="process-step"><div class="step-num">01</div><div class="step-content"><h3>Book a Consult</h3><p>Understand your business, current constraints, and priorities.</p></div></div>
<div class="process-step"><div class="step-num">02</div><div class="step-content"><h3>Structured Assessment</h3><p>Deep dive into operations, sales, leadership cadence, and team structure.</p></div></div>
<div class="process-step"><div class="step-num">03</div><div class="step-content"><h3>Implementation</h3><p>Build and install the systems your business needs alongside your team.</p></div></div>
<div class="process-step"><div class="step-num">04</div><div class="step-content"><h3>Ongoing Support</h3><p>Maintain, refine, and improve execution week to week.</p></div></div>
</div>
</div>
</section>

<section class="section" style="padding:40px 0">
<div class="container text-center">
<span class="eyebrow">As Featured In</span>
<div style="display:flex;justify-content:center;align-items:center;gap:48px;flex-wrap:wrap;margin-top:24px">
<a href="https://thepittsburghwire.com" target="_blank" rel="noopener" style="font-size:1.3rem;font-weight:700;color:{COLORS['navy']};opacity:.7;transition:opacity .2s">The Pittsburgh Wire</a>
<a href="https://www.youtube.com/@TheProspectingShow" target="_blank" rel="noopener" style="font-size:1.3rem;font-weight:700;color:{COLORS['navy']};opacity:.7;transition:opacity .2s">The Prospecting Show</a>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:48px">
<span class="eyebrow">Insights</span>
<h2>Latest From the Blog</h2>
</div>
<div class="grid grid-3">
{blog_cards}
</div>
<div class="text-center" style="margin-top:32px">
<a href="/blog/" class="btn btn-outline">View All Articles</a>
</div>
</div>
</section>

{make_cta()}
"""
    return make_page(
        "Business Consulting Pittsburgh | Proven Results | Elixir Consulting Group",
        "Elixir Consulting Group helps business owners build operations, sales systems, and leadership cadence that produce consistent execution and measurable growth. Based in Pittsburgh, PA.",
        "/",
        body,
        schema
    )


def gen_about():
    schema = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Elixir Consulting Group","url":"https://elixirconsultinggroup.com","founder":{"@type":"Person","name":"Dr. Connor Robertson","url":"https://drconnorrobertson.com"},"address":{"@type":"PostalAddress","streetAddress":"429 Fourth Ave. Suite 300","addressLocality":"Pittsburgh","addressRegion":"PA","postalCode":"15219","addressCountry":"US"}}
</script>"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / About</p>
<h1>About Elixir Consulting Group</h1>
<p>Built for business owners who are tired of operating in reaction mode.</p>
</div>
</section>

<section class="section">
<div class="container">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center">
<div>
<span class="eyebrow">Our Story</span>
<h2>From Chaos to Structure</h2>
<p>Elixir Consulting Group was built for business owners who are tired of operating in reaction mode. Many companies grow quickly but never pause to build the systems that support that growth. Over time, everything becomes harder than it should be. Decisions slow down. Teams get confused. The owner becomes the bottleneck.</p>
<p>Our work exists to fix that. We focus on helping owners move from chaos to structure without overcomplicating the business. That means simplifying processes, installing a clear operating cadence, and making execution visible every week.</p>
<p>The goal is not perfection. The goal is consistency.</p>
</div>
<div style="background:{COLORS['off_white']};border-radius:16px;padding:48px">
<h3 style="margin-bottom:24px">By the Numbers</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
<div><span class="stat-num" style="font-size:2rem">150+</span><br><span class="stat-label">Businesses Served</span></div>
<div><span class="stat-num" style="font-size:2rem">92%</span><br><span class="stat-label">Retention Rate</span></div>
<div><span class="stat-num" style="font-size:2rem">50+</span><br><span class="stat-label">Industries</span></div>
<div><span class="stat-num" style="font-size:2rem">5x</span><br><span class="stat-label">Avg. ROI</span></div>
</div>
</div>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div style="display:grid;grid-template-columns:1fr 2fr;gap:60px;align-items:start">
<div style="text-align:center">
<div style="width:160px;height:160px;border-radius:50%;background:{COLORS['navy']};margin:0 auto 24px;display:flex;align-items:center;justify-content:center;color:{COLORS['gold']};font-size:3rem;font-weight:700">CR</div>
<h3>Dr. Connor Robertson</h3>
<p style="color:{COLORS['mid_gray']}">Founder & Lead Consultant</p>
</div>
<div>
<span class="eyebrow">Leadership</span>
<h2>About Dr. Connor Robertson</h2>
<p>Dr. Connor Robertson is the founder and lead consultant at Elixir Consulting Group, bringing extensive experience in business strategy, operational growth, and organizational development.</p>
<p>Through his work with entrepreneurs and established companies, Dr. Robertson helps organizations identify opportunities, improve performance, and achieve sustainable long-term success. His approach is hands-on and implementation-focused. He works alongside owners and leadership teams to install the systems, not just recommend them.</p>
<p>Dr. Robertson's expertise spans business strategy, operations consulting, AI and digital transformation, sales system design, and leadership development. His work has helped businesses across industries build the structure they need to grow without chaos.</p>
<a href="https://drconnorrobertson.com" target="_blank" rel="noopener" class="btn btn-primary" style="margin-top:12px">Visit DrConnorRobertson.com</a>
</div>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:48px">
<span class="eyebrow">Our Beliefs</span>
<h2>What We Believe</h2>
<p style="max-width:600px;margin:0 auto">These core principles guide everything we do with our clients.</p>
</div>
<div class="grid grid-3">
<div class="card"><h3>Structure Creates Freedom</h3><p>When expectations, workflows, and priorities are clear, people make better decisions without constant oversight.</p></div>
<div class="card"><h3>Simple Systems Win</h3><p>If a system is too complicated, it will not be used. We build systems that teams actually follow.</p></div>
<div class="card"><h3>Execution Beats Strategy</h3><p>Most businesses already know what they should do. The problem is follow-through. Weekly execution matters more than big plans.</p></div>
<div class="card"><h3>Cadence Prevents Chaos</h3><p>When meetings, reporting, and priorities run on a predictable rhythm, emergencies decrease and results improve.</p></div>
<div class="card"><h3>Operations Drive Results</h3><p>Talent alone does not scale. Systems are what turn effort into consistent outcomes.</p></div>
<div class="card"><h3>Implementation Over Advice</h3><p>We do not drop a binder and disappear. Our work is hands-on and focused on installing systems that work.</p></div>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:48px">
<span class="eyebrow">Our Process</span>
<h2>How We Approach Our Work</h2>
</div>
<div style="max-width:700px;margin:0 auto">
<div class="process-step"><div class="step-num">01</div><div class="step-content"><h3>Mapping Current State</h3><p>We start by understanding what is actually happening today in your business.</p></div></div>
<div class="process-step"><div class="step-num">02</div><div class="step-content"><h3>Identifying High-Impact Changes</h3><p>We identify the few changes that will make the biggest impact on your operations.</p></div></div>
<div class="process-step"><div class="step-num">03</div><div class="step-content"><h3>Building Systems</h3><p>We build workflows, scorecards, and cadence that fit your business.</p></div></div>
<div class="process-step"><div class="step-num">04</div><div class="step-content"><h3>Ongoing Support</h3><p>We help the team adopt and run the systems week to week to ensure they stick.</p></div></div>
</div>
</div>
</section>

{make_cta()}
"""
    return make_page(
        "About Elixir Consulting Group | Pittsburgh Business Consulting",
        "Learn about Elixir Consulting Group, founded by Dr. Connor Robertson. We help business owners build operations, sales systems, and leadership cadence in Pittsburgh, PA.",
        "/about/",
        body,
        schema
    )


def gen_services_overview():
    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Services</p>
<h1>Our Services</h1>
<p>Practical systems and implementation support for business owners who want structure, clarity, and measurable results.</p>
</div>
</section>

<section class="section">
<div class="container">
<div class="text-center" style="max-width:700px;margin:0 auto 48px">
<span class="eyebrow">Led by Dr. Connor Robertson</span>
<h2>Five Core Service Areas</h2>
<p>All of Elixir Consulting Group's services are guided by <a href="https://drconnorrobertson.com" target="_blank" rel="noopener">Dr. Connor Robertson</a>, whose expertise in business strategy, operational systems, and revenue optimization ensures each engagement delivers measurable results.</p>
</div>
<div class="grid grid-3">
<div class="card" style="border-top:4px solid {COLORS['gold']}">
<h3>Business Strategy</h3>
<p>Strategic planning, competitive positioning, growth roadmaps, and execution frameworks that turn vision into weekly action.</p>
<a href="/services/business-strategy/" class="btn btn-outline" style="margin-top:12px">Learn More</a>
</div>
<div class="card" style="border-top:4px solid {COLORS['gold']}">
<h3>AI Consulting</h3>
<p>Evaluate and implement AI tools, automate workflows, and lead digital transformation without disrupting your operations.</p>
<a href="/services/ai-consulting/" class="btn btn-outline" style="margin-top:12px">Learn More</a>
</div>
<div class="card" style="border-top:4px solid {COLORS['gold']}">
<h3>Operations Consulting</h3>
<p>Process mapping, SOPs, workflow cleanup, role clarity, and the weekly operating cadence that keeps execution consistent.</p>
<a href="/services/operations/" class="btn btn-outline" style="margin-top:12px">Learn More</a>
</div>
<div class="card" style="border-top:4px solid {COLORS['gold']}">
<h3>Sales Strategy</h3>
<p>Pipeline structure, follow-up standards, CRM configuration, and a sales process your team can run the same way every time.</p>
<a href="/services/sales-strategy/" class="btn btn-outline" style="margin-top:12px">Learn More</a>
</div>
<div class="card" style="border-top:4px solid {COLORS['gold']}">
<h3>Leadership Consulting</h3>
<p>Executive coaching, leadership cadence, accountability structures, scorecards, and the rhythms that produce decisions.</p>
<a href="/services/leadership/" class="btn btn-outline" style="margin-top:12px">Learn More</a>
</div>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:48px">
<span class="eyebrow">Our Approach</span>
<h2>How Engagements Work</h2>
</div>
<div style="max-width:700px;margin:0 auto">
<div class="process-step"><div class="step-num">01</div><div class="step-content"><h3>Initial Consult</h3><p>Understand goals, constraints, and determine fit.</p></div></div>
<div class="process-step"><div class="step-num">02</div><div class="step-content"><h3>Assessment</h3><p>Identify bottlenecks, gaps, and priority fixes across your business.</p></div></div>
<div class="process-step"><div class="step-num">03</div><div class="step-content"><h3>Implementation</h3><p>Build systems and install cadence alongside your team.</p></div></div>
<div class="process-step"><div class="step-num">04</div><div class="step-content"><h3>Ongoing Support</h3><p>Maintain, refine, and improve execution over time.</p></div></div>
</div>
</div>
</section>

{make_cta()}
"""
    return make_page(
        "Business Consulting Services | Elixir Consulting Group",
        "Explore Elixir Consulting Group's five core services: business strategy, AI consulting, operations, sales strategy, and leadership development. Pittsburgh, PA.",
        "/services/",
        body
    )


def gen_service_page(slug, title, tagline, intro, items, outcomes):
    items_html = ""
    for item in items:
        items_html += f"""<div class="card"><h3>{item[0]}</h3><p>{item[1]}</p></div>\n"""

    outcomes_html = ""
    for o in outcomes:
        outcomes_html += f'<div class="process-step"><div class="step-num" style="background:{COLORS["gold"]};color:{COLORS["navy_dark"]}">&#10003;</div><div class="step-content"><p style="font-weight:600;margin-bottom:0">{o}</p></div></div>\n'

    # FAQ section with schema
    faq_html = ""
    faq_schema_items = []
    if slug in SERVICE_FAQS:
        for q, a in SERVICE_FAQS[slug]:
            faq_html += f"""<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><p>{a}</p></div></div>\n"""
            faq_schema_items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})

    faq_section = ""
    if faq_html:
        faq_section = f"""
<section class="section section-gray">
<div class="container" style="max-width:800px">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Common Questions</span>
<h2>Frequently Asked Questions</h2>
</div>
{faq_html}
</div>
</section>
"""

    # Related blog posts
    related_keywords = {
        "business-strategy": ["strategy", "scale", "growth", "exit"],
        "ai-consulting": ["ai", "digital", "technology", "automation"],
        "operations": ["operations", "efficiency", "cost", "systems", "scale"],
        "sales-strategy": ["sales", "revenue", "close rate", "pipeline"],
        "leadership": ["leadership", "cadence", "accountability", "runs without"],
    }
    keywords = related_keywords.get(slug, [])
    related_posts = []
    for post in BLOG_POSTS:
        if len(related_posts) >= 3:
            break
        title_lower = post["title"].lower()
        if any(kw in title_lower for kw in keywords):
            related_posts.append(post)

    related_html = ""
    if related_posts:
        cards = ""
        for post in related_posts:
            cards += f"""<div class="card blog-card"><div class="blog-content"><p class="blog-date">{post['date']}</p><h3><a href="/blog/{post['slug']}/">{post['title']}</a></h3><p>{post['excerpt'][:120]}...</p></div></div>\n"""
        related_html = f"""
<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Related Reading</span>
<h2>From the Blog</h2>
</div>
<div class="grid grid-3">{cards}</div>
</div>
</section>
"""

    # Schema
    schema = ""
    if faq_schema_items:
        schema = f"""<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items}, indent=2)}
</script>"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / <a href="/services/">Services</a> / {title}</p>
<h1>{title}</h1>
<p>{tagline}</p>
</div>
</section>

<section class="section">
<div class="container">
<div style="max-width:800px;margin:0 auto">
<p style="font-size:1.1rem;line-height:1.8">{intro}</p>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:48px">
<span class="eyebrow">What We Deliver</span>
<h2>Key Focus Areas</h2>
</div>
<div class="grid grid-2">
{items_html}
</div>
</div>
</section>

<section class="section">
<div class="container">
<div style="max-width:700px;margin:0 auto">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Results</span>
<h2>Common Outcomes</h2>
</div>
{outcomes_html}
</div>
</div>
</section>

{faq_section}
{related_html}
{make_cta()}
"""
    return make_page(
        f"{title} | Elixir Consulting Group",
        f"{tagline} Elixir Consulting Group provides {title.lower()} services for business owners in Pittsburgh, PA and nationwide.",
        f"/services/{slug}/",
        body,
        schema
    )


def gen_city_page(slug, city, state_abbr, services_focus, intro, geo_description):
    """Generate a city-specific service landing page with FAQ schema."""
    faqs = [
        (f"Does Elixir Consulting Group serve businesses in {city}?", f"Yes. Elixir Consulting Group is based in Pittsburgh, PA and actively serves businesses in {city} and the surrounding region. We work both on-site and remotely to deliver business consulting, operations improvement, AI consulting, and leadership development."),
        (f"What consulting services are available in {city}?", f"We offer business strategy consulting, AI and digital transformation, operations consulting, sales strategy, and leadership development for businesses in {city}. Our engagements are tailored to each client's specific needs and goals."),
        (f"How much does business consulting cost in {city}?", f"Consulting fees depend on the scope of the engagement. We offer both project-based and retainer-based arrangements. The first step is a free consult where we discuss your business and determine if there is a fit."),
        (f"Can you work with my {city} business remotely?", f"Absolutely. While we are based in Pittsburgh, our virtual consulting process is designed to be just as effective as in-person work. Many of our {city} area clients work with us through a combination of virtual and in-person sessions."),
        (f"What industries do you work with in {city}?", f"We work with businesses across all industries in {city}, including professional services, construction, healthcare, manufacturing, technology, real estate, and retail. Our frameworks are industry-agnostic because core operational challenges tend to be universal."),
    ]

    faq_html = ""
    faq_schema_items = []
    for q, a in faqs:
        faq_html += f"""<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><p>{a}</p></div></div>\n"""
        faq_schema_items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})

    schema = f"""<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items}, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Elixir Consulting Group", "description": f"Business consulting firm serving {city}, {state_abbr}. Specializing in operations, AI consulting, sales systems, and leadership development.", "url": f"https://elixirconsultinggroup.com/{slug}/", "address": {"@type": "PostalAddress", "streetAddress": "429 Fourth Ave. Suite 300", "addressLocality": "Pittsburgh", "addressRegion": "PA", "postalCode": "15219", "addressCountry": "US"}, "areaServed": {"@type": "City", "name": city}, "founder": {"@type": "Person", "name": "Dr. Connor Robertson", "url": "https://drconnorrobertson.com"}}, indent=2)}
</script>"""

    services_cards = ""
    for svc_title, svc_desc, svc_link in services_focus:
        services_cards += f"""<div class="card"><div class="card-icon">&#9881;</div><h3><a href="{svc_link}">{svc_title}</a></h3><p>{svc_desc}</p><a href="{svc_link}" style="font-weight:600;font-size:.9rem">Learn more &rarr;</a></div>\n"""

    # Related blog posts for city pages
    related_posts = BLOG_POSTS[:4]
    blog_cards = ""
    for post in related_posts:
        blog_cards += f"""<div class="card blog-card"><div class="blog-content"><p class="blog-date">{post['date']}</p><h3><a href="/blog/{post['slug']}/">{post['title']}</a></h3><p>{post['excerpt'][:120]}...</p></div></div>\n"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / <a href="/services/">Services</a> / {city}</p>
<h1>Business Consulting in {city}, {state_abbr}</h1>
<p>Elixir Consulting Group helps {city} businesses build operations, sales systems, and leadership cadence that produce consistent execution and measurable growth.</p>
</div>
</section>

<section class="section">
<div class="container">
<div style="max-width:800px;margin:0 auto">
<p style="font-size:1.1rem;line-height:1.8">{intro}</p>
<p style="font-size:1.05rem;line-height:1.8;margin-top:16px">{geo_description}</p>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:48px">
<span class="eyebrow">Our Services in {city}</span>
<h2>How We Help {city} Businesses</h2>
</div>
<div class="grid grid-3">
{services_cards}
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="grid grid-2" style="align-items:center;gap:60px">
<div>
<span class="eyebrow">Why Choose Elixir</span>
<h2>Local Expertise, Proven Results</h2>
<p>As a Pittsburgh-based consulting firm, we understand the unique business landscape of the greater Pittsburgh region including {city}. Our founder, <a href="https://drconnorrobertson.com" target="_blank" rel="noopener">Dr. Connor Robertson</a>, has worked with dozens of businesses in Western Pennsylvania to install systems that improve execution and drive measurable results.</p>
<p>We have been featured in <a href="https://thepittsburghwire.com" target="_blank" rel="noopener">The Pittsburgh Wire</a> for our work helping local businesses grow through structured operations and AI adoption.</p>
<a href="/contact/" class="btn btn-primary" style="margin-top:16px">Book a Free Consult</a>
</div>
<div>
<div class="grid grid-2">
<div class="stat-card card"><span class="stat-num">150+</span><span class="stat-label">Businesses Served</span></div>
<div class="stat-card card"><span class="stat-num">92%</span><span class="stat-label">Client Retention</span></div>
<div class="stat-card card"><span class="stat-num">40%</span><span class="stat-label">Avg Efficiency Gain</span></div>
<div class="stat-card card"><span class="stat-num">5x</span><span class="stat-label">Avg ROI</span></div>
</div>
</div>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container" style="max-width:800px">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Common Questions</span>
<h2>{city} Business Consulting FAQ</h2>
</div>
{faq_html}
</div>
</section>

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Insights</span>
<h2>Latest From Our Blog</h2>
</div>
<div class="grid grid-2">
{blog_cards}
</div>
<div class="text-center" style="margin-top:24px">
<a href="/blog/" class="btn btn-outline">View All Articles</a>
</div>
</div>
</section>

{make_cta()}
"""
    return make_page(
        f"Business Consultant {city}, {state_abbr} | Elixir Consulting Group",
        f"Elixir Consulting Group provides business consulting, AI consulting, operations improvement, and leadership development for businesses in {city}, {state_abbr}.",
        f"/{slug}/",
        body,
        schema
    )


def gen_industries():
    cards = ""
    for i, (name, desc) in enumerate(INDUSTRIES):
        cards += f"""<div class="industry-card card">
<div class="ind-icon">{INDUSTRY_ICONS[i]}</div>
<h3>{name}</h3>
<p>{desc}</p>
</div>\n"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Industries</p>
<h1>Industries We Serve</h1>
<p>Our frameworks are designed to work across industries because core operational challenges tend to be universal.</p>
</div>
</section>

<section class="section">
<div class="container">
<div class="grid grid-2">
{cards}
</div>
</div>
</section>

<section class="section section-gray">
<div class="container text-center">
<span class="eyebrow">Not Sure If We Can Help?</span>
<h2>Most Operational Challenges Are Universal</h2>
<p style="max-width:600px;margin:0 auto 24px">Whether you are in manufacturing, healthcare, or professional services, the core problems are the same: inconsistent execution, owner dependency, and lack of structure. We solve these across industries.</p>
<a href="/contact/" class="btn btn-primary">Book a Consult</a>
</div>
</section>

{make_cta()}
"""
    return make_page(
        "Industries We Serve | Elixir Consulting Group",
        "Elixir Consulting Group works with businesses across industries including professional services, construction, healthcare, manufacturing, technology, and real estate.",
        "/industries/",
        body
    )


def gen_case_studies():
    cards = ""
    for cs in CASE_STUDIES:
        results_html = "".join([f"<li>{r}</li>" for r in cs['results']])
        cards += f"""<div class="card" style="padding:0;overflow:hidden">
<div style="background:{COLORS['navy']};padding:24px 32px;color:{COLORS['white']}">
<span style="font-size:.8rem;text-transform:uppercase;letter-spacing:1px;color:{COLORS['gold']}">{cs['industry']}</span>
<h3 style="color:{COLORS['white']};margin-top:8px">{cs['title']}</h3>
</div>
<div style="padding:32px">
<h4 style="color:{COLORS['navy']};margin-bottom:8px">Challenge</h4>
<p>{cs['challenge']}</p>
<h4 style="color:{COLORS['navy']};margin-bottom:8px">Solution</h4>
<p>{cs['solution']}</p>
<h4 style="color:{COLORS['navy']};margin-bottom:8px">Results</h4>
<ul style="list-style:none;padding:0">{results_html}</ul>
</div>
</div>\n"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Case Studies</p>
<h1>Case Studies</h1>
<p>Real results from real businesses. See how Elixir Consulting Group helps companies build structure and improve execution.</p>
</div>
</section>

<section class="section">
<div class="container">
<div class="grid grid-2">
{cards}
</div>
</div>
</section>

{make_cta()}
"""
    return make_page(
        "Case Studies | Client Success Stories | Elixir Consulting Group",
        "See real case studies from Elixir Consulting Group clients. Manufacturing, professional services, construction, and healthcare success stories.",
        "/case-studies/",
        body
    )


def gen_blog_index():
    cards = ""
    for post in BLOG_POSTS:
        cards += f"""<div class="card blog-card">
<div class="blog-img">E</div>
<div class="blog-content">
<p class="blog-date">{post['date']}</p>
<h3><a href="/blog/{post['slug']}/">{post['title']}</a></h3>
<p>{post['excerpt'][:150]}...</p>
<a href="/blog/{post['slug']}/" style="font-weight:600;font-size:.9rem">Read More &rarr;</a>
</div>
</div>\n"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Blog</p>
<h1>Blog</h1>
<p>Insights on business strategy, operations, AI consulting, and growth from Elixir Consulting Group.</p>
</div>
</section>

<section class="section">
<div class="container">
<div class="grid grid-3">
{cards}
</div>
</div>
</section>
"""
    return make_page(
        "Business Consulting Blog | Elixir Consulting Group",
        "Read insights on business strategy, operations, AI consulting, sales systems, and growth from Elixir Consulting Group in Pittsburgh, PA.",
        "/blog/",
        body
    )


def gen_blog_post(post):
    schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{post['title']}","datePublished":"{post['date']}","author":{{"@type":"Person","name":"Dr. Connor Robertson","url":"https://drconnorrobertson.com"}},"publisher":{{"@type":"Organization","name":"Elixir Consulting Group","url":"https://elixirconsultinggroup.com"}},"mainEntityOfPage":"{DOMAIN}/blog/{post['slug']}/"}}
</script>"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {post['title'][:50]}...</p>
<h1 style="font-size:clamp(1.6rem,4vw,2.4rem)">{post['title']}</h1>
<p style="font-size:.9rem;margin-top:8px">By Dr. Connor Robertson | {post['date']}</p>
</div>
</section>

<section class="section">
<div class="container">
<article style="max-width:800px;margin:0 auto;font-size:1.05rem;line-height:1.85">
{post['content']}
</article>
</div>
</section>

<section class="section section-gray">
<div class="container text-center">
<h2>Ready to Improve Your Business Operations?</h2>
<p style="max-width:500px;margin:0 auto 24px">If this article resonated with you, a consult is the best next step to understand how these ideas apply to your specific business.</p>
<a href="/contact/" class="btn btn-primary">Book a Consult</a>
</div>
</section>
"""
    return make_page(
        f"{post['title']} | Elixir Consulting Group",
        post['excerpt'][:160],
        f"/blog/{post['slug']}/",
        body,
        schema
    )


def gen_contact():
    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Contact</p>
<h1>Contact Us</h1>
<p>Ready to build structure that scales? The first step is a conversation.</p>
</div>
</section>

<section class="section">
<div class="container">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:60px">
<div>
<span class="eyebrow">Get in Touch</span>
<h2>Book a Consult</h2>
<p>Every engagement starts with a consult where we learn about your business, goals, and current constraints. There is no obligation and no pressure. If there is a fit, we will discuss next steps.</p>
<form action="#" method="POST" style="margin-top:32px">
<div class="form-group"><label>Full Name</label><input type="text" name="name" required placeholder="Your full name"></div>
<div class="form-group"><label>Email</label><input type="email" name="email" required placeholder="your@email.com"></div>
<div class="form-group"><label>Phone</label><input type="tel" name="phone" placeholder="(555) 123-4567"></div>
<div class="form-group"><label>Company Name</label><input type="text" name="company" placeholder="Your company"></div>
<div class="form-group"><label>How Can We Help?</label>
<select name="service">
<option value="">Select a service area</option>
<option value="business-strategy">Business Strategy</option>
<option value="ai-consulting">AI Consulting</option>
<option value="operations">Operations Consulting</option>
<option value="sales-strategy">Sales Strategy</option>
<option value="leadership">Leadership Consulting</option>
<option value="other">Other</option>
</select>
</div>
<div class="form-group"><label>Message</label><textarea name="message" placeholder="Tell us about your business and what you are looking to improve..."></textarea></div>
<button type="submit" class="btn btn-primary" style="width:100%">Submit</button>
</form>
</div>
<div>
<div class="contact-info-card" style="margin-top:48px">
<h3>Office Location</h3>
<p>{ADDRESS}</p>
</div>
<div class="contact-info-card">
<h3>Hours</h3>
<p>Monday - Saturday: 8:00 AM - 6:00 PM<br>Sunday: Closed</p>
</div>
<div class="contact-info-card">
<h3>Remote Clients</h3>
<p>We work with businesses nationwide through virtual consulting and implementation support.</p>
</div>
<div style="background:{COLORS['navy']};border-radius:12px;padding:32px;margin-top:16px;color:{COLORS['white']}">
<h3 style="color:{COLORS['gold']};margin-bottom:12px">What to Expect</h3>
<p style="color:rgba(255,255,255,.85);font-size:.95rem">After you submit the form, we will reach out within one business day to schedule your consult. During the call, we will discuss your business, identify priorities, and determine if there is a fit for an engagement.</p>
</div>
</div>
</div>
</div>
</section>
"""
    return make_page(
        "Contact Elixir Consulting Group | Book a Consult",
        "Contact Elixir Consulting Group to book a business consulting engagement. Based in Pittsburgh, PA. Serving clients nationwide.",
        "/contact/",
        body
    )


def gen_faq():
    faq_schema_items = []
    faq_html = ""
    for q, a in FAQ_ITEMS:
        faq_html += f"""<div class="faq-item">
<div class="faq-q">{q}</div>
<div class="faq-a"><p>{a}</p></div>
</div>\n"""
        faq_schema_items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    schema = f"""<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items}, indent=2)}
</script>"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / FAQ</p>
<h1>Frequently Asked Questions</h1>
<p>Common questions about working with Elixir Consulting Group.</p>
</div>
</section>

<section class="section">
<div class="container" style="max-width:800px">
{faq_html}
</div>
</section>

{make_cta()}
"""
    return make_page(
        "FAQ | Elixir Consulting Group | Business Consulting Questions",
        "Answers to frequently asked questions about Elixir Consulting Group's business consulting services, pricing, process, and engagement structure.",
        "/faq/",
        body,
        schema
    )


def gen_testimonials():
    cards = ""
    for t in TESTIMONIALS:
        cards += f"""<div class="testimonial-card">
<p class="quote">"{t['text']}"</p>
<p class="author">{t['name']}</p>
<p class="role">{t['role']}</p>
</div>\n"""

    schema = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"Elixir Consulting Group","aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"47","bestRating":"5"}}
</script>"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Testimonials</p>
<h1>Client Testimonials</h1>
<p>What business owners and leaders say about working with Elixir Consulting Group.</p>
</div>
</section>

<section class="section">
<div class="container">
<div class="grid grid-2">
{cards}
</div>
</div>
</section>

{make_cta()}
"""
    return make_page(
        "Client Testimonials | Elixir Consulting Group",
        "Read client testimonials and reviews from business owners who have worked with Elixir Consulting Group for operations, sales systems, and leadership consulting.",
        "/testimonials/",
        body,
        schema
    )


def gen_sitemap():
    urls = [
        ("/", "1.0", "weekly"),
        ("/about/", "0.8", "monthly"),
        ("/services/", "0.9", "monthly"),
        ("/services/business-strategy/", "0.8", "monthly"),
        ("/services/ai-consulting/", "0.8", "monthly"),
        ("/services/operations/", "0.8", "monthly"),
        ("/services/sales-strategy/", "0.8", "monthly"),
        ("/services/leadership/", "0.8", "monthly"),
        ("/pittsburgh-business-consultant/", "0.9", "monthly"),
        ("/pittsburgh-ai-consulting/", "0.9", "monthly"),
        ("/pittsburgh-operations-consulting/", "0.9", "monthly"),
        ("/cranberry-township-business-consultant/", "0.8", "monthly"),
        ("/wexford-business-consultant/", "0.8", "monthly"),
        ("/industries/", "0.7", "monthly"),
        ("/case-studies/", "0.7", "monthly"),
        ("/blog/", "0.8", "weekly"),
        ("/contact/", "0.7", "monthly"),
        ("/faq/", "0.7", "monthly"),
        ("/testimonials/", "0.7", "monthly"),
    ]
    for post in BLOG_POSTS:
        urls.append((f"/blog/{post['slug']}/", "0.6", "monthly"))

    entries = ""
    for path, priority, freq in urls:
        entries += f"""  <url>
    <loc>{DOMAIN}{path}</loc>
    <lastmod>{DATE_NOW}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}</urlset>"""


def gen_robots():
    return f"""User-agent: *
Allow: /
Sitemap: {DOMAIN}/sitemap.xml"""


def gen_vercel_json():
    return json.dumps({
        "cleanUrls": True,
        "trailingSlash": True,
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {"key": "X-Content-Type-Options", "value": "nosniff"},
                    {"key": "X-Frame-Options", "value": "DENY"},
                    {"key": "X-XSS-Protection", "value": "1; mode=block"},
                    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}
                ]
            },
            {
                "source": "/(.*).html",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=3600, stale-while-revalidate=86400"}
                ]
            }
        ]
    }, indent=2)


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

SITE_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("Elixir Consulting Group - Static Site Generator")
print("=" * 60)

# Homepage
print("\n[1/14] Homepage")
write_page("/index.html", gen_homepage())

# About
print("\n[2/14] About")
write_page("/about/", gen_about())

# Services Overview
print("\n[3/14] Services Overview")
write_page("/services/", gen_services_overview())

# Service Pages
print("\n[4/14] Business Strategy")
write_page("/services/business-strategy/", gen_service_page(
    "business-strategy",
    "Business Strategy Consulting",
    "Strategic planning and execution frameworks that turn vision into measurable results.",
    "Most businesses do not lack strategy. They lack execution. At Elixir Consulting Group, we bridge that gap by building strategic frameworks that connect high-level goals to weekly action. Our business strategy work starts with understanding where you are, where you want to go, and what is standing in the way. From there, we build a practical roadmap with clear priorities, timelines, and accountability structures.",
    [
        ("Strategic Planning", "Define your competitive position, growth trajectory, and key priorities for the next 12-24 months."),
        ("Growth Roadmaps", "Build a step-by-step plan to scale revenue, expand into new markets, or launch new service lines."),
        ("Competitive Analysis", "Understand your market position and identify the opportunities your competitors are missing."),
        ("Execution Frameworks", "Turn strategy into weekly action with scorecards, cadence, and accountability structures."),
        ("Exit Planning", "Prepare your business for a profitable sale by building systems that create transferable value."),
        ("Market Positioning", "Clarify your value proposition and build messaging that resonates with your ideal customers."),
    ],
    [
        "Clear strategic direction with defined priorities",
        "Measurable goals tied to weekly execution",
        "Stronger competitive positioning",
        "Better decision-making across the leadership team",
        "Increased business value and exit readiness",
    ]
))

print("\n[5/14] AI Consulting")
write_page("/services/ai-consulting/", gen_service_page(
    "ai-consulting",
    "AI Consulting & Digital Transformation",
    "Evaluate, implement, and optimize AI tools that improve efficiency without disrupting your operations.",
    "AI and digital transformation are not about chasing the latest technology. They are about finding the right tools to solve real problems in your business. At Elixir Consulting Group, we help businesses evaluate which AI applications will deliver the highest return, implement them without disrupting existing operations, and train teams to use them effectively. Our approach is practical, not theoretical.",
    [
        ("AI Readiness Assessment", "Evaluate your current technology stack and identify where AI can deliver the highest impact with the least disruption."),
        ("Workflow Automation", "Implement AI-powered automation for repetitive tasks like data entry, scheduling, reporting, and client communication."),
        ("Tool Selection & Implementation", "Navigate the AI tool landscape and implement solutions that fit your business size, budget, and technical capacity."),
        ("Data Analysis & Insights", "Deploy AI analytics tools that surface actionable insights from your existing business data."),
        ("Team Training & Adoption", "Ensure your team understands and adopts new tools through structured training and change management."),
        ("Digital Process Design", "Redesign manual workflows into digital processes that scale efficiently as your business grows."),
    ],
    [
        "Reduced time spent on repetitive manual tasks",
        "Better decision-making through data-driven insights",
        "Improved customer response time and satisfaction",
        "Lower operational costs through automation",
        "Technology that supports growth without adding headcount",
    ]
))

print("\n[6/14] Operations Consulting")
write_page("/services/operations/", gen_service_page(
    "operations",
    "Operations Consulting",
    "Build the operational systems that turn effort into consistent, scalable results.",
    "Operations consulting is the foundation of everything we do at Elixir Consulting Group. When a business grows beyond informal processes, things start to break. Delivery becomes inconsistent, the owner becomes the bottleneck, and the team spends more time managing chaos than producing results. We fix this by mapping what is actually happening, identifying bottlenecks, and rebuilding workflows so delivery becomes repeatable and scalable.",
    [
        ("Process Mapping & Workflow Design", "Document and optimize your core workflows so delivery is consistent regardless of who is handling the work."),
        ("SOPs & Documentation", "Build standard operating procedures that people actually use, not 50-page manuals that sit on a shelf."),
        ("Role Clarity & Accountability", "Define clear responsibilities, handoff points, and accountability structures so nothing falls through the cracks."),
        ("Tool & Tech Stack Optimization", "Simplify and streamline the tools your team uses to reduce friction and improve efficiency."),
        ("Hiring & Onboarding Systems", "Build repeatable hiring and onboarding processes that get new team members productive faster."),
        ("Weekly Operating Cadence", "Install a structured weekly rhythm of meetings, reporting, and priorities that keeps execution on track."),
    ],
    [
        "Consistent delivery quality regardless of who handles the work",
        "Owner reclaims 10-15 hours per week",
        "Reduced errors and rework across the team",
        "Faster onboarding for new hires",
        "Predictable operations that scale with growth",
    ]
))

print("\n[7/14] Sales Strategy")
write_page("/services/sales-strategy/", gen_service_page(
    "sales-strategy",
    "Sales Strategy & Revenue Systems",
    "Build a sales process that your team can run consistently without guessing.",
    "If your pipeline feels inconsistent, follow-up depends on personalities, or forecasting is a guess, you do not need more leads. You need a cleaner process. At Elixir Consulting Group, we build sales systems that create predictability. From offer clarity to pipeline stages to CRM configuration, we install the structure that allows your team to execute the same process every time.",
    [
        ("Offer Clarity & Positioning", "Define your value proposition, pricing strategy, and messaging so your team can sell with confidence."),
        ("Pipeline Design", "Build clear pipeline stages with defined criteria for advancement, so deals move forward predictably."),
        ("Follow-Up Systems", "Install lead handling and follow-up standards that ensure no opportunity falls through the cracks."),
        ("CRM Setup & Optimization", "Configure your CRM to support your actual sales process, not the other way around."),
        ("Sales Cadence & Reporting", "Build weekly sales meetings and reporting structures that create visibility and accountability."),
        ("Forecasting & Visibility", "Create forecasting frameworks that give you predictable revenue projections based on real pipeline data."),
    ],
    [
        "Higher close rates from a more structured process",
        "Better follow-up with fewer dropped leads",
        "Predictable revenue pipeline with real visibility",
        "Sales team aligned on process instead of improvising",
        "Less stress around sales performance",
    ]
))

print("\n[8/14] Leadership Consulting")
write_page("/services/leadership/", gen_service_page(
    "leadership",
    "Leadership Consulting & Executive Coaching",
    "Install the leadership rhythms, accountability structures, and cadence that produce decisions instead of meetings.",
    "Leadership consulting at Elixir Consulting Group is not about personality assessments or abstract coaching. It is about installing practical systems that help leadership teams make better decisions, hold each other accountable, and run the business with clarity. We work with owners and executives to build the weekly rhythms and structures that create consistent leadership execution.",
    [
        ("Leadership Cadence Design", "Build weekly leadership meetings that produce decisions, not just discussions. Structured agendas, scorecards, and follow-through."),
        ("Executive Coaching", "One-on-one coaching for owners and executives focused on leadership effectiveness, delegation, and strategic thinking."),
        ("Accountability Structures", "Install clear accountability frameworks so every team member knows what they own and how they are measured."),
        ("Scorecard Development", "Build scorecards that track the metrics that actually matter, giving leaders real-time visibility into business health."),
        ("Team Alignment", "Align the leadership team around shared priorities, clear roles, and a consistent operating rhythm."),
        ("Succession Planning", "Build the leadership bench and development pathways that reduce owner dependency and create organizational resilience."),
    ],
    [
        "Leadership meetings that produce decisions",
        "Clear accountability across the organization",
        "Better visibility into what is working and what is not",
        "Reduced owner involvement in day-to-day decisions",
        "Stronger leadership team capable of running the business independently",
    ]
))

# Industries
print("\n[9/14] Industries")
write_page("/industries/", gen_industries())

# Case Studies
print("\n[10/14] Case Studies")
write_page("/case-studies/", gen_case_studies())

# Blog Index
print("\n[11/14] Blog Index")
write_page("/blog/", gen_blog_index())

# Blog Posts
print("\n[12/14] Blog Posts")
for post in BLOG_POSTS:
    write_page(f"/blog/{post['slug']}/", gen_blog_post(post))

# City Pages
print("\n[12.5/14] City-Specific Service Pages")

write_page("/pittsburgh-business-consultant/", gen_city_page(
    "pittsburgh-business-consultant", "Pittsburgh", "PA",
    [
        ("Business Strategy", "Strategic planning, growth roadmaps, and execution frameworks for Pittsburgh businesses.", "/services/business-strategy/"),
        ("Operations Consulting", "Process mapping, SOPs, and weekly operating cadence that keeps your Pittsburgh business running consistently.", "/services/operations/"),
        ("AI Consulting", "Evaluate and implement AI tools that improve efficiency for Pittsburgh companies without disruption.", "/services/ai-consulting/"),
        ("Sales Strategy", "Build a repeatable sales process that your Pittsburgh-based team can run consistently.", "/services/sales-strategy/"),
        ("Leadership Development", "Install leadership rhythms and accountability structures for Pittsburgh business leaders.", "/services/leadership/"),
        ("Growth & Scaling", "Build the foundation to scale your Pittsburgh business from $1M to $10M and beyond.", "/services/"),
    ],
    "Pittsburgh is experiencing a renaissance in business innovation, and Elixir Consulting Group is at the center of it. As a Pittsburgh-based consulting firm, we work directly with local business owners to install the operations, sales processes, and leadership systems that produce consistent execution and measurable growth. Whether you are a startup in the Strip District, a manufacturer in the North Hills, or a professional services firm downtown, we help you build the structure your business needs to scale.",
    "Pittsburgh offers a unique combination of world-class talent from Carnegie Mellon University and the University of Pittsburgh, affordable business costs compared to coastal cities, and a thriving innovation ecosystem. These advantages make Pittsburgh an ideal city to build and grow a business, and Elixir Consulting Group helps local companies capitalize on these strengths."
))

write_page("/pittsburgh-ai-consulting/", gen_city_page(
    "pittsburgh-ai-consulting", "Pittsburgh", "PA",
    [
        ("AI Readiness Assessment", "Evaluate where AI can deliver the highest impact in your Pittsburgh business.", "/services/ai-consulting/"),
        ("Workflow Automation", "Implement AI-powered automation for repetitive tasks in your Pittsburgh operations.", "/services/ai-consulting/"),
        ("Digital Transformation", "Navigate the transition from manual to digital processes for your Pittsburgh company.", "/services/ai-consulting/"),
        ("Data Analytics", "Deploy AI analytics tools that surface actionable insights from your business data.", "/services/ai-consulting/"),
        ("Team Training", "Ensure your Pittsburgh team adopts and effectively uses new AI tools.", "/services/ai-consulting/"),
        ("Operations Integration", "Integrate AI tools seamlessly into your existing operational workflows.", "/services/operations/"),
    ],
    "Pittsburgh has become a national leader in artificial intelligence, with Carnegie Mellon University's AI research program consistently ranked among the best in the world. Elixir Consulting Group brings this expertise to local businesses, helping Pittsburgh companies evaluate, implement, and optimize AI tools that deliver real returns. We bridge the gap between cutting-edge AI research and practical business application.",
    "The Pittsburgh AI ecosystem includes world-class research institutions, a growing number of AI startups, and established companies investing heavily in AI capabilities. This ecosystem gives local businesses access to talent and expertise that would be prohibitively expensive in other markets. Elixir Consulting Group helps you tap into this advantage."
))

write_page("/pittsburgh-operations-consulting/", gen_city_page(
    "pittsburgh-operations-consulting", "Pittsburgh", "PA",
    [
        ("Process Mapping", "Document and optimize your core workflows for consistent delivery.", "/services/operations/"),
        ("SOPs & Documentation", "Build standard operating procedures that your Pittsburgh team actually uses.", "/services/operations/"),
        ("Weekly Operating Cadence", "Install a structured weekly rhythm that keeps your business on track.", "/services/operations/"),
        ("Role Clarity", "Define clear responsibilities and accountability structures.", "/services/operations/"),
        ("Hiring & Onboarding", "Build repeatable systems that get new team members productive faster.", "/services/operations/"),
        ("Tool Optimization", "Streamline your tech stack to reduce friction and improve efficiency.", "/services/operations/"),
    ],
    "Pittsburgh businesses across industries share common operational challenges: inconsistent delivery, owner dependency, and processes that depend on tribal knowledge rather than documented systems. Elixir Consulting Group specializes in solving these problems for Pittsburgh companies by installing practical operational systems that produce consistent, scalable results.",
    "From manufacturing firms in the Mon Valley to professional services companies in downtown Pittsburgh, we have helped businesses across the region build the operational foundation they need to grow. Our approach is hands-on and practical, working alongside your team to build systems that fit your specific business."
))

write_page("/cranberry-township-business-consultant/", gen_city_page(
    "cranberry-township-business-consultant", "Cranberry Township", "PA",
    [
        ("Business Strategy", "Strategic planning and growth roadmaps for Cranberry Township businesses.", "/services/business-strategy/"),
        ("Operations Consulting", "Build efficient operations that scale for your Cranberry Township company.", "/services/operations/"),
        ("AI & Technology", "Implement AI tools that give your Cranberry Township business a competitive edge.", "/services/ai-consulting/"),
        ("Sales Systems", "Build repeatable sales processes for businesses in the Cranberry Township area.", "/services/sales-strategy/"),
        ("Leadership Development", "Install accountability structures and leadership cadence.", "/services/leadership/"),
        ("Growth Planning", "Scale your Cranberry Township business with proven frameworks.", "/services/"),
    ],
    "Cranberry Township has become one of the fastest-growing business communities in Western Pennsylvania. With its strategic location along the I-79 corridor, proximity to Pittsburgh, and growing commercial infrastructure, Cranberry Township is home to a diverse mix of businesses from tech companies to professional services firms to retail operations. Elixir Consulting Group serves Cranberry Township businesses with the same hands-on consulting approach we bring to all our Pittsburgh-area clients.",
    "The Cranberry Township business community benefits from excellent infrastructure, a skilled workforce drawn from the greater Pittsburgh region, and a business-friendly environment. Elixir Consulting Group helps local businesses capitalize on these advantages by building the systems and processes that turn growth potential into measurable results."
))

write_page("/wexford-business-consultant/", gen_city_page(
    "wexford-business-consultant", "Wexford", "PA",
    [
        ("Business Strategy", "Strategic planning and execution frameworks for Wexford-area businesses.", "/services/business-strategy/"),
        ("Operations Consulting", "Streamline operations and build scalable systems for your Wexford business.", "/services/operations/"),
        ("AI Consulting", "Practical AI adoption for Wexford businesses looking to improve efficiency.", "/services/ai-consulting/"),
        ("Sales Strategy", "Build a structured sales process for your Wexford-based company.", "/services/sales-strategy/"),
        ("Leadership & Coaching", "Executive coaching and leadership development for Wexford business leaders.", "/services/leadership/"),
        ("Exit Planning", "Prepare your Wexford business for a profitable sale or transition.", "/services/business-strategy/"),
    ],
    "Wexford, located in Pine Township just north of Pittsburgh, is a thriving business community with a mix of established companies and growing enterprises. Elixir Consulting Group provides Wexford businesses with expert consulting in operations, sales strategy, AI adoption, and leadership development. Our proximity to Wexford means we can work closely with your team while bringing the full resources of a Pittsburgh-based consulting firm.",
    "The Wexford business community is part of the rapidly growing northern suburbs of Pittsburgh, benefiting from proximity to major transportation corridors, a strong local economy, and access to the Pittsburgh talent pool. Elixir Consulting Group helps Wexford businesses build the operational structure and strategic clarity needed to thrive in this competitive environment."
))

# Contact
print("\n[13/14] Contact")
write_page("/contact/", gen_contact())

# FAQ
print("\n[14/14] FAQ & Testimonials")
write_page("/faq/", gen_faq())
write_page("/testimonials/", gen_testimonials())

# Sitemap, robots.txt, vercel.json
print("\nGenerating sitemap.xml, robots.txt, vercel.json...")
with open(os.path.join(SITE_DIR, "sitemap.xml"), "w") as f:
    f.write(gen_sitemap())
print("  Created: sitemap.xml")

with open(os.path.join(SITE_DIR, "robots.txt"), "w") as f:
    f.write(gen_robots())
print("  Created: robots.txt")

with open(os.path.join(SITE_DIR, "vercel.json"), "w") as f:
    f.write(gen_vercel_json())
print("  Created: vercel.json")

# Count files
total = 0
for root, dirs, files in os.walk(SITE_DIR):
    for f in files:
        if f.endswith('.html'):
            total += 1
print(f"\n{'='*60}")
print(f"DONE! Generated {total} HTML pages + sitemap + robots.txt + vercel.json")
print("SEO optimization complete: 10 new blog posts, 5 city pages, FAQ schema on all service pages, internal cross-links, As Featured In section")
print(f"{'='*60}")
