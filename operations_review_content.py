"""Original expense-review example for one existing operations landing page."""
import re

REVIEW = '''<section class="section" data-operations-review><div class="container" style="max-width:900px">
<span class="eyebrow">Define the review before changing spending</span><h2>Expense Optimization Consulting in Pittsburgh</h2>
<p>Start with a spending category such as software subscriptions, supplier contracts, or outsourced services. An expense review can produce a reconciled cost baseline, a renewal calendar, and a decision register showing which options save cash after transition costs. Bring a recent invoice, the current contract, and the name of the person responsible for the service to the <a href="/contact/">initial consulting discussion</a>.</p>
<p>An expense total does not identify which cost can be changed without disrupting delivery. Start with a category, the service it supports, its contract terms and the person responsible for the decision. If expense review is part of a proposed Elixir operations engagement, agree the records, analysis and implementation responsibilities in the scope before work begins.</p>
<p>Useful inputs include recent bills, payment records, contract renewal dates, approved users and service requirements. A bank withdrawal alone may combine several billing periods or services. Reconcile the billed amount, credits and actual payment before treating the current run rate as a baseline.</p>
<h3>A fictional software-renewal comparison</h3>
<p>Assume a small business pays $1,200 per month for a software package. An alternative package costs $900 per month, and a hypothetical change requires $1,800 of one-time migration work. These are invented amounts for an arithmetic example, not vendor prices, a client result or promised savings.</p>
<ul><li>Keeping the package for twelve months costs $14,400 under the stated assumption.</li><li>Twelve months of the alternative package cost $10,800. Adding $1,800 of migration work produces $12,600 of first-year modeled spending.</li><li>The difference is $1,800 in the first year. The ongoing monthly price difference is $300; $1,800 divided by $300 gives six months of simple payback.</li></ul>
<p>Those figures assume the new package starts immediately, the old one can stop without penalty and there are no additional implementation costs. If the business must keep the old package for three overlapping months, another $3,600 brings the first-year alternative total to $16,200. It would then cost $1,800 more than keeping the original package during that twelve-month window. Confirm cancellation terms before accepting an annualized price difference as available cash.</p>
<h3>Check service dependencies before choosing an option</h3>
<p>Compare essential functions, integrations, customer-facing obligations, data export and access controls. Name the person who will test each requirement. A lower subscription price does not establish that an alternative can support the workflow. If staff time, training, a setup fee or service interruption matters, add a supported estimate or leave the item visibly unresolved.</p>
<p>Keep the proposal separate from an approved action. The review owner should identify who can authorize a change, who controls cancellation and who confirms that records remain accessible. Do not cancel a tool or supplier contract merely because a spreadsheet shows a lower price.</p>
<h3>Agree what the operational handoff contains</h3>
<p>A useful proposed handoff is a category register showing the original evidence, current cost, renewal or notice date, options considered, transition costs, service dependencies and the requested decision. Ask the consultant which parts they will prepare and which need input from your finance, legal, security or operating team. Scope and specialist review depend on the actual contract and business.</p>
<p>For an approved change, record the implementation owner, cancellation confirmation and first new invoice. At the next review, compare realized bills with the documented baseline and explain changes in usage or service scope. Avoid counting a negotiated price reduction, an avoided renewal and a headcount estimate as three separate savings amounts if they describe the same underlying change.</p>
<p><a href="/services/operations/">Review the operations consulting scope</a> for process mapping, documentation and operating cadence. For the decision meeting, use <a href="/blog/the-communication-framework-that-prevents-misunderstandings-at-work/">a clear work-request handoff</a> to name the result, approver and completion evidence. Bring the review category and unresolved questions to <a href="/contact/">the initial consulting discussion</a>; the example above is not a quotation for that engagement.</p>
<p style="font-size:.9rem">Original educational review example · November 21, 2026. No client savings or average return is represented.</p>
</div></section>'''

def apply_operations_review(html):
    old = 'From manufacturing firms in the Mon Valley to professional services companies in downtown Pittsburgh, we have helped businesses across the region build the operational foundation they need to grow. Our approach is hands-on and practical, working alongside your team to build systems that fit your specific business.'
    new = 'For a Pittsburgh operations review, bring one workflow, its responsible team and the records needed to explain the current problem. Define the proposed deliverables and decision authority before comparing an implementation plan.'
    if old not in html:
        raise ValueError('Expected operations introduction missing')
    html = html.replace(old, new, 1)
    sections = list(re.finditer(r'<section\b[^>]*>[\s\S]*?</section>', html))
    selected = [m for m in sections if 'Local Expertise, Proven Results' in m[0]]
    if len(selected) != 1:
        raise ValueError('Expected one legacy operations results panel')
    m = selected[0]
    return html[:m.start()] + REVIEW + html[m.end():]
