"""Authored owner-support comparison; program facts are narrowly sourced."""
import csv
import io
import json
from html import escape
from pathlib import Path
from expansion_content import guide, p, ul, table

ROOT = Path(__file__).resolve().parent
BRIEF_ROWS = [
    ('Decision', 'Write the one decision or operating problem you need help with.'),
    ('Stage', 'State whether you are exploring ownership, starting, or running an existing business.'),
    ('Evidence', 'Name a recent, non-sensitive example and the record that explains it.'),
    ('Work needed', 'Separate advice, specialist judgment, implementation, and daily operating ownership.'),
    ('Deliverable', 'Describe the decision, record, or working change you expect to receive.'),
    ('Internal owner', 'Name the role that will approve, maintain, and review the result.'),
    ('Boundaries and fees', 'List exclusions, remaining internal work, access, availability, fees, and referrals to clarify.'),
    ('Review point', 'Set a review date and explain what evidence would change the plan.'),
]


def brief_csv():
    output = io.StringIO(newline='')
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['field', 'question_to_answer', 'your_notes'])
    for field, prompt in BRIEF_ROWS:
        writer.writerow([field, prompt, ''])
    return output.getvalue()


def business_coach_alternatives():
    source = json.loads((ROOT / 'data/commercial-sources.json').read_text())['sources']['sba-resource-partners']
    source_link = '<a href="' + source['url'] + '">SBA resource-partner guide and local assistance finder</a>'
    rows = [
        ('Experienced mentor, including SCORE', 'You need perspective on a decision and relevant operating experience', 'Check the match and agree what you will prepare and implement'),
        ('SBDC advising', 'You need business planning, advising, or technical assistance', 'Ask the local center about scope, availability, eligibility, and any fees'),
        ('Peer group', 'You need challenge and perspective from other owners', 'Clarify relevance, confidentiality, participation, and follow-through'),
        ('Specialist adviser', 'A defined technical or professional question needs qualified judgment', 'Confirm the appropriate expertise, work boundary, and written output'),
        ('Implementation consultant', 'A defined workflow must be diagnosed, built, and tested', 'Name the internal owner and agree pilot and handover evidence'),
        ('Fractional operating leader', 'The business needs recurring operating decisions owned for an agreed scope', 'Specify authority, availability, responsibilities, and continuity'),
        ('Internal operations manager', 'Daily management and ongoing team ownership belong inside the business', 'Give the role the authority, resources, and escalation path it needs'),
    ]
    sections = [
        ('Compare the work each alternative would own',
         p('Begin with the work you need done. Mentoring and peer conversations can improve a decision; a project can build a defined change; an operating role can own recurring decisions. Compare the responsibility before comparing a label or fee.')
         + '<p>Scroll the comparison horizontally on a narrow screen to read every column.</p>'
         + table('Owner-support alternatives and the responsibility to clarify', ['Alternative', 'When to consider it', 'Responsibility to resolve'], rows)),
        ('Use mentoring or advising when the decision needs development',
         p('The SBA describes SCORE mentoring at no cost and lists SBDC advising for current and prospective owners. Use its local finder to ask about the available match and scope. A mentoring conversation, a training session, and an implementation engagement are different commitments.')
         + '<p>Start with the ' + source_link + '. Bring one decision, the assumptions behind it, and the evidence you already have. Ask what you should prepare, what the adviser will help you examine, and what you will still need to carry out yourself.</p>'
         + p('For an ownership decision, separate exploring a business model from evaluating a particular transaction. General business support does not replace the qualified financial, legal, or other specialist work appropriate to the actual decision. Keep unresolved questions visible rather than treating a referral or introductory conversation as approval.')),
        ('Turn an implementation need into a testable brief',
         p('Illustrative example: an owner receives useful guidance about delegation but the team still lacks an agreed customer-credit limit. A short decision-rights project can turn the intent into a rule the manager can use. This is a fictional operating example, not a reported client result.')
         + p('The brief should identify who approves the rule, what information the manager checks, which exceptions return to the owner, and where the decision is recorded. The implementation provider can help design and test that workflow; the business still names the person responsible for using and maintaining it.')
         + ul(['Trace a routine request and an exception through the proposed rule.', 'Have the intended manager explain the decision and escalation without relying on the owner’s memory.', 'Keep the approved rule, open issues, handover owner, and next review together.'])
         + p('If the unresolved problem is the owner’s willingness to delegate rather than the missing rule, coaching may still be useful. The conversation and the workflow project can complement each other when their responsibilities are explicit.')),
        ('Separate a defined project from recurring operating leadership',
         p('An implementation project has a work boundary: an agreed process, configuration, pilot, or handover. Daily management involves repeated decisions, supervision, capacity tradeoffs, and exceptions after the project ends. Buying a project does not automatically assign those continuing responsibilities.')
         + p('A fractional role may provide recurring leadership for an agreed scope and availability. An internal manager may provide ongoing ownership inside the team. In either case, document decision rights, access, escalation, coverage, and the counterpart inside the business. A role title alone does not establish the authority or hours available.')
         + p('Bring a recent missed handoff to the discussion. Ask who would make the next decision, who would do the work, and who would remain accountable once the outside engagement finishes. If those answers point to different roles, sequence the support rather than expecting one label to cover everything.')),
        ('Ask every provider the same commitment questions',
         ul(['What exact decision or work package will this engagement address?', 'What will you deliver, and what must our team still do?', 'Who approves changes and owns the result inside the business?', 'What relevant experience, qualifications, availability, and access does the work require?', 'What is excluded, how are fees determined, and what could change the scope?', 'How will we check progress, handle an exception, and decide whether to continue?'])
         + p('Keep advice, implementation, and operating capacity visible when comparing costs. A lower fee may cover a smaller commitment; a larger fee does not by itself establish a better fit. Ask for the written work boundary and compare your remaining responsibilities as well as the outside price.')),
        ('Prepare a one-page owner-support brief',
         p('Write one problem in plain language, attach a non-sensitive example, and state the next decision you need. Identify the expected output and the person who will maintain it. This turns an open-ended request for help into a conversation the provider can respond to concretely.')
         + '<p><a href="/downloads/owner-support-brief.csv" download>Download the owner-support brief CSV</a>. Its eight prompts are blank planning fields, not client information or a provider score. Keep private records in an appropriate restricted file and use references in the shared brief.</p>'
         + p('Review the brief after the first agreed checkpoint. If new evidence shows that the problem is different, revise the work and preserve the reason. A decision to use mentoring, a specialist, or an internal role can be the appropriate outcome even when no implementation engagement follows.')),
        ('Sources and editorial scope',
         p('Program information checked on ' + source['checked_on'] + '. The SBA source describes its resource partners. The fit questions and fictional example are Elixir’s editorial analysis, not program eligibility decisions or evidence of provider performance.')
         + '<p>' + source_link + '.</p>'
         + p('Elixir Consulting Group publishes this guide and offers paid implementation consulting. Confirm the actual provider, local availability, work scope, and fees directly before making a commitment.')),
    ]
    page = guide('business-coaching', 'Business Ownership Coach Alternatives',
                 'Compare a business coach, operations consultant and fractional COO by what each delivers, who implements the work and when each option fits.',
                 'If you need perspective, compare mentoring, business advising, or peers. If you need a workflow built or recurring decisions owned, compare implementation and operating leadership. Use a specialist for a defined technical question.',
                 sections, ['/compare/operations-consultant-vs-business-coach/', '/services/leadership/', '/lists/questions-before-hiring-operations-consultant/', '/alternatives/full-time-coo/'], 'Alternatives', '/alternatives/')
    page.update(seo_title='Business Ownership Coach Alternatives: Coach, Consultant or Fractional COO?',
                sources=['sba-resource-partners'], source_checked_on=source['checked_on'],
                modified='2026-11-21', revision_date='2026-11-21', exclude_toc_from_snippets=True)
    return page
