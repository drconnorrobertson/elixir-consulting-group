"""Operational playbooks with worked examples and explicit acceptance checks."""
from html import escape

TOPICS = [
    (
        "vendor-renewal-calendar", "Vendor Renewal Calendar for Small Businesses",
        "Build a vendor renewal calendar that gives owners time to review spending, test alternatives, and act before notice deadlines.",
        "A useful calendar tells the team when a decision is due and which contract establishes that date. Start with recurring spend the business cannot easily pause.",
        "Record the legal vendor name, service owner, agreement version, end date, cancellation instructions, and evidence of delivery. Add an internal review date early enough for procurement and service testing. Keep unknown deadlines visibly unresolved.",
        "A fictional software contract ends June 30 and requires notice 60 days before expiry. The team starts in March to allow time to test exports and approve a replacement. The owner checks how the contract counts days and confirms the notice method before scheduling delivery.",
        "Choose three agreements. Ask a backup owner to locate each deadline in the signed record and explain what action keeps the business from renewing by default.",
        "/pittsburgh-operations-consulting/", "/playbooks/subscription-seat-audit/",
    ),
    (
        "subscription-seat-audit", "Software Subscription Seat Audit Playbook",
        "Reconcile paid software seats to assigned users and actual use before removing access or changing subscription quantities.",
        "Paid seats, assigned seats, and active users answer different questions. Export each count for the same billing period and reconcile by license type before deciding what to remove.",
        "Label active roles, pending departures, shared service accounts, and reserved seasonal seats separately. Ask department owners to confirm unusual access. Check whether reductions take effect immediately or only at renewal.",
        "A fictional company pays for 60 seats. It finds 49 assigned, of which 4 belong to departed employees and 3 support scheduled integrations. The owner verifies the integrations, removes the former employees through the normal offboarding process, and checks the next contract opportunity to lower the paid quantity.",
        "Compare the next invoice with the approved change. Ask the application owner to verify that essential service accounts and access to exported records still work.",
        "/pittsburgh-operations-consulting/", "/playbooks/vendor-renewal-calendar/",
    ),
    (
        "supplier-bid-comparison", "Supplier Bid Comparison for Operating Teams",
        "Compare supplier bids using landed cost, delivery reliability, service requirements, and an explicit trial plan.",
        "Write a common order profile before asking for quotes. Compare the same quantities, delivery location, packaging, payment terms, and minimum service level.",
        "Record unit price, freight, duties where applicable, minimum quantities, payment timing, defects and credits, and the cost of carrying surplus stock. Give delivery and quality their own acceptance criteria.",
        "A fictional supplier quotes $9 a unit for orders of 500 and $400 freight. Another quotes $10 for 200 units with no freight. The first quote lands at $9.80 per unit before storage, but ties up $4,900 on the first order. The second requires $2,000 and can suit a trial with uncertain demand.",
        "Give purchasing a sample order to place and receiving a checklist to complete. Verify invoice, quality, delivery date, and escalation contact before switching regular volume.",
        "/services/operations/", "/playbooks/vendor-renewal-calendar/",
    ),
    (
        "service-backlog-triage", "Service Backlog Triage Playbook",
        "Triage a service backlog by age, customer commitment, and blocked work using a daily queue and recovery plan.",
        "Export open items at a fixed time. Capture the original receipt date, promised date, next action, and blocker so reassigning an item preserves its history.",
        "Group work by decisions the team can act on today. Assign one owner to release each blocker. Escalate commitments at risk and tell the customer when they can expect a meaningful update.",
        "A fictional team has 50 open jobs. Twelve lack customer approval and five are due tomorrow. The supervisor assigns one person to contact the 12 customers and reserves field capacity for the five jobs with complete inputs.",
        "During the next huddle, check whether the oldest open work is getting younger and whether overdue commitments fell without hiding items in a waiting status.",
        "/services/operations/", "/playbooks/weekly-commitment-review/",
    ),
    (
        "weekly-commitment-review", "Weekly Commitment Review for Leadership Teams",
        "Run a leadership meeting around operating commitments, evidence of completion, and decisions required this week.",
        "Bring the prior week's commitments and the decisions the team needs now. Each commitment has a named owner, due date, and observable finish condition.",
        "Separate a missed deliverable from a changed priority. Ask what blocked completion, who can clear it, and whether the existing promise should be renegotiated. Update the original record.",
        "A fictional team promises to reduce open quotes older than five days. When the review shows most quotes are waiting on a single approval, the team assigns a backup approver and sets a threshold for quotes that can go out without escalation.",
        "A person absent from the meeting should be able to tell what was decided, what evidence will demonstrate completion, and when to raise a blocker.",
        "/services/leadership/", "/playbooks/service-backlog-triage/",
    ),
    (
        "customer-onboarding-handoff", "Sales-to-Delivery Customer Onboarding Handoff",
        "Transfer scope, commitments, customer context, and exceptions from sales to delivery with an acceptance checklist.",
        "Start with what the customer actually approved. Give delivery a short handoff that points to the authorized scope, owner, kickoff date, and unresolved decisions.",
        "Ask delivery to accept or return the handoff. Required fields include buying reason, approved deliverables, exclusions, promised timing, customer contacts, dependencies, and exceptions that still need approval.",
        "A fictional proposal promises a report during the first month while the kickoff notes say weekly dashboards. Delivery flags the conflict before kickoff and the account owner confirms what was actually agreed with the customer.",
        "Review the first five transfers. Track missing fields and scope clarifications discovered after kickoff. Assign a person to update the originating sales process when the same gap repeats.",
        "/services/sales-strategy/", "/playbooks/founder-sales-handoff/",
    ),
    (
        "operating-metric-definitions", "Operating Metrics Dictionary for Small Teams",
        "Define operating metrics so leaders can reconcile a scorecard to source records and act on changes consistently.",
        "Document the decision each metric helps someone make. Put the formula, timing, population, exclusions, source, and owner next to the metric name.",
        "Choose a sample date range and recalculate the result from records. Include boundary cases such as cancellations, reopened tickets, or late data. State how corrections affect prior reports.",
        "A fictional support team defines first response as the first reply from a person during published support hours. An automatic receipt therefore contributes no response time measurement. A ticket reopened next week stays part of the original cohort.",
        "Ask a second analyst to calculate the number independently using the written definition. Resolve differences before publishing the metric in the weekly meeting.",
        "/services/leadership/", "/playbooks/weekly-commitment-review/",
    ),
    (
        "process-exception-register", "Process Exception Register for Small Businesses",
        "Create an exception register for refunds, delivery promises, approvals, and process failures that need a clear decision.",
        "Define which deviations operators can resolve under existing policy and which need review. Give staff one place to record a decision request and its supporting evidence.",
        "Capture the rule affected, impact, options, owner, and decision deadline. Keep a reusable decision trail. Review repeated exceptions to see when a rule, system field, or training step needs revision.",
        "A fictional field team repeatedly waives a return visit charge when a scheduling error causes the issue. The manager compares the jobs, confirms the policy boundary, and adjusts scheduling instructions to prevent repeat disputes.",
        "Sample a closed exception. The team should be able to explain the authority used, the evidence reviewed, how the customer was informed, and what would prevent recurrence.",
        "/services/operations/", "/playbooks/weekly-commitment-review/",
    ),
    (
        "route-density-planning", "Route Density Planning for Field Service Teams",
        "Improve field service route density by grouping compatible jobs around drive time, crew skills, and customer windows.",
        "Separate travel, on-site work, and uncertainty. Begin with completed routes from a representative week and use real arrival times when available.",
        "Group nearby jobs that require comparable skills, equipment, and service windows. Reserve time for variable work and confirm which visits can move without affecting a customer commitment.",
        "A fictional crew completes three 60-minute visits and spends 90 minutes driving. Clustering the visits reduces travel to 45 minutes. The team uses the recovered time as a buffer until it can demonstrate a reliable fourth appointment.",
        "Pilot one route on two comparable days. Compare on-time arrival and completed work alongside travel time so route savings reflect service results.",
        "/industries/construction-trades/", "/playbooks/service-backlog-triage/",
    ),
    (
        "month-end-operations-review", "Month-End Operations Review Playbook",
        "Review volume, capacity, recurring costs, and missed commitments with an action log that carries into the next month.",
        "Plan the review around decisions. Give finance and operations one time window, definitions, and a short list of areas where results changed.",
        "Reconcile volume and margin where data supports it, identify constraints, and choose the next action at the level the team can control. Record unresolved data differences separately from decisions.",
        "A fictional service team notices overtime alongside flat completed jobs. A closer review shows repeat visits from missing first-visit equipment. The team tests a dispatch checklist for one work type before changing staffing.",
        "At the next review, ask which action changed the result and inspect a sample of underlying records. Reopen a decision when a key assumption proves wrong.",
        "/services/operations/", "/playbooks/operating-metric-definitions/",
    ),
]
TOPICS.extend([
    (
        "vendor-invoice-variance-review", "Vendor Invoice Variance Review Playbook",
        "Trace unexplained changes in vendor invoices to quantities, contract rates, fees, and one-time charges.",
        "Review invoices against the purchase order and effective rate schedule. Preserve the version that applied on the service date.",
        "Build a variance bridge. Calculate the impact of quantities at the old rate, then the impact of any rate changes at the new quantities. Separate credits, taxes, and new fees.",
        "A vendor billed 240 units at $11 instead of 200 at $10. The $640 increase consists of $400 for additional volume and $240 in rate variance. Check which units were accepted and which notice authorized the rate.",
        "Ask an approver to reproduce the calculation and trace each disputed line to the supporting record. Verify any agreed credit against the next statement.",
        "/pittsburgh-operations-consulting/", "/playbooks/vendor-renewal-calendar/",
    ),
    (
        "field-service-first-visit-completion", "First-Visit Completion Playbook for Field Service",
        "Improve first-visit completion by identifying missing parts, site information, and approval before dispatch.",
        "Define first-visit completion against the originally promised scope. Track planned multi-visit work separately so routine project stages do not distort the result.",
        "Sample recent returns and assign each a primary cause. For missing parts, compare job category and equipment model with the van stock list. For access failures, confirm the site contact and entry window before dispatch.",
        "A fictional team completes 72 of 90 eligible jobs on the first visit. Six of the 18 returns involve an unverified equipment model. Test a dispatch field requiring model identification on that job type before changing stock across the whole fleet.",
        "Recheck first-visit completion with the same denominator and measure the time added to dispatch. Confirm that jobs still complete safely within the promised scope.",
        "/industries/construction-trades/", "/playbooks/route-density-planning/",
    ),
    (
        "quote-approval-delegation", "Quote Approval and Delegation Playbook",
        "Give sales staff clear quote authority and route unusual price, scope, or contract terms to the right approver.",
        "Map offers the team can quote routinely and the exceptions that need a decision. Use observed cases to define approval boundaries.",
        "Record the proposed price, estimated direct costs, terms, reason for exception, and decision deadline. Assign authority by margin and nonstandard commitments as well as total price.",
        "A fictional $8,000 quote carries $6,400 in direct costs, leaving a 20% contribution margin before overhead. The standard floor is 25%. The approver can revise scope, change price, or document a specific reason for accepting the exception.",
        "Sample approved quotes after handoff. Compare approval time and margin to baseline and confirm delivery received the same scope the customer accepted.",
        "/services/sales-strategy/", "/playbooks/customer-onboarding-handoff/",
    ),
    (
        "customer-complaint-escalation-matrix", "Customer Complaint Escalation Matrix Playbook",
        "Route customer complaints by impact and authority with concrete response owners, next actions, and closure evidence.",
        "Identify the complaints that front-line staff can resolve using existing policy and those that need a duty manager or specialist.",
        "For each severity band, specify acknowledgement expectation, required details, decision authority, escalation path, and which promises can be made before review. Give staff a backup contact.",
        "A fictional customer receives the wrong part and faces an installation delay. The representative verifies the order, reserves a correct part, and escalates the requested reimbursement because it exceeds their authority.",
        "Walk a simulated routine complaint and an urgent one through the matrix. Check that the customer receives one consistent status and that the team can explain who owns follow-up.",
        "/services/operations/", "/playbooks/process-exception-register/",
    ),
    (
        "shift-handoff-log", "Shift Handoff Log for Service and Operations Teams",
        "Pass open work, changes, blocked jobs, and urgent decisions between shifts using an auditable handoff log.",
        "Build the handoff around the work the next shift must pick up. Separate immediate action from useful context and identify the owner of each item.",
        "Record the work reference, current condition, next check, deadline, and escalation contact. Keep the log with the system of record, or link back to it, so updates are visible to both shifts.",
        "A fictional dispatch team has a truck waiting on a part with a 9 a.m. delivery promise. The departing lead lists the vendor confirmation, the backup stock location, and the time to update the customer if the part is late.",
        "Ask the incoming lead to identify the first three actions without calling the outgoing lead. Review missed handoffs for incomplete inputs and unclear ownership.",
        "/services/operations/", "/playbooks/service-backlog-triage/",
    ),
    (
        "manual-report-retirement", "Manual Report Retirement Playbook",
        "Identify duplicate reports, test their replacements, and retire spreadsheets without losing operating decisions or audit history.",
        "Inventory each report’s actual readers, the decision it supports, calculation owner, source files, and deadlines. Find hand-edited fields before comparing replacements.",
        "Run the replacement alongside the current report for a representative cycle. Explain differences by definition, data freshness, or calculation. Keep a documented rollback option and follow the applicable retention process.",
        "A fictional sales report counts repeat buyers only after a second completed invoice, while the new dashboard counts a second order. The team confirms the original metric supports collection analysis and revises the dashboard definition before retirement.",
        "Ask readers to reproduce a recent decision with the replacement. After switching, confirm that the data owner can retrieve the last approved version and correct a source error.",
        "/services/operations/", "/playbooks/operating-metric-definitions/",
    ),
])


TOPICS.extend([('purchase-order-three-way-match',
  'Three-Way Purchase Order Matching Playbook',
  'Set up a three-way match for purchase orders, receipts, and invoices.',
  'A three-way match connects what the company ordered, what it accepted, and what the vendor billed.',
  'Give each discrepancy an owner. Compare line identifiers, agreed prices, accepted quantities, and '
  'approved adjustments. Keep partial receipts open through the next delivery.',
  'An order for 100 units at $12 yields an accepted receipt of 90. An invoice for $1,200 exceeds accepted '
  'goods by $120. The buyer records the 10-unit variance and asks the supplier for the missing shipment or a '
  'corrected invoice.',
  'Trace one closed variance through the receipt, approval and vendor statement before expanding the '
  'workflow.',
  '/services/operations/',
  '/playbooks/vendor-invoice-variance-review/'),
 ('minimum-stock-reorder-point',
  'Minimum Stock and Reorder Point Playbook',
  'Calculate a practical reorder point from demand, replenishment time, and an explicit buffer.',
  'A reorder point tells the team when to act. Use actual consumption and replenishment time for the item '
  'being ordered.',
  'Collect daily demand and lead times from completed orders. State how open purchase orders and allocated '
  'units affect available inventory. Review items with unusual lead times separately.',
  'A team uses eight units per day and normally waits six days for delivery. With a 16-unit buffer, its '
  'starting reorder point is 64 units. Test a late delivery and check whether existing inbound stock changes '
  'the decision.',
  'Pilot the rule on one product family and review stockouts and excess holdings together.',
  '/services/operations/',
  '/playbooks/supplier-bid-comparison/'),
 ('sales-discount-review',
  'Sales Discount Review and Margin Playbook',
  'Review discounts against contribution, volume assumptions, and concessions before approving sales terms.',
  'Review the economics of the proposed transaction using a common cost and scope baseline.',
  'Capture the discount type, list amount, approved scope, direct costs, volume assumptions, expiry date and '
  'renewal treatment. Include concessions such as free setup or accelerated delivery.',
  'A $10,000 sale with $6,000 in direct costs yields $4,000 of contribution. A 15% discount reduces '
  'contribution to $2,500, a decline of 37.5%. Compare this change with any supportable increase in sold '
  'volume.',
  'Check a sample of closed deals for realized price, direct cost and undocumented concessions.',
  '/services/sales-strategy/',
  '/playbooks/quote-approval-delegation/'),
 ('rush-order-intake',
  'Rush Order Intake and Capacity Playbook',
  'Protect existing delivery commitments when urgent orders compete for constrained capacity.',
  'Define who can promise a rush date and which resource must be checked before agreeing to it.',
  'Record the requested date, required work, bottleneck hours, inputs still missing, and scheduled jobs that '
  'would move. Communicate revised expectations to affected customers through the account owner.',
  'An urgent job requires three hours on a workstation with two hours free. The scheduler offers a '
  'next-morning slot or obtains explicit approval to move an existing one-hour job.',
  'Audit promised versus actual delivery and check whether any displaced commitments went uncommunicated.',
  '/services/operations/',
  '/playbooks/service-backlog-triage/'),
 ('renewal-risk-sales-handoff',
  'Customer Renewal Risk Handoff Playbook',
  'Surface contract dates, service gaps, and decision owners before an account renewal reaches escalation.',
  'Start with the customer outcome expected under the agreement and the most recent evidence of delivery.',
  'Build a handoff with notice date, decision maker, open support cases, promised milestones, commercial '
  'concessions, and the next conversation. Assign delivery and account owners separately.',
  'A customer is 45 days from renewal and its last two service reports disagree about response time. '
  'Delivery reconciles the reporting data while the account owner schedules a review before internal pricing '
  'is approved.',
  'Check whether the account plan identifies the unresolved decision and the owner can still act before the '
  'contractual deadline.',
  '/services/sales-strategy/',
  '/playbooks/customer-onboarding-handoff/'),
 ('workflow-pilot-rollback',
  'Workflow Pilot Rollback Plan',
  'Prepare reversible workflow changes with stop conditions, clean handbacks, and evidence for restarting.',
  'Design the fallback while the team still has the old workflow and access to its records.',
  'Write the decision owner, stop threshold, record reconciliation method, communication tree and restart '
  'checks. Select one point at which work switches sources to avoid conflicting updates.',
  'A scheduling pilot misroutes two appointments. The lead stops intake to the pilot, reconciles open work '
  'against the dispatch queue, and asks account owners to confirm affected appointments before resuming the '
  'old process.',
  'Run a rehearsal using sample records and confirm that an incoming operator can reconcile in-flight work '
  'without guesswork.',
  '/services/operations/',
  '/playbooks/shift-handoff-log/')])

TOPICS.extend([('overtime-approval-capacity',
  'Overtime Approval and Capacity Playbook',
  'Review overtime requests against the work due, staffing capacity, and causes of repeat overtime.',
  'Start with the work that must be completed, the hours needed at the constraint, and the latest acceptable '
  'delivery time.',
  'Create a request with work reference, estimated regular and overtime hours, remaining alternatives, '
  'supervisor approval, and a plan for communicating any delivery changes. Log the actual hours and cause '
  'afterward.',
  'A team needs 20 hours for priority jobs with 16 regular hours left. Two hours can move to the next shift '
  'with no impact. Approve the remaining two hours if coverage and workload permit, and confirm the jobs '
  'completed against the promise.',
  'Review repeated reasons separately from one-off absences. Compare overtime and completion rates on the '
  'same job mix to see whether the change improved delivery.',
  '/services/operations/',
  '/playbooks/rush-order-intake/'),
 ('returns-disposition-workflow',
  'Returns Disposition Workflow for Small Businesses',
  'Route returned inventory through inspection, refund, restocking, refurbishment, or disposal with '
  'traceable records.',
  'Give each return one reference tied to the original order. Record the reason, condition, and customer '
  'commitment independently.',
  'Use an inspection checklist and an approved disposition rule. Require separate approval for disposition '
  'beyond frontline authority and keep inventory movements synchronized with the financial credit.',
  'A warehouse receives 12 returned units. Seven are unopened and eligible for restock, three need testing, '
  'and two are damaged. Record inspections by unit or lot so the stock count and customer credit each '
  'reconcile without putting damaged items back into available stock.',
  'Sample five closed returns and compare the original sale, receipt, disposition, inventory movement, and '
  'credit. Investigate mismatches before changing the rule.',
  '/services/operations/',
  '/playbooks/customer-complaint-escalation-matrix/'),
 ('service-territory-boundary-review',
  'Field Service Territory Boundary Review',
  'Redraw a service territory using actual travel times, job density, skill coverage, and customer '
  'commitments.',
  'Collect a representative set of completed jobs and flag time windows, equipment, and skills required at '
  'each stop.',
  'Compare existing and proposed boundaries using the same job list. Calculate travel minutes per completed '
  'job, verify coverage at the boundary, and identify unusually long drives that need a special rule.',
  'A team is considering moving eight weekly jobs between territories. The receiving territory saves 120 '
  'minutes of travel but needs a licensed worker for three of the jobs. Test routing only on days with the '
  'relevant skill available.',
  'Check travel, missed windows, and jobs deferred during a short pilot. Retain the old assignment as a '
  'fallback and document which boundary exception caused trouble.',
  '/industries/construction-trades/',
  '/playbooks/route-density-planning/'),
 ('job-closeout-completeness',
  'Job Closeout Completeness Checklist',
  'Prevent delayed invoicing and callbacks by checking evidence, changes, and follow-up at job closeout.',
  'Choose the evidence required to mark work complete, such as customer acceptance, service notes, approved '
  'changes, or part serial numbers.',
  'Have the crew submit a closeout record with job scope, work performed, exceptions, required approvals, '
  'and records needed by billing. Give billing a way to return incomplete closeouts with a reason.',
  'A crew finishes an installation but the client verbally requested an added unit. Billing pauses the '
  'additional charge until the account owner checks the approved scope and flags the extra unit for a '
  'documented resolution.',
  'Sample closed jobs from the field log through billing. Compare days to invoice and late scope corrections '
  'to the starting baseline.',
  '/services/operations/',
  '/playbooks/customer-onboarding-handoff/')])

TOPICS.extend([('service-callback-root-cause',
  'Service Callback Root Cause Review',
  'Separate repeat visits caused by workmanship, missing inputs, and changes in customer scope.',
  'Define a callback by linking the second visit to the original ticket and classifying the reason after '
  'evidence review.',
  'Compare work notes, dispatch instructions, parts used, and customer acceptance. Choose a single corrective '
  'action for the most frequent preventable category while retaining secondary causes.',
  'A fictional team reviews 20 callbacks. Eight concern the same fitting, six are new requests and six involve '
  'other issues. Inspect the installation steps and receipt lots for the eight before deciding whether '
  'training or part selection needs to change.',
  'Track the corrected category for the same job types over the next cycle and check that operators still '
  'record returns consistently.',
  '/services/operations/',
  '/playbooks/field-service-first-visit-completion/'),
 ('capacity-buffer-for-emergency-work',
  'Capacity Buffer for Emergency Service Work',
  'Size a dispatch capacity buffer using actual urgent job volume and response commitments.',
  'Start with historic urgent arrivals by shift and the actual hours they required from the constrained crew.',
  'Compare weeks by day and time. Reserve capacity where urgent demand appears, assign authority to release '
  'unused time, and define which regular work can move without breaching a promise.',
  'A fictional crew averages four urgent hours on Mondays across six weeks, with nine in one outlier. The team '
  'reserves four hours and agrees which backup crew or flexible jobs cover the remaining peak exposure.',
  'Review how often the buffer was used, how many emergency commitments were missed, and what regular work was '
  'displaced.',
  '/services/operations/',
  '/playbooks/rush-order-intake/'),
 ('supplier-on-time-in-full-scorecard',
  'Supplier On-Time In-Full Scorecard',
  'Score delivery against agreed dates and accepted quantities using an auditable supplier performance '
  'measure.',
  'Measure at the order line or purchase order level consistently. Use the committed date recorded before the '
  'delivery period and document how revised commitments are handled.',
  'Record ordered and accepted quantity, delivery time, quality holds, and exceptions. Flag whether split '
  'shipments satisfy the original commitment and decide how to treat approved early deliveries.',
  'Of 30 fictional orders, 25 arrive on time and in full. Three arrive on time but short, and two arrive late. '
  'The combined measure is 83.3%. Review the shortage and lateness reasons separately before choosing a '
  'supplier action.',
  'Ask purchasing and receiving to score the same orders independently. Resolve conflicting date and quantity '
  'interpretations before issuing the scorecard.',
  '/services/operations/',
  '/playbooks/purchase-order-three-way-match/'),
 ('recurring-meeting-consolidation',
  'Recurring Meeting Consolidation Playbook',
  'Reduce duplicate operating meetings while preserving the decisions, escalation routes, and records teams '
  'rely on.',
  'Inventory standing meetings and write down the recurring decision or commitment each meeting produces.',
  'Map overlapping decisions and separate status updates that can be handled in the existing work record. '
  'Establish the owner, schedule and handoff for every decision that moves.',
  'Two fictional meetings review service backlog on adjacent days using different reports. The leads adopt one '
  'shared queue, move staffing decisions into one review, and keep an urgent route for commitments at risk the '
  'same day.',
  'After three weeks, sample past decisions and check whether the replacement still captures who decided, '
  'which evidence they used, and who executes the result.',
  '/services/leadership/',
  '/playbooks/weekly-commitment-review/')])

TOPICS.extend([('dispatch-cancellation-recovery',
  'Dispatch Cancellation Recovery Playbook',
  'Recover field-service capacity after a cancellation without breaking promised windows or sending an '
  'unprepared crew.',
  'Create a short list of customer-approved openings and jobs that can move on short notice. Keep the '
  "customer's preferred contact method and the time by which the offer expires.",
  'Screen replacement jobs by travel distance, part availability, crew skills, and promised window. Confirm '
  'the new booking before changing the route. Retain the original cancellation reason for trend reporting.',
  'A technician frees a 90-minute slot. A 45-minute inspection nearby requires 20 minutes of round-trip '
  'travel and has a confirmed customer window. A 60-minute repair needs a part held across town. Schedule '
  'the inspection and leave a buffer for the next job.',
  'Compare recovered billable hours, customer acceptance, and any missed promises after rerouting. Review '
  'cancellations by notice time to see where the standby list is most useful.',
  '/services/operations/',
  '/playbooks/route-density-planning/'),
 ('inventory-cycle-count-discrepancy',
  'Inventory Cycle Count Discrepancy Playbook',
  'Investigate physical-versus-system inventory discrepancies before approving adjustments.',
  'Define what the count covers, including location, lot, units of measure, and a transaction cutoff. Assign '
  'a second counter when the first difference is material.',
  'Hold or record moves around the cutoff, then compare receipts, issues, transfers and returns. Record the '
  'adjustment separately from the root cause and approval. Preserve both count sheets.',
  'A bin shows 72 units in the system and 60 physically. Twelve units were moved to a staging shelf just '
  'before the count and never transferred in the system. Confirm both locations and correct the transfer, '
  'preserving the total stock balance.',
  'Recount affected bins after the correction and sample upcoming transfers for the same issue. Track '
  'recurring differences by location and transaction type.',
  '/services/operations/',
  '/playbooks/minimum-stock-reorder-point/'),
 ('billing-dispute-triage',
  'Billing Dispute Triage Playbook',
  'Resolve customer billing disputes by tying each disputed line to approved scope, delivery records, and '
  'decision authority.',
  'Capture the exact invoice line and what the customer believes should change. Give one account owner '
  'responsibility for updates and agree when they will respond.',
  'Compare the original agreement, approved changes, delivery log, payment history, and billing setup. Mark '
  'what is supported, what needs correction, and which team can approve a credit or revised bill.',
  'A customer disputes $600 on a $4,000 invoice. The initial review confirms $400 of authorized extra work '
  'and finds a $200 duplicate charge. Correct the duplicate, explain the documented balance, and retain the '
  'disposition in the account record.',
  'Before closing the case, verify customer communication, the account balance, and any credit. Review '
  'repeated disputes by source so billing can fix the entry point.',
  '/services/operations/',
  '/playbooks/job-closeout-completeness/')])

TOPICS.extend([('field-service-van-stock-replenishment',
  'Field Service Van Stock Replenishment Playbook',
  'Set van stock levels by job type and replenish used parts without losing track of inventory.',
  'Use completed jobs to identify which parts belong on each van. Review consumption and return visits '
  'before changing stock.',
  'Create one list per service profile. Give each part a bin, minimum, maximum and replenishment owner. Log '
  'parts removed from a van for a different job or truck.',
  'A crew uses six common fittings over three routes. The next scheduled refill is two routes away and two '
  'remain. The lead adds enough for expected use and a documented buffer, then checks a slower-moving '
  'specialty fitting separately.',
  'Compare stockout callbacks, unused stock and replenishment effort over several refill cycles.',
  '/services/operations/',
  '/playbooks/field-service-first-visit-completion/'),
 ('service-appointment-confirmation',
  'Service Appointment Confirmation Playbook',
  'Confirm site access, customer availability and job inputs before assigning crew time.',
  'Identify appointments where a missing contact or an inaccessible site creates significant wasted travel.',
  'Confirm the window, access instructions, site contact, and any equipment or paperwork needed. Define when '
  'to release an unconfirmed slot and who handles exceptions.',
  'A 90-minute visit requires access to a locked utility room. The customer confirms their appointment but '
  'the building contact is unavailable. Dispatch keeps the booking conditional until the crew has a working '
  'access plan.',
  'Sample visits with access delays. Compare wasted drive time and customer rescheduling after the new '
  'confirmation step.',
  '/industries/construction-trades/',
  '/playbooks/dispatch-cancellation-recovery/'),
 ('customer-support-response-time-audit',
  'Customer Support Response Time Audit',
  'Recalculate response times using a consistent clock and a sample of original ticket events.',
  'Choose whether the measure tracks elapsed time or staffed hours. Document the qualifying human response '
  'and the rules for merged tickets.',
  'Export receipt and response events. Preserve timezone and shift information, classify auto-replies '
  'separately, and trace outliers to the original thread.',
  'A ticket arrives Friday at 4:45 p.m. and receives a reply Monday at 9:15 a.m. A team staffed 9 to 5 on '
  'weekdays counts 30 staffed minutes. Its parallel elapsed measure records the full weekend wait.',
  'Have two reviewers reproduce a sample of results and show how much the definition changes reported '
  'performance.',
  '/services/operations/',
  '/playbooks/operating-metric-definitions/'),
 ('duplicate-vendor-record-cleanup',
  'Duplicate Vendor Record Cleanup Playbook',
  'Find and resolve duplicate supplier records while preserving purchase, payment, and tax reporting '
  'history.',
  'Inventory active and inactive vendor records together. Keep banking and tax records in the approved '
  'system with restricted access.',
  'Compare legal names, registration identifiers where available, remittance details, and open transactions. '
  'Route potential matches through an authorized reviewer before merging or retiring records.',
  'Two entries share a trading name, but invoices show separate legal entities. The reviewer keeps both '
  'records and adds distinguishing details so purchase orders can select the correct payee.',
  'Reconcile open purchase orders and balances before and after any approved cleanup, and confirm future '
  'invoices use the intended record.',
  '/services/operations/',
  '/playbooks/purchase-order-three-way-match/')])

TOPICS.extend([('warehouse-pick-error-review',
  'Warehouse Pick Error Review Playbook',
  'Trace mispicks to slotting, barcodes, order edits or packing checks.',
  'Start with a specific wrong shipment and reconstruct the records available at each step.',
  'Capture the expected SKU, scanned item, label version, storage slot, pack check and any changes after '
  'release. Preserve the original pick ticket before correcting the order.',
  'A picker scans the correct outer case but two inner packs contain the wrong variant. Receiving checks the '
  'same lot, isolates affected stock and gives packing a temporary inner-pack verification step.',
  'Compare defects per order line and time per order after the change. Inspect corrected orders for new '
  'delays and reject changes that move the error downstream.',
  '/services/operations/',
  '/playbooks/inventory-cycle-count-discrepancy/'),
 ('scheduled-maintenance-completion',
  'Scheduled Maintenance Completion Playbook',
  'Track whether essential maintenance finishes on time and whether deferred tasks have operating owners.',
  'List maintenance tasks with due dates, affected assets and the operating windows needed to perform them.',
  'Record completion evidence, technician, exceptions, and rescheduled work. Define who can defer work and '
  'how they notify dispatch or production. Use manufacturer guidance and qualified personnel to determine '
  'the work itself.',
  'A shop has 24 preventive tasks due in a month. Twenty finish by their approved date, three are late and '
  'one is deferred because a replacement part is unavailable. Review 20 of 24 as on time and give the '
  'deferred task a named owner.',
  'Check completion against original dates as well as approved revised dates. Sample records for evidence '
  'that the listed work happened.',
  '/services/operations/',
  '/playbooks/month-end-operations-review/'),
 ('service-work-queue-aging',
  'Service Work Queue Aging Playbook',
  'Use aging buckets and blocked-work detail to spot stalled service orders before deadlines are missed.',
  'Capture the original receipt time and define which events change status without resetting queue age.',
  'Calculate open age for each ticket, track promised dates separately and group by blocker. Identify the '
  'oldest item with a next action each day.',
  'A queue has 40 items including six older than seven days. Four depend on the same vendor quote. Assign '
  'one coordinator to resolve that dependency and verify remaining customer dates individually.',
  'Compare the age of the oldest items and the proportion overdue. Check whether moving items to another '
  'status hides them from the review.',
  '/services/operations/',
  '/playbooks/service-backlog-triage/'),
 ('handoff-acceptance-criteria',
  'Internal Handoff Acceptance Criteria Playbook',
  'Specify what the receiving team must have before accepting work from another department.',
  'Choose one recurring transfer where missing details lead to delayed work or rework.',
  'Define required fields, source records, exception path and acknowledgment. Let the receiving team mark an '
  'item accepted, conditional or returned with the next action.',
  'Estimating hands a job to production with drawings and approved scope but no access date. Production '
  'accepts document review and leaves scheduling conditional until the account owner confirms site access.',
  'Review an accepted and a returned handoff with both teams. Check whether the record states what can '
  'start, what is blocked and who resolves it.',
  '/services/operations/',
  '/playbooks/shift-handoff-log/')])

TOPICS.extend([('quote-expiration-review',
  'Quote Expiration Review Playbook',
  'Keep expired quotes from turning into unsupported pricing, stale availability or missed follow-up.',
  'Give quotes an expiration date and put that date where the customer and sales team can see it.',
  'Track quote version, accepted date, vendor assumptions and availability. Define which changes require '
  'formal reapproval, and which salesperson handles the customer conversation.',
  'A customer accepts a 30-day quote on day 38. A supplier has raised the included equipment price by $450. '
  'The seller checks the proposal terms and current costs, then takes a revised quote or a documented '
  'exception to the approver.',
  'Sample orders placed after expiration. Check current price, availability and the version accepted by the '
  'customer.',
  '/services/sales-strategy/',
  '/playbooks/quote-approval-delegation/'),
 ('service-labor-utilization',
  'Service Labor Utilization Measurement Playbook',
  'Measure how field-service time is used without losing sight of training, travel, quality and customer '
  'outcomes.',
  'Define available hours and productive service hours before comparing technicians, shifts or territories.',
  'Classify travel, on-site work, training, leave and idle time consistently. Review hours by job mix. Pair '
  'utilization with on-time arrival, safety, quality and completion measures.',
  'A technician has 32 scheduled working hours after leave. They spend 22 on site, six traveling and four in '
  'training, yielding 68.75% on-site utilization. A manager checks route assignments before deciding whether '
  'low utilization reflects avoidable delay.',
  'Have supervisors classify a sample independently, then review trends across comparable schedules instead '
  'of using a raw score to explain individual performance.',
  '/services/operations/',
  '/playbooks/route-density-planning/'),
 ('service-warranty-rework-tracking',
  'Service Warranty Rework Tracking Playbook',
  'Track work repeated under warranty and its direct labor, parts and travel costs.',
  'Give every work order performed under warranty a link to the original job and a code for the nature of '
  'the work.',
  'Record the customer commitment, approved coverage decision, required parts, direct labor and trip time. '
  'Keep warranty goodwill decisions distinct from corrections already owed under policy.',
  'A fictional shop replaces five failed parts. The total includes $150 in materials, four crew hours at $35 '
  'direct labor, and $60 in travel. Track the resulting $350 direct cost separately from any supplier '
  'recovery.',
  'Review repeating failures by job type, product or lot. Check that credits and spare part use reconcile to '
  'the original repair record.',
  '/services/operations/',
  '/playbooks/service-callback-root-cause/')])


def field_guides():
    for slug, title, description, intro, method, example, check, service, related in TOPICS:
        yield {
            "path": f"/playbooks/{slug}/",
            "title": title,
            "description": description,
            "intro": intro,
            "sections": [
                ("Set up the work", f"<p>{escape(method)}</p>"),
                ("Worked example", f"<p>{escape(example)}</p>"),
                ("Check the result", f"<p>{escape(check)}</p>"),
            ],
            "links": [service, related],
            "kind": "Implementation playbook",
            "parent": "/playbooks/",
            "modified": "2026-11-27",
        }
