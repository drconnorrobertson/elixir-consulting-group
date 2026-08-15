#!/usr/bin/env python3
"""
Elixir Consulting Group - Static Site Generator
Generates all HTML pages, sitemap.xml, robots.txt, and vercel.json
"""

import os
import re
import json
import html as htmllib
from datetime import datetime

DOMAIN = "https://elixirconsultinggroup.com"
YEAR = "2026"
DATE_NOW = "2026-08-15"
ADDRESS = "429 Fourth Ave. Suite 300, Pittsburgh, PA 15219"
PHONE = "(412) 387-7656"
PHONE_HREF = "tel:+14123877656"
EMAIL = "info@elixirconsultinggroup.com"
OG_IMAGE = DOMAIN + "/images/og-image.png"
HEADSHOT = "/images/dr-connor-robertson.jpg"
HEADSHOT_ALT = "Dr. Connor Robertson, Founder and Lead Consultant at Elixir Consulting Group"

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
img.lazy{{opacity:0;transition:opacity .3s}}
img.lazy.loaded{{opacity:1}}
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
.faq-item.active .faq-a{{max-height:1400px;padding:0 24px 20px}}
.faq-a p{{margin-bottom:0}}

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

/* Utility bar */
.topbar{{background:{COLORS['navy_dark']};color:rgba(255,255,255,.82);font-size:.82rem}}
.topbar-inner{{max-width:1200px;margin:0 auto;padding:0 24px;height:40px;display:flex;align-items:center;justify-content:space-between;gap:16px}}
.topbar a{{color:rgba(255,255,255,.9);font-weight:600}}
.topbar a:hover{{color:{COLORS['gold']}}}
.topbar-links{{display:flex;align-items:center;gap:20px;flex-shrink:0}}
.topbar-note{{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.site-main{{margin-top:112px}}
.skip-link{{position:absolute;left:-9999px;top:0;background:{COLORS['navy']};color:#fff;padding:12px 20px;z-index:2000;border-radius:0 0 6px 0}}
.skip-link:focus{{left:0;color:#fff}}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{{outline:3px solid {COLORS['gold']};outline-offset:2px}}

/* Trust bar */
.trust-bar{{background:{COLORS['off_white']};border-top:1px solid {COLORS['border']};border-bottom:1px solid {COLORS['border']};padding:22px 0}}
.trust-row{{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:12px 28px;text-align:center}}
.trust-item{{display:flex;align-items:center;gap:8px;font-size:.88rem;font-weight:600;color:{COLORS['navy']};white-space:nowrap}}
@media(max-width:1180px){{.trust-item{{font-size:.83rem}}.trust-row{{gap:10px 20px}}}}
.trust-item span{{color:{COLORS['gold']};font-size:1.05rem;line-height:1}}

/* Article typography (blog) */
.article-body{{max-width:760px;margin:0 auto;font-size:1.075rem;line-height:1.85;color:{COLORS['text_light']}}}
.article-body>p{{margin-bottom:1.35rem}}
.article-body h2{{margin-top:2.4rem;margin-bottom:.9rem;font-size:clamp(1.45rem,3.4vw,1.9rem);scroll-margin-top:130px}}
.article-body h3{{margin-top:1.9rem;margin-bottom:.6rem;font-size:clamp(1.15rem,2.6vw,1.35rem);scroll-margin-top:130px}}
.article-body ul,.article-body ol{{margin:0 0 1.35rem 1.25rem;padding-left:1rem}}
.article-body li{{margin-bottom:.55rem;color:{COLORS['text_light']}}}
.article-body img{{width:100%;border-radius:12px;margin:2rem 0}}
.article-body a{{color:{COLORS['navy']};text-decoration:underline;text-underline-offset:2px;font-weight:500}}
.article-body a:hover{{color:{COLORS['gold']}}}
.article-body strong{{color:{COLORS['text']}}}
.article-body blockquote,.article-body .pullquote{{margin:2rem 0;padding:20px 28px;border-left:4px solid {COLORS['gold']};background:{COLORS['off_white']};border-radius:0 10px 10px 0;font-style:italic;font-size:1.1rem;color:{COLORS['text']}}}
.article-body blockquote p:last-child,.article-body .pullquote p:last-child{{margin-bottom:0}}
.article-body table{{width:100%;border-collapse:collapse;margin:1.75rem 0;font-size:.95rem}}
.article-body th,.article-body td{{border:1px solid {COLORS['border']};padding:10px 14px;text-align:left}}
.article-body th{{background:{COLORS['off_white']};color:{COLORS['navy']}}}
.article-body .stat-highlight,.article-body .big-number{{margin:2rem 0;padding:28px 32px;background:{COLORS['navy']};border-radius:14px;text-align:center;color:#fff}}
.article-body .stat-highlight .stat-num,.article-body .big-number .stat-num{{color:{COLORS['gold']};font-size:2.6rem;display:block;margin-bottom:6px}}
.article-body .stat-highlight .stat-label,.article-body .big-number .stat-label{{color:rgba(255,255,255,.85);font-size:1rem;margin-bottom:0}}
.article-body .checklist{{list-style:none;margin-left:0;padding-left:0}}
.article-body .checklist li{{position:relative;padding-left:30px;margin-bottom:.7rem}}
.article-body .checklist li::before{{content:'\\2713';position:absolute;left:0;top:0;color:{COLORS['gold']};font-weight:700}}
.article-hero-img{{width:100%;max-height:460px;object-fit:cover;border-radius:14px;margin-bottom:12px}}
.article-figcaption{{font-size:.85rem;color:{COLORS['mid_gray']};text-align:center;margin-bottom:32px}}
.post-meta{{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:18px;color:rgba(255,255,255,.85);font-size:.92rem}}
.post-meta img{{width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.35)}}
.post-meta .dot{{opacity:.5}}
.post-tag{{display:inline-block;background:rgba(201,168,76,.16);color:{COLORS['gold']};border:1px solid rgba(201,168,76,.4);border-radius:999px;padding:4px 12px;font-size:.75rem;font-weight:700;letter-spacing:1px;text-transform:uppercase}}
.author-box{{max-width:760px;margin:48px auto 0;display:flex;gap:24px;align-items:flex-start;background:{COLORS['off_white']};border-radius:14px;padding:28px}}
.author-box img{{width:96px;height:96px;border-radius:50%;object-fit:cover;flex-shrink:0}}
.author-box h3{{font-size:1.15rem;margin-bottom:2px}}
.author-box .author-role{{font-size:.85rem;color:{COLORS['mid_gray']};margin-bottom:10px}}
.author-box p{{font-size:.95rem;margin-bottom:10px}}

/* Blog index */
.blog-toolbar{{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin-bottom:32px}}
.blog-search{{flex:1 1 260px;min-width:0;padding:13px 16px;border:1px solid {COLORS['border']};border-radius:10px;font-size:1rem;font-family:inherit}}
.blog-filters{{display:flex;flex-wrap:wrap;gap:8px}}
.filter-chip{{border:1px solid {COLORS['border']};background:#fff;color:{COLORS['navy']};border-radius:999px;padding:9px 16px;font-size:.85rem;font-weight:600;cursor:pointer;transition:all .2s;min-height:40px}}
.filter-chip:hover{{border-color:{COLORS['gold']}}}
.filter-chip.active{{background:{COLORS['navy']};color:#fff;border-color:{COLORS['navy']}}}
.post-list{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:28px}}
.post-card{{display:flex;flex-direction:column;background:#fff;border:1px solid {COLORS['border']};border-radius:14px;overflow:hidden;transition:transform .25s,box-shadow .25s,border-color .25s}}
.post-card:hover{{transform:translateY(-4px);box-shadow:0 12px 34px rgba(0,0,0,.09);border-color:{COLORS['gold']}}}
.post-card .thumb{{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:{COLORS['navy']}}}
.post-card .pc-body{{padding:22px;display:flex;flex-direction:column;flex:1}}
.post-card .pc-cat{{font-size:.72rem;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:{COLORS['gold']};margin-bottom:8px}}
.post-card h3{{font-size:1.08rem;line-height:1.35;margin-bottom:9px}}
.post-card h3 a{{color:{COLORS['navy']}}}
.post-card h3 a:hover{{color:{COLORS['gold']}}}
.post-card p{{font-size:.93rem;margin-bottom:14px;flex:1}}
.post-card .pc-meta{{font-size:.82rem;color:{COLORS['mid_gray']};display:flex;gap:8px;align-items:center}}
.featured-post{{display:grid;grid-template-columns:1.15fr 1fr;gap:0;background:#fff;border:1px solid {COLORS['border']};border-radius:16px;overflow:hidden;margin-bottom:44px}}
.featured-post img{{width:100%;height:100%;min-height:300px;object-fit:cover;background:{COLORS['navy']}}}
.featured-post .fp-body{{padding:40px}}
.featured-post h2{{font-size:clamp(1.4rem,3vw,2rem);margin-bottom:12px}}
.no-results{{text-align:center;padding:48px 0;color:{COLORS['mid_gray']};display:none}}
.load-more-wrap{{text-align:center;margin-top:40px}}

/* Ingested legacy sections */
.content-section{{padding:70px 0}}
.content-section h2{{margin-bottom:1rem}}
.content-section h3{{margin-top:1.75rem}}
.content-section p,.content-section li{{color:{COLORS['text_light']}}}
.content-section ul{{margin:0 0 1.25rem 1.5rem}}
.content-section li{{margin-bottom:.5rem}}
.cta-section{{background:linear-gradient(135deg,{COLORS['navy']} 0%,{COLORS['navy_dark']} 100%);padding:60px 0;text-align:center;color:{COLORS['white']}}}
.cta-section h2,.cta-section p{{color:{COLORS['white']}}}
.cta-section p{{color:rgba(255,255,255,.8);max-width:560px;margin:0 auto 24px}}
.related-posts{{padding:70px 0;background:{COLORS['off_white']}}}
.services-link{{display:inline-block;margin:0 10px 10px 0;padding:10px 18px;border:1px solid {COLORS['border']};border-radius:8px;background:#fff;font-weight:600;font-size:.9rem}}
.services-link:hover{{border-color:{COLORS['gold']}}}

/* Contact strip */
.contact-strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:8px}}
.contact-strip a{{display:flex;align-items:center;gap:12px;min-height:56px;padding:16px 20px;background:{COLORS['off_white']};border:1px solid {COLORS['border']};border-radius:12px;font-weight:600;color:{COLORS['navy']}}}
.contact-strip a:hover{{border-color:{COLORS['gold']};color:{COLORS['navy']}}}
.contact-strip .ic{{color:{COLORS['gold']};font-size:1.15rem}}

/* ===== MOBILE OPTIMIZATION PASS =====
   The off-canvas drawer is positioned with transform (not `right:-100%`):
   .header sets backdrop-filter, which makes it the containing block for its
   fixed children, and a percentage offset there resolved against a viewport
   that the drawer itself had widened -- the menu never came on screen and
   every page scrolled ~50px horizontally. translateX(105%) is relative to
   the drawer's own width, so neither problem can recur. */
html,body{{overflow-x:hidden}}
body{{max-width:100%}}
img,video,iframe{{max-width:100%;height:auto}}
h1,h2,h3,h4,h5,p,li,a,td{{overflow-wrap:break-word;word-wrap:break-word}}
.nav-toggle{{display:none}}
.nav-backdrop{{display:none}}
.split-2{{display:grid;grid-template-columns:1fr 1fr;gap:60px}}
.split-2.split-center{{align-items:center}}
.split-1-2{{display:grid;grid-template-columns:1fr 2fr;gap:60px;align-items:start}}
.split-stats{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
.contact-line{{display:flex;align-items:center;min-height:48px;font-size:1.05rem;font-weight:600}}
@media(max-width:968px){{
.footer-grid{{grid-template-columns:1fr 1fr}}
.grid-3{{grid-template-columns:1fr}}
.featured-post{{grid-template-columns:1fr}}
.featured-post img{{min-height:220px;max-height:280px}}
.featured-post .fp-body{{padding:28px 24px}}
}}
@media(max-width:900px){{
.split-2,.split-1-2{{grid-template-columns:1fr;gap:36px}}
}}
@media(max-width:768px){{
.nav-toggle{{display:flex;flex-direction:column;justify-content:center;align-items:center;gap:5px;width:44px;height:44px;padding:0;margin-right:-6px;background:none;border:0;cursor:pointer;position:relative;z-index:1002;flex-shrink:0}}
.nav-toggle span{{display:block;width:24px;height:2px;margin:0;border-radius:2px;background:{COLORS['navy']};transition:transform .3s,opacity .3s}}
.nav-toggle.active span:nth-child(1){{transform:translateY(7px) rotate(45deg)}}
.nav-toggle.active span:nth-child(2){{opacity:0}}
.nav-toggle.active span:nth-child(3){{transform:translateY(-7px) rotate(-45deg)}}
.nav-menu{{position:fixed;top:0;right:0;left:auto;bottom:auto;display:flex;flex-direction:column;align-items:stretch;gap:2px;width:min(320px,86vw);height:100vh;margin:0;padding:80px 20px 32px;list-style:none;background:{COLORS['white']};box-shadow:-4px 0 24px rgba(0,0,0,.18);transform:translateX(105%);transition:transform .3s ease;z-index:1001;overflow-y:auto;-webkit-overflow-scrolling:touch}}
.nav-menu.active{{transform:translateX(0)}}
.nav-menu li{{width:100%;margin:0}}
.nav-menu a{{display:flex;align-items:center;width:100%;min-height:48px;padding:12px 14px;font-size:1rem;font-weight:500;color:{COLORS['text']};border-radius:8px}}
.nav-menu a:hover{{background:{COLORS['off_white']};color:{COLORS['navy']}}}
.nav-menu .btn,.nav-menu .btn-primary{{justify-content:center;margin-top:10px;color:{COLORS['white']};background:{COLORS['navy']}}}
.nav-backdrop{{display:block;position:fixed;top:0;right:0;bottom:0;left:0;background:rgba(0,0,0,.45);opacity:0;pointer-events:none;transition:opacity .3s;z-index:1000}}
.nav-backdrop.active{{opacity:1;pointer-events:auto}}
.header{{z-index:1001}}
body.nav-open{{overflow:hidden}}
.header-inner{{height:64px}}
main[style]{{margin-top:64px!important}}
.site-main{{margin-top:100px}}
.topbar-inner{{height:38px;padding:0 20px;font-size:.83rem;justify-content:center;gap:18px}}
.topbar-note{{display:none}}
.topbar-links{{gap:18px}}
.topbar a{{display:inline-flex;align-items:center;min-height:36px}}
.logo{{display:inline-flex;align-items:center;min-height:44px}}
.post-list{{grid-template-columns:1fr;gap:20px}}
.post-card .pc-cat{{font-size:.8rem}}
.post-card .pc-meta{{font-size:.87rem}}
.post-card h3{{font-size:1.12rem}}
.author-box{{flex-direction:column;align-items:center;text-align:center;gap:16px;padding:24px 20px}}
.blog-toolbar{{flex-direction:column;align-items:stretch}}
/* flex-basis grows the *height* once the toolbar stacks, so pin it back down */
.blog-search{{flex:0 0 auto;width:100%;min-height:52px}}
.blog-filters{{overflow-x:auto;flex-wrap:nowrap;padding-bottom:6px;-webkit-overflow-scrolling:touch;scrollbar-width:none}}
.blog-filters::-webkit-scrollbar{{display:none}}
.filter-chip{{flex:0 0 auto;min-height:44px}}
.trust-row{{gap:12px 22px}}
.trust-item{{font-size:.85rem}}
.article-body{{font-size:1.03rem}}
.article-body .stat-highlight,.article-body .big-number{{padding:22px 20px}}
.article-body .stat-highlight .stat-num,.article-body .big-number .stat-num{{font-size:2.1rem}}
.article-body blockquote,.article-body .pullquote{{padding:16px 18px;font-size:1rem}}
.article-body table{{display:block;overflow-x:auto;white-space:nowrap}}
.content-section{{padding:44px 0}}
.related-posts{{padding:44px 0}}
.post-meta{{font-size:.86rem;gap:6px 8px}}
.post-meta .dot{{display:none}}
.services-link{{display:inline-flex;align-items:center;min-height:44px}}
.grid{{gap:20px}}
.grid-2,.grid-3,.grid-4{{grid-template-columns:1fr}}
.footer-grid{{grid-template-columns:1fr;gap:28px}}
.process-step{{flex-direction:row;text-align:left;align-items:flex-start;gap:16px}}
/* touch targets >=44px */
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:48px}}
.footer li{{margin-bottom:0}}
.footer li a{{display:inline-block;min-height:44px;padding:11px 0;line-height:1.45}}
.card>a,.card h3 a,.blog-card .blog-content a,.industry-card a,.footer p a{{display:inline-flex;align-items:center;min-height:44px}}
/* Standalone links sitting inside cards and stat blocks are tap targets too.
   Links inline within a sentence stay as-is; WCAG exempts those. */
.stat-label a,.contact-info-card p a,.post-card .pc-body>a{{display:inline-flex;align-items:center;min-height:44px}}
.breadcrumb a{{display:inline-flex;align-items:center;min-height:44px;padding:0 2px}}
.services-link{{display:inline-flex;align-items:center;min-height:44px;margin-bottom:10px}}
.faq-q{{min-height:56px;padding:18px 20px}}
/* no sub-14px body copy */
.breadcrumb{{font-size:.9rem}}
.footer-desc{{font-size:.95rem}}
.footer-bottom{{font-size:.9rem}}
.footer li a{{font-size:.95rem}}
.eyebrow{{font-size:.875rem}}
.stat-label{{font-size:.95rem}}
.card p{{font-size:1rem}}
.testimonial-card .quote{{font-size:1rem}}
.testimonial-card .role{{font-size:.9rem}}
.blog-card .blog-date{{font-size:.9rem}}
/* 16px input text avoids iOS focus zoom */
.form-group input,.form-group select,.form-group textarea{{font-size:16px;min-height:48px}}
.form-group textarea{{min-height:130px}}
.form-group label{{font-size:.95rem}}
button[type=submit]{{width:100%;min-height:52px}}
}}
@media(max-width:480px){{
.container{{padding:0 20px}}
.section{{padding:44px 0}}
.section-sm{{padding:32px 0}}
.card,.industry-card{{padding:24px 20px}}
.testimonial-card{{padding:22px 20px}}
.contact-info-card{{padding:24px 20px}}
.hero{{padding:72px 0 52px}}
.page-hero{{padding:56px 0 36px}}
.cta-banner{{padding:44px 0}}
.footer{{padding:44px 0 0}}
.hero .btn,.cta-banner .btn,.page-hero .btn{{width:100%;margin-right:0;margin-bottom:12px}}
.stat-num{{font-size:2rem}}
.split-stats{{gap:16px}}
.blog-card .blog-img{{height:160px}}
.post-card .pc-body{{padding:18px}}
.featured-post .fp-body{{padding:24px 20px}}
.author-box img{{width:84px;height:84px}}
.article-hero-img{{max-height:240px;border-radius:10px}}
.contact-strip a{{padding:14px 16px}}
}}
@media(max-width:360px){{
.container{{padding:0 16px}}
h1{{font-size:1.7rem}}
.logo{{font-size:1.15rem}}
.stat-num{{font-size:1.8rem}}
.split-stats{{grid-template-columns:1fr}}
.topbar-inner{{gap:10px;font-size:.8rem}}
.trust-row{{flex-direction:column;gap:10px}}
}}
@media(prefers-reduced-motion:reduce){{
*,*::before,*::after{{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
.card:hover,.post-card:hover,.btn:hover{{transform:none}}
}}
@media print{{
.header,.topbar,.nav-backdrop,.cta-banner,.cta-section,.related-posts,.trust-bar,.skip-link,.blog-toolbar,.load-more-wrap,.footer form,button{{display:none!important}}
.site-main{{margin-top:0}}
body{{color:#000;background:#fff;font-size:11pt;line-height:1.45}}
h1,h2,h3,h4{{color:#000;page-break-after:avoid}}
.page-hero,.hero,.section-navy{{background:none!important;color:#000!important;padding:0 0 12pt}}
.page-hero h1,.page-hero p,.hero h1,.hero p,.section-navy h2,.section-navy p{{color:#000!important}}
.section,.section-sm{{padding:12pt 0}}
.card,.industry-card,.post-card{{box-shadow:none;border:1px solid #ccc;page-break-inside:avoid}}
.article-body{{max-width:none;font-size:11pt}}
a[href^="/"]::after{{content:" (elixirconsultinggroup.com" attr(href) ")";font-size:9pt;color:#444}}
a[href^="http"]::after{{content:" (" attr(href) ")";font-size:9pt;color:#444}}
.footer{{background:none;color:#000;border-top:1px solid #ccc}}
.footer a,.footer h4{{color:#000}}
.faq-item .faq-a{{max-height:none!important;padding:0 0 8pt!important;overflow:visible}}
.faq-q::after{{display:none}}
img{{max-width:60%;page-break-inside:avoid}}
}}
"""

NAV_ITEMS = [
    ("About", "/about/"),
    ("Services", "/services/"),
    ("Industries", "/industries/"),
    ("Process", "/process/"),
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

# Page-specific FAQ sets. Every one of these is rendered visibly on the page it
# belongs to as well as emitted as FAQPage schema -- schema without matching
# on-page content is a guideline violation, so the two always ship together.
HOME_FAQS = [FAQ_ITEMS[0], FAQ_ITEMS[1], FAQ_ITEMS[2], FAQ_ITEMS[6], FAQ_ITEMS[8], FAQ_ITEMS[10]]

ABOUT_FAQS = [
    FAQ_ITEMS[13],
    FAQ_ITEMS[1],
    ("What is Dr. Connor Robertson's background?",
     "Dr. Robertson is the founder and lead consultant at Elixir Consulting Group, with experience spanning business strategy, operational growth, and organizational development. He has worked with dozens of businesses to install systems that improve execution, and he is the author of six books on acquisitions and business strategy."),
    ("Who does Elixir Consulting Group actually work with day to day?",
     "Owners and small leadership teams. Most of our clients run businesses between $1M and $30M in revenue where the owner is still deeply involved in operations and wants that to change."),
    ("Does Dr. Robertson work on engagements personally?",
     "Yes. Engagements are led personally rather than handed to a junior team. The implementation model only works when the person building the systems is the person sitting with your leadership team every week."),
    FAQ_ITEMS[9],
]

SERVICES_FAQS = [
    ("Which service should we start with?",
     "Most businesses start with operations because it surfaces the constraints affecting everything else. If your revenue is inconsistent, we often start with sales strategy instead. The consult determines the starting point."),
    ("Can services be combined in one engagement?",
     "Yes, and they usually are. Operational problems rarely stay in one lane. A typical engagement combines two or three of our five service areas around a single set of priorities."),
    FAQ_ITEMS[4],
    FAQ_ITEMS[6],
    FAQ_ITEMS[7],
    FAQ_ITEMS[12],
]

INDUSTRIES_FAQS = [
    FAQ_ITEMS[5],
    ("Do you need industry-specific experience to help our business?",
     "In most cases, no. The core problems we solve -- unclear process, weak accountability, inconsistent follow-through, owner dependency -- are structural rather than industry-specific. We learn the domain details from your team and bring the operating system."),
    ("What if our industry is heavily regulated?",
     "Regulated environments generally benefit more from documented process, not less. We build systems that fit inside your compliance requirements rather than working around them."),
    FAQ_ITEMS[0],
    FAQ_ITEMS[3],
]

CASE_STUDY_FAQS = [
    ("Are these case studies from real engagements?",
     "Yes. Details are generalized and client names are withheld to protect confidentiality, but the situations, interventions, and outcomes reflect real engagements."),
    ("How quickly do results usually appear?",
     "Operational changes such as meeting cadence and role clarity tend to show up within the first 30 to 60 days. Revenue and margin effects typically follow over a full quarter or two as the new systems compound."),
    FAQ_ITEMS[8],
    FAQ_ITEMS[4],
    FAQ_ITEMS[10],
]

TESTIMONIAL_FAQS = [
    ("Can I speak with a current client before engaging?",
     "In most cases yes. Once we have determined there is a likely fit, we can connect you with a client in a comparable situation so you can hear directly what the work involves."),
    ("Why are client names abbreviated?",
     "Many clients prefer that their consulting work stays private, particularly around exit planning or leadership restructuring. We abbreviate names to respect that."),
    FAQ_ITEMS[8],
    FAQ_ITEMS[1],
    FAQ_ITEMS[10],
]

CONTACT_FAQS = [
    FAQ_ITEMS[10],
    FAQ_ITEMS[2],
    ("How soon will someone respond?",
     "We respond to consult requests within one business day. If you need to talk sooner, call {} directly.".format(PHONE)),
    FAQ_ITEMS[3],
    FAQ_ITEMS[6],
    ("Is the first consult free?",
     "Yes. The first conversation is a consult to understand your business and determine whether there is a fit. There is no cost and no obligation."),
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
        "slug": "manufacturing-delivery-delays",
        "title": "Manufacturing Firm Reduces Delivery Delays by 40%",
        "industry": "Manufacturing",
        "profile": "45 employees | $12M revenue | Western Pennsylvania",
        "duration": "5-month engagement",
        "services": [("Operations Consulting", "/services/operations/"), ("Leadership Consulting", "/services/leadership/")],
        "challenge": "A 45-person manufacturing company was experiencing chronic delivery delays, inconsistent quality, and growing client complaints. The owner was personally managing every production issue.",
        "solution": "We mapped the entire production workflow, identified three major bottleneck points, and installed a weekly production cadence with clear accountability. SOPs were built for quality checkpoints, and a simple dashboard gave leadership real-time visibility into order status.",
        "results": ["40% reduction in delivery delays within 90 days", "Client complaints dropped by 60%", "Owner reclaimed 12 hours per week", "Team adopted weekly scorecards for ongoing accountability"],
        "metrics": [("40%", "Fewer delivery delays"), ("60%", "Drop in complaints"), ("12 hrs", "Owner time reclaimed weekly")],
        "quote": "We thought we had a people problem. It turned out we had a handoff problem, and nobody could see it because nobody had ever drawn the process on a wall.",
        "quote_role": "Owner, Manufacturing Client",
        "situation": """<p>The company had grown from 18 to 45 employees in four years without changing how work moved through the shop. Every order still passed through the owner at least twice, once for scheduling and once when something went wrong. By the time we were brought in, "something went wrong" was the normal case rather than the exception.</p>
<p>Delivery dates were being quoted from memory. Production scheduling lived in a spreadsheet that one person maintained and nobody else fully understood. Quality issues were caught at final inspection, which meant rework happened at the most expensive possible moment. Client complaints had roughly doubled year over year, and two long-standing accounts had put the company on notice.</p>
<p>What made this hard to diagnose from the inside is that no individual step was broken. Every department could point to work leaving their area on time. The delay was accumulating in the gaps between departments, where nobody owned the handoff and nobody was measuring it.</p>""",
        "approach": """<h3>Mapping what actually happened</h3>
<p>We started by walking a real order through the building end to end, timestamping every stage, including the waiting. That exercise produced a process map that contradicted the one leadership believed was true. Three bottlenecks accounted for most of the accumulated delay: an undocumented approval step before cutting, a materials staging area with no ownership, and a final inspection queue that had no prioritization logic.</p>
<h3>Installing the cadence</h3>
<p>We built a daily 15-minute production huddle around a visible board showing every active order and its stage. The rule was simple: any order that had not moved in 24 hours got named out loud, with a person and a date attached. Weekly, the leadership team reviewed the same board at a higher altitude and looked at trends rather than individual orders.</p>
<h3>Writing SOPs people would use</h3>
<p>Quality checkpoints were moved upstream and documented as one-page checklists at the station where the work happened, not in a binder in the office. Each checklist named the person accountable and the specific condition that had to be true before the work moved on.</p>
<h3>Making status visible without asking</h3>
<p>A simple dashboard, built on tools the company already owned, gave leadership real-time order status. The point was not sophisticated analytics. The point was that the owner stopped being the routing mechanism for information.</p>""",
        "outcome": """<p>Within 90 days, delivery delays were down 40% and client complaints had dropped roughly 60%. The two at-risk accounts stayed. The owner's own estimate was that he recovered about 12 hours a week, which he redirected into business development for the first time in three years.</p>
<p>The change that mattered most was not any single fix. It was that problems started surfacing in the daily huddle while they were still small, rather than surfacing at final inspection when they were expensive. Eighteen months later the company was still running the same board.</p>""",
    },
    {
        "slug": "professional-services-close-rate",
        "title": "Professional Services Firm Doubles Close Rate",
        "industry": "Professional Services",
        "profile": "22 employees | $4.5M revenue | Multi-state",
        "duration": "4-month engagement",
        "services": [("Sales Strategy", "/services/sales-strategy/"), ("Operations Consulting", "/services/operations/")],
        "challenge": "A growing consulting firm had strong inbound interest but was closing less than 20% of qualified leads. Follow-up was inconsistent, proposals took too long, and there was no structured sales process.",
        "solution": "We built a five-stage sales pipeline with clear criteria for each stage, standardized proposal templates, and installed a weekly pipeline review cadence. CRM was cleaned up and configured to support the new process.",
        "results": ["Close rate improved from 18% to 38%", "Average proposal turnaround reduced from 5 days to 1 day", "Pipeline visibility enabled better revenue forecasting", "Sales team adopted the process with minimal resistance"],
        "metrics": [("18% to 38%", "Close rate"), ("5 days to 1", "Proposal turnaround"), ("100%", "Pipeline visibility")],
        "quote": "We were not losing deals to competitors. We were losing them to the twelve days it took us to send a proposal.",
        "quote_role": "Managing Partner, Professional Services Client",
        "situation": """<p>This firm had the problem most owners would say they want: more qualified inbound than they could handle. The trouble was that interest was not converting. Roughly one in five qualified conversations turned into signed work, and nobody could explain why the other four went quiet.</p>
<p>The diagnosis owners usually reach for here is that they need better leads or a better closer. Neither was true. The firm's win rate on deals that reached a proposal was actually strong. The losses were happening earlier and quieter, in the space between an interested conversation and a document arriving in someone's inbox.</p>
<p>Follow-up depended entirely on who owned the relationship and how busy that person was that week. Proposals were written from scratch every time, which meant a five-day average turnaround and occasionally twelve. By then, the urgency that generated the inquiry had evaporated.</p>""",
        "approach": """<h3>Defining what a stage actually means</h3>
<p>We built a five-stage pipeline where advancement required a specific, observable condition rather than a feeling. A deal did not move to "Proposal" because it felt promising. It moved because a decision-maker had confirmed budget authority and a timeline. This single change removed most of the optimism from the forecast.</p>
<h3>Killing the blank page</h3>
<p>We built modular proposal templates covering the firm's five most common engagement types, with the pricing logic already embedded. Writing a proposal became assembling one. Turnaround dropped to a single day, and the quality became more consistent than when every partner wrote from scratch.</p>
<h3>Follow-up as a system, not a personality trait</h3>
<p>Every stage got a defined follow-up standard with a maximum elapsed time and an owner. The CRM was reconfigured to surface anything past that threshold. Nobody had to remember; the system remembered.</p>
<h3>A weekly review with teeth</h3>
<p>The pipeline review moved from an ad hoc conversation to a standing 45-minute meeting with a fixed agenda: what moved, what did not, and what specifically happens next on every stalled deal.</p>""",
        "outcome": """<p>Close rate moved from 18% to 38% over the engagement. Proposal turnaround went from a five-day average to one day. Because stage criteria were now observable, the firm could forecast revenue with enough confidence to make hiring decisions ahead of demand rather than after it.</p>
<p>The team's adoption was faster than expected, largely because the new process removed work rather than adding it. Partners were no longer writing proposals from scratch or trying to remember who they owed a follow-up.</p>""",
    },
    {
        "slug": "construction-operating-cadence",
        "title": "Construction Company Installs Operating Cadence",
        "industry": "Construction",
        "profile": "60 employees | $8M revenue | Regional",
        "duration": "6-month engagement",
        "services": [("Leadership Consulting", "/services/leadership/"), ("Operations Consulting", "/services/operations/")],
        "challenge": "A regional construction company with $8M in revenue was growing fast but struggling with project coordination, subcontractor management, and internal communication. The leadership team spent most of their time in reactive mode.",
        "solution": "We installed a leadership cadence with weekly strategic meetings, daily huddles for project managers, and a scorecard system that tracked key metrics across all active projects. Role clarity was established for project handoffs.",
        "results": ["Leadership meetings went from reactive to strategic", "Project handoff errors reduced by 70%", "Subcontractor coordination improved significantly", "Owner was able to focus on business development instead of operations"],
        "metrics": [("70%", "Fewer handoff errors"), ("100%", "Projects on one scorecard"), ("6 mo", "To full adoption")],
        "quote": "Our leadership meetings used to be three hours of updates nobody acted on. Now they are forty minutes and we leave with decisions.",
        "quote_role": "President, Construction Client",
        "situation": """<p>Growth had outrun coordination. The company was running more concurrent projects than at any point in its history, and the informal communication that worked at half the size had stopped working entirely. Project managers were solving the same problems in parallel without knowing it.</p>
<p>Leadership meetings had become status recitations. Each person reported what happened, nobody made decisions, and the meeting ran three hours because there was no mechanism to end a topic. The genuinely urgent items were being handled in hallway conversations afterward, which meant they were invisible to everyone not in the hallway.</p>
<p>Handoffs between estimating, project management, and field crews were where most of the cost leaked. Assumptions made during estimating were not reliably transmitted, so field crews discovered scope surprises at the worst possible time.</p>""",
        "approach": """<h3>Two cadences, two altitudes</h3>
<p>Project managers got a daily 15-minute huddle focused strictly on blockers and the next 24 hours. Leadership got a weekly meeting with a fixed agenda built around a scorecard, where the only items discussed were metrics off target and decisions requiring the group. Everything else moved to written updates.</p>
<h3>One scorecard for every project</h3>
<p>We built a single scorecard covering all active projects with a consistent set of measures: schedule variance, budget variance, open RFIs, and safety incidents. Consistency mattered more than sophistication. When every project reports the same numbers the same way, outliers announce themselves.</p>
<h3>Making the handoff a real event</h3>
<p>The estimating-to-field handoff was redesigned as a documented meeting with a checklist of assumptions, exclusions, and known risks. It added roughly 40 minutes per project and removed the category of surprise that had been the most expensive.</p>
<h3>Naming who owns what</h3>
<p>We wrote a one-page accountability chart for each seat, defining what that role owns, what it is measured on, and what it decides without escalating. Most disputes turned out to be about ownership rather than competence.</p>""",
        "outcome": """<p>Handoff errors fell roughly 70%. Leadership meetings shortened to 40 minutes and produced decisions rather than updates. Subcontractor coordination improved because project managers were working from a shared picture instead of individual ones.</p>
<p>The owner's time shifted measurably toward business development. That was the outcome he had wanted for years and had not been able to reach, because the business had no mechanism to run without him inside it every day.</p>""",
    },
    {
        "slug": "healthcare-patient-operations",
        "title": "Healthcare Practice Streamlines Patient Operations",
        "industry": "Healthcare",
        "profile": "4 locations | 70 staff | Regional practice",
        "duration": "6-month engagement",
        "services": [("Operations Consulting", "/services/operations/"), ("Leadership Consulting", "/services/leadership/")],
        "challenge": "A multi-location healthcare practice was struggling with inconsistent patient experiences across locations, high staff turnover, and operational complexity that was growing faster than revenue.",
        "solution": "We standardized patient intake and communication workflows across all locations, built onboarding systems for new staff, and created a centralized reporting dashboard. Leadership meetings were restructured around metrics instead of anecdotes.",
        "results": ["Patient satisfaction scores improved by 35%", "New staff onboarding time reduced by 50%", "Operations became consistent across all locations", "Revenue per location increased through better retention"],
        "metrics": [("35%", "Higher patient satisfaction"), ("50%", "Faster onboarding"), ("4", "Locations aligned")],
        "quote": "Each office had quietly invented its own version of the practice. Patients could feel the difference even when we could not.",
        "quote_role": "Practice Administrator, Healthcare Client",
        "situation": """<p>Four locations had been added over six years, each largely inheriting the habits of whoever opened it. There was no single documented way to intake a patient, confirm an appointment, or handle a callback. Each office had drifted into its own version, and the differences had compounded quietly.</p>
<p>Patients noticed. Satisfaction scores varied by more than 20 points between the highest and lowest location, and the practice had no way to explain the gap because it had no way to compare the underlying process.</p>
<p>Staff turnover made it worse. New hires were trained by shadowing whoever was available, which propagated whatever local variant that person happened to use. Onboarding took roughly eight weeks to full productivity, and every departure reset the clock.</p>""",
        "approach": """<h3>Finding the best existing version</h3>
<p>Rather than designing an ideal workflow in a conference room, we documented how each location actually handled intake, scheduling, and follow-up, then assembled a standard from the best-performing pieces. Staff were far more willing to adopt a process that visibly came from their own colleagues.</p>
<h3>Onboarding that does not depend on who is free</h3>
<p>We built a structured 30-day onboarding path with defined milestones, a named owner for each week, and simple competency checks. New staff stopped learning by osmosis.</p>
<h3>One set of numbers</h3>
<p>A centralized dashboard reported the same measures for every location: appointment adherence, callback response time, patient satisfaction, and staffing levels. For the first time, the leadership team could see whether a location was struggling or simply different.</p>
<h3>Meetings about metrics, not anecdotes</h3>
<p>Leadership meetings were rebuilt around the dashboard. The shift from "here is a story about a difficult morning" to "this measure moved and here is why" changed what the group spent its attention on.</p>""",
        "outcome": """<p>Patient satisfaction improved roughly 35% overall, driven mostly by the lower-performing locations converging on the standard. Onboarding time to full productivity dropped by about half. Revenue per location rose, primarily through better patient retention rather than new acquisition.</p>
<p>The durable result was comparability. Once every location ran the same process and reported the same measures, leadership could tell the difference between a local problem and a systemic one, which is a distinction the practice had never been able to make.</p>""",
    },
]

# ─── Industries ─────────────────────────────────────────────────────────
INDUSTRIES = [
    {
        "slug": "professional-services",
        "name": "Professional Services",
        "icon": "&#9881;",
        "image": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800&q=80",
        "short": "Consulting firms, agencies, law offices, and accounting practices that need better client delivery and business development systems.",
        "intro": "Professional services firms sell the time and judgment of their people, which makes every operational weakness a margin problem. When delivery depends on who happens to be assigned, quality swings, utilization is hard to plan, and partners end up doing work they should have delegated two levels down.",
        "challenges": [
            ("Delivery quality varies by who is staffed", "Without documented delivery standards, every engagement is a fresh improvisation and clients experience a different firm depending on the team."),
            ("Business development competes with billable work", "Partners who are the best sellers are also the best deliverers, so pipeline dries up whenever the firm gets busy."),
            ("Utilization is measured after the fact", "Staffing decisions get made reactively, which produces simultaneous burnout and bench time inside the same quarter."),
            ("Scope creep goes unpriced", "Additional work gets absorbed rather than billed because there is no defined change process."),
        ],
        "approach": [
            ("Productize the delivery", "Define your two or three core engagement types with a documented scope, sequence, and deliverable set so quality does not depend on the assignment."),
            ("Separate selling from delivering", "Install a business development cadence that survives a busy quarter, with owners and weekly commitments that are not the first thing dropped."),
            ("Forward-looking staffing", "Build a simple capacity model that looks eight weeks ahead, so hiring and bench decisions are made on data rather than panic."),
            ("A real change-order process", "Define what counts as out of scope and the exact steps to price it, so the conversation happens before the work does."),
        ],
        "outcomes": ["Consistent delivery regardless of team assignment", "Pipeline that does not collapse when the firm gets busy", "Higher realization rates on billed hours", "Partners spending time at the altitude they are paid for"],
    },
    {
        "slug": "construction-trades",
        "name": "Construction & Trades",
        "icon": "&#9879;",
        "image": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800&q=80",
        "short": "General contractors, specialty trades, and construction companies that need project coordination, estimating systems, and operational structure.",
        "intro": "Construction businesses lose money in the gaps: between estimating and the field, between the general and the subs, between what was assumed and what was communicated. The work itself is rarely the problem. The coordination around it usually is.",
        "challenges": [
            ("Estimating assumptions never reach the field", "Crews discover scope surprises on site, at the point where fixing them is most expensive."),
            ("Every project reports differently", "Without a common scorecard, leadership cannot tell a struggling job from a normal one until the numbers land."),
            ("Subcontractor coordination lives in text messages", "Commitments are made individually and tracked nowhere, so accountability evaporates the moment a schedule slips."),
            ("The owner is the escalation path for everything", "Growth is capped by how many decisions one person can absorb in a day."),
        ],
        "approach": [
            ("Formalize the handoff", "Turn estimating-to-field into a documented meeting with assumptions, exclusions, and known risks written down and acknowledged."),
            ("One scorecard across all jobs", "Schedule variance, budget variance, open RFIs, and safety on every project, reported identically, so outliers surface themselves."),
            ("Daily huddle, weekly review", "Fifteen minutes on blockers at the project level; a fixed-agenda leadership meeting on trends and decisions."),
            ("Written accountability by seat", "Define what each role owns, is measured on, and can decide without escalating."),
        ],
        "outcomes": ["Fewer scope surprises discovered on site", "Comparable data across every active job", "Subcontractor commitments that are tracked and enforced", "Owner time redirected from firefighting to backlog"],
    },
    {
        "slug": "healthcare",
        "name": "Healthcare",
        "icon": "&#9764;",
        "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&q=80",
        "short": "Medical practices, dental offices, therapy clinics, and healthcare organizations that need streamlined patient operations and staff management.",
        "intro": "Healthcare practices carry a documentation burden most businesses never face, and then run their actual operations on undocumented habit. Multi-location practices drift especially fast, because each office quietly invents its own version of the practice.",
        "challenges": [
            ("Patient experience varies by location", "Intake, scheduling, and follow-up drift apart until patients can feel the difference between offices."),
            ("Onboarding happens by shadowing", "New staff learn whatever local variant their trainer uses, which propagates inconsistency with every hire."),
            ("Turnover resets institutional knowledge", "When process lives in people rather than documents, every departure costs more than a salary."),
            ("Leadership decides from anecdotes", "Without comparable measures across sites, the loudest story wins the agenda."),
        ],
        "approach": [
            ("Standardize from the best existing version", "Document how each location actually works, then build the standard from the highest-performing pieces. Adoption is far easier when the process visibly came from colleagues."),
            ("Structured 30-day onboarding", "Defined milestones, a named owner per week, and simple competency checks, so productivity does not depend on who was free that day."),
            ("One dashboard, every site", "Appointment adherence, callback response time, satisfaction, and staffing reported identically across locations."),
            ("Metric-led leadership meetings", "Replace status stories with a standing review of the measures that move."),
        ],
        "outcomes": ["Consistent patient experience across every location", "Onboarding time to productivity cut substantially", "Comparable data that separates local problems from systemic ones", "Better retention driving revenue per location"],
    },
    {
        "slug": "manufacturing",
        "name": "Manufacturing",
        "icon": "&#9878;",
        "image": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&q=80",
        "short": "Production facilities and manufacturers that need process optimization, quality systems, and supply chain coordination.",
        "intro": "Manufacturers usually have more data than most businesses and less visibility. The numbers exist in the ERP; what is missing is the cadence that turns them into decisions before a problem reaches final inspection.",
        "challenges": [
            ("Delay accumulates between departments", "Every area reports finishing on time while orders still ship late, because nobody owns the gaps."),
            ("Quality is caught at the end", "Final inspection is the most expensive possible place to discover a defect."),
            ("Scheduling lives in one person's head", "A single spreadsheet and a single expert is a continuity risk, not a system."),
            ("Owner as routing mechanism", "When status flows through one person, that person becomes the constraint on throughput."),
        ],
        "approach": [
            ("Walk a real order end to end", "Timestamp every stage including the waiting. The resulting map almost always contradicts the one leadership believes."),
            ("Move quality checks upstream", "One-page checklists at the station where the work happens, with a named owner and a specific pass condition."),
            ("Daily production huddle", "A visible board of active orders; anything that has not moved in 24 hours gets a person and a date attached out loud."),
            ("Status without asking", "A simple dashboard on tools you already own, so information stops being routed through the owner."),
        ],
        "outcomes": ["Measurable reduction in delivery delays", "Defects caught upstream where rework is cheap", "Scheduling knowledge documented rather than personal", "Leadership seeing problems while they are still small"],
    },
    {
        "slug": "technology",
        "name": "Technology",
        "icon": "&#128187;",
        "image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80",
        "short": "Software companies, IT services, and tech startups that need scalable operations and structured growth frameworks.",
        "intro": "Technology companies are usually excellent at building product and improvised everywhere else. The engineering org has rituals, retrospectives, and metrics; sales, onboarding, and support often have none of it, and that asymmetry is what stalls growth after product-market fit.",
        "challenges": [
            ("Go-to-market has no operating rhythm", "Engineering runs on cadence while revenue functions run on individual heroics."),
            ("Customer onboarding is bespoke every time", "Time-to-value varies wildly, which shows up later as churn nobody can attribute."),
            ("Support absorbs product debt silently", "Recurring issues get handled ticket by ticket instead of aggregated into a product signal."),
            ("Hiring outpaces the operating model", "Headcount grows faster than the documentation and ownership needed to absorb it."),
        ],
        "approach": [
            ("Extend cadence past engineering", "Weekly pipeline and retention reviews with the same discipline the product org already applies to itself."),
            ("Standardize time-to-value", "Define the onboarding path, its milestones, and the measure that tells you a customer is actually live."),
            ("Close the support-to-product loop", "Aggregate ticket themes into a standing review so recurring pain becomes roadmap input."),
            ("Documented ownership before the next hire", "Write the accountability chart ahead of headcount, not after the confusion."),
        ],
        "outcomes": ["Revenue functions running on rhythm, not heroics", "Predictable time-to-value and lower early churn", "Support volume feeding the roadmap", "Onboarding that scales with headcount"],
    },
    {
        "slug": "real-estate",
        "name": "Real Estate",
        "icon": "&#127968;",
        "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&q=80",
        "short": "Brokerages, property managers, and real estate investors that need deal flow systems and operational efficiency.",
        "intro": "Real estate businesses run on deal flow and follow-up, and both degrade quietly. The pipeline looks healthy right up until the month it does not, because nothing in the process forces an honest look at what is actually progressing.",
        "challenges": [
            ("Deal flow depends on individual relationships", "When sourcing lives entirely with one or two people, the business inherits their bandwidth as a ceiling."),
            ("Follow-up is inconsistent by nature of the work", "Long cycles and constant interruption make it easy for a warm lead to go cold unnoticed."),
            ("Property operations vary by manager", "Tenant experience, maintenance response, and reporting drift apart across a portfolio."),
            ("Reporting is assembled, not produced", "Investor and owner reporting eats days each month because the underlying data is scattered."),
        ],
        "approach": [
            ("Systematize sourcing", "Define the channels, the weekly activity targets, and the owner for each, so deal flow is a process rather than a personality."),
            ("Follow-up standards with a clock", "Every stage gets a maximum elapsed time and an owner; the CRM surfaces anything past it."),
            ("A property operations standard", "One documented approach to maintenance intake, tenant communication, and turnover across the portfolio."),
            ("Reporting that assembles itself", "Standardize the inputs so the monthly package is generated rather than reconstructed."),
        ],
        "outcomes": ["Deal flow that does not depend on one person's calendar", "Fewer warm leads lost to silence", "Consistent tenant and owner experience across properties", "Monthly reporting in hours instead of days"],
    },
    {
        "slug": "retail-ecommerce",
        "name": "Retail & E-Commerce",
        "icon": "&#128722;",
        "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&q=80",
        "short": "Brick-and-mortar retailers and online sellers that need inventory management, customer experience systems, and growth strategy.",
        "intro": "Retail and e-commerce businesses live and die on working capital and repeat purchase, and both are downstream of operational discipline. Most owners we meet are optimizing ad spend while inventory decisions quietly consume the margin those ads generated.",
        "challenges": [
            ("Inventory decisions are made on instinct", "Overstock ties up cash while stockouts hand revenue to a competitor, often in the same month."),
            ("Customer experience is inconsistent across channels", "In-store, online, and support each behave differently, which erodes the repeat purchase rate."),
            ("Acquisition cost is tracked, retention is not", "Marketing gets scrutinized weekly while the far cheaper lever goes unmeasured."),
            ("Peak season exposes every weak process", "The systems that hold at normal volume fail exactly when the stakes are highest."),
        ],
        "approach": [
            ("Inventory on a reorder discipline", "Defined reorder points, lead-time assumptions, and a weekly review, so purchasing stops being a gut call."),
            ("One customer standard across channels", "Document the experience you intend, then make each channel meet it."),
            ("Measure retention explicitly", "Repeat rate, time between purchases, and cohort value alongside acquisition cost."),
            ("Rehearse peak before it arrives", "Stress the process at planned volume and fix what breaks while it is cheap to fix."),
        ],
        "outcomes": ["Working capital freed from the wrong inventory", "A consistent experience that supports repeat purchase", "Retention treated as a managed metric", "Peak season that runs on process rather than adrenaline"],
    },
    {
        "slug": "financial-services",
        "name": "Financial Services",
        "icon": "&#128176;",
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80",
        "short": "Wealth management firms, insurance agencies, and financial planners that need client management and compliance-friendly operations.",
        "intro": "Financial services firms operate under real compliance constraints, and those constraints are usually blamed for operational drag that has a different cause. Documented process is not in tension with compliance; it is the thing that makes compliance survivable.",
        "challenges": [
            ("Client service depends on the advisor", "Service levels vary across the book, and the firm has no way to see it until a client leaves."),
            ("Compliance work is reactive", "Documentation gets assembled under audit pressure rather than produced as a byproduct of normal work."),
            ("Onboarding a new client takes too long", "Paperwork-heavy processes with no defined sequence stretch time-to-funded."),
            ("Succession risk sits unaddressed", "Relationships live with individuals, which caps enterprise value and creates continuity exposure."),
        ],
        "approach": [
            ("Define the service model by segment", "Document what each client tier receives and when, so service is a standard rather than a habit."),
            ("Compliance as a byproduct", "Design workflows so the documentation an audit requires is produced during normal work, not reconstructed after."),
            ("A defined onboarding sequence", "Named steps, owners, and elapsed-time targets from signed to funded."),
            ("Institutionalize the relationship", "Move client knowledge into shared systems so the firm, not the individual, owns the relationship."),
        ],
        "outcomes": ["Consistent service across the entire book", "Audit readiness without a fire drill", "Faster time from signed to funded", "Reduced key-person risk and higher enterprise value"],
    },
]

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
<div class="topbar">
<div class="topbar-inner">
<span class="topbar-note">Pittsburgh, PA &middot; Serving business owners nationwide</span>
<span class="topbar-links">
<a href="/search/" aria-label="Search the site">&#9906; Search</a>
<a href="{PHONE_HREF}">&#9742; {PHONE}</a>
<a href="mailto:{EMAIL}">&#9993; Email Us</a>
</span>
</div>
</div>
<div class="header-inner">
<a href="/" class="logo" aria-label="Elixir Consulting Group home">Elixir<span>.</span></a>
<nav aria-label="Main">
<button type="button" class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav-menu">
<span></span><span></span><span></span>
</button>
<ul class="nav-menu" id="nav-menu">
{nav_html}
</ul>
</nav>
</div>
</header>"""


def make_trust_bar():
    return """<div class="trust-bar">
<div class="container">
<div class="trust-row">
<span class="trust-item"><span>&#9733;</span> 150+ businesses served</span>
<span class="trust-item"><span>&#10003;</span> 92% client retention</span>
<span class="trust-item"><span>&#9873;</span> Led by Dr. Connor Robertson</span>
<span class="trust-item"><span>&#9781;</span> Implementation, not advice</span>
<span class="trust-item"><span>&#9992;</span> Pittsburgh based, nationwide</span>
</div>
</div>
</div>"""


def render_faq_section(items, heading="Frequently Asked Questions", intro="", gray=True):
    """Visible FAQ accordion. Always paired with make_page(faq=items) for FAQPage schema."""
    rows = ""
    for q, a in items:
        rows += f"""<div class="faq-item">
<div class="faq-q" role="button" tabindex="0">{q}</div>
<div class="faq-a"><p>{a}</p></div>
</div>\n"""
    intro_html = f'<p style="max-width:640px;margin:0 auto">{intro}</p>' if intro else ""
    return f"""<section class="section{' section-gray' if gray else ''}">
<div class="container">
<div class="text-center" style="margin-bottom:36px">
<span class="eyebrow">Questions</span>
<h2>{heading}</h2>
{intro_html}
</div>
<div style="max-width:820px;margin:0 auto">
{rows}
</div>
</div>
</section>"""


_GLOBAL_SCHEMA_CACHE = []


def make_global_schema():
    """Organization + WebSite + Person graph emitted on every page.

    Organization rather than LocalBusiness: the practice is headquartered in
    Pittsburgh but the client base is nationwide, so a local-business type would
    misrepresent the service area.
    """
    if _GLOBAL_SCHEMA_CACHE:
        return _GLOBAL_SCHEMA_CACHE[0]

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": DOMAIN + "/#organization",
                "name": "Elixir Consulting Group",
                "alternateName": "Elixir Consulting",
                "url": DOMAIN,
                "logo": {"@type": "ImageObject", "url": OG_IMAGE, "width": 1200, "height": 630},
                "image": OG_IMAGE,
                "description": "Business consulting firm specializing in operations, sales systems, AI adoption, and leadership development for owner-led companies. Headquartered in Pittsburgh, PA, serving clients nationwide.",
                "telephone": "+1-412-387-7656",
                "email": EMAIL,
                "foundingDate": "2019",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "429 Fourth Ave. Suite 300",
                    "addressLocality": "Pittsburgh",
                    "addressRegion": "PA",
                    "postalCode": "15219",
                    "addressCountry": "US",
                },
                "areaServed": {"@type": "Country", "name": "United States"},
                "founder": {"@id": DOMAIN + "/#founder"},
                "knowsAbout": [
                    "Business Strategy Consulting", "Operations Consulting",
                    "AI Consulting", "Sales Strategy", "Leadership Development",
                    "Exit Planning", "Business Process Improvement",
                ],
                "contactPoint": {
                    "@type": "ContactPoint",
                    "telephone": "+1-412-387-7656",
                    "email": EMAIL,
                    "contactType": "sales",
                    "areaServed": "US",
                    "availableLanguage": "English",
                },
                "sameAs": [
                    "https://drconnorrobertson.com",
                    "https://thepittsburghwire.com",
                    "https://www.youtube.com/@TheProspectingShow",
                ],
            },
            {
                "@type": "Person",
                "@id": DOMAIN + "/#founder",
                "name": "Dr. Connor Robertson",
                "url": "https://drconnorrobertson.com",
                "image": DOMAIN + HEADSHOT,
                "jobTitle": "Founder & Lead Consultant",
                "worksFor": {"@id": DOMAIN + "/#organization"},
                "sameAs": [
                    "https://drconnorrobertson.com",
                    "https://drconnorrobertsonbooks.com",
                    "https://www.barnesandnoble.com/s/Connor+Robertson",
                ],
            },
            {
                "@type": "WebSite",
                "@id": DOMAIN + "/#website",
                "url": DOMAIN,
                "name": "Elixir Consulting Group",
                "publisher": {"@id": DOMAIN + "/#organization"},
                "inLanguage": "en-US",
            },
        ],
    }
    out = '<script type="application/ld+json">\n' + json.dumps(graph) + '\n</script>'
    _GLOBAL_SCHEMA_CACHE.append(out)
    return out


def make_faq_schema(items):
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(obj) + '\n</script>'


def make_footer():
    return f"""<footer class="footer">
<div class="container">
<div class="footer-grid">
<div>
<h4>Elixir Consulting Group</h4>
<p class="footer-desc">Business growth, operations, and execution support for owners who want results. Based in Pittsburgh, PA. Serving clients nationwide.</p>
<p style="margin-top:16px;font-size:.9rem">{ADDRESS}</p>
<p style="margin-top:10px;font-size:.95rem"><a href="{PHONE_HREF}" style="font-weight:700;color:#fff">{PHONE}</a></p>
<p style="font-size:.95rem"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p style="margin-top:16px"><a href="/contact/" class="btn btn-gold" style="padding:12px 24px;font-size:.9rem">Book a Consult</a></p>
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
<li><a href="/blog/author/dr-connor-robertson/">Articles by Dr. Robertson</a></li>
<li><a href="/process/">How We Work</a></li>
<li><a href="/faq/">FAQ</a></li>
<li><a href="/testimonials/">Testimonials</a></li>
<li><a href="/search/">Search</a></li>
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
<li><a href="/consulting/">All Locations</a></li>
</ul>
</div>
<div>
<h4>Connect</h4>
<ul>
<li><a href="/contact/">Contact Us</a></li>
<li><a href="tel:+14123877656">(412) 387-7656</a></li>
<li><a href="mailto:info@elixirconsultinggroup.com">info@elixirconsultinggroup.com</a></li>
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


def make_breadcrumb_schema(path, last_name=None):
    """Generate BreadcrumbList JSON-LD schema from the URL path."""
    if path in ("/404", "/404.html") or path == "":
        return ""
    
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}]
    
    # Map path segments to readable names
    segment_names = {
        "about": "About",
        "services": "Services",
        "business-strategy": "Business Strategy",
        "ai-consulting": "AI Consulting",
        "operations": "Operations",
        "sales-strategy": "Sales Strategy",
        "leadership": "Leadership",
        "blog": "Blog",
        "contact": "Contact",
        "faq": "FAQ",
        "industries": "Industries",
        "case-studies": "Case Studies",
        "testimonials": "Testimonials",
    }
    
    parts = [p for p in path.strip("/").split("/") if p]
    accumulated = ""
    for i, part in enumerate(parts):
        accumulated += f"/{part}"
        name = segment_names.get(part, part.replace("-", " ").title())
        if last_name and i == len(parts) - 1:
            name = last_name
        pos = i + 2
        item_url = DOMAIN + accumulated + "/"
        items.append({"@type": "ListItem", "position": pos, "name": name, "item": item_url})
    
    import json as _json
    schema_obj = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    return f"""<script type="application/ld+json">
{_json.dumps(schema_obj)}
</script>"""


def esc_attr(s):
    """Escape a string for safe use inside a double-quoted HTML attribute."""
    return (str(s).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def esc_text(s):
    """Escape plain text (titles, excerpts) for placement in element content."""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def og_image_for(path):
    """Use a page's own Open Graph card when make_og_images.py has produced one.

    Falls back to the site-wide card, so adding a page never yields a broken
    social preview and generating a card for it later needs no template change.
    """
    slug = path.strip("/").replace("/", "-") or "home"
    if os.path.isfile(os.path.join(SITE_DIR, "images", "og", f"{slug}.png")):
        return f"{DOMAIN}/images/og/{slug}.png"
    return OG_IMAGE


def make_page(title, description, path, body, schema="", canonical=None,
              image=None, og_type="website", extra_head="", faq=None,
              published=None, modified=None, crumb_override=None, og_title=None):
    if canonical is None:
        canonical = DOMAIN + path
    image = image or og_image_for(path)
    description = clip(description, 158)

    title_a = esc_attr(og_title or title)
    desc_a = esc_attr(description)
    image_a = esc_attr(image)

    article_meta = ""
    if og_type == "article":
        article_meta = f"""<meta property="article:published_time" content="{published or DATE_NOW}">
<meta property="article:modified_time" content="{modified or published or DATE_NOW}">
<meta property="article:author" content="Dr. Connor Robertson">
<meta property="article:publisher" content="https://elixirconsultinggroup.com">
"""

    faq_schema = make_faq_schema(faq) if faq else ""
    global_schema = make_global_schema()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>{title}</title>
<meta name="description" content="{desc_a}">
<meta name="author" content="Dr. Connor Robertson">
<meta name="theme-color" content="#002E5B">
<meta name="format-detection" content="telephone=yes">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/images/icon-192.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Elixir Consulting Group Blog" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com" crossorigin>
<link rel="dns-prefetch" href="https://images.unsplash.com">
<meta property="og:title" content="{title_a}">
<meta property="og:description" content="{desc_a}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Elixir Consulting Group">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{image_a}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title_a}">
{article_meta}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title_a}">
<meta name="twitter:description" content="{desc_a}">
<meta name="twitter:image" content="{image_a}">
<meta name="twitter:image:alt" content="{title_a}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="google-site-verification" content="googleb0b4e7581f87b498">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{SHARED_CSS}</style>
{global_schema}
{schema}
{faq_schema}
{make_breadcrumb_schema(path, crumb_override)}
{extra_head}
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<div class="nav-backdrop" aria-hidden="true"></div>
{make_header(path)}
<main class="site-main" id="main-content">
{body}
</main>
{make_footer()}
<script>
(function(){{
var menu=document.querySelector('.nav-menu')||document.querySelector('.nav-links');
var toggle=document.querySelector('.nav-toggle');
var backdrop=document.querySelector('.nav-backdrop');
if(!menu||!toggle)return;
function setOpen(open){{
menu.classList.toggle('active',open);
toggle.classList.toggle('active',open);
if(backdrop)backdrop.classList.toggle('active',open);
document.body.classList.toggle('nav-open',open);
toggle.setAttribute('aria-expanded',open?'true':'false');
}}
toggle.addEventListener('click',function(e){{e.stopPropagation();setOpen(!menu.classList.contains('active'))}});
if(backdrop)backdrop.addEventListener('click',function(){{setOpen(false)}});
menu.addEventListener('click',function(e){{if(e.target.closest('a'))setOpen(false)}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')setOpen(false)}});
window.addEventListener('resize',function(){{if(window.innerWidth>768)setOpen(false)}});
}})();
document.querySelectorAll('.faq-item').forEach(function(item){{
var q=item.querySelector('.faq-q');if(!q)return;
q.setAttribute('aria-expanded','false');
function tog(){{var open=!item.classList.contains('active');item.classList.toggle('active',open);q.setAttribute('aria-expanded',open?'true':'false')}}
q.addEventListener('click',tog);
q.addEventListener('keydown',function(e){{if(e.key==='Enter'||e.key===' '){{e.preventDefault();tog()}}}});
}});
if('IntersectionObserver' in window){{const observer=new IntersectionObserver(function(entries){{entries.forEach(function(entry){{if(entry.isIntersecting){{const img=entry.target;img.src=img.dataset.src;img.classList.add('loaded');observer.unobserve(img)}}}});}});document.querySelectorAll('img[data-src]').forEach(img=>observer.observe(img))}}else{{document.querySelectorAll('img[data-src]').forEach(function(img){{img.src=img.dataset.src}})}}
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

def gen_homepage(all_posts=None):
    all_posts = all_posts or []
    testimonials_html = ""
    for t in TESTIMONIALS[:6]:
        testimonials_html += f"""<div class="testimonial-card">
<p class="quote">"{t['text']}"</p>
<p class="author">{t['name']}</p>
<p class="role">{t['role']}</p>
</div>\n"""

    industry_cards = ""
    for ind in INDUSTRIES:
        industry_cards += (
            f'<div class="card" style="padding:24px">'
            f'<div class="ind-icon" style="font-size:1.6rem;margin-bottom:8px">{ind["icon"]}</div>'
            f'<h3 style="font-size:1.05rem"><a href="/industries/{ind["slug"]}/">{ind["name"]}</a></h3>'
            f'<p style="font-size:.9rem;margin-bottom:0">{clip(ind["short"], 85)}</p></div>\n')

    featured = all_posts[:3]
    blog_cards = "".join(post_card(p) for p in featured)
    post_count = len(all_posts)

    schema = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Elixir Consulting Group",
  "description": "Business consulting firm specializing in operations, sales systems, AI consulting, and leadership development for business owners.",
  "url": "https://elixirconsultinggroup.com",
  "logo": "https://elixirconsultinggroup.com/images/og-image.png",
  "image": "https://elixirconsultinggroup.com/images/og-image.png",
  "telephone": "+1-412-387-7656",
  "email": "info@elixirconsultinggroup.com",
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
<a href="{PHONE_HREF}" class="btn btn-outline" style="border-color:rgba(255,255,255,.4);color:#fff">Call {PHONE}</a>
</div>
</section>

{make_trust_bar()}

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

<section class="section section-navy">
<div class="container">
<div class="text-center" style="margin-bottom:44px">
<span class="eyebrow">Proof</span>
<h2>What Changes When the Systems Go In</h2>
<p style="max-width:660px;margin:0 auto">Four documented engagements. Details are generalized to protect client confidentiality; the numbers are not.</p>
</div>
<div class="grid grid-4">
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">40%</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Fewer delivery delays<br><a href="/case-studies/manufacturing-delivery-delays/" style="color:{COLORS['gold']};font-size:.85rem">Manufacturing &rarr;</a></span></div>
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">2x</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Close rate<br><a href="/case-studies/professional-services-close-rate/" style="color:{COLORS['gold']};font-size:.85rem">Professional Services &rarr;</a></span></div>
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">70%</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Fewer handoff errors<br><a href="/case-studies/construction-operating-cadence/" style="color:{COLORS['gold']};font-size:.85rem">Construction &rarr;</a></span></div>
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">35%</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Higher satisfaction<br><a href="/case-studies/healthcare-patient-operations/" style="color:{COLORS['gold']};font-size:.85rem">Healthcare &rarr;</a></span></div>
</div>
<div class="text-center" style="margin-top:36px">
<a href="/case-studies/" class="btn btn-gold">Read the Case Studies</a>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="split-2 split-center">
<div>
<span class="eyebrow">How We Work</span>
<h2>Implementation Is the Product</h2>
<p>Most consulting engagements end at the recommendation. Ours starts there. We map how work actually moves through your business, design the systems with your leadership team, then sit in the room while they get adopted and fix what does not survive contact with reality.</p>
<p>Engagements run roughly 90 days to six months and end when your team runs the cadence without us.</p>
<a href="/process/" class="btn btn-primary" style="margin-top:8px">See the Full Process</a>
</div>
<div>
<div class="process-step"><div class="step-num">01</div><div class="step-content"><h3>Consult</h3><p>An honest read on whether we are the right partner, including when the answer is no.</p></div></div>
<div class="process-step"><div class="step-num">02</div><div class="step-content"><h3>Structured Assessment</h3><p>We map what actually happens, not what the org chart says should.</p></div></div>
<div class="process-step"><div class="step-num">03</div><div class="step-content"><h3>Design</h3><p>Cadence, scorecards, and ownership built with your team, not for them.</p></div></div>
<div class="process-step"><div class="step-num">04</div><div class="step-content"><h3>Implementation</h3><p>We run the first cycles alongside your people and adjust while adjustment is cheap.</p></div></div>
</div>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:44px">
<span class="eyebrow">Industries</span>
<h2>Sector Context, Not Generic Advice</h2>
<p style="max-width:660px;margin:0 auto">The frameworks transfer between industries because the constraints are structural. The context does not, which is why each sector gets its own page.</p>
</div>
<div class="grid grid-4">
{industry_cards}
</div>
<div class="text-center" style="margin-top:32px">
<a href="/industries/" class="btn btn-outline">All Eight Industries</a>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="split-2 split-center">
<div>
<span class="eyebrow">About the Founder</span>
<h2>Dr. Connor Robertson</h2>
<p>Dr. Connor Robertson is the founder and lead consultant at Elixir Consulting Group. With extensive experience in business strategy, operational growth, and organizational development, Dr. Robertson helps businesses identify opportunities, improve performance, and achieve sustainable success.</p>
<p>Through hands-on implementation and structured frameworks, he works directly with owners and leadership teams to install the systems that produce real results.</p>
<a href="https://drconnorrobertson.com" target="_blank" rel="noopener" class="btn btn-outline" style="margin-top:8px">Learn More About Dr. Robertson</a>
</div>
<div style="background:{COLORS['off_white']};border-radius:16px;padding:48px;text-align:center">
<img src="/images/dr-connor-robertson.jpg" alt="Dr. Connor Robertson, Founder and Lead Consultant at Elixir Consulting Group" width="800" height="800" style="border-radius:50%;width:clamp(140px,40vw,160px);height:clamp(140px,40vw,160px);object-fit:cover;margin:0 auto 24px;display:block" loading="lazy">
<h3 style="margin-bottom:4px">Dr. Connor Robertson</h3>
<p style="color:{COLORS['mid_gray']};margin-bottom:16px">Founder & Lead Consultant</p>
<p style="font-size:.9rem">Specializing in business strategy, operations, AI consulting, and organizational development.</p>
</div>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:48px">
<span class="eyebrow">Resources</span>
<h2>Books by Dr. Connor Robertson</h2>
<p style="max-width:700px;margin:0 auto">Practical guides on business acquisitions, wealth building, and operational strategy. Each book distills the frameworks and systems Dr. Robertson uses with consulting clients into actionable playbooks.</p>
</div>
<div class="grid grid-3">
<div class="card">
<h3>Creative Acquisitions</h3>
<p>The playbook for modern dealmakers. How to buy real businesses using flexible, creative, and durable acquisition strategies.</p>
<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">
<a href="https://www.barnesandnoble.com/w/creative-acquisitions-by-dr-connor-robertson-connor-robertson/1148958050" target="_blank" rel="noopener" class="btn btn-primary" style="padding:8px 16px;font-size:.8rem">Barnes & Noble</a>
<a href="https://www.kobo.com/us/en/ebook/creative-acquisitions-by-dr-connor-robertson" target="_blank" rel="noopener" class="btn btn-outline" style="padding:8px 16px;font-size:.8rem">Kobo</a>
</div>
</div>
<div class="card">
<h3>Buying Wealth</h3>
<p>A straightforward guide to ownership and practical wealth-building through asset acquisition, disciplined leverage, and systematic growth.</p>
<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">
<a href="https://play.google.com/store/books/details/Dr_Connor_Robertson_Buying_Wealth?id=Dw2HEQAAQBAJ" target="_blank" rel="noopener" class="btn btn-primary" style="padding:8px 16px;font-size:.8rem">Google Play</a>
</div>
</div>
<div class="card">
<h3>The 7 Minute Phone Call</h3>
<p>How to restart stalled conversations and move deals forward faster. A practical guide to building trust through short, structured calls.</p>
<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">
<a href="https://play.google.com/store/books/details/Dr_Connor_Robertson_The_7_Minute_Phone_Call?id=9QyHEQAAQBAJ" target="_blank" rel="noopener" class="btn btn-primary" style="padding:8px 16px;font-size:.8rem">Google Play</a>
</div>
</div>
<div class="card">
<h3>Buy The Building, Keep The Profits</h3>
<p>Why the real money is in owning the real estate your company occupies, and how to structure the deal.</p>
<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">
<a href="https://play.google.com/store/books/details/Dr_Connor_Robertson_Buy_the_Building_Keep_the_Prof?id=MRWfEQAAQBAJ" target="_blank" rel="noopener" class="btn btn-primary" style="padding:8px 16px;font-size:.8rem">Google Play</a>
<a href="https://www.barnesandnoble.com/w/buy-the-building-keep-the-profits-by-dr-connor-robertson-connor-robertson/1148885434" target="_blank" rel="noopener" class="btn btn-outline" style="padding:8px 16px;font-size:.8rem">Barnes & Noble</a>
<a href="https://www.kobo.com/us/en/ebook/buy-the-building-keep-the-profits-by-dr-connor-robertson" target="_blank" rel="noopener" class="btn btn-outline" style="padding:8px 16px;font-size:.8rem">Kobo</a>
</div>
</div>
<div class="card">
<h3>PadSplit Playbook</h3>
<p>Scaling affordable housing through shared living. A practical guide for property owners and operators.</p>
<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">
<a href="https://play.google.com/store/books/details/Dr_Connor_Robertson_Padsplit_Playbook_Scaling_Affo?id=9sSqEQAAQBAJ" target="_blank" rel="noopener" class="btn btn-primary" style="padding:8px 16px;font-size:.8rem">Google Play</a>
<a href="https://www.barnesandnoble.com/w/padsplit-playbook-by-dr-connor-robertson-connor-robertson/1149135521" target="_blank" rel="noopener" class="btn btn-outline" style="padding:8px 16px;font-size:.8rem">Barnes & Noble</a>
<a href="https://www.kobo.com/us/en/ebook/padsplit-playbook-by-dr-connor-robertson" target="_blank" rel="noopener" class="btn btn-outline" style="padding:8px 16px;font-size:.8rem">Kobo</a>
</div>
</div>
<div class="card">
<h3>Built to Run</h3>
<p>Build systems and processes that let your business operate without constant owner involvement. The framework for owner-independent operations.</p>
<p style="color:{COLORS['mid_gray']};font-size:.85rem;font-style:italic;margin-top:12px">Coming Soon</p>
</div>
</div>
<div class="text-center" style="margin-top:40px">
<a href="https://drconnorrobertsonbooks.com" target="_blank" rel="noopener" class="btn btn-primary">Browse All Books</a>
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
<p style="max-width:620px;margin:0 auto">{post_count} articles on operations, sales systems, AI adoption, leadership, and growth.</p>
</div>
<div class="post-list">
{blog_cards}
</div>
<div class="text-center" style="margin-top:32px">
<a href="/blog/" class="btn btn-outline">View All Articles</a>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:36px">
<span class="eyebrow">Where We Work</span>
<h2>Pittsburgh Based. Nationwide Reach.</h2>
<p style="max-width:680px;margin:0 auto">Our office is at {ADDRESS}. Roughly half of our clients are outside the region, working with us through a structured virtual process that produces the same outcomes.</p>
</div>
<div class="text-center" style="max-width:860px;margin:0 auto">
<a href="/pittsburgh-business-consultant/" class="services-link">Pittsburgh</a>
<a href="/pittsburgh-ai-consulting/" class="services-link">Pittsburgh AI</a>
<a href="/pittsburgh-operations-consulting/" class="services-link">Pittsburgh Operations</a>
<a href="/cranberry-township-business-consultant/" class="services-link">Cranberry Township</a>
<a href="/wexford-business-consultant/" class="services-link">Wexford</a>
<a href="/consulting/" class="services-link">All Locations</a>
</div>
</div>
</section>

{render_faq_section(HOME_FAQS, "Common Questions", "Straight answers to what business owners ask before booking a consult.")}

{make_cta()}
"""
    return make_page(
        "Business Consulting Pittsburgh, PA | Elixir Consulting Group",
        "Elixir Consulting Group helps business owners build operations, sales systems, and leadership cadence that produce consistent execution and measurable growth. Based in Pittsburgh, PA.",
        "/",
        body,
        schema,
        faq=HOME_FAQS,
    )


def gen_about():
    schema = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Elixir Consulting Group","url":"https://elixirconsultinggroup.com","logo":"https://elixirconsultinggroup.com/images/og-image.png","image":"https://elixirconsultinggroup.com/images/og-image.png","telephone":"+1-412-387-7656","email":"info@elixirconsultinggroup.com","founder":{"@type":"Person","name":"Dr. Connor Robertson","url":"https://drconnorrobertson.com"},"address":{"@type":"PostalAddress","streetAddress":"429 Fourth Ave. Suite 300","addressLocality":"Pittsburgh","addressRegion":"PA","postalCode":"15219","addressCountry":"US"}}
</script>"""

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / About</p>
<h1>About Elixir Consulting Group</h1>
<p>Built for business owners who are tired of operating in reaction mode.</p>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">
<div class="split-1-2 split-center">
<div style="text-align:center">
<img src="{HEADSHOT}" alt="{HEADSHOT_ALT}" width="800" height="800" style="width:clamp(220px,72vw,340px);height:clamp(220px,72vw,340px);border-radius:50%;object-fit:cover;margin:0 auto 24px;display:block;box-shadow:0 16px 44px rgba(0,46,91,.22)" fetchpriority="high" decoding="async">
<h2 style="font-size:clamp(1.5rem,4vw,1.9rem);margin-bottom:4px">Dr. Connor Robertson</h2>
<p style="color:{COLORS['mid_gray']};font-weight:600;margin-bottom:16px">Founder &amp; Lead Consultant</p>
<div class="contact-strip" style="grid-template-columns:1fr;max-width:320px;margin:0 auto">
<a href="{PHONE_HREF}"><span class="ic">&#9742;</span> {PHONE}</a>
<a href="/contact/"><span class="ic">&#9993;</span> Book a Consult</a>
</div>
</div>
<div>
<span class="eyebrow">Meet the Founder</span>
<h2>Hands-On, Implementation-First Consulting</h2>
<p>Dr. Connor Robertson is the founder and lead consultant at Elixir Consulting Group, bringing extensive experience in business strategy, operational growth, and organizational development to owner-led companies across the country.</p>
<p>Working with entrepreneurs and established companies, Dr. Robertson helps organizations identify opportunities, improve performance, and achieve sustainable long-term success. His approach is hands-on: he works alongside owners and leadership teams to install the systems rather than hand over a set of recommendations and walk away.</p>
<p>His expertise spans business strategy, operations consulting, AI and digital transformation, sales system design, and leadership development. He is the author of six books on business acquisitions and strategy, including <a href="https://www.barnesandnoble.com/w/creative-acquisitions-by-dr-connor-robertson-connor-robertson/1148958050" target="_blank" rel="noopener"><em>Creative Acquisitions</em></a>, <a href="https://play.google.com/store/books/details/Dr_Connor_Robertson_Buying_Wealth?id=Dw2HEQAAQBAJ" target="_blank" rel="noopener"><em>Buying Wealth</em></a>, and <a href="https://play.google.com/store/books/details/Dr_Connor_Robertson_The_7_Minute_Phone_Call?id=9QyHEQAAQBAJ" target="_blank" rel="noopener"><em>The 7 Minute Phone Call</em></a>.</p>
<div class="split-stats" style="margin:24px 0">
<div><span class="stat-num" style="font-size:1.9rem">150+</span><br><span class="stat-label">Businesses Served</span></div>
<div><span class="stat-num" style="font-size:1.9rem">6</span><br><span class="stat-label">Books Published</span></div>
</div>
<a href="https://drconnorrobertson.com" target="_blank" rel="noopener" class="btn btn-primary">Visit DrConnorRobertson.com</a>
<a href="/blog/" class="btn btn-outline">Read His Articles</a>
</div>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="split-2 split-center">
<div>
<span class="eyebrow">Our Story</span>
<h2>From Chaos to Structure</h2>
<p>Elixir Consulting Group was built for business owners who are tired of operating in reaction mode. Many companies grow quickly but never pause to build the systems that support that growth. Over time, everything becomes harder than it should be. Decisions slow down. Teams get confused. The owner becomes the bottleneck.</p>
<p>Our work exists to fix that. We focus on helping owners move from chaos to structure without overcomplicating the business. That means simplifying processes, installing a clear operating cadence, and making execution visible every week.</p>
<p>The goal is not perfection. The goal is consistency.</p>
</div>
<div style="background:{COLORS['off_white']};border-radius:16px;padding:48px">
<h3 style="margin-bottom:24px">By the Numbers</h3>
<div class="split-stats">
<div><span class="stat-num" style="font-size:2rem">150+</span><br><span class="stat-label">Businesses Served</span></div>
<div><span class="stat-num" style="font-size:2rem">92%</span><br><span class="stat-label">Retention Rate</span></div>
<div><span class="stat-num" style="font-size:2rem">50+</span><br><span class="stat-label">Industries</span></div>
<div><span class="stat-num" style="font-size:2rem">5x</span><br><span class="stat-label">Avg. ROI</span></div>
</div>
</div>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div style="max-width:820px;margin:0 auto">
<div>
<span class="eyebrow">Background</span>
<h2>More on Dr. Connor Robertson</h2>
<p>Dr. Connor Robertson is the founder and lead consultant at Elixir Consulting Group, bringing extensive experience in business strategy, operational growth, and organizational development.</p>
<p>Through his work with entrepreneurs and established companies, Dr. Robertson helps organizations identify opportunities, improve performance, and achieve sustainable long-term success. His approach is hands-on and implementation-focused. He works alongside owners and leadership teams to install the systems, not just recommend them.</p>
<p>Dr. Robertson's expertise spans business strategy, operations consulting, AI and digital transformation, sales system design, and leadership development. His work has helped businesses across industries build the structure they need to grow without chaos.</p>
<p>He is the author of six books on business acquisitions and strategy, including <a href="https://www.barnesandnoble.com/w/creative-acquisitions-by-dr-connor-robertson-connor-robertson/1148958050" target="_blank" rel="noopener"><em>Creative Acquisitions</em></a>, <a href="https://play.google.com/store/books/details/Dr_Connor_Robertson_Buying_Wealth?id=Dw2HEQAAQBAJ" target="_blank" rel="noopener"><em>Buying Wealth</em></a>, and <a href="https://play.google.com/store/books/details/Dr_Connor_Robertson_The_7_Minute_Phone_Call?id=9QyHEQAAQBAJ" target="_blank" rel="noopener"><em>The 7 Minute Phone Call</em></a>. His books are available on <a href="https://www.barnesandnoble.com/s/Connor+Robertson" target="_blank" rel="noopener">Barnes & Noble</a>, <a href="https://play.google.com/store/books/details/Dr_Connor_Robertson_Buying_Wealth?id=Dw2HEQAAQBAJ" target="_blank" rel="noopener">Google Play</a>, and <a href="https://www.kobo.com/us/en/search?query=Connor+Robertson&fcsearchfield=Author" target="_blank" rel="noopener">Kobo</a>.</p>
<a href="https://drconnorrobertson.com" target="_blank" rel="noopener" class="btn btn-primary" style="margin-top:12px">Visit DrConnorRobertson.com</a>
</div>
</div>
</div>
</section>

<section class="section section-gray">
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

<section class="section">
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

{render_faq_section(ABOUT_FAQS, "About Elixir: Common Questions")}

{make_cta()}
"""
    return make_page(
        "About Dr. Connor Robertson | Elixir Consulting Group",
        "Meet Dr. Connor Robertson, founder of Elixir Consulting Group. We help business owners install operations, sales systems, and leadership cadence. Pittsburgh, PA and nationwide.",
        "/about/",
        body,
        schema,
        faq=ABOUT_FAQS,
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

{render_faq_section(SERVICES_FAQS, "Service FAQs", gray=False)}

{make_cta()}
"""
    return make_page(
        "Business Consulting Services | Elixir Consulting Group",
        "Five core consulting services: business strategy, AI consulting, operations, sales strategy, and leadership development. Implementation-focused, from Pittsburgh, PA and nationwide.",
        "/services/",
        body,
        faq=SERVICES_FAQS,
    )


def gen_service_page(slug, title, tagline, intro, items, outcomes, all_posts=None):
    all_posts = all_posts or []
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
    related_articles = related_by_keywords(all_posts, [title] + keywords, 3) if all_posts else []

    related_html = ""
    if related_articles:
        cards = "".join(post_card(post) for post in related_articles)
        related_html = f"""
<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Related Reading</span>
<h2>From the Blog</h2>
</div>
<div class="post-list">{cards}</div>
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
    seo_titles = {
        "ai-consulting": "AI Consulting for Business Owners | Elixir Consulting",
        "leadership": "Leadership Consulting & Coaching | Elixir Consulting",
    }
    service_schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": title,
        "serviceType": title,
        "description": clip(tagline + " " + intro, 300),
        "provider": {"@id": DOMAIN + "/#organization"},
        "areaServed": {"@type": "Country", "name": "United States"},
        "url": DOMAIN + f"/services/{slug}/",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": f"{title} deliverables",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": i[0],
                                                   "description": i[1]}}
                for i in items
            ],
        },
    }) + '\n</script>'
    schema = service_schema + "\n" + schema

    return make_page(
        seo_titles.get(slug, f"{title} | Elixir Consulting Group"),
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
{json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Elixir Consulting Group", "description": f"Business consulting firm serving {city}, {state_abbr}. Specializing in operations, AI consulting, sales systems, and leadership development.", "url": f"https://elixirconsultinggroup.com/{slug}/", "logo": "https://elixirconsultinggroup.com/images/og-image.png", "image": "https://elixirconsultinggroup.com/images/og-image.png", "telephone": "+1-412-387-7656", "email": "info@elixirconsultinggroup.com", "address": {"@type": "PostalAddress", "streetAddress": "429 Fourth Ave. Suite 300", "addressLocality": "Pittsburgh", "addressRegion": "PA", "postalCode": "15219", "addressCountry": "US"}, "areaServed": {"@type": "City", "name": city}, "founder": {"@type": "Person", "name": "Dr. Connor Robertson", "url": "https://drconnorrobertson.com"}}, indent=2)}
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
    focus = {
        "pittsburgh-ai-consulting": ("AI Consulting", "AI consulting and digital transformation"),
        "pittsburgh-operations-consulting": ("Operations Consulting", "operations consulting, process design, and weekly operating cadence"),
    }.get(slug, ("Business Consultant", "business strategy, operations, sales systems, and leadership development"))
    return make_page(
        f"{focus[0]} in {city}, {state_abbr} | Elixir",
        clip(f"Elixir Consulting Group provides {focus[1]} for businesses in {city}, {state_abbr}. Implementation-focused engagements. Call {PHONE}.", 158),
        f"/{slug}/",
        body,
        schema,
    )


# ─── Regional consulting pages (/consulting/<city>/) ───────────────────
#
# These 30 pages were originally written by separate tooling with their own
# navigation, footer, and stylesheet. Same treatment as the blog: read the
# narrative off disk, throw the old shell away, and re-render through the
# shared template so the whole site stays on one design system.

CONSULTING_SERVICES = [
    ("Business Strategy", "/services/business-strategy/"),
    ("AI Consulting", "/services/ai-consulting/"),
    ("Operations", "/services/operations/"),
    ("Sales Strategy", "/services/sales-strategy/"),
    ("Leadership", "/services/leadership/"),
]


def _delocalize(html):
    """Rewrite absolute self-links to relative paths so links stay portable."""
    return html.replace("https://elixirconsultinggroup.com/", "/").replace(
        "https://elixirconsultinggroup.com", "/")


def parse_consulting_page(slug, html):
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    title = htmllib.unescape(
        re.sub(r"\s*\|\s*Elixir Consulting Group\s*$", "", t.group(1).strip())) if t else ""

    h1 = re.search(r"<h1>(.*?)</h1>", html, re.S)
    heading = htmllib.unescape(h1.group(1).strip()) if h1 else title

    city = heading
    m = re.match(r"Business Consulting in (.+?),\s*([A-Z]{2})$", heading)
    state = "PA"
    if m:
        city, state = m.group(1), m.group(2)
    else:
        city = slug.replace("-", " ").title()
    city = re.sub(r"[ ,]+%s$" % state, "", city, flags=re.I).strip(" ,")
    heading = f"Business Consulting in {city}, {state}"

    desc = _meta(html, "description", attr="name")

    tag = re.search(r"<p>(.*?)</p>", html[html.find("<h1>"):], re.S) if "<h1>" in html else None
    tagline = htmllib.unescape(tag.group(1).strip()) if tag else (
        f"Strategic business consulting tailored to {city}'s market dynamics and economic landscape.")

    # Pages this generator has already rewritten carry an explicit marker, so
    # look for that first; fall back to the legacy markup on the first pass.
    marker = re.search(r'<section class="content-section" id="location-body"[^>]*>', html)
    if marker:
        content = _find_balanced(html, marker.start(), "section").strip()
    else:
        content = ""
        for s in re.findall(r'<section class="content-section[^"]*">(.*?)</section>', html, re.S):
            # One of these is a boilerplate service list we re-render below.
            if "services-link" in s or "Our Consulting Services" in s:
                continue
            inner = re.search(r'<div class="container">(.*?)</div>\s*$', s.strip(), re.S)
            content += (inner.group(1) if inner else s).strip() + "\n"

    return {
        "slug": slug,
        "city": city,
        "state": state,
        "heading": heading,
        "tagline": _delocalize(tagline),
        "description": desc,
        "content": _delocalize(content).strip(),
    }


def load_consulting_pages():
    pages = []
    base = os.path.join(SITE_DIR, "consulting")
    if not os.path.isdir(base):
        return pages
    for slug in sorted(os.listdir(base)):
        fp = os.path.join(base, slug, "index.html")
        if not os.path.isfile(fp):
            continue
        try:
            with open(fp, encoding="utf-8") as f:
                parsed = parse_consulting_page(slug, f.read())
        except Exception as exc:
            print(f"  ! skipped consulting/{slug}: {exc}")
            continue
        if len(strip_tags(parsed["content"]).split()) < 40:
            print(f"  ! consulting/{slug} has no extractable body, skipping")
            continue
        pages.append(parsed)
    return pages


def consulting_faqs(page):
    city = page["city"]
    return [
        (f"Do you work with businesses in {city}?",
         f"Yes. Elixir Consulting Group works with owner-led businesses in {city} and across {page['state']}, combining virtual strategy work with on-site collaboration when the engagement calls for it. Our office is at {ADDRESS}."),
        (f"What consulting services are available to {city} businesses?",
         "Business strategy, operations consulting, AI and digital transformation, sales strategy, and leadership development. Most engagements combine two or three of these because operational problems rarely stay in one lane."),
        (f"How much does business consulting cost in {city}?",
         "Pricing depends on the scope of the engagement and the size of your business. We offer both project-based and retainer arrangements. The first step is a consult where we determine whether there is a fit before discussing pricing."),
        (f"How long does a typical {city} engagement last?",
         "Most engagements run between 90 days and six months depending on scope. Many clients continue with monthly advisory support once the initial systems are installed."),
        (f"How do we get started?",
         f"Book a consult. We will talk through your business, what is currently breaking, and what you want the next 12 months to look like, then tell you honestly whether we are the right partner for it. Call {PHONE} or use the contact page."),
    ]


def gen_consulting_page(page, siblings):
    city = page["city"]
    faqs = consulting_faqs(page)

    service_cards = ""
    for name, href in CONSULTING_SERVICES:
        service_cards += f"""<div class="card">
<h3><a href="{href}">{name}</a></h3>
<p>{name} consulting for {city} businesses, built around implementation rather than recommendations.</p>
<a href="{href}">Learn more &rarr;</a>
</div>\n"""

    nearby = [p for p in siblings if p["slug"] != page["slug"]]
    seed = sum(ord(c) for c in page["slug"])
    nearby = [nearby[(seed + i) % len(nearby)] for i in range(min(8, len(nearby)))] if nearby else []
    nearby_links = " &nbsp;&middot;&nbsp; ".join(
        f'<a href="/consulting/{p["slug"]}/">{p["city"]}</a>' for p in nearby)

    testimonial = TESTIMONIALS[seed % len(TESTIMONIALS)]

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Elixir Consulting Group",
        "url": DOMAIN,
        "logo": OG_IMAGE,
        "image": OG_IMAGE,
        "telephone": "+1-412-387-7656",
        "email": EMAIL,
        "description": f"Business consulting for companies in {city}, {page['state']}. Strategy, operations, AI consulting, sales systems, and leadership development.",
        "address": {"@type": "PostalAddress", "streetAddress": "429 Fourth Ave. Suite 300",
                    "addressLocality": "Pittsburgh", "addressRegion": "PA",
                    "postalCode": "15219", "addressCountry": "US"},
        "areaServed": [{"@type": "City", "name": city}, {"@type": "Country", "name": "United States"}],
        "founder": {"@type": "Person", "name": "Dr. Connor Robertson", "url": "https://drconnorrobertson.com"},
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / <a href="/consulting/">Consulting</a> / {city}</p>
<h1>{esc_text(page['heading'])}</h1>
<p>{esc_text(page['tagline'])}</p>
<div style="margin-top:24px">
<a href="/contact/" class="btn btn-gold">Book a Consult</a>
<a href="{PHONE_HREF}" class="btn btn-outline" style="border-color:rgba(255,255,255,.4);color:#fff">Call {PHONE}</a>
</div>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">
<div class="split-1-2">
<div>
<div class="contact-info-card">
<span class="eyebrow">Talk to Us</span>
<h3 style="margin-bottom:12px">Serving {city} Businesses</h3>
<p style="font-size:.95rem;margin-bottom:16px">Pittsburgh-based, working with owners across {page['state']} and nationwide.</p>
<p style="margin-bottom:6px"><a href="{PHONE_HREF}" style="font-weight:700">{PHONE}</a></p>
<p style="margin-bottom:16px"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<a href="/contact/" class="btn btn-primary" style="width:100%">Book a Consult</a>
</div>
<div class="testimonial-card" style="margin-top:20px">
<p class="quote">"{testimonial['text']}"</p>
<p class="author">{testimonial['name']}</p>
<p class="role">{testimonial['role']}</p>
</div>
</div>
<section class="content-section" id="location-body" style="padding:0">
{page['content']}
</section>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:44px">
<span class="eyebrow">What We Do</span>
<h2>Consulting Services for {city}</h2>
<p style="max-width:620px;margin:0 auto">Every engagement is built around installing systems your team will actually run, not a report that sits on a shelf.</p>
</div>
<div class="grid grid-3">
{service_cards}
</div>
</div>
</section>

{render_faq_section(faqs, f"{city} Consulting FAQs", gray=False)}

<section class="section section-gray">
<div class="container text-center">
<span class="eyebrow">Nearby</span>
<h2 style="margin-bottom:16px">Other Areas We Serve</h2>
<p style="max-width:760px;margin:0 auto 12px">{nearby_links}</p>
<a href="/consulting/" class="btn btn-outline" style="margin-top:16px">View All Locations</a>
</div>
</section>

{make_cta()}
"""
    desc = page["description"] or (
        f"Business consulting in {city}, {page['state']}. Strategy, operations, AI, sales systems, "
        f"and leadership development from Elixir Consulting Group. Call {PHONE}.")
    return make_page(
        f"{city}, {page['state']} Business Consulting Services | Elixir",
        clip(desc, 158),
        f"/consulting/{page['slug']}/",
        body,
        schema,
        faq=faqs,
        crumb_override=city,
    )


def gen_consulting_index(pages):
    cards = ""
    for p in sorted(pages, key=lambda x: x["city"]):
        cards += f"""<div class="card">
<h3><a href="/consulting/{p['slug']}/">{esc_text(p['city'])}, {p['state']}</a></h3>
<p>{esc_text(clip(p['tagline'], 120))}</p>
<a href="/consulting/{p['slug']}/">View {p['city']} consulting &rarr;</a>
</div>\n"""

    faqs = [
        ("Which areas does Elixir Consulting Group serve?",
         "We are based in Pittsburgh, PA and work with businesses throughout Western Pennsylvania, across the state, and nationwide. Our engagement model combines virtual strategy work with on-site collaboration when it matters."),
        ("Do you have to be local to work with Elixir?",
         "No. A large share of our clients are outside the Pittsburgh region. The systems we install -- operating cadence, scorecards, sales process, documented workflows -- are built and run the same way regardless of geography."),
        ("Is there a difference between your local and remote engagements?",
         "The structure is identical. Local engagements simply include more in-person working sessions. Outcomes depend on the leadership team's commitment to the cadence, not on travel time."),
        ("How do I know which location page applies to me?",
         "The location pages provide market context for each area we serve. If your city is not listed, that does not mean we cannot help -- book a consult and we will tell you honestly whether there is a fit."),
    ]

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Business Consulting Locations",
        "url": DOMAIN + "/consulting/",
        "description": "Regions served by Elixir Consulting Group, a Pittsburgh-based business consulting firm working with owner-led companies nationwide.",
        "hasPart": [
            {"@type": "WebPage", "name": f"Business Consulting in {p['city']}, {p['state']}",
             "url": DOMAIN + f"/consulting/{p['slug']}/"}
            for p in sorted(pages, key=lambda x: x["city"])
        ],
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Consulting Locations</p>
<h1>Business Consulting Locations</h1>
<p>Elixir Consulting Group is headquartered in Pittsburgh, PA and works with owner-led businesses across Pennsylvania and nationwide.</p>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:44px">
<span class="eyebrow">Regions We Serve</span>
<h2>Local Market Context, Nationwide Reach</h2>
<p style="max-width:680px;margin:0 auto">Each page below covers the business landscape of a specific market and how our operations, sales, and leadership work applies there.</p>
</div>
<div class="grid grid-3">
{cards}
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Focused Service Areas</span>
<h2>Pittsburgh Metro Pages</h2>
</div>
<div class="grid grid-3">
<div class="card"><h3><a href="/pittsburgh-business-consultant/">Pittsburgh Business Consultant</a></h3><p>Strategy, operations, and leadership consulting for Pittsburgh companies.</p></div>
<div class="card"><h3><a href="/pittsburgh-ai-consulting/">Pittsburgh AI Consulting</a></h3><p>Practical AI evaluation, implementation, and team adoption.</p></div>
<div class="card"><h3><a href="/pittsburgh-operations-consulting/">Pittsburgh Operations Consulting</a></h3><p>Process mapping, SOPs, and weekly operating cadence.</p></div>
<div class="card"><h3><a href="/cranberry-township-business-consultant/">Cranberry Township</a></h3><p>Consulting for one of Western PA's fastest-growing business communities.</p></div>
<div class="card"><h3><a href="/wexford-business-consultant/">Wexford</a></h3><p>Consulting for businesses across Pittsburgh's northern suburbs.</p></div>
<div class="card"><h3><a href="/contact/">Not Listed?</a></h3><p>We work with clients nationwide. Book a consult and we will tell you if there is a fit.</p></div>
</div>
</div>
</section>

{render_faq_section(faqs, "Location FAQs", gray=False)}

{make_cta()}
"""
    return make_page(
        "Consulting Locations | Elixir Consulting Group",
        f"Elixir Consulting Group serves business owners in Pittsburgh, across Pennsylvania, and nationwide. Browse {len(pages)} regional consulting pages or book a consult at {PHONE}.",
        "/consulting/",
        body,
        schema,
        faq=faqs,
    )


# ─── Industry detail pages ─────────────────────────────────────────────

def industry_faqs(ind):
    name = ind["name"]
    return [
        (f"Do you have experience with {name.lower()} businesses?",
         f"Yes. {name} is one of the sectors we work in regularly. That said, the problems we solve are structural rather than sector-specific: unclear process, weak accountability, inconsistent follow-through, and owner dependency show up the same way in every industry. We bring the operating system and learn the domain detail from your team."),
        (f"What does a {name.lower()} engagement typically involve?",
         "Every engagement starts with a consult, then a structured assessment of how work actually moves through your business today. From there we identify the few changes with the largest effect and build them alongside your team. Most engagements run 90 days to six months."),
        ("Will this disrupt our day-to-day operations?",
         "No. We work alongside your existing team and introduce changes in phases. We do not stop the business to rebuild it. The point of the work is that your team keeps running while the systems get better underneath them."),
        ("How do you measure whether it worked?",
         "We set baseline metrics at the start and review them weekly. The specific measures depend on the engagement, but they are always things your team can see and influence, not abstractions that only appear in a quarterly report."),
        (f"How much does consulting for a {name.lower()} business cost?",
         f"Pricing depends on scope and the size of your business. We offer both project-based and retainer arrangements. The first step is a consult to determine whether there is a fit before discussing pricing. Call {PHONE} to start that conversation."),
    ]


def gen_industry_page(ind, all_posts):
    faqs = industry_faqs(ind)
    name = ind["name"]

    challenges = "".join(
        f'<div class="card"><h3>{t}</h3><p>{d}</p></div>\n' for t, d in ind["challenges"])
    approach = "".join(
        f'<div class="process-step"><div class="step-num">{i:02d}</div>'
        f'<div class="step-content"><h3>{t}</h3><p>{d}</p></div></div>\n'
        for i, (t, d) in enumerate(ind["approach"], 1))
    outcomes = "".join(f"<li>{o}</li>\n" for o in ind["outcomes"])

    others = [x for x in INDUSTRIES if x["slug"] != ind["slug"]]
    seed = sum(ord(c) for c in ind["slug"])
    other_cards = "".join(
        f'<div class="card"><div class="ind-icon">{o["icon"]}</div>'
        f'<h3><a href="/industries/{o["slug"]}/">{o["name"]}</a></h3>'
        f'<p>{clip(o["short"], 110)}</p></div>\n'
        for o in [others[(seed + i) % len(others)] for i in range(3)])

    related = related_by_keywords(all_posts, [name] + [t for t, _ in ind["challenges"]], 3)
    related_cards = "".join(post_card(p) for p in related)

    case = next((c for c in CASE_STUDIES if c["industry"].lower() in name.lower()
                 or name.lower().startswith(c["industry"].lower())), None)
    case_html = ""
    if case:
        metrics = "".join(
            f'<div><span class="stat-num" style="font-size:1.8rem">{v}</span>'
            f'<br><span class="stat-label">{l}</span></div>' for v, l in case["metrics"])
        case_html = f"""
<section class="section section-navy">
<div class="container">
<div class="split-2 split-center">
<div>
<span class="eyebrow">{name} Case Study</span>
<h2>{case['title']}</h2>
<p>{case['challenge']}</p>
<a href="/case-studies/{case['slug']}/" class="btn btn-gold" style="margin-top:12px">Read the Full Case Study</a>
</div>
<div class="split-stats">{metrics}</div>
</div>
</div>
</section>
"""

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"Business Consulting for {name}",
        "serviceType": "Business Consulting",
        "description": clip(ind["intro"], 300),
        "provider": {"@id": DOMAIN + "/#organization"},
        "areaServed": {"@type": "Country", "name": "United States"},
        "audience": {"@type": "BusinessAudience", "audienceType": name},
        "url": DOMAIN + f"/industries/{ind['slug']}/",
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / <a href="/industries/">Industries</a> / {name}</p>
<p style="margin-bottom:14px"><span class="post-tag">Industry</span></p>
<h1>Business Consulting for {name}</h1>
<p>{clip(ind['short'], 190)}</p>
<div style="margin-top:24px">
<a href="/contact/" class="btn btn-gold">Book a Consult</a>
<a href="{PHONE_HREF}" class="btn btn-outline" style="border-color:rgba(255,255,255,.4);color:#fff">Call {PHONE}</a>
</div>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">
<div class="split-2 split-center">
<div>
<span class="eyebrow">The Context</span>
<h2>What Makes {name} Different</h2>
<p>{ind['intro']}</p>
<p>We work with owner-led {name.lower()} businesses that have proven demand and are held back by how the work gets done rather than whether anyone wants it.</p>
<a href="/case-studies/" class="btn btn-outline" style="margin-top:8px">See Client Results</a>
</div>
<div>
<img src="{esc_attr(ind['image'])}" alt="{esc_attr(name)} business operations - Elixir Consulting Group" width="800" height="600" loading="lazy" decoding="async" style="border-radius:14px;width:100%;height:340px;object-fit:cover">
</div>
</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:44px">
<span class="eyebrow">Common Constraints</span>
<h2>What We See in {name}</h2>
<p style="max-width:680px;margin:0 auto">These are the patterns that come up most often. If two or more sound familiar, there is usually a systems problem underneath them.</p>
</div>
<div class="grid grid-2">
{challenges}
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="split-1-2">
<div>
<span class="eyebrow">Our Approach</span>
<h2>How We Work in {name}</h2>
<p>Implementation, not recommendations. We build the systems with your team and stay involved long enough to know they stuck.</p>
<div class="contact-info-card" style="margin-top:20px">
<h3 style="margin-bottom:10px">Expected Outcomes</h3>
<ul style="margin:0 0 0 1.1rem;padding-left:.5rem">
{outcomes}
</ul>
</div>
</div>
<div>
{approach}
</div>
</div>
</div>
</section>

{case_html}

<section class="section{'' if case_html else ' section-gray'}">
<div class="container">
<div class="text-center" style="margin-bottom:44px">
<span class="eyebrow">Services</span>
<h2>Where {name} Engagements Usually Start</h2>
</div>
<div class="grid grid-3">
<div class="card"><h3><a href="/services/operations/">Operations Consulting</a></h3><p>Process mapping, SOPs, role clarity, and the weekly cadence that keeps delivery consistent.</p><a href="/services/operations/">Learn more &rarr;</a></div>
<div class="card"><h3><a href="/services/sales-strategy/">Sales Strategy</a></h3><p>Pipeline structure, follow-up standards, and CRM configuration your team will actually run.</p><a href="/services/sales-strategy/">Learn more &rarr;</a></div>
<div class="card"><h3><a href="/services/leadership/">Leadership Consulting</a></h3><p>Meeting rhythm, scorecards, and accountability that produce decisions instead of updates.</p><a href="/services/leadership/">Learn more &rarr;</a></div>
</div>
</div>
</section>

{render_faq_section(faqs, f"{name} Consulting FAQs", gray=bool(case_html))}

<section class="related-posts">
<div class="container">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Further Reading</span>
<h2>Articles Relevant to {name}</h2>
</div>
<div class="post-list">
{related_cards}
</div>
</div>
</section>

<section class="section">
<div class="container text-center">
<span class="eyebrow">More Sectors</span>
<h2 style="margin-bottom:36px">Other Industries We Serve</h2>
<div class="grid grid-3">
{other_cards}
</div>
<a href="/industries/" class="btn btn-outline" style="margin-top:32px">View All Industries</a>
</div>
</section>

{make_cta()}
"""
    return make_page(
        f"{name} Consulting | Elixir Consulting Group",
        clip(f"Operations, sales, and leadership consulting for {name.lower()} businesses. {ind['short']}", 158),
        f"/industries/{ind['slug']}/",
        body,
        schema,
        faq=faqs,
        crumb_override=name,
    )


# ─── Case study detail pages ───────────────────────────────────────────

def case_study_faqs(cs):
    return [
        ("Is this a real engagement?",
         "Yes. Details are generalized and the client is not named to protect confidentiality, but the situation, the work, and the outcomes reflect an actual engagement."),
        (f"How long did the {cs['industry'].lower()} engagement take?",
         f"This was a {cs['duration'].replace(' engagement', '')} engagement. Most of our work runs between 90 days and six months depending on scope, and many clients continue with monthly advisory support afterward."),
        ("Would this approach work for a business our size?",
         "The specific interventions scale, but the sequence does not change: map what actually happens, find the few constraints that matter, install cadence and ownership, then measure weekly. We work with businesses roughly between $1M and $30M in revenue."),
        ("How quickly do results usually appear?",
         "Cadence and role clarity changes tend to show up inside the first 30 to 60 days. Financial effects usually follow over a quarter or two as the new systems compound."),
        ("How do we find out whether we have a similar problem?",
         f"Book a consult. We will talk through how work moves through your business today and tell you honestly whether there is a fit. Call {PHONE} or use the contact page."),
    ]


def gen_case_study_page(cs, all_posts):
    faqs = case_study_faqs(cs)

    metrics = "".join(
        f'<div class="stat-card card"><span class="stat-num">{v}</span>'
        f'<span class="stat-label">{l}</span></div>\n' for v, l in cs["metrics"])
    results = "".join(f"<li>{r}</li>\n" for r in cs["results"])
    services = " ".join(
        f'<a href="{href}" class="services-link">{name}</a>' for name, href in cs["services"])

    others = [c for c in CASE_STUDIES if c["slug"] != cs["slug"]]
    other_cards = "".join(
        f'<div class="card"><p class="pc-cat">{o["industry"]}</p>'
        f'<h3><a href="/case-studies/{o["slug"]}/">{o["title"]}</a></h3>'
        f'<p>{clip(o["challenge"], 120)}</p>'
        f'<a href="/case-studies/{o["slug"]}/">Read the case study &rarr;</a></div>\n' for o in others)

    related = related_by_keywords(all_posts, [cs["industry"]] + [s for s, _ in cs["services"]], 3)
    related_cards = "".join(post_card(p) for p in related)

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": clip(cs["title"], 110),
        "description": clip(cs["challenge"], 300),
        "articleSection": "Case Study",
        "datePublished": "2026-01-15",
        "dateModified": DATE_NOW,
        "inLanguage": "en-US",
        "image": [OG_IMAGE],
        "about": {"@type": "Thing", "name": cs["industry"]},
        "author": {"@id": DOMAIN + "/#founder"},
        "publisher": {"@id": DOMAIN + "/#organization"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": DOMAIN + f"/case-studies/{cs['slug']}/"},
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / <a href="/case-studies/">Case Studies</a> / {esc_text(clip(cs['title'], 40))}</p>
<p style="margin-bottom:14px"><span class="post-tag">{cs['industry']} Case Study</span></p>
<h1 style="font-size:clamp(1.65rem,4.2vw,2.6rem)">{cs['title']}</h1>
<p>{cs['profile']} &middot; {cs['duration']}</p>
</div>
</section>

<section class="section-sm" style="background:{COLORS['off_white']};border-bottom:1px solid {COLORS['border']}">
<div class="container">
<div class="grid grid-3">
{metrics}
</div>
</div>
</section>

<section class="section">
<div class="container">
<article class="article-body">
<h2>The Situation</h2>
{cs['situation']}

<blockquote>"{cs['quote']}" &mdash; {cs['quote_role']}</blockquote>

<h2>What We Did</h2>
{cs['approach']}

<h2>The Outcome</h2>
{cs['outcome']}
</article>

<div style="max-width:760px;margin:40px auto 0">
<div class="contact-info-card">
<span class="eyebrow">Results at a Glance</span>
<ul style="margin:12px 0 0 1.1rem">
{results}
</ul>
</div>
<div style="margin-top:24px">
<p style="font-weight:600;color:{COLORS['navy']};margin-bottom:10px">Services involved in this engagement</p>
{services}
</div>
</div>
</div>
</section>

<section class="cta-banner">
<div class="container">
<span class="eyebrow">Recognize Any of This?</span>
<h2>Find Out Where Your Business Is Actually Stuck</h2>
<p>A consult is a conversation about how work moves through your business today, and an honest read on whether we are the right partner for it.</p>
<a href="/contact/" class="btn btn-gold">Book a Consult</a>
</div>
</section>

{render_faq_section(faqs, "Questions About This Engagement", gray=False)}

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:36px">
<span class="eyebrow">More Results</span>
<h2>Other Case Studies</h2>
</div>
<div class="grid grid-3">
{other_cards}
</div>
</div>
</section>

<section class="related-posts" style="background:#fff">
<div class="container">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Further Reading</span>
<h2>Related Articles</h2>
</div>
<div class="post-list">
{related_cards}
</div>
</div>
</section>

{make_cta()}
"""
    return make_page(
        seo_title_for(cs["title"]),
        clip(f"{cs['industry']} case study: {cs['challenge']}", 158),
        f"/case-studies/{cs['slug']}/",
        body,
        schema,
        og_title=cs["title"],
        faq=faqs,
        crumb_override=clip(cs["title"], 60),
    )


def related_by_keywords(all_posts, keywords, count=3):
    """Pick posts whose title or category best matches a set of keywords.

    Used to wire industry and case study pages into the blog archive so no page
    is a dead end and topical authority accumulates around each theme.
    """
    words = set()
    for k in keywords:
        for w in re.findall(r"[a-z]{4,}", k.lower()):
            words.add(w)
    scored = []
    for i, p in enumerate(all_posts):
        hay = (p["title"] + " " + p["category"] + " " + p["excerpt"]).lower()
        score = sum(1 for w in words if w in hay)
        scored.append((-score, i, p))
    scored.sort(key=lambda x: (x[0], x[1]))
    return [p for _, _, p in scored[:count]]


def gen_industries():
    cards = ""
    for ind in INDUSTRIES:
        cards += f"""<div class="industry-card card">
<div class="ind-icon">{ind['icon']}</div>
<h3><a href="/industries/{ind['slug']}/">{ind['name']}</a></h3>
<p>{ind['short']}</p>
<a href="/industries/{ind['slug']}/">{ind['name']} consulting &rarr;</a>
</div>\n"""

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Industries Served",
        "url": DOMAIN + "/industries/",
        "description": "Sectors Elixir Consulting Group works in, and the operational patterns specific to each.",
        "hasPart": [
            {"@type": "WebPage", "name": f"Business Consulting for {i['name']}",
             "url": DOMAIN + f"/industries/{i['slug']}/"} for i in INDUSTRIES
        ],
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Industries</p>
<h1>Industries We Serve</h1>
<p>The operational problems we solve are structural, so the frameworks transfer. The context does not, which is why each sector gets its own page.</p>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:44px">
<span class="eyebrow">Eight Sectors</span>
<h2>Pick Your Industry</h2>
<p style="max-width:660px;margin:0 auto">Each page covers the constraints we see most often in that sector, how we approach them, and the outcomes to expect.</p>
</div>
<div class="grid grid-2">
{cards}
</div>
</div>
</section>

<section class="section section-navy">
<div class="container text-center">
<span class="eyebrow">Not Listed?</span>
<h2>Most Operational Challenges Are Universal</h2>
<p style="max-width:640px;margin:0 auto 24px">Whether you are in manufacturing, healthcare, or professional services, the core problems repeat: inconsistent execution, owner dependency, and no structure underneath the growth. If your sector is not above, that does not mean we cannot help.</p>
<a href="/contact/" class="btn btn-gold">Book a Consult</a>
</div>
</section>
"""
    body += render_faq_section(INDUSTRIES_FAQS, "Industry FAQs")
    body += make_cta()
    return make_page(
        "Industries We Serve | Elixir Consulting Group",
        "Operations, sales, and leadership consulting across professional services, construction, healthcare, manufacturing, technology, real estate, retail, and financial services.",
        "/industries/",
        body,
        schema,
        faq=INDUSTRIES_FAQS,
    )


def gen_case_studies():
    cards = ""
    for cs in CASE_STUDIES:
        results_html = "".join([f"<li>{r}</li>" for r in cs['results'][:3]])
        metrics_html = " ".join(
            f'<span style="display:inline-block;margin-right:18px"><strong style="color:{COLORS["navy"]};font-size:1.25rem">{v}</strong> '
            f'<span style="font-size:.85rem;color:{COLORS["mid_gray"]}">{l}</span></span>'
            for v, l in cs['metrics'][:2])
        cards += f"""<div class="card" style="padding:0;overflow:hidden">
<div style="background:{COLORS['navy']};padding:24px 32px;color:{COLORS['white']}">
<span style="font-size:.8rem;text-transform:uppercase;letter-spacing:1px;color:{COLORS['gold']}">{cs['industry']}</span>
<h3 style="color:{COLORS['white']};margin-top:8px"><a href="/case-studies/{cs['slug']}/" style="color:{COLORS['white']}">{cs['title']}</a></h3>
<p style="color:rgba(255,255,255,.7);font-size:.85rem;margin-bottom:0">{cs['profile']}</p>
</div>
<div style="padding:32px">
<div style="margin-bottom:18px">{metrics_html}</div>
<h4 style="color:{COLORS['navy']};margin-bottom:8px">Challenge</h4>
<p>{cs['challenge']}</p>
<h4 style="color:{COLORS['navy']};margin-bottom:8px">Results</h4>
<ul style="list-style:none;padding:0">{results_html}</ul>
<a href="/case-studies/{cs['slug']}/" class="btn btn-outline" style="margin-top:16px">Read the Full Case Study</a>
</div>
</div>\n"""

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Client Case Studies",
        "url": DOMAIN + "/case-studies/",
        "description": "Documented engagements from Elixir Consulting Group across manufacturing, professional services, construction, and healthcare.",
        "hasPart": [
            {"@type": "Article", "headline": c["title"],
             "url": DOMAIN + f"/case-studies/{c['slug']}/"} for c in CASE_STUDIES
        ],
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Case Studies</p>
<h1>Case Studies</h1>
<p>Four engagements, documented end to end: what was actually broken, what we built, and what changed. Details are generalized to protect client confidentiality.</p>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">
<div class="grid grid-2">
{cards}
</div>
</div>
</section>

<section class="section section-navy">
<div class="container">
<div class="text-center" style="margin-bottom:40px">
<span class="eyebrow">The Common Thread</span>
<h2>The Same Sequence Every Time</h2>
<p style="max-width:660px;margin:0 auto">Different industries, different symptoms, one method.</p>
</div>
<div class="grid grid-4">
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">01</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Map what actually happens</span></div>
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">02</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Find the few real constraints</span></div>
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">03</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Install cadence and ownership</span></div>
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">04</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Measure weekly until it sticks</span></div>
</div>
<div class="text-center" style="margin-top:36px">
<a href="/process/" class="btn btn-gold">See How Engagements Work</a>
</div>
</div>
</section>
"""
    body += render_faq_section(CASE_STUDY_FAQS, "Case Study FAQs")
    body += make_cta()
    return make_page(
        "Case Studies | Elixir Consulting Group",
        "Real case studies from Elixir Consulting Group engagements across manufacturing, professional services, construction, and healthcare. See the systems installed and the results they produced.",
        "/case-studies/",
        body,
        schema,
        faq=CASE_STUDY_FAQS,
    )


# ─── Blog: ingestion, taxonomy, and rendering ──────────────────────────
#
# The blog is the largest surface on this site (330+ posts). Posts arrive from
# two places: the BLOG_POSTS list above, and standalone HTML files that earlier
# tooling wrote straight into blog/<slug>/index.html. Rather than let those two
# drift apart, every run re-reads the HTML on disk, pulls out just the article
# content, and re-renders each post through the same template as everything
# else. The extraction targets <article>, which this generator also emits, so
# the pass is idempotent -- running it twice produces identical files.

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

CATEGORY_RULES = [
    ("AI & Technology", ["ai-", "-ai", "artificial", "agentic", "automat", "chatgpt", "llm",
                         "digital-transformation", "technology", "tech-", "software", "data-",
                         "machine-learning", "robot", "cyber", "saas", "crm", "cloud"]),
    ("Sales & Revenue", ["sales", "revenue", "pipeline", "lead", "prospect", "closing",
                         "pricing", "customer-acquisition", "b2b", "cold-call", "negotiat"]),
    ("Operations", ["operation", "process", "workflow", "sop", "efficien", "productiv",
                    "systems", "supply", "onboarding", "dashboard", "quality", "logistics",
                    "inventory", "project-management", "remote-work"]),
    ("Leadership", ["leader", "team", "culture", "hiring", "hire", "manager", "management",
                    "coaching", "delegat", "accountab", "talent", "employee", "succession"]),
    ("Strategy & Growth", ["strateg", "growth", "scal", "plan", "market", "brand",
                           "competit", "expansion", "positioning", "innovation", "transform"]),
    ("Finance & Exit", ["exit", "sell", "acquisition", "valuation", "m-a", "merger", "profit",
                        "cash-flow", "financ", "cost", "roi", "invest", "capital", "budget"]),
    ("Pittsburgh & Local", ["pittsburgh", "cranberry", "wexford", "pennsylvania", "regional",
                            "local", "western-pa"]),
]

# Images already served elsewhere on the site, grouped so a post without its own
# artwork still gets something topical instead of an empty grey box.
CATEGORY_IMAGES = {
    "AI & Technology": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80",
    "Sales & Revenue": "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&q=80",
    "Operations": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80",
    "Leadership": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80",
    "Strategy & Growth": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80",
    "Finance & Exit": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80",
    "Pittsburgh & Local": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80",
    "Insights": "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?w=800&q=80",
}

CATEGORY_ORDER = [c for c, _ in CATEGORY_RULES] + ["Insights"]


def classify_post(slug, title):
    """Assign a post to a single category using slug and title keywords."""
    hay = (slug + " " + title).lower()
    best, best_score = "Insights", 0
    for cat, keys in CATEGORY_RULES:
        score = sum(3 if k in slug.lower() else 1 for k in keys if k in hay)
        if score > best_score:
            best, best_score = cat, score
    return best


def strip_tags(html):
    return re.sub(r"<[^>]+>", " ", html)


def read_minutes(html):
    words = len(strip_tags(html).split())
    return max(1, round(words / 225))


def pretty_date(iso):
    try:
        y, m, d = iso.split("-")
        return f"{MONTHS[int(m) - 1]} {int(d)}, {y}"
    except Exception:
        return iso


def clip(text, limit):
    text = re.sub(r"\s+", " ", strip_tags(text)).strip()
    if len(text) <= limit:
        return text
    # Reserve room for the ellipsis so the result never exceeds `limit`.
    # Without that, re-reading a clipped value on the next build clips it again.
    cut = text[:max(1, limit - 3)].rsplit(" ", 1)[0].rstrip(" ,.;:-")
    return cut + "..."


def _find_balanced(html, start, tag="div"):
    """Return the inner HTML of the element beginning at `start`, matching nesting."""
    open_end = html.find(">", start)
    if open_end == -1:
        return ""
    depth, i = 1, open_end + 1
    pat = re.compile(r"<(/?)%s\b" % tag, re.I)
    while depth > 0:
        m = pat.search(html, i)
        if not m:
            return html[open_end + 1:]
        depth += -1 if m.group(1) else 1
        i = m.end()
    return html[open_end + 1:html.rfind("<", open_end, i)]


def clean_article_html(html):
    """Normalize legacy markup so every post renders through the same stylesheet."""
    # Unwrap Elementor/WordPress page-builder scaffolding left over from the
    # original site migration -- the wrappers carry no styles here, only noise.
    for _ in range(12):
        new = re.sub(r"<div[^>]*class=\"[^\"]*elementor[^\"]*\"[^>]*>", "", html)
        if new == html:
            break
        html = new
    html = re.sub(r"\s*class=\"(wp-block-[^\"]*)\"", "", html)
    html = re.sub(r"<div class=\"article-meta\">.*?</div>", "", html, flags=re.S)
    html = re.sub(r'<script[^>]*>.*?</script>', "", html, flags=re.S)
    # The page-level <h1> is rendered by the template; anything the body carries
    # would be a second one, so demote it to keep the outline valid.
    html = re.sub(r"<(/?)h1\b", r"<\1h2", html)
    html = re.sub(r"<section class=\"related-posts\">.*?</section>", "", html, flags=re.S)
    html = _rebalance_divs(html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def _rebalance_divs(html):
    """Drop </div> tags that close nothing and close any div left hanging.

    Unwrapping page-builder scaffolding and lifting the lead image out of the
    body both leave orphaned closers behind. Deleting the *last* closer instead
    of the unmatched one would strip a real wrapper (a stat callout, say) and
    let it swallow the rest of the article, so match position by position.
    """
    kept, depth, pos = [], 0, 0
    for m in re.finditer(r"<div\b|</div>", html):
        if m.group(0).startswith("</"):
            if depth == 0:
                kept.append(html[pos:m.start()])
                pos = m.end()
                continue
            depth -= 1
        else:
            depth += 1
    kept.append(html[pos:])
    html = "".join(kept)
    return html + "</div>" * max(0, depth)


def _meta(html, prop, attr="property"):
    """Read a meta tag's content, decoded back to plain text.

    Decoding matters: these values get re-escaped on the way out, so returning
    them still-escaped would compound `&` into `&amp;amp;` on every rebuild.
    """
    m = re.search(r'<meta %s="%s" content="(.*?)"\s*/?>' % (attr, re.escape(prop)), html, re.S)
    return htmllib.unescape(m.group(1).strip()) if m else ""


def parse_existing_post(slug, html):
    """Pull title, description, date, artwork, and body out of a rendered post."""
    title = _meta(html, "og:title")
    if not title:
        t = re.search(r"<title>(.*?)</title>", html, re.S)
        title = htmllib.unescape(t.group(1).strip()) if t else slug.replace("-", " ").title()
    title = re.sub(r"\s*\|\s*Elixir Consulting Group\s*$", "", title).strip()

    desc = _meta(html, "description", attr="name") or _meta(html, "og:description")
    image = _meta(html, "og:image")

    # Allow the whitespace json.dumps inserts after the colon, otherwise a
    # rebuild loses the original publish date and stamps today's instead.
    d = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})', html)
    if not d:
        d = re.search(r'article:published_time" content="(\d{4}-\d{2}-\d{2})', html)
    date = d.group(1) if d else DATE_NOW
    dm = re.search(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})', html)
    if not dm:
        dm = re.search(r'article:modified_time" content="(\d{4}-\d{2}-\d{2})', html)
    modified = dm.group(1) if dm else date

    art = re.search(r"<article[^>]*>", html)
    if art:
        body = _find_balanced(html, art.start(), "article")
    else:
        wrap = re.search(r'<div class="article-wrap">', html)
        if wrap:
            body = _find_balanced(html, wrap.start(), "div")
        else:
            main = re.search(r"<main[^>]*>", html)
            body = _find_balanced(html, main.start(), "main") if main else ""

    # The lead image is re-rendered above the article, so take it out of the body.
    img_alt = ""
    lead = re.search(r'<(?:div class="hero-img">\s*)?<img[^>]*>', body[:1200])
    if lead:
        src = re.search(r'src="([^"]+)"', lead.group(0))
        alt = re.search(r'alt="([^"]*)"', lead.group(0))
        if src and ("unsplash" in src.group(1) or "images/" in src.group(1)):
            image = image or htmllib.unescape(src.group(1))
            img_alt = htmllib.unescape(alt.group(1)) if alt else ""
            body = body[:lead.start()] + body[lead.end():]
            body = re.sub(r'^\s*</div>', '', body.lstrip(), count=1)

    # Only FAQs written into the article itself count as authored. The <head>
    # block is whatever this generator emitted last run; re-capturing that would
    # freeze generated questions in place forever.
    custom_faqs = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
        try:
            obj = json.loads(block)
        except Exception:
            continue
        if obj.get("@type") == "FAQPage":
            for q in obj.get("mainEntity", []):
                name = q.get("name", "").strip()
                ans = (q.get("acceptedAnswer") or {}).get("text", "").strip()
                if name and ans:
                    custom_faqs.append([name, ans])

    return {
        "slug": slug,
        "title": title,
        "description": desc,
        "custom_faqs": custom_faqs,
        "date": date,
        "modified": modified,
        "image": image,
        "image_alt": img_alt,
        "content": clean_article_html(body),
    }


# Links that older article bodies point at, which never existed as blog posts.
BODY_LINK_ALIASES = {
    "/blog/dr-connor-robertson/": "/about/",
    "/blog/dr-connor-robertson": "/about/",
    "/blog/contact": "/contact/",
    "/blog/contact/": "/contact/",
    "/blog/about/": "/about/",
    "/blog/services/": "/services/",
}


def repair_body_links(posts):
    """Point in-article links at pages that actually exist.

    Article bodies inherited cross-links to posts that were planned but never
    published. Rather than ship dead ends, alias the known cases and send the
    rest to the closest published slug, falling back to the blog index.
    """
    import difflib

    slugs = set(posts)
    fixed = 0
    for p in posts.values():
        body = p["content"]

        def sub(m):
            nonlocal fixed
            href = m.group(1)
            if href in BODY_LINK_ALIASES:
                fixed += 1
                return 'href="%s"' % BODY_LINK_ALIASES[href]
            slug = href.strip("/").split("/")[-1]
            if slug in slugs or slug == "blog":
                return m.group(0)
            near = difflib.get_close_matches(slug, slugs, n=1, cutoff=0.72)
            fixed += 1
            return 'href="/blog/%s/"' % near[0] if near else 'href="/blog/"'

        p["content"] = re.sub(r'href="(/blog/[^"]*)"', sub, body)
    if fixed:
        print(f"  Repaired {fixed} stale in-article links")


def load_all_posts():
    """Merge in-script posts with every post already written to blog/<slug>/."""
    posts = {}
    for p in BLOG_POSTS:
        posts[p["slug"]] = {
            "slug": p["slug"],
            "title": p["title"],
            "description": p["excerpt"],
            "date": p["date"],
            "modified": p["date"],
            "image": "",
            "image_alt": "",
            "content": clean_article_html(p["content"]),
        }

    blog_dir = os.path.join(SITE_DIR, "blog")
    if os.path.isdir(blog_dir):
        for slug in sorted(os.listdir(blog_dir)):
            fp = os.path.join(blog_dir, slug, "index.html")
            if not os.path.isfile(fp):
                continue
            try:
                with open(fp, encoding="utf-8") as f:
                    html = f.read()
                parsed = parse_existing_post(slug, html)
            except Exception as exc:  # a malformed file must not sink the build
                print(f"  ! skipped blog/{slug}: {exc}")
                continue
            if len(strip_tags(parsed["content"]).split()) < 60:
                # Nothing usable on disk; keep the in-script version if we have one.
                if slug in posts:
                    continue
                print(f"  ! blog/{slug} has no extractable body, skipping")
                continue
            existing = posts.get(slug)
            if existing:
                # On-disk copy wins for body, but keep in-script metadata as backup.
                parsed["description"] = parsed["description"] or existing["description"]
            posts[slug] = parsed

    repair_body_links(posts)

    # Hand-written FAQs only exist in the source markup on the first pass, so
    # persist them to a sidecar rather than losing them on the next rebuild.
    store = load_custom_faqs()
    for slug, p in posts.items():
        found = p.pop("custom_faqs", None)
        if found:
            store[slug] = found
        if slug in store:
            p["custom_faqs"] = store[slug]
    save_custom_faqs(store)

    out = []
    for p in posts.values():
        p["title"] = p["title"].strip()
        p["category"] = classify_post(p["slug"], p["title"])
        p["description"] = (p["description"] or clip(p["content"], 160)).strip()
        p["image"] = p["image"] or CATEGORY_IMAGES.get(p["category"], CATEGORY_IMAGES["Insights"])
        p["image_alt"] = p["image_alt"] or f"{p['title']} - Elixir Consulting Group"
        p["og_image"] = p["image"].replace("w=800", "w=1200")
        p["read_min"] = read_minutes(p["content"])
        p["excerpt"] = clip(p["description"], 155)
        p["url"] = f"/blog/{p['slug']}/"
        out.append(p)

    out.sort(key=lambda x: (x["date"], x["slug"]), reverse=True)
    dedupe_descriptions(out)
    canonicalize_duplicate_titles(out)
    return out


def first_paragraph(html):
    m = re.search(r"<p[^>]*>(.*?)</p>", html, re.S)
    return strip_tags(m.group(1)) if m else strip_tags(html)


def dedupe_descriptions(posts):
    """Give every post its own meta description.

    Several imported posts shipped with the same boilerplate description, which
    reads to a search engine as duplicate content. Where that happens, derive
    one from the post's own opening paragraph.
    """
    seen, changed = {}, 0
    for p in posts:
        key = p["description"].strip().lower()
        if key not in seen:
            seen[key] = p["slug"]
            continue
        candidate = clip(first_paragraph(p["content"]), 158)
        if candidate.strip().lower() in seen or len(candidate) < 60:
            candidate = clip(f"{p['title']}. {first_paragraph(p['content'])}", 158)
        p["description"] = candidate
        p["excerpt"] = clip(candidate, 155)
        seen[candidate.strip().lower()] = p["slug"]
        changed += 1
    if changed:
        print(f"  Rewrote {changed} duplicate meta descriptions")


def canonicalize_duplicate_titles(posts):
    """Point re-published duplicates at the original via rel=canonical."""
    first, dupes = {}, 0
    for p in posts:
        key = re.sub(r"\W+", "", p["title"].lower())
        if key in first:
            p["canonical"] = DOMAIN + first[key]["url"]
            p["duplicate_of"] = first[key]["slug"]
            dupes += 1
        else:
            first[key] = p
    if dupes:
        print(f"  Canonicalized {dupes} duplicate-title posts")


CUSTOM_FAQ_FILE = "data/post-faqs.json"


def load_custom_faqs():
    path = os.path.join(SITE_DIR, CUSTOM_FAQ_FILE)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_custom_faqs(store):
    path = os.path.join(SITE_DIR, CUSTOM_FAQ_FILE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2, sort_keys=True)
        f.write("\n")


def post_faqs(post):
    """Three real, on-page answered questions per post, weighted toward its topic.

    A handful of posts arrived with their own hand-written FAQ schema. Those are
    better than anything picked by keyword, so they win when present.
    """
    custom = post.get("custom_faqs")
    if custom:
        return [tuple(x) for x in custom[:6]]
    keys = dict(CATEGORY_RULES).get(post["category"], [])
    scored = []
    for i, (q, a) in enumerate(FAQ_ITEMS):
        hay = (q + " " + a).lower()
        scored.append((sum(1 for k in keys if k.strip("-") in hay), i, q, a))
    scored.sort(key=lambda x: (-x[0], x[1]))
    picked = [(q, a) for _, _, q, a in scored[:2]]
    # Rotate the third so the set varies across the archive instead of repeating.
    rest = [(q, a) for _, _, q, a in scored[2:]]
    if rest:
        picked.append(rest[sum(ord(c) for c in post["slug"]) % len(rest)])
    return picked


def related_posts(post, all_posts, count=3):
    """Same-category posts first, then recent ones, so every post links onward."""
    same = [p for p in all_posts if p["category"] == post["category"] and p["slug"] != post["slug"]]
    seed = sum(ord(c) for c in post["slug"])
    picked = []
    if same:
        start = seed % len(same)
        picked = [same[(start + i) % len(same)] for i in range(min(count, len(same)))]
    if len(picked) < count:
        chosen = {p["slug"] for p in picked} | {post["slug"]}
        for p in all_posts:
            if p["slug"] not in chosen:
                picked.append(p)
                chosen.add(p["slug"])
            if len(picked) == count:
                break
    return picked


def post_card(p, lazy=True):
    loading = 'loading="lazy" decoding="async"' if lazy else 'loading="eager" fetchpriority="high"'
    return f"""<article class="post-card" data-cat="{esc_attr(p['category'])}" data-search="{esc_attr((p['title'] + ' ' + p['excerpt'] + ' ' + p['category']).lower())}">
<a href="{p['url']}" tabindex="-1" aria-hidden="true"><img class="thumb" src="{esc_attr(p['image'])}" alt="{esc_attr(p['image_alt'])}" width="800" height="450" {loading}></a>
<div class="pc-body">
<p class="pc-cat">{p['category']}</p>
<h3><a href="{p['url']}">{esc_text(p['title'])}</a></h3>
<p>{esc_text(p['excerpt'])}</p>
<p class="pc-meta"><time datetime="{p['date']}">{pretty_date(p['date'])}</time> <span aria-hidden="true">&middot;</span> {p['read_min']} min read</p>
</div>
</article>\n"""


def gen_blog_index(all_posts):
    featured = all_posts[0]
    rest = all_posts[1:]

    cards = "".join(post_card(p, lazy=(i > 5)) for i, p in enumerate(rest))
    page_size = 24

    counts = {}
    for p in all_posts:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    category_links = "".join(
        f'<a href="/blog/category/{category_slug(c)}/" class="services-link">{c} ({counts[c]})</a>'
        for c in CATEGORY_ORDER if counts.get(c))
    chips = '<button type="button" class="filter-chip active" data-filter="all">All ({})</button>'.format(len(all_posts))
    for cat in CATEGORY_ORDER:
        if counts.get(cat):
            chips += f'<button type="button" class="filter-chip" data-filter="{esc_attr(cat)}">{cat} ({counts[cat]})</button>'

    faqs = [
        ("How often does Elixir Consulting Group publish new articles?",
         "We publish new articles regularly on business strategy, operations, AI adoption, sales systems, and leadership. The archive currently holds more than {} articles covering the operational problems we see most often in owner-led businesses.".format(len(all_posts))),
        ("Who writes the articles on this blog?",
         "Articles are written by Dr. Connor Robertson, founder and lead consultant at Elixir Consulting Group, drawing on hands-on implementation work with business owners across industries."),
        ("Can I apply these ideas without hiring a consultant?",
         "Yes. Every article is written to be actionable on its own. If you want help installing the systems faster or want an outside read on where your business is actually stuck, a consult is the next step."),
        ("What topics does the blog cover?",
         "Coverage spans business strategy, operations and process design, AI and automation, sales and revenue systems, leadership and accountability, exit planning, and the Pittsburgh regional economy."),
    ]

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Elixir Consulting Group Blog",
        "url": DOMAIN + "/blog/",
        "description": "Insights on business strategy, operations, AI consulting, sales systems, and leadership from Elixir Consulting Group.",
        "publisher": {"@type": "Organization", "name": "Elixir Consulting Group", "url": DOMAIN},
        "blogPost": [
            {"@type": "BlogPosting", "headline": p["title"], "url": DOMAIN + p["url"],
             "datePublished": p["date"],
             "author": {"@type": "Person", "name": "Dr. Connor Robertson"}}
            for p in all_posts[:25]
        ],
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Blog</p>
<h1>Insights for Business Owners</h1>
<p>{len(all_posts)} articles on strategy, operations, AI adoption, sales systems, and leadership &mdash; written from the implementation side of the table.</p>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">

<a href="{featured['url']}" style="display:block" aria-label="Featured article: {esc_attr(featured['title'])}">
<div class="featured-post">
<img src="{esc_attr(featured['image'])}" alt="{esc_attr(featured['image_alt'])}" width="800" height="450" fetchpriority="high" decoding="async">
<div class="fp-body">
<p class="pc-cat" style="margin-bottom:10px">Latest &middot; {featured['category']}</p>
<h2>{esc_text(featured['title'])}</h2>
<p>{esc_text(featured['excerpt'])}</p>
<p class="pc-meta" style="margin-bottom:18px"><time datetime="{featured['date']}">{pretty_date(featured['date'])}</time> <span aria-hidden="true">&middot;</span> {featured['read_min']} min read</p>
<span class="btn btn-primary">Read the Article</span>
</div>
</div>
</a>

<div class="text-center" style="margin-bottom:28px">
<span class="eyebrow">Browse by Topic</span>
<div style="margin-top:12px">{category_links}</div>
<p style="margin-top:14px;font-size:.95rem">All articles are written by <a href="/blog/author/dr-connor-robertson/">Dr. Connor Robertson</a>. <a href="/feed.xml">Subscribe via RSS</a>.</p>
</div>

<div class="blog-toolbar">
<label class="sr-only" for="blog-search" style="position:absolute;left:-9999px">Search articles</label>
<input type="search" id="blog-search" class="blog-search" placeholder="Search {len(all_posts)} articles..." autocomplete="off">
<div class="blog-filters" role="group" aria-label="Filter articles by category">
{chips}
</div>
</div>

<div class="post-list" id="post-list">
{cards}
</div>
<p class="no-results" id="no-results">No articles matched that search. Try a different term or clear the filters.</p>
<div class="load-more-wrap"><button type="button" class="btn btn-outline" id="load-more">Load More Articles</button></div>

</div>
</section>

{render_faq_section(faqs, "Blog FAQs")}

{make_cta()}

<script>
/* Every card ships in the HTML so the archive stays crawlable and searchable
   offline, but painting 300+ of them at once is wasteful. Show a page at a
   time; searching or filtering widens the window to cover all matches. */
(function(){{
var PAGE={page_size};
var search=document.getElementById('blog-search');
var chips=document.querySelectorAll('.filter-chip');
var cards=Array.prototype.slice.call(document.querySelectorAll('#post-list .post-card'));
var empty=document.getElementById('no-results');
var more=document.getElementById('load-more');
var cat='all',limit=PAGE;
function apply(){{
var q=(search&&search.value||'').trim().toLowerCase();
var matched=0,shown=0;
cards.forEach(function(c){{
var okCat=(cat==='all'||c.getAttribute('data-cat')===cat);
var okQ=(!q||c.getAttribute('data-search').indexOf(q)>-1);
if(okCat&&okQ){{
matched++;
var show=shown<limit;
c.style.display=show?'':'none';
if(show)shown++;
}}else{{c.style.display='none'}}
}});
empty.style.display=matched?'none':'block';
if(more)more.parentNode.style.display=(matched>shown)?'':'none';
}}
function reset(){{limit=PAGE;apply()}}
if(search)search.addEventListener('input',reset);
chips.forEach(function(b){{b.addEventListener('click',function(){{
chips.forEach(function(x){{x.classList.remove('active')}});
b.classList.add('active');
cat=b.getAttribute('data-filter');
reset();
}})}});
if(more)more.addEventListener('click',function(){{limit+=PAGE;apply()}});
apply();
}})();
</script>
"""
    return make_page(
        "Business Consulting Blog | Elixir Consulting Group",
        "Practical articles on business strategy, operations, AI adoption, sales systems, and leadership for owner-led companies. Written by Dr. Connor Robertson of Elixir Consulting Group.",
        "/blog/",
        body,
        schema,
        faq=faqs,
    )


def seo_title_for(title, suffix=" | Elixir Consulting Group"):
    """Build a <title> that survives SERP truncation (~60 characters).

    Long headlines are cut at their natural break (a colon or dash) rather than
    mid-phrase; the full headline still ships as the H1 and og:title.
    """
    if len(title) + len(suffix) <= 62:
        return title + suffix
    if len(title) <= 62:
        return title
    return title[:62].rsplit(" ", 1)[0].rstrip(" ,.;:-")


def gen_blog_post(post, all_posts):
    rel = related_posts(post, all_posts)
    rel_cards = "".join(post_card(p) for p in rel)
    faqs = post_faqs(post)

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": clip(post["title"], 110),
        "description": post["description"],
        "datePublished": post["date"],
        "dateModified": post["modified"],
        "articleSection": post["category"],
        "wordCount": len(strip_tags(post["content"]).split()),
        "timeRequired": f"PT{post['read_min']}M",
        "inLanguage": "en-US",
        "image": [post["og_image"]],
        "author": {
            "@type": "Person",
            "name": "Dr. Connor Robertson",
            "url": "https://drconnorrobertson.com",
            "jobTitle": "Founder & Lead Consultant",
            "worksFor": {"@type": "Organization", "name": "Elixir Consulting Group"},
        },
        "publisher": {
            "@type": "Organization",
            "name": "Elixir Consulting Group",
            "url": DOMAIN,
            "logo": {"@type": "ImageObject", "url": OG_IMAGE},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": DOMAIN + post["url"]},
        "isPartOf": {"@type": "Blog", "name": "Elixir Consulting Group Blog", "@id": DOMAIN + "/blog/"},
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {esc_text(clip(post['title'], 48))}</p>
<p style="margin-bottom:14px"><span class="post-tag">{post['category']}</span></p>
<h1 style="font-size:clamp(1.65rem,4.2vw,2.6rem);max-width:900px;margin-left:auto;margin-right:auto">{esc_text(post['title'])}</h1>
<p>{esc_text(post['excerpt'])}</p>
<div class="post-meta">
<img src="{HEADSHOT}" alt="{HEADSHOT_ALT}" width="88" height="88" loading="lazy" decoding="async">
<span>By <a href="/blog/author/dr-connor-robertson/" style="color:#fff;font-weight:600">Dr. Connor Robertson</a></span>
<span class="dot" aria-hidden="true">&middot;</span>
<time datetime="{post['date']}">{pretty_date(post['date'])}</time>
<span class="dot" aria-hidden="true">&middot;</span>
<span>{post['read_min']} min read</span>
</div>
</div>
</section>

<section class="section">
<div class="container">
<figure style="max-width:860px;margin:0 auto 8px">
<img class="article-hero-img" src="{esc_attr(post['image'])}" alt="{esc_attr(post['image_alt'])}" width="1200" height="630" fetchpriority="high" decoding="async">
</figure>
<article class="article-body" id="post-body">
{post['content']}
</article>

<div class="author-box">
<img src="{HEADSHOT}" alt="{HEADSHOT_ALT}" width="192" height="192" loading="lazy" decoding="async">
<div>
<h3>Dr. Connor Robertson</h3>
<p class="author-role">Founder &amp; Lead Consultant, Elixir Consulting Group</p>
<p>Dr. Robertson works hands-on with owners and leadership teams to install operations, sales, and leadership systems that hold up under growth. He is the author of six books on acquisitions and business strategy.</p>
<p style="margin-bottom:0"><a href="/about/">Read the full bio</a> &nbsp;&middot;&nbsp; <a href="/blog/author/dr-connor-robertson/">All his articles</a> &nbsp;&middot;&nbsp; <a href="/contact/">Book a consult</a></p>
</div>
</div>
</div>
</section>

{render_faq_section(faqs, "Related Questions", gray=False)}

<section class="related-posts">
<div class="container">
<div class="text-center" style="margin-bottom:32px">
<span class="eyebrow">Keep Reading</span>
<h2>Related Articles</h2>
</div>
<div class="post-list">
{rel_cards}
</div>
<div class="text-center" style="margin-top:32px">
<a href="/blog/" class="btn btn-outline">Browse All Articles</a>
</div>
</div>
</section>

{make_cta()}
"""
    return make_page(
        seo_title_for(post["title"]),
        clip(post["description"], 158),
        post["url"],
        body,
        schema,
        og_title=post["title"],
        canonical=post.get("canonical"),
        image=post["og_image"],
        og_type="article",
        published=post["date"],
        modified=post["modified"],
        faq=faqs,
        crumb_override=clip(post["title"], 60),
    )


# ─── Process page ──────────────────────────────────────────────────────

PROCESS_STEPS = [
    ("Consult", "60&ndash;90 minutes",
     "We talk through your business: what is working, what keeps breaking, and what you want the next twelve months to look like. No deck, no pitch. At the end of it you get an honest read on whether we are the right partner, including when the answer is no.",
     ["What is actually constraining growth right now", "Whether the problem is structural or situational", "A clear yes or no on fit"]),
    ("Structured Assessment", "2&ndash;3 weeks",
     "We map how work really moves through your business, not how the org chart says it should. That means walking real jobs end to end, interviewing the people doing the work, and looking at the numbers you already have. The output is a written picture of your current state and the few constraints that matter most.",
     ["A process map built from observation, not assumption", "Baseline metrics we will measure against", "A prioritized list of the highest-leverage changes"]),
    ("Design", "1&ndash;2 weeks",
     "We design the systems with your leadership team rather than for them. Cadence, scorecards, ownership, and documented workflows get built to fit how your business actually operates. Anything too complicated to run without us is the wrong design.",
     ["Meeting rhythm and agendas", "Scorecards with owners for each measure", "SOPs written where the work happens"]),
    ("Implementation", "8&ndash;16 weeks",
     "This is the part most firms skip. We sit in the meetings, run the first cycles alongside your team, and fix what does not survive contact with reality. Systems get adjusted while people are learning them, which is the only window where adjustment is cheap.",
     ["Weekly working sessions with your team", "Live adjustment as the systems meet reality", "Adoption measured, not assumed"]),
    ("Handover & Advisory", "Ongoing, optional",
     "The engagement ends when your team runs the cadence without us in the room. Many clients continue with monthly advisory to keep the systems evolving as the business changes, but that is a choice rather than a requirement.",
     ["Your team running the cadence independently", "Documented systems that survive turnover", "Optional monthly advisory"]),
]

PROCESS_FAQS = [
    ("How long does a full engagement take?",
     "Most engagements run between 90 days and six months end to end. The assessment and design phases are short; implementation is where the time goes, because adoption cannot be rushed without losing it."),
    ("What do you need from our team?",
     "Access and attendance. We need to talk to the people doing the work, not just leadership, and we need the leadership team in the weekly sessions. Engagements fail when the owner delegates the implementation and stops showing up."),
    ("Do you work on-site or remotely?",
     "Both. The assessment usually benefits from on-site time, and implementation works well in a hybrid rhythm. Our virtual process is structured to be as effective as in-person work, which is how we serve clients nationwide from Pittsburgh."),
    ("What happens if it is not working?",
     "We tell you. The weekly measurement exists precisely so that a system that is not being adopted becomes visible in week three rather than month five. Then we change the design, because the design was wrong."),
    ("Is the first consult really free?",
     "Yes. There is no cost and no obligation. It exists so both sides can decide whether the work makes sense."),
    ("What does it cost?",
     f"Pricing depends on scope and business size, and we offer both project-based and retainer arrangements. We discuss it after the consult, once we both know what the work actually involves. Call {PHONE} to start."),
]


def gen_process():
    steps = ""
    for i, (name, dur, desc, deliverables) in enumerate(PROCESS_STEPS, 1):
        items = "".join(f"<li>{d}</li>\n" for d in deliverables)
        steps += f"""<div class="card" style="border-left:4px solid {COLORS['gold']}">
<div style="display:flex;flex-wrap:wrap;align-items:baseline;gap:12px;margin-bottom:10px">
<span class="stat-num" style="font-size:1.6rem">{i:02d}</span>
<h3 style="margin-bottom:0">{name}</h3>
<span class="post-tag" style="color:{COLORS['navy']};background:{COLORS['off_white']};border-color:{COLORS['border']}">{dur}</span>
</div>
<p>{desc}</p>
<p style="font-weight:600;color:{COLORS['navy']};margin-bottom:6px;font-size:.9rem">What you get</p>
<ul class="checklist" style="list-style:none;padding-left:0;margin-left:0">
{items}
</ul>
</div>\n"""

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How an Elixir Consulting Group engagement works",
        "description": "The five phases of a business consulting engagement, from initial consult through handover.",
        "totalTime": "P180D",
        "step": [
            {"@type": "HowToStep", "position": i, "name": name,
             "text": re.sub(r"<[^>]+>", "", desc)}
            for i, (name, _d, desc, _x) in enumerate(PROCESS_STEPS, 1)
        ],
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Process</p>
<h1>How We Work</h1>
<p>Five phases, roughly 90 days to six months. The engagement ends when your team runs the systems without us in the room.</p>
<div style="margin-top:24px">
<a href="/contact/" class="btn btn-gold">Book a Consult</a>
<a href="/case-studies/" class="btn btn-outline" style="border-color:rgba(255,255,255,.4);color:#fff">See the Results</a>
</div>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:44px;max-width:720px;margin-left:auto;margin-right:auto">
<span class="eyebrow">The Method</span>
<h2>Implementation Is the Product</h2>
<p>Most consulting engagements end at the recommendation. Ours starts there. The assessment and the design matter, but they are inputs. What you are actually buying is a team that sits in the room while the systems get adopted and fixes what does not survive contact with reality.</p>
</div>
<div class="grid grid-2">
{steps}
</div>
</div>
</section>

<section class="section section-navy">
<div class="container">
<div class="text-center" style="margin-bottom:40px">
<span class="eyebrow">What We Will Not Do</span>
<h2>Being Clear About the Boundaries</h2>
</div>
<div class="grid grid-3">
<div class="card" style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14)">
<h3 style="color:#fff">Hand you a binder</h3>
<p style="color:rgba(255,255,255,.8)">A report you have to implement alone is the failure mode we exist to avoid. If we are not in the room for implementation, the engagement has not started.</p>
</div>
<div class="card" style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14)">
<h3 style="color:#fff">Replace your team</h3>
<p style="color:rgba(255,255,255,.8)">We build on the people you already have. If the honest answer is that a seat is wrong, we will say so, but our default is that the systems are the problem.</p>
</div>
<div class="card" style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14)">
<h3 style="color:#fff">Take work that will not succeed</h3>
<p style="color:rgba(255,255,255,.8)">If the leadership team is not going to show up weekly, the engagement will fail regardless of the design. We would rather tell you that during the consult.</p>
</div>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:40px">
<span class="eyebrow">Where We Start</span>
<h2>Five Service Areas, One Method</h2>
</div>
<div class="grid grid-3">
<div class="card"><h3><a href="/services/operations/">Operations</a></h3><p>Process, SOPs, role clarity, and the weekly cadence that keeps delivery consistent.</p></div>
<div class="card"><h3><a href="/services/sales-strategy/">Sales Strategy</a></h3><p>Pipeline structure, follow-up standards, and CRM configuration your team will run.</p></div>
<div class="card"><h3><a href="/services/leadership/">Leadership</a></h3><p>Meeting rhythm, scorecards, and accountability that produce decisions.</p></div>
<div class="card"><h3><a href="/services/business-strategy/">Business Strategy</a></h3><p>Growth roadmaps and execution frameworks tied to weekly action.</p></div>
<div class="card"><h3><a href="/services/ai-consulting/">AI Consulting</a></h3><p>Practical AI evaluation, implementation, and team adoption without disruption.</p></div>
<div class="card"><h3><a href="/industries/">By Industry</a></h3><p>Sector-specific context across eight industries we work in regularly.</p></div>
</div>
</div>
</section>

{render_faq_section(PROCESS_FAQS, "Process FAQs")}

{make_cta()}
"""
    return make_page(
        "How We Work | Our Consulting Process | Elixir Consulting Group",
        "The five phases of an Elixir Consulting Group engagement: consult, assessment, design, implementation, and handover. Typically 90 days to six months.",
        "/process/",
        body,
        schema,
        faq=PROCESS_FAQS,
    )


# ─── Blog category archives ────────────────────────────────────────────

def category_slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


CATEGORY_INTROS = {
    "AI & Technology": "Practical coverage of AI adoption, automation, and digital transformation for owner-led businesses. Less hype, more implementation.",
    "Sales & Revenue": "Pipeline structure, follow-up discipline, pricing, and the revenue systems that make forecasting something other than a guess.",
    "Operations": "Process design, SOPs, workflow, and the operating cadence that turns effort into consistent output.",
    "Leadership": "Meeting rhythm, accountability, hiring, delegation, and the work of building a team that executes without you.",
    "Strategy & Growth": "Positioning, planning, and the execution frameworks that connect a strategy to what happens on Monday.",
    "Finance & Exit": "Margin, cash flow, valuation, acquisitions, and preparing a business to be worth buying.",
    "Pittsburgh & Local": "Regional economic coverage and what it means for business owners in Western Pennsylvania.",
    "Insights": "General commentary on running an owner-led business well.",
}


def gen_category_page(cat, posts, all_posts):
    slug = category_slug(cat)
    cards = "".join(post_card(p, lazy=(i > 5)) for i, p in enumerate(posts))
    intro = CATEGORY_INTROS.get(cat, f"Articles on {cat.lower()} from Elixir Consulting Group.")

    others = "".join(
        f'<a href="/blog/category/{category_slug(c)}/" class="services-link">{c}</a>'
        for c in CATEGORY_ORDER if c != cat and any(p["category"] == c for p in all_posts))

    faqs = [
        (f"How many {cat.lower()} articles are there?",
         f"This archive currently holds {len(posts)} articles on {cat.lower()}, part of a library of {len(all_posts)} across every topic we cover."),
        ("Who writes these articles?",
         "Dr. Connor Robertson, founder and lead consultant at Elixir Consulting Group, drawing on hands-on implementation work with owner-led businesses."),
        (f"Do you offer consulting in {cat.lower()}?",
         f"Yes. Reading is a fine start, but the articles describe systems we install directly with clients. Book a consult or call {PHONE} to talk about your specific situation."),
        ("How often is this archive updated?",
         "New articles are published regularly. The newest work appears first on this page and on the main blog index."),
    ]

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"{cat} Articles",
        "url": DOMAIN + f"/blog/category/{slug}/",
        "description": intro,
        "isPartOf": {"@type": "Blog", "@id": DOMAIN + "/blog/"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(posts),
            "itemListElement": [
                {"@type": "ListItem", "position": i, "url": DOMAIN + p["url"], "name": p["title"]}
                for i, p in enumerate(posts[:30], 1)
            ],
        },
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {cat}</p>
<p style="margin-bottom:14px"><span class="post-tag">Category</span></p>
<h1>{cat}</h1>
<p>{intro}</p>
<p style="margin-top:12px;font-size:.95rem;color:rgba(255,255,255,.7)">{len(posts)} articles</p>
</div>
</section>

<section class="section">
<div class="container">
<div class="post-list">
{cards}
</div>
</div>
</section>

<section class="section section-gray">
<div class="container text-center">
<span class="eyebrow">Browse</span>
<h2 style="margin-bottom:24px">Other Categories</h2>
<div>{others}</div>
<div style="margin-top:28px"><a href="/blog/" class="btn btn-outline">All {len(all_posts)} Articles</a></div>
</div>
</section>

{render_faq_section(faqs, f"{cat} FAQs", gray=False)}

{make_cta()}
"""
    return make_page(
        f"{cat} Articles | Elixir Consulting Group Blog",
        clip(intro + f" {len(posts)} articles from Elixir Consulting Group.", 158),
        f"/blog/category/{slug}/",
        body,
        schema,
        faq=faqs,
        crumb_override=cat,
    )


# ─── Author archive ────────────────────────────────────────────────────

def gen_author_page(all_posts):
    recent = all_posts[:36]
    cards = "".join(post_card(p, lazy=(i > 5)) for i, p in enumerate(recent))
    counts = {}
    for p in all_posts:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    cat_links = "".join(
        f'<a href="/blog/category/{category_slug(c)}/" class="services-link">{c} ({counts[c]})</a>'
        for c in CATEGORY_ORDER if counts.get(c))

    faqs = [
        ("Who is Dr. Connor Robertson?",
         "Dr. Connor Robertson is the founder and lead consultant at Elixir Consulting Group, a Pittsburgh-based firm that installs operations, sales, and leadership systems in owner-led businesses. He is the author of six books on acquisitions and business strategy."),
        ("Does he write all of these articles himself?",
         f"Yes. Every one of the {len(all_posts)} articles in this archive is written from his own implementation work with clients."),
        ("Can I work with him directly?",
         "Yes. Engagements are led personally rather than handed to a junior team, because the implementation model only works when the person designing the systems is in the room while they are adopted."),
        ("Where else can I find his work?",
         "At drconnorrobertson.com, and his books are available through Barnes & Noble, Google Play, and Kobo."),
    ]

    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "url": DOMAIN + "/blog/author/dr-connor-robertson/",
        "mainEntity": {"@id": DOMAIN + "/#founder"},
        "about": {"@id": DOMAIN + "/#founder"},
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / Author</p>
<img src="{HEADSHOT}" alt="{HEADSHOT_ALT}" width="800" height="800" style="width:150px;height:150px;border-radius:50%;object-fit:cover;margin:0 auto 20px;display:block;border:3px solid rgba(201,168,76,.5)" fetchpriority="high" decoding="async">
<h1>Dr. Connor Robertson</h1>
<p>Founder &amp; Lead Consultant, Elixir Consulting Group. {len(all_posts)} articles on operations, sales systems, leadership, and growth.</p>
<div style="margin-top:24px">
<a href="/about/" class="btn btn-gold">Full Bio</a>
<a href="/contact/" class="btn btn-outline" style="border-color:rgba(255,255,255,.4);color:#fff">Book a Consult</a>
</div>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">
<div class="text-center" style="margin-bottom:36px">
<span class="eyebrow">Browse by Topic</span>
<h2>Categories</h2>
</div>
<div class="text-center" style="max-width:820px;margin:0 auto">{cat_links}</div>
</div>
</section>

<section class="section section-gray">
<div class="container">
<div class="text-center" style="margin-bottom:36px">
<span class="eyebrow">Latest</span>
<h2>Recent Articles</h2>
</div>
<div class="post-list">
{cards}
</div>
<div class="text-center" style="margin-top:36px">
<a href="/blog/" class="btn btn-primary">All {len(all_posts)} Articles</a>
</div>
</div>
</section>

{render_faq_section(faqs, "About the Author", gray=False)}

{make_cta()}
"""
    return make_page(
        "Dr. Connor Robertson | Articles & Insights | Elixir Consulting",
        f"All {len(all_posts)} articles by Dr. Connor Robertson, founder of Elixir Consulting Group, on operations, sales systems, leadership, AI adoption, and business growth.",
        "/blog/author/dr-connor-robertson/",
        body,
        schema,
        faq=faqs,
        crumb_override="Dr. Connor Robertson",
    )


# ─── Site search ───────────────────────────────────────────────────────

def gen_search_page(all_posts, page_count):
    faqs = [
        ("How does this search work?",
         f"It searches titles, summaries, and categories across all {all_posts} articles plus every service, industry, location, and case study page. It runs entirely in your browser, so nothing you type is sent anywhere."),
        ("I cannot find what I am looking for.",
         f"Try a shorter or more general term, or browse the blog by category. If it is a question about your own business rather than a topic, call {PHONE} or book a consult and ask directly."),
        ("Do you have articles on my industry?",
         "Probably. Start with the industries pages, which link to the most relevant articles for each of the eight sectors we work in most often."),
    ]

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Search</p>
<h1>Search</h1>
<p>Search {page_count} pages across the site: articles, services, industries, case studies, and locations.</p>
</div>
</section>

<section class="section">
<div class="container" style="max-width:860px">
<label for="site-search" style="position:absolute;left:-9999px">Search the site</label>
<input type="search" id="site-search" class="blog-search" style="width:100%;font-size:1.05rem;padding:16px 18px" placeholder="Try: operations cadence, sales pipeline, exit planning..." autocomplete="off" autofocus>
<p id="search-count" style="margin-top:14px;color:{COLORS['mid_gray']};font-size:.92rem">Start typing to search.</p>
<div id="search-results" style="margin-top:24px"></div>
<div id="search-empty" style="display:none;text-align:center;padding:40px 0">
<p>Nothing matched that search.</p>
<p><a href="/blog/" class="btn btn-outline">Browse the blog</a> <a href="/contact/" class="btn btn-primary">Ask us directly</a></p>
</div>
</div>
</section>

{render_faq_section(faqs, "Search Help")}

{make_cta()}

<script>
/* The index is a static JSON file so this page stays a plain static asset --
   no server, no third-party search service, nothing typed here leaves the browser. */
(function(){{
var input=document.getElementById('site-search');
var out=document.getElementById('search-results');
var count=document.getElementById('search-count');
var empty=document.getElementById('search-empty');
var idx=[],ready=false;
fetch('/search-index.json').then(function(r){{return r.json()}}).then(function(d){{
idx=d;ready=true;if(input.value)run();
}}).catch(function(){{count.textContent='Search index could not be loaded. Try the blog index instead.'}});
function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
function run(){{
var q=input.value.trim().toLowerCase();
if(!ready){{count.textContent='Loading index...';return}}
if(q.length<2){{out.innerHTML='';empty.style.display='none';count.textContent='Start typing to search.';return}}
var terms=q.split(/\\s+/);
/* Match a trimmed stem as well as the literal term, so "manufacturing" still
   finds "manufacturers" and "operations" finds "operational". */
var stems=terms.map(function(t){{return t.length>=6?t.slice(0,t.length-3):t}});
var hits=[],loose=[];
for(var i=0;i<idx.length;i++){{
var it=idx[i],hay=it.s,title=it.t.toLowerCase(),score=0,matched=0;
for(var t=0;t<terms.length;t++){{
var exact=hay.indexOf(terms[t])>-1;
if(!exact&&hay.indexOf(stems[t])<0)continue;
matched++;
score+=(title.indexOf(terms[t])>-1?4:(title.indexOf(stems[t])>-1?3:(exact?2:1)));
}}
if(matched===terms.length)hits.push([score+10,it]);
else if(matched>0)loose.push([score,it]);
}}
/* Requiring every term is right when it finds enough; when a multi-word query
   is too narrow, fall back to partial matches rather than showing nothing. */
if(hits.length<3&&loose.length)hits=hits.concat(loose);
hits.sort(function(a,b){{return b[0]-a[0]}});
count.textContent=hits.length+(hits.length===1?' result':' results');
empty.style.display=hits.length?'none':'block';
out.innerHTML=hits.slice(0,60).map(function(h){{
var it=h[1];
return '<div class="card" style="margin-bottom:14px;padding:20px 24px">'+
'<p class="pc-cat">'+esc(it.k)+'</p>'+
'<h3 style="font-size:1.05rem;margin-bottom:6px"><a href="'+esc(it.u)+'">'+esc(it.t)+'</a></h3>'+
'<p style="font-size:.93rem;margin-bottom:0">'+esc(it.d)+'</p></div>';
}}).join('');
}}
input.addEventListener('input',run);
var pre=new URLSearchParams(location.search).get('q');
if(pre){{input.value=pre;run()}}
}})();
</script>
"""
    return make_page(
        "Search | Elixir Consulting Group",
        f"Search {page_count} pages across Elixir Consulting Group: articles on operations, sales, leadership, and AI, plus services, industries, case studies, and locations.",
        "/search/",
        body,
        faq=faqs,
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
<div class="split-2">
<div>
<span class="eyebrow">Get in Touch</span>
<h2>Book a Consult</h2>
<p>Every engagement starts with a consult where we learn about your business, goals, and current constraints. There is no obligation and no pressure. If there is a fit, we will discuss next steps.</p>
<div class="contact-strip" style="margin-bottom:28px">
<a href="{PHONE_HREF}"><span class="ic">&#9742;</span> {PHONE}</a>
<a href="mailto:{EMAIL}"><span class="ic">&#9993;</span> Email Us</a>
</div>
<form id="consult-form" action="mailto:{EMAIL}" method="POST" enctype="text/plain" style="margin-top:8px">
<div class="form-group"><label for="cf-name">Full Name</label><input id="cf-name" type="text" name="name" required autocomplete="name" placeholder="Your full name"></div>
<div class="form-group"><label for="cf-email">Email</label><input id="cf-email" type="email" name="email" required autocomplete="email" placeholder="your@email.com"></div>
<div class="form-group"><label for="cf-phone">Phone</label><input id="cf-phone" type="tel" name="phone" autocomplete="tel" placeholder="(555) 123-4567"></div>
<div class="form-group"><label for="cf-company">Company Name</label><input id="cf-company" type="text" name="company" autocomplete="organization" placeholder="Your company"></div>
<div class="form-group"><label for="cf-service">How Can We Help?</label>
<select id="cf-service" name="service">
<option value="">Select a service area</option>
<option value="business-strategy">Business Strategy</option>
<option value="ai-consulting">AI Consulting</option>
<option value="operations">Operations Consulting</option>
<option value="sales-strategy">Sales Strategy</option>
<option value="leadership">Leadership Consulting</option>
<option value="other">Other</option>
</select>
</div>
<div class="form-group"><label for="cf-message">Message</label><textarea id="cf-message" name="message" placeholder="Tell us about your business and what you are looking to improve..."></textarea></div>
<button type="submit" class="btn btn-primary" style="width:100%">Request a Consult</button>
<p id="cf-status" role="status" aria-live="polite" style="margin-top:14px;font-size:.9rem;color:{COLORS['mid_gray']}">
Prefer to skip the form? Call <a href="{PHONE_HREF}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.
</p>
</form>
<script>
/* This is a static site with no server to post to. Rather than let a submit
   silently discard a lead, compose the message and hand it to the visitor's
   mail client, and keep the phone number visible either way. Swap the handler
   for a real endpoint when one exists. */
(function(){{
var form=document.getElementById('consult-form');
var status=document.getElementById('cf-status');
if(!form)return;
form.addEventListener('submit',function(e){{
e.preventDefault();
var get=function(id){{var el=document.getElementById(id);return el?el.value.trim():''}};
var name=get('cf-name'),email=get('cf-email');
if(!name||!email){{status.textContent='Please add your name and email so we can reply.';return}}
var lines=[
'Name: '+name,
'Email: '+email,
'Phone: '+(get('cf-phone')||'not provided'),
'Company: '+(get('cf-company')||'not provided'),
'Service area: '+(get('cf-service')||'not specified'),
'',
get('cf-message')||'(no message)'
].join('\n');
var href='mailto:{EMAIL}'
  +'?subject='+encodeURIComponent('Consult request from '+name)
  +'&body='+encodeURIComponent(lines);
status.innerHTML='Opening your email app with the details filled in. If nothing happens, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="{PHONE_HREF}">{PHONE}</a>.';
window.location.href=href;
}});
}})();
</script>
</div>
<div>
<div class="contact-info-card" style="margin-top:48px">
<h3>Call or Email</h3>
<p style="margin-bottom:6px"><a href="{PHONE_HREF}" style="font-weight:700;font-size:1.15rem">{PHONE}</a></p>
<p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>
<div class="contact-info-card">
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
    body += render_faq_section(CONTACT_FAQS, "Before You Reach Out", gray=False)
    return make_page(
        "Contact Elixir Consulting Group | Book a Free Consult",
        f"Book a consult with Elixir Consulting Group. Call {PHONE} or email {EMAIL}. Based in Pittsburgh, PA and serving business owners nationwide.",
        "/contact/",
        body,
        faq=CONTACT_FAQS,
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

    # Individual Review items for the testimonials actually shown on this page.
    # No aggregateRating: numeric star ratings were never collected for these,
    # and asserting one that nothing on the page supports is exactly the kind of
    # self-serving markup search engines discount or penalize.
    schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Client testimonials for Elixir Consulting Group",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "item": {
                    "@type": "Review",
                    "reviewBody": t["text"],
                    "author": {"@type": "Person", "name": t["name"], "jobTitle": t["role"]},
                    "itemReviewed": {"@id": DOMAIN + "/#organization"},
                    "publisher": {"@id": DOMAIN + "/#organization"},
                },
            }
            for i, t in enumerate(TESTIMONIALS, 1)
        ],
    }) + '\n</script>'

    body = f"""
<section class="page-hero">
<div class="container">
<p class="breadcrumb"><a href="/">Home</a> / Testimonials</p>
<h1>Client Testimonials</h1>
<p>What business owners and leaders say about working with Elixir Consulting Group. Names are abbreviated at client request; several engagements involved exit planning or leadership restructuring that clients prefer to keep private.</p>
</div>
</section>

{make_trust_bar()}

<section class="section">
<div class="container">
<div class="grid grid-2">
{cards}
</div>
</div>
</section>

<section class="section section-navy">
<div class="container">
<div class="text-center" style="margin-bottom:40px">
<span class="eyebrow">Beyond the Quotes</span>
<h2>The Documented Version</h2>
<p style="max-width:660px;margin:0 auto">Testimonials are useful, but numbers are better. Each case study below covers a full engagement: what was broken, what we built, and what measurably changed.</p>
</div>
<div class="grid grid-4">
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">40%</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Fewer delivery delays</span></div>
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">2x</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Close rate</span></div>
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">70%</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Fewer handoff errors</span></div>
<div class="stat-card"><span class="stat-num" style="color:{COLORS['gold']}">35%</span><span class="stat-label" style="color:rgba(255,255,255,.85)">Higher satisfaction</span></div>
</div>
<div class="text-center" style="margin-top:36px">
<a href="/case-studies/" class="btn btn-gold">Read the Case Studies</a>
</div>
</div>
</section>
"""
    body += render_faq_section(TESTIMONIAL_FAQS, "Testimonial FAQs")
    body += make_cta()
    return make_page(
        "Client Testimonials | Elixir Consulting Group",
        "Testimonials from business owners who worked with Elixir Consulting Group on operations, sales systems, and leadership cadence. Pittsburgh, PA and nationwide.",
        "/testimonials/",
        body,
        schema,
        faq=TESTIMONIAL_FAQS,
    )


# ─── Feeds, search index, and static site assets ───────────────────────

def rfc822(iso):
    try:
        y, m, d = (int(x) for x in iso.split("-"))
        dt = datetime(y, m, d, 12, 0, 0)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        mons = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return f"{days[dt.weekday()]}, {d:02d} {mons[m-1]} {y} 12:00:00 +0000"
    except Exception:
        return "Thu, 01 Jan 2026 12:00:00 +0000"


def xml_escape(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;"))


def gen_rss(all_posts, limit=50):
    items = ""
    for p in all_posts[:limit]:
        items += f"""  <item>
    <title>{xml_escape(p['title'])}</title>
    <link>{DOMAIN}{p['url']}</link>
    <guid isPermaLink="true">{DOMAIN}{p['url']}</guid>
    <description>{xml_escape(p['excerpt'])}</description>
    <category>{xml_escape(p['category'])}</category>
    <dc:creator>Dr. Connor Robertson</dc:creator>
    <pubDate>{rfc822(p['date'])}</pubDate>
  </item>\n"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
  <title>Elixir Consulting Group Blog</title>
  <link>{DOMAIN}/blog/</link>
  <atom:link href="{DOMAIN}/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Practical articles on business strategy, operations, AI adoption, sales systems, and leadership for owner-led companies.</description>
  <language>en-us</language>
  <copyright>Copyright {YEAR} Elixir Consulting Group</copyright>
  <managingEditor>{EMAIL} (Dr. Connor Robertson)</managingEditor>
  <webMaster>{EMAIL} (Elixir Consulting Group)</webMaster>
  <lastBuildDate>{rfc822(all_posts[0]['date'] if all_posts else DATE_NOW)}</lastBuildDate>
  <image>
    <url>{OG_IMAGE}</url>
    <title>Elixir Consulting Group Blog</title>
    <link>{DOMAIN}/blog/</link>
  </image>
{items}</channel>
</rss>"""


def gen_search_index(all_posts, consulting_pages):
    """Static JSON index powering /search/.

    Kept deliberately small: a title, a URL, a short description, a kind label,
    and one pre-lowercased haystack string the page can substring-match. At a few
    hundred entries this stays well under the size where a real search service
    would be worth the dependency.
    """
    entries = []

    def add(title, url, desc, kind, extra=""):
        entries.append({
            "t": title, "u": url, "d": clip(desc, 150), "k": kind,
            "s": " ".join([title, desc, kind, extra]).lower(),
        })

    add("Home", "/", "Business consulting for owner-led companies: operations, sales systems, and leadership cadence.", "Page")
    add("About Dr. Connor Robertson", "/about/", "Founder and lead consultant at Elixir Consulting Group, author of six books on acquisitions and strategy.", "Page", "bio founder team")
    add("How We Work", "/process/", "The five phases of an engagement: consult, assessment, design, implementation, handover.", "Page", "process method engagement phases")
    add("Services", "/services/", "Five core consulting services covering strategy, AI, operations, sales, and leadership.", "Page")
    add("Contact", "/contact/", f"Book a consult. Call {PHONE} or email {EMAIL}.", "Page", "book consult phone email")
    add("FAQ", "/faq/", "Answers on pricing, process, engagement length, and what working together involves.", "Page", "questions pricing cost")
    add("Testimonials", "/testimonials/", "What clients say about working with Elixir Consulting Group.", "Page", "reviews clients")
    add("Case Studies", "/case-studies/", "Documented engagements with the systems installed and the results they produced.", "Page", "results proof")
    add("Industries", "/industries/", "Eight sectors we work in regularly, with the constraints specific to each.", "Page")
    add("Consulting Locations", "/consulting/", "Regions served, from Pittsburgh across Pennsylvania and nationwide.", "Page", "locations cities areas")
    add("Search", "/search/", "Search every page on the site.", "Page")

    for slug, title, desc in [
        ("business-strategy", "Business Strategy Consulting", "Strategic planning, growth roadmaps, competitive analysis, and execution frameworks."),
        ("ai-consulting", "AI Consulting & Digital Transformation", "AI readiness, workflow automation, tool selection, and team adoption."),
        ("operations", "Operations Consulting", "Process mapping, SOPs, role clarity, and weekly operating cadence."),
        ("sales-strategy", "Sales Strategy & Revenue Systems", "Pipeline design, follow-up systems, CRM optimization, and forecasting."),
        ("leadership", "Leadership Consulting & Executive Coaching", "Leadership cadence, scorecards, accountability, and succession planning."),
    ]:
        add(title, f"/services/{slug}/", desc, "Service")

    for ind in INDUSTRIES:
        add(f"{ind['name']} Consulting", f"/industries/{ind['slug']}/", ind["short"], "Industry")

    for cs in CASE_STUDIES:
        add(cs["title"], f"/case-studies/{cs['slug']}/", cs["challenge"], "Case Study", cs["industry"])

    for cat in CATEGORY_ORDER:
        if any(p["category"] == cat for p in all_posts):
            add(f"{cat} Articles", f"/blog/category/{category_slug(cat)}/",
                CATEGORY_INTROS.get(cat, ""), "Category")

    for cp in consulting_pages:
        add(f"Business Consulting in {cp['city']}, {cp['state']}",
            f"/consulting/{cp['slug']}/", cp["tagline"], "Location")

    for landing, city in [
        ("pittsburgh-business-consultant", "Pittsburgh"),
        ("pittsburgh-ai-consulting", "Pittsburgh AI"),
        ("pittsburgh-operations-consulting", "Pittsburgh Operations"),
        ("cranberry-township-business-consultant", "Cranberry Township"),
        ("wexford-business-consultant", "Wexford"),
    ]:
        add(f"{city} Business Consulting", f"/{landing}/",
            f"Consulting services for businesses in {city} and the surrounding area.", "Location")

    for p in all_posts:
        add(p["title"], p["url"], p["excerpt"], p["category"])

    return json.dumps(entries, separators=(",", ":"))


def gen_sitemap_index(names):
    parts = "".join(
        f"  <sitemap>\n    <loc>{DOMAIN}/{n}</loc>\n    <lastmod>{DATE_NOW}</lastmod>\n  </sitemap>\n"
        for n in names)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{parts}</sitemapindex>"""


def gen_urlset(urls, lastmod=None):
    lastmod = lastmod or {}
    entries = ""
    for path, priority, freq in urls:
        entries += f"""  <url>
    <loc>{DOMAIN}{path}</loc>
    <lastmod>{lastmod.get(path, DATE_NOW)}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}</urlset>"""


def gen_manifest():
    return json.dumps({
        "name": "Elixir Consulting Group",
        "short_name": "Elixir",
        "description": "Business consulting for owner-led companies: operations, sales systems, and leadership cadence.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#FFFFFF",
        "theme_color": COLORS["navy"],
        "lang": "en-US",
        "icons": [
            {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
            {"src": "/images/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/images/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, indent=2)


def gen_security_txt():
    return f"""Contact: mailto:{EMAIL}
Contact: tel:+14123877656
Preferred-Languages: en
Canonical: {DOMAIN}/.well-known/security.txt
Expires: 2027-12-31T23:59:59.000Z
Policy: {DOMAIN}/contact/

# Elixir Consulting Group runs a static marketing site. If you have found a
# security issue, email the address above and we will respond within one
# business day.
"""


def gen_humans_txt():
    return f"""/* TEAM */
Founder & Lead Consultant: Dr. Connor Robertson
Site: {DOMAIN}
Contact: {EMAIL}
Location: Pittsburgh, Pennsylvania, USA

/* SITE */
Last update: {DATE_NOW}
Standards: HTML5, CSS3, JSON-LD
Components: Static site generator (Python), no runtime dependencies
Typography: Inter
"""


def gen_robots():
    return f"""# Elixir Consulting Group
User-agent: *
Allow: /
Disallow: /search?
Disallow: /*?q=

# Crawl the whole site; nothing here is private.
Sitemap: {DOMAIN}/sitemap.xml
Sitemap: {DOMAIN}/sitemap-pages.xml
Sitemap: {DOMAIN}/sitemap-blog.xml
Sitemap: {DOMAIN}/sitemap-locations.xml
"""


# Core pages, split out so the sitemap index can group them separately from
# the blog archive and the location pages. Large sitemaps are easier for search
# engines to process (and for us to debug) when they are partitioned by type.
CORE_SITEMAP_URLS = [
    ("/", "1.0", "weekly"),
    ("/about/", "0.85", "monthly"),
    ("/process/", "0.85", "monthly"),
    ("/services/", "0.9", "monthly"),
    ("/services/business-strategy/", "0.85", "monthly"),
    ("/services/ai-consulting/", "0.85", "monthly"),
    ("/services/operations/", "0.85", "monthly"),
    ("/services/sales-strategy/", "0.85", "monthly"),
    ("/services/leadership/", "0.85", "monthly"),
    ("/industries/", "0.8", "monthly"),
    ("/case-studies/", "0.8", "monthly"),
    ("/blog/", "0.85", "daily"),
    ("/blog/author/dr-connor-robertson/", "0.6", "weekly"),
    ("/contact/", "0.85", "monthly"),
    ("/faq/", "0.75", "monthly"),
    ("/testimonials/", "0.75", "monthly"),
    ("/search/", "0.3", "yearly"),
]


def sitemap_pages_urls():
    urls = list(CORE_SITEMAP_URLS)
    for ind in INDUSTRIES:
        urls.append((f"/industries/{ind['slug']}/", "0.75", "monthly"))
    for cs in CASE_STUDIES:
        urls.append((f"/case-studies/{cs['slug']}/", "0.75", "monthly"))
    return urls


def sitemap_blog_urls(all_posts, categories):
    urls = [(f"/blog/category/{category_slug(c)}/", "0.7", "weekly") for c in categories]
    lastmod = {}
    for i, post in enumerate(all_posts):
        urls.append((post["url"], "0.75" if i < 12 else "0.6", "monthly"))
        lastmod[post["url"]] = post.get("modified") or post["date"]
    return urls, lastmod


def sitemap_location_urls(consulting_pages):
    urls = [
        ("/consulting/", "0.8", "monthly"),
        ("/pittsburgh-business-consultant/", "0.9", "monthly"),
        ("/pittsburgh-ai-consulting/", "0.9", "monthly"),
        ("/pittsburgh-operations-consulting/", "0.9", "monthly"),
        ("/cranberry-township-business-consultant/", "0.8", "monthly"),
        ("/wexford-business-consultant/", "0.8", "monthly"),
    ]
    for cp in consulting_pages:
        urls.append((f"/consulting/{cp['slug']}/", "0.7", "monthly"))
    return urls


def gen_vercel_json():
    return json.dumps({
        "cleanUrls": True,
        "trailingSlash": True,
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {"key": "X-Content-Type-Options", "value": "nosniff"},
                    {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
                    {"key": "X-XSS-Protection", "value": "1; mode=block"},
                    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                    {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
                    {"key": "Strict-Transport-Security", "value": "max-age=31536000; includeSubDomains"}
                ]
            },
            {
                "source": "/(.*).html",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=3600, stale-while-revalidate=86400"},
                    {"key": "Content-Type", "value": "text/html; charset=utf-8"}
                ]
            },
            {
                "source": "/sitemap.xml",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=86400"},
                    {"key": "Content-Type", "value": "application/xml"}
                ]
            },
            {
                "source": "/robots.txt",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=86400"},
                    {"key": "Content-Type", "value": "text/plain"}
                ]
            },
            {
                "source": "/images/(.*)",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}
                ]
            },
            {
                "source": "/favicon.svg",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=604800"},
                    {"key": "Content-Type", "value": "image/svg+xml"}
                ]
            }
        ],
        "redirects": [
            {
                "source": "/dr-connor-robertson/",
                "destination": "/about/",
                "statusCode": 301
            },
            {
                "source": "/resources/",
                "destination": "/blog/",
                "statusCode": 301
            },
            {
                "source": "/operations-consulting/",
                "destination": "/services/operations/",
                "statusCode": 301
            },
            {
                "source": "/sitemap_index.xml",
                "destination": "/sitemap.xml",
                "statusCode": 301
            },
            {
                "source": "/locations/",
                "destination": "/consulting/",
                "statusCode": 301
            },
            {
                "source": "/about-us/",
                "destination": "/about/",
                "statusCode": 301
            },
            {
                "source": "/team/",
                "destination": "/about/",
                "statusCode": 301
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

# Ingest the blog first. Reading finishes before any write, so re-running is
# safe, and every downstream page can cross-link into the real archive.
print("\n[1/16] Reading the blog archive")
ALL_POSTS = load_all_posts()
# Canonicalized duplicates still get a page, but they stay out of the index,
# the related-post pool, and the sitemap so only the original competes.
INDEX_POSTS = [p for p in ALL_POSTS if not p.get("duplicate_of")]
POSTS_BY_CATEGORY = {}
for post in INDEX_POSTS:
    POSTS_BY_CATEGORY.setdefault(post["category"], []).append(post)
ACTIVE_CATEGORIES = [c for c in CATEGORY_ORDER if POSTS_BY_CATEGORY.get(c)]
print(f"  {len(ALL_POSTS)} posts ({len(INDEX_POSTS)} canonical) across "
      f"{len(ACTIVE_CATEGORIES)} categories")

print("\n[2/16] Homepage")
write_page("/index.html", gen_homepage(INDEX_POSTS))

# About
print("\n[3/16] About")
write_page("/about/", gen_about())

# Services Overview
print("\n[3.5/16] Services Overview")
write_page("/services/", gen_services_overview())

# Service Pages
print("\n[4/16] Business Strategy")
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
    ],
    all_posts=INDEX_POSTS,
))

print("\n[5/16] AI Consulting")
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
    ],
    all_posts=INDEX_POSTS,
))

print("\n[6/16] Operations Consulting")
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
    ],
    all_posts=INDEX_POSTS,
))

print("\n[7/16] Sales Strategy")
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
    ],
    all_posts=INDEX_POSTS,
))

print("\n[8/16] Leadership Consulting")
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
    ],
    all_posts=INDEX_POSTS,
))

# Industries and case studies need the post list for cross-linking, so they
# are generated after the blog ingest below.
print("\n[9/16] Industries index")
write_page("/industries/", gen_industries())

print("\n[10/16] Case Studies index")
write_page("/case-studies/", gen_case_studies())

print("\n[10.5/16] Process")
write_page("/process/", gen_process())

# Blog: ingest everything on disk first, then re-render the whole archive so
# posts written by other tooling share this template. Reading completes before
# any write, so the pass is safe to re-run.
print("\n[11/16] Blog Index")
write_page("/blog/", gen_blog_index(INDEX_POSTS))

print("\n[12/16] Blog Posts")
for post in ALL_POSTS:
    write_page(post["url"], gen_blog_post(post, INDEX_POSTS))

# Category archives give each of the eight topics its own indexable landing
# page, which a 330-post flat archive cannot do on its own.
print("\n[13/16] Blog Category Archives & Author Page")
for cat in ACTIVE_CATEGORIES:
    write_page(f"/blog/category/{category_slug(cat)}/",
               gen_category_page(cat, POSTS_BY_CATEGORY[cat], INDEX_POSTS))
write_page("/blog/author/dr-connor-robertson/", gen_author_page(INDEX_POSTS))

print("\n[14/16] Industry & Case Study Detail Pages")
for ind in INDUSTRIES:
    write_page(f"/industries/{ind['slug']}/", gen_industry_page(ind, INDEX_POSTS))
for cs in CASE_STUDIES:
    write_page(f"/case-studies/{cs['slug']}/", gen_case_study_page(cs, INDEX_POSTS))

# City Pages
print("\n[14.5/16] City-Specific Service Pages")

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

# Regional consulting pages (same ingest-then-rerender approach as the blog)
print("\n[14.75/16] Regional Consulting Pages")
CONSULTING_PAGES = load_consulting_pages()
print(f"  Loaded {len(CONSULTING_PAGES)} location pages")
write_page("/consulting/", gen_consulting_index(CONSULTING_PAGES))
for cpage in CONSULTING_PAGES:
    write_page(f"/consulting/{cpage['slug']}/", gen_consulting_page(cpage, CONSULTING_PAGES))

# Contact
print("\n[15/16] Contact & FAQ")
write_page("/contact/", gen_contact())

# FAQ
print("\n[15.5/16] Testimonials")
write_page("/faq/", gen_faq())
write_page("/testimonials/", gen_testimonials())

# 404 Page
def gen_404():
    body = """
<section class="page-hero">
<div class="container">
<h1>Page Not Found</h1>
<p>The page you are looking for does not exist or has been moved.</p>
</div>
</section>

<section class="section">
<div class="container">
<div style="text-align:center;max-width:600px;margin:0 auto">
<h2 style="margin-bottom:2rem">404</h2>
<p style="font-size:1.1rem;margin-bottom:2rem;color:#666">We could not find the page you were looking for. Here are some helpful links to get you back on track.</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:2rem 0">
<a href="/" class="btn btn-primary">Home</a>
<a href="/services/" class="btn btn-outline">Services</a>
<a href="/blog/" class="btn btn-outline">Blog</a>
<a href="/contact/" class="btn btn-primary">Contact Us</a>
</div>
</div>
</div>
</section>

<section class="cta-banner">
<div class="container">
<h2>Need help finding what you are looking for?</h2>
<p>Contact our team and we can point you in the right direction.</p>
<a href="/contact/" class="btn btn-gold">Get in Touch</a>
</div>
</section>"""

    return make_page("Page Not Found | Elixir Consulting Group", "The page you requested could not be found.", "/404", body)

print("\n[15.7/16] 404 Page")
write_page("/404.html", gen_404())

# Search page needs the final page count, so it is written last among pages.
print("\n[15.9/16] Search")
SEARCH_INDEX = gen_search_index(INDEX_POSTS, CONSULTING_PAGES)
write_page("/search/", gen_search_page(len(INDEX_POSTS), len(json.loads(SEARCH_INDEX))))

# Sitemaps, feeds, and static assets
print("\n[16/16] Sitemaps, feeds, and site assets")


def write_asset(name, content):
    path = os.path.join(SITE_DIR, name)
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(name) else None
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  Created: /{name}")


BLOG_URLS, BLOG_LASTMOD = sitemap_blog_urls(INDEX_POSTS, ACTIVE_CATEGORIES)
write_asset("sitemap-pages.xml", gen_urlset(sitemap_pages_urls()))
write_asset("sitemap-blog.xml", gen_urlset(BLOG_URLS, BLOG_LASTMOD))
write_asset("sitemap-locations.xml", gen_urlset(sitemap_location_urls(CONSULTING_PAGES)))
write_asset("sitemap.xml", gen_sitemap_index(
    ["sitemap-pages.xml", "sitemap-blog.xml", "sitemap-locations.xml"]))
write_asset("feed.xml", gen_rss(INDEX_POSTS))
write_asset("search-index.json", SEARCH_INDEX)
write_asset("site.webmanifest", gen_manifest())
write_asset("robots.txt", gen_robots())
write_asset("humans.txt", gen_humans_txt())
write_asset(".well-known/security.txt", gen_security_txt())
write_asset("vercel.json", gen_vercel_json())

# Count files
total = 0
for root, dirs, files in os.walk(SITE_DIR):
    for f in files:
        if f.endswith('.html'):
            total += 1
print(f"\n{'='*60}")
print(f"DONE! Generated {total} HTML pages + sitemap + robots.txt + vercel.json")
_sitemap_urls = sum(
    open(os.path.join(SITE_DIR, n)).read().count("<url>")
    for n in ("sitemap-pages.xml", "sitemap-blog.xml", "sitemap-locations.xml"))
print(f"  {len(ALL_POSTS)} posts, {len(ACTIVE_CATEGORIES)} category archives, "
      f"{len(INDUSTRIES)} industry pages, {len(CASE_STUDIES)} case studies, "
      f"{len(CONSULTING_PAGES)} location pages")
print(f"  {_sitemap_urls} URLs across 3 sitemaps + RSS feed + search index")
print("  Every page: Organization + WebSite + Person graph, FAQPage, BreadcrumbList,")
print("  canonical, OG/Twitter card. Posts add BlogPosting; industries add Service.")
print(f"{'='*60}")
