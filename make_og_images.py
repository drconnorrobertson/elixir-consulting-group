#!/usr/bin/env python3
"""Generate per-page Open Graph cards for the site's evergreen pages.

Blog posts use their own article artwork, so this covers everything else:
the homepage, services, industries, case studies, and the top-level location
pages. Run it after adding a page; generate_site.py points a page at
/images/og/<slug>.png automatically when the file exists.
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageChops

W, H = 1200, 630
NAVY = (0, 46, 91)
NAVY_D = (0, 31, 63)
GOLD = (201, 168, 76)
WHITE = (255, 255, 255)
MUTED = (226, 233, 241)

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "og")

FONT_PATHS_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]
FONT_PATHS_REG = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def font(size, bold=True):
    for path in (FONT_PATHS_BOLD if bold else FONT_PATHS_REG):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def base_canvas():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        draw.line(
            [(0, y), (W, y)],
            fill=(
                int(NAVY[0] + (NAVY_D[0] - NAVY[0]) * t),
                int(NAVY[1] + (NAVY_D[1] - NAVY[1]) * t),
                int(NAVY[2] + (NAVY_D[2] - NAVY[2]) * t),
            ),
        )
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(60, 0, -1):
        rad = i * 9
        a = int(2.2 * (60 - i) / 60 * 10)
        gd.ellipse([W - 200 - rad, -200 - rad, W - 200 + rad, -200 + rad],
                   fill=(a, int(a * .83), int(a * .37)))
    return ImageChops.add(img, glow)


def card(slug, eyebrow, title, subtitle, headshot=None):
    img = base_canvas()
    d = ImageDraw.Draw(img)

    d.text((80, 74), "ELIXIR CONSULTING GROUP", font=font(26), fill=GOLD)
    d.line([(82, 118), (400, 118)], fill=GOLD, width=3)

    y = 168
    if eyebrow:
        d.text((80, y), eyebrow.upper(), font=font(24), fill=(150, 176, 204))
        y += 46

    title_font = font(64)
    lines = wrap(d, title, title_font, W - 200)
    if len(lines) > 3:
        title_font = font(52)
        lines = wrap(d, title, title_font, W - 200)[:4]
    for line in lines:
        d.text((80, y), line, font=title_font, fill=WHITE)
        y += title_font.size + 12

    if subtitle:
        y += 14
        sub_font = font(30, bold=False)
        # Keep the subtitle clear of the headshot medallion when one is drawn.
        sub_width = (W - 480) if headshot else (W - 220)
        for line in wrap(d, subtitle, sub_font, sub_width)[:3]:
            d.text((80, y), line, font=sub_font, fill=MUTED)
            y += sub_font.size + 10

    d.text((80, H - 92), "elixirconsultinggroup.com", font=font(26), fill=GOLD)
    d.text((80, H - 56), "Pittsburgh, PA  |  (412) 387-7656", font=font(24, bold=False),
           fill=(168, 190, 214))

    if headshot and os.path.exists(headshot):
        size = 180
        hs = Image.open(headshot).convert("RGB").resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
        ring = Image.new("RGB", (size + 12, size + 12), GOLD)
        rmask = Image.new("L", (size + 12, size + 12), 0)
        ImageDraw.Draw(rmask).ellipse([0, 0, size + 11, size + 11], fill=255)
        img.paste(ring, (W - size - 110, H - size - 130), rmask)
        img.paste(hs, (W - size - 104, H - size - 124), mask)

    d.rectangle([0, H - 10, W, H], fill=GOLD)

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{slug}.png")
    img.save(path, optimize=True)
    return path


CARDS = [
    ("home", "Business Consulting", "Build Structure That Scales Your Business",
     "Operations, sales systems, and leadership cadence for owner-led companies."),
    ("about", "Founder", "Dr. Connor Robertson",
     "Founder and lead consultant. Implementation, not recommendations."),
    ("process", "How We Work", "Five Phases, One Method",
     "Consult, assessment, design, implementation, handover."),
    ("services", "Services", "Five Ways We Install Structure",
     "Strategy, AI, operations, sales, and leadership consulting."),
    ("services-business-strategy", "Service", "Business Strategy Consulting",
     "Growth roadmaps and execution frameworks tied to weekly action."),
    ("services-ai-consulting", "Service", "AI Consulting & Digital Transformation",
     "Practical AI adoption that improves efficiency without disruption."),
    ("services-operations", "Service", "Operations Consulting",
     "Process, SOPs, role clarity, and weekly operating cadence."),
    ("services-sales-strategy", "Service", "Sales Strategy & Revenue Systems",
     "Pipeline structure and follow-up your team can run consistently."),
    ("services-leadership", "Service", "Leadership Consulting & Coaching",
     "Cadence, scorecards, and accountability that produce decisions."),
    ("industries", "Industries", "Eight Sectors We Know Well",
     "The constraints are structural. The context is not."),
    ("case-studies", "Case Studies", "What Actually Changed",
     "Four engagements documented end to end, with the numbers."),
    ("blog", "Insights", "Articles for Business Owners",
     "Strategy, operations, AI adoption, sales, and leadership."),
    ("contact", "Contact", "Book a Consult",
     "No cost, no obligation. An honest read on whether we are a fit."),
    ("faq", "FAQ", "Questions Owners Ask First",
     "Pricing, process, engagement length, and what the work involves."),
    ("testimonials", "Social Proof", "What Clients Say",
     "Owners on what changed after the systems went in."),
    ("consulting", "Locations", "Pittsburgh Based, Nationwide Reach",
     "Regional market context across every area we serve."),
    ("search", "Search", "Find Anything on the Site",
     "Articles, services, industries, case studies, and locations."),
]

INDUSTRY_CARDS = [
    ("professional-services", "Professional Services"),
    ("construction-trades", "Construction & Trades"),
    ("healthcare", "Healthcare"),
    ("manufacturing", "Manufacturing"),
    ("technology", "Technology"),
    ("real-estate", "Real Estate"),
    ("retail-ecommerce", "Retail & E-Commerce"),
    ("financial-services", "Financial Services"),
]

CASE_CARDS = [
    ("manufacturing-delivery-delays", "Manufacturing", "Delivery Delays Down 40%"),
    ("professional-services-close-rate", "Professional Services", "Close Rate Doubled"),
    ("construction-operating-cadence", "Construction", "Operating Cadence Installed"),
    ("healthcare-patient-operations", "Healthcare", "Patient Operations Streamlined"),
]

LOCATION_CARDS = [
    ("pittsburgh-business-consultant", "Pittsburgh, PA", "Business Consultant"),
    ("pittsburgh-ai-consulting", "Pittsburgh, PA", "AI Consulting"),
    ("pittsburgh-operations-consulting", "Pittsburgh, PA", "Operations Consulting"),
    ("cranberry-township-business-consultant", "Cranberry Township, PA", "Business Consultant"),
    ("wexford-business-consultant", "Wexford, PA", "Business Consultant"),
]


def main():
    headshot = os.path.join(os.path.dirname(OUT_DIR), "dr-connor-robertson.jpg")
    count = 0
    for slug, eyebrow, title, subtitle in CARDS:
        card(slug, eyebrow, title, subtitle,
             headshot=headshot if slug in ("about", "home", "blog") else None)
        count += 1
    for slug, name in INDUSTRY_CARDS:
        card(f"industries-{slug}", "Industry", f"{name} Consulting",
             "Operations, sales, and leadership systems built for your sector.")
        count += 1
    for slug, industry, headline in CASE_CARDS:
        card(f"case-studies-{slug}", f"{industry} Case Study", headline,
             "What was broken, what we built, and what changed.")
        count += 1
    for slug, city, kind in LOCATION_CARDS:
        card(slug, city, kind,
             "Implementation-focused consulting for owner-led businesses.")
        count += 1
    print(f"Generated {count} Open Graph cards in images/og/")


if __name__ == "__main__":
    main()
