"""Original service, decision, and workflow content for the Elixir expansion."""
from html import escape as e


def p(text):
    return '<p>' + e(text) + '</p>'


def ul(items, ordered=False):
    tag = 'ol' if ordered else 'ul'
    return '<' + tag + '>' + ''.join('<li>' + e(i) + '</li>' for i in items) + '</' + tag + '>'


def table(caption, headings, rows):
    return ('<div class="table-scroll" tabindex="0" role="region" aria-label="' + e(caption) + '"><table><caption>' + e(caption) + '</caption><thead><tr>'
            + ''.join('<th scope="col">' + e(h) + '</th>' for h in headings)
            + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<th scope="row">' + e(c) + '</th>' if j == 0 else '<td>' + e(c) + '</td>' for j, c in enumerate(row)) + '</tr>' for row in rows)
            + '</tbody></table></div>')


SERVICES = [
 dict(slug='operational-assessment', title='Operational Assessment Services for Small Businesses', parent='operations',
 intro='Find the operating constraint before buying another tool or redesigning every process. An operational assessment traces real work from demand through delivery and identifies a manageable sequence of changes.',
 fit='Use an assessment when sales, delivery, and finance describe different causes for the same recurring problem. Rising backlog, repeated owner intervention, and missed commitments are useful starting signals, but they are not a diagnosis.',
 outputs=['A map of one agreed end-to-end workflow, including waiting points and unofficial workarounds.', 'An evidence register separating measured facts, employee observations, and unresolved assumptions.', 'A prioritized constraint list showing impact, effort, dependencies, and a responsible manager.', 'An implementation brief defining the first pilot, baseline, acceptance test, and review date.'],
 steps=['Trace a small sample of completed, delayed, and reworked jobs with the people who handled them.', 'Compare the written process with the actual sequence, then test competing explanations against records.', 'Select the first intervention with the leadership team and define what would demonstrate improvement.'],
 inputs='Bring recent job or project records, a role list, existing procedures, and the measures your team already uses. Include difficult cases, not just successful ones. Identify who can approve access and who can commit the implementation team.',
 acceptance='The assessment is usable when the accountable manager can explain the constraint, point to supporting evidence, and start a bounded pilot. A long report without a named implementation owner is an incomplete handover.',
 boundary='An operational assessment is different from a financial audit, legal review, or certification. Agree on the business process under review and involve qualified advisers where specialist requirements affect the proposed change.',
 template='weekly-operations-scorecard-template-service-business', example='/examples/operations-assessment-report/'),
 dict(slug='sop-documentation', title='SOP Documentation Services for Growing Teams', parent='operations',
 intro='Turn repeatable work into procedures another qualified team member can follow. SOP documentation connects the trigger, steps, decisions, evidence, and exception path instead of collecting screenshots without context.',
 fit='This work fits teams where training depends on shadowing one person, routine tasks vary by employee, or a key absence exposes undocumented knowledge. Begin with a process that repeats often enough to test.',
 outputs=['A prioritized process inventory with a named owner and review cycle.', 'Procedures containing scope, prerequisites, actions, decision rules, and completion evidence.', 'A controlled home for current versions and a retirement rule for outdated instructions.', 'A practical walkthrough in which a second person attempts the task and records missing information.'],
 steps=['Observe a real execution and capture the judgment calls as well as the normal steps.', 'Draft a short procedure around the task, then have an experienced operator check accuracy.', 'Test with an appropriate backup, resolve gaps, and assign ownership for future updates.'],
 inputs='Bring existing checklists, training notes, approved policies, access requirements, and examples of errors. Choose a subject-matter expert who has time to validate the document; writing alone cannot establish that the steps are safe or correct.',
 acceptance='A procedure is ready when its intended user can complete a representative task, identify when to stop, and find the exception contact. Record the version and test date so successful training is attached to the instructions actually used.',
 boundary='SOPs should reflect approved operating practices. Documentation work does not replace technical, safety, clinical, financial, or legal approval required for the underlying activity.',
 template='employee-cross-training-matrix-template', example='/playbooks/sop-rollout/'),
 dict(slug='business-process-mapping', title='Business Process Mapping Consulting for Small Teams', parent='operations',
 intro='Make the flow of work visible before trying to automate it. Business process mapping identifies who acts, what information changes hands, where decisions occur, and why work waits.',
 fit='Use process mapping when departments each finish their part but the customer still experiences delays. It is particularly useful before a CRM rollout, onboarding redesign, or change in delivery responsibility.',
 outputs=['A current-state map based on actual cases, with explicit start and finish boundaries.', 'A handoff register identifying the sender, receiver, information required, and acceptance rule.', 'An exception map covering rejected, incomplete, urgent, and cancelled work.', 'A proposed future-state pilot with the changed steps and a simple measurement plan.'],
 steps=['Agree on one customer outcome and trace the events needed to achieve it.', 'Walk the map with each participating role and verify disputed steps against records.', 'Remove an unnecessary handoff or clarify a decision, then test the revised sequence on real work.'],
 inputs='Bring a recent example from intake through completion, the systems touched along the way, and people from both sides of each handoff. A manager-only workshop can miss the informal work that keeps the current system running.',
 acceptance='A useful map lets two operators independently explain where a case is, who owns the next action, and what blocks progress. Keep a text equivalent so the process remains understandable outside the diagram.',
 boundary='Mapping describes how work moves; it does not itself change staffing, permission levels, or contract terms. Assign those decisions separately before adopting the proposed state.',
 template='sales-to-operations-handoff-checklist', example='/examples/business-process-map/'),
 dict(slug='crm-cleanup', title='CRM Cleanup Services for Small Sales Teams', parent='sales-strategy',
 intro='Repair the record quality behind sales follow-up and forecasting. CRM cleanup focuses on duplicate records, ownership, stage definitions, missing next actions, and the intake rules that recreate bad data.',
 fit='This is a starting point when sellers avoid the CRM, managers maintain private forecast spreadsheets, or automated follow-up reaches the wrong contacts. Fix the definitions before adding more automated activity.',
 outputs=['A field and lifecycle dictionary explaining how active records should be maintained.', 'A sampled duplicate review and an approved merge, archive, and exception policy.', 'Views for unassigned opportunities, overdue actions, stale stages, and conflicting data.', 'A monitored intake and ownership process that reduces recurrence after the initial cleanup.'],
 steps=['Back up records and test proposed changes on a small recoverable sample.', 'Resolve conflicting values with the business owner, preserving relevant history and communication preferences.', 'Review the cleaned pipeline with sellers and assign responsibility for ongoing data quality.'],
 inputs='Provide administrator-approved access, existing reports, integration details, and examples of records sellers do not trust. Clarify your retention and communication rules before approving merges or deletion.',
 acceptance='The team should be able to explain each active opportunity, its owner, stage evidence, and next action. Reconcile important counts before and after cleanup; a smaller database is not proof that the right information survived.',
 boundary='Cleanup does not necessarily require migration. Confirm the supported CRM, integrations, backup method, and permission boundaries during scoping; do not assume a particular vendor partnership or certification.',
 template='crm-data-cleanup-checklist-small-business', example='/playbooks/crm-rollout/'),
 dict(slug='crm-implementation', title='CRM Implementation Consulting for Small Businesses', parent='sales-strategy',
 intro='Install a CRM around the sales process your team needs to run. Implementation includes definitions, ownership, data migration decisions, follow-up rules, testing, and adoption rather than ending when the software account is configured.',
 fit='Consider implementation when leads are scattered across inboxes, stage reports cannot be reconciled, or your current setup does not support the agreed sales workflow. First decide whether a repair would solve the problem with less disruption.',
 outputs=['A requirements brief distinguishing essential workflows from optional features.', 'Configured stages, required information, owner assignment, and follow-up views.', 'A migration and reconciliation plan with a recoverable source export and controlled cutover.', 'Scenario testing, role-based training, administrator handover, and an exception log.'],
 steps=['Define the sales stages and evidence required to move between them before configuring fields.', 'Pilot a representative set of records and integrations, including duplicate and failure cases.', 'Train a small user group, reconcile the pilot, and expand after the team can run the workflow.'],
 inputs='Bring current tools, data sources, sales stages, lead channels, reporting needs, and communication constraints. Name a business decision maker and an internal administrator. Confirm that necessary vendor access and licenses can be arranged.',
 acceptance='A lead should reach the correct owner, progress on recorded evidence, and retain its history through a handoff. Managers should reproduce the main reports from agreed definitions, and the internal administrator should know how to maintain the setup.',
 boundary='Vendor selection, licensing, custom development, and third-party integrations depend on scope. Confirm platform compatibility before committing to a rollout date or migration promise.',
 template='lead-response-time-sla-template', example='/guides/crm-implementation-cost-small-business/'),
 dict(slug='sales-process-implementation', title='Sales Process Implementation for Owner-Led Companies', parent='sales-strategy',
 intro='Build a sales process that tells the team what qualifies an opportunity, what the buyer must decide next, and when delivery can accept the sale. The goal is consistent execution supported by evidence in the pipeline.',
 fit='This fits companies where sales performance depends on the founder remembering every conversation, proposals remain open indefinitely, or closed-won deals create surprises for operations.',
 outputs=['A fit and qualification guide using actual customer patterns and disqualifiers.', 'Pipeline stages with entry evidence, exit criteria, next-action rules, and close reasons.', 'A proposal and follow-up workflow identifying decisions rather than repeated generic check-ins.', 'An accepted sales-to-delivery handoff and a manager review cadence.'],
 steps=['Review recent wins, losses, and stalled deals with the people who sold and delivered them.', 'Define observable buyer decisions and translate them into a small number of usable stages.', 'Pilot the process with active opportunities, then coach the team on the exceptions that appear.'],
 inputs='Bring proposals, deal histories, current CRM reports, and examples of scope disputes. Include the delivery leader so qualification and promised timelines reflect actual operating capacity.',
 acceptance='Two sellers should classify the same opportunity similarly and explain the next decision needed. A delivery manager should be able to accept a new customer using the recorded scope and dependencies.',
 boundary='A documented process cannot guarantee lead volume or close rates. Establish a baseline and distinguish sales execution problems from demand, offer, pricing, or delivery constraints.',
 template='sales-pipeline-aging-report-template', example='/playbooks/founder-sales-handoff/'),
 dict(slug='kpi-dashboard-setup', title='KPI Dashboard Setup for Small Business Operations', parent='operations',
 intro='Build an operating dashboard that leads to decisions. KPI setup begins with the measure definition, source, owner, and action threshold so a polished chart does not hide inconsistent numbers.',
 fit='Use this work when leadership meetings debate whose report is correct, revenue is the only reliable measure, or problems appear only after customers complain. Start with a few measures tied to the current operating constraint.',
 outputs=['A metric dictionary with period, numerator, denominator, exclusions, and source.', 'A compact dashboard covering demand, capacity, delivery, and quality where relevant.', 'An exception review process with owners, actions, due dates, and follow-up.', 'A data validation and maintenance routine for the person responsible for each measure.'],
 steps=['Select decisions the leadership team needs to make and work backward to the evidence needed.', 'Reconcile a sample period with source records and resolve definition disagreements.', 'Run the dashboard through several review cycles, replacing measures that do not prompt useful action.'],
 inputs='Bring the reports you already use, sample source records, reporting cutoffs, and recurring leadership questions. Identify who can validate the data and what manual collection effort the team can sustain.',
 acceptance='Two people should obtain the same number from the written definition. Each flagged measure should have an owner and an agreed response; the team should know when the number is stale or incomplete.',
 boundary='Dashboard setup is not an assurance opinion on financial statements. Keep operational measures distinct from finance-approved reporting and agree on any accounting definitions with the appropriate adviser.',
 template='weekly-operations-scorecard-template-service-business', example='/examples/weekly-operations-dashboard/'),
 dict(slug='leadership-operating-cadence', title='Leadership Operating Cadence Implementation', parent='leadership',
 intro='Connect weekly decisions, monthly reviews, and quarterly priorities into a leadership rhythm the team can maintain. An operating cadence gives issues a decision path and actions a closure standard.',
 fit='This fits teams with many meetings but repeated unresolved issues, shifting priorities, or an owner who must repeatedly ask for status. Clarify decision authority before increasing meeting frequency.',
 outputs=['A meeting map with purpose, participants, inputs, and decisions for each session.', 'A shared scorecard and exception agenda connected to current priorities.', 'A decision and action log with owners, due dates, dependencies, and closure evidence.', 'A facilitation and handover guide for the internal leader who will sustain the rhythm.'],
 steps=['Review current meetings and identify duplicate reporting and decisions that never reach an owner.', 'Pilot a weekly exception review with a limited scorecard and a visible action log.', 'Connect recurring issues to monthly resource decisions and quarterly priorities, then hand facilitation to the team.'],
 inputs='Bring meeting agendas, action lists, priorities, and examples of decisions waiting for approval. Have the leadership group agree which decisions belong in the room and which should remain with the responsible manager.',
 acceptance='The team should leave knowing what was decided, what remains unresolved, and who acts next. A completed action needs evidence, not a status label changed just before the next meeting.',
 boundary='A cadence supports management accountability but cannot substitute for role clarity or difficult personnel decisions. Keep confidential employee matters in the appropriate management process.',
 template='decision-rights-matrix-small-business-template', example='/examples/weekly-operations-dashboard/'),
 dict(slug='owner-dependency-reduction', title='Owner Dependency Reduction Through Business Systems', parent='leadership',
 intro='Identify the recurring decisions and knowledge that keep the owner in every workflow. Reducing owner dependency combines authority, information, procedures, backup coverage, and a deliberate transfer of responsibility.',
 fit='This fits a business where holidays stall approvals, employees repeatedly ask the same questions, or customer relationships cannot move beyond the founder. Start with frequent decisions whose risks can be bounded.',
 outputs=['An interruption inventory showing the decisions, contacts, and tasks returning to the owner.', 'A decision-rights matrix with clear boundaries and escalation triggers.', 'Documented critical workflows and validated backups for important tasks.', 'A staged absence or delegation test with a record of interruptions and system changes.'],
 steps=['Record a representative week of owner interruptions and identify what information or authority was missing.', 'Transfer one decision category with a clear limit, backup, and review method.', 'Run a short controlled absence test, then improve the exceptions before extending the transfer.'],
 inputs='Bring an honest view of the owner’s calendar, approval requests, customer dependencies, and critical access arrangements. Name a capable receiving manager and identify the training or authority they still need.',
 acceptance='A manager should make agreed decisions within the boundary and know when to escalate. The owner can review results without re-approving every routine action or becoming the only source of essential information.',
 boundary='This does not promise a fully passive business or eliminate appropriate owner oversight. Some decisions remain with the owner because of risk, governance, or professional responsibility.',
 template='owner-vacation-business-continuity-checklist', example='/playbooks/operations-manager-first-90-days/'),
 dict(slug='ai-workflow-implementation', title='AI Workflow Implementation for Small Business Teams', parent='ai-consulting',
 intro='Evaluate and install a bounded AI-assisted workflow with measurable output requirements and human review. Begin with the business task and total operating effort, including verification and recovery.',
 fit='This fits repetitive work with accessible inputs, observable outputs, and a practical fallback. Drafting internal summaries or organizing a review queue may be easier to test than autonomous customer commitments or financial actions.',
 outputs=['A task and data-use brief describing permitted inputs and approval responsibilities.', 'A baseline and test set covering ordinary, difficult, incomplete, and unacceptable cases.', 'A pilot workflow with review gates, failure handling, and a manual fallback.', 'An operating guide recording quality checks, monitoring, access, and rollout criteria.'],
 steps=['Map the existing task and define what an acceptable output must contain or avoid.', 'Test representative cases and count review, correction, and exception-handling time.', 'Pilot with a small group and expand only when the evidence supports a manageable operating benefit.'],
 inputs='Bring real task examples that can be used appropriately, existing quality checks, and the staff who can judge output accuracy. Confirm data permissions and vendor requirements before providing business information to a tool.',
 acceptance='The team should detect important errors, route exceptions, and complete the task manually when the tool is unavailable. A successful demonstration alone is not an acceptance test.',
 boundary='AI output requires task-appropriate verification. The engagement scope must define prohibited actions, approved data, human authority, and any specialist review needed for the use case.',
 template='ai-pilot-success-criteria-template', example='/blog/automation-exception-handling-checklist/'),
 dict(slug='client-onboarding-systems', title='Client Onboarding Systems for Service Businesses', parent='operations',
 intro='Build the path from accepted sale to a client who is ready for delivery. An onboarding system makes scope, customer inputs, internal ownership, and the first milestone visible in one coordinated workflow.',
 fit='This fits firms where clients repeat their story after signing, teams start with missing documents, or kickoff dates slip because prerequisites were never assigned. Look at the handoff before adding more reminder emails.',
 outputs=['A readiness checklist linking commercial, access, staffing, and customer prerequisites.', 'An intake and validation workflow that distinguishes received information from usable information.', 'A customer communication plan with named contacts, next actions, and dependency dates.', 'An exception queue for missing inputs, scope ambiguity, and readiness decisions.'],
 steps=['Trace recent onboardings and identify the information that arrived too late to support delivery.', 'Define the minimum accepted handoff and assign each missing prerequisite to one owner.', 'Pilot the process on a new client and review time waiting separately from internal processing effort.'],
 inputs='Bring agreements, welcome messages, intake forms, project templates, and examples of delayed starts. Include sales, delivery, and whoever manages customer document collection.',
 acceptance='The delivery lead should be able to confirm whether work is ready to start and explain each blocker. The customer should know who owns the next action and what a delayed input means for scheduling.',
 boundary='An onboarding system supports communication and control; it does not change the contract by itself. Confirm any revised scope, payment condition, or milestone through the agreed commercial process.',
 template='client-onboarding-missing-documents-workflow', example='/guides/professional-services-scope-to-invoice/'),
 dict(slug='multi-location-operations', title='Multi-Location Operations Systems and Scorecards', parent='operations',
 intro='Create consistent operating definitions and escalation rules across locations while preserving local context. Multi-location systems help owners distinguish a site-specific constraint from a process problem shared across the business.',
 fit='This fits companies preparing another location or trying to understand why existing sites produce different outcomes. Common definitions and manager readiness should come before a larger reporting dashboard.',
 outputs=['A common operating standard covering key workflows, local exceptions, and manager authority.', 'A location scorecard with comparable definitions and context for demand, staffing, and mix.', 'A manager review cadence and issue path connecting local action with central decisions.', 'A readiness and handover plan for applying the system at an additional site.'],
 steps=['Compare the same workflow at two sites and separate necessary variation from avoidable inconsistency.', 'Pilot common measures and have managers independently calculate a sample period.', 'Transfer the practices that work, document exceptions, and test support coverage before adding another site.'],
 inputs='Bring location-level schedules, delivery records, role structures, and current reports. Identify differences in customer mix, equipment, staffing, or opening hours that could make a raw comparison misleading.',
 acceptance='A local manager should know what they own, when to escalate, and how to calculate the shared measures. Central leadership should see the specific constraint behind a site’s variance rather than only a rank.',
 boundary='A consistent operating model does not imply every site needs identical staffing or targets. Location opening decisions also require the relevant financial, property, regulatory, and specialist reviews.',
 template='multi-location-manager-scorecard-template', example='/playbooks/second-location-opening/'),
]


def service_pages():
    pages = []
    for s in SERVICES:
        sections = [
            ('When this work is a fit', p(s['fit'])),
            ('Deliverables to define in the scope', ul(s['outputs'])),
            ('How implementation progresses', ul(s['steps'], True)),
            ('What to bring to a scoping conversation', p(s['inputs'])),
            ('Acceptance and handover', p(s['acceptance'])),
            ('Scope boundaries', p(s['boundary'])),
        ]
        pages.append(dict(path='/services/' + s['slug'] + '/', title=s['title'],
            description=s['intro'].split('. ')[0] + '.', intro=s['intro'], sections=sections,
            kind='Service', parent='/services/' + s['parent'] + '/',
            links=['/blog/' + s['template'] + '/', s['example'], '/process/']))
    return pages


def guide(slug, title, description, intro, sections, links, kind='Buying guide', parent='/guides/'):
    return dict(path=parent + slug + '/', title=title, description=description, intro=intro,
                sections=sections, links=links, kind=kind, parent=parent)


def buying_pages():
    return [
        guide('operations-consulting-cost', 'Operations Consulting Cost: Scope, Fees & Buyer Checklist',
            'Understand operations consulting pricing drivers, compare proposals, and separate diagnostic, implementation, and ongoing support costs.',
            'Operations consulting cost depends on the workflow, the number of teams involved, the reliability of the evidence, and how much implementation support is included. Compare the total work and internal commitment before comparing a fee.', [
                ('Separate the three parts of an engagement', table('What the fee may cover', ['Work', 'What to check', 'Common exclusion'], [
                    ('Assessment', 'Workflow sample, evidence review, priorities, and a pilot brief', 'Building or operating the new process'),
                    ('Implementation', 'Configuration, procedure design, pilot cycles, and training', 'Unbounded custom development or additional departments'),
                    ('Ongoing support', 'Review cadence, defined access, monitoring, and revision work', 'Unlimited delivery ownership or emergency coverage')])),
                ('What increases the amount of work?', p('Multiple locations, conflicting data sources, undocumented exceptions, and unclear authority add discovery and coordination. A narrow onboarding redesign with one decision maker is a different project from replacing workflows across sales, service, and finance. Identify these differences in the proposal rather than assuming every assessment or implementation is equivalent.')),
                ('Compare a project fee with the full operating cost', p('Add the consulting fee, licenses or purchases, internal staff time, migration work, and temporary parallel operation. Identify which costs are one-time and which continue after handover. A less expensive proposal can require more internal work; that can still be the right choice when the team has the capacity and skill to perform it.')),
                ('An illustrative comparison', p('Proposal A delivers a workflow map and recommendations. Proposal B includes those outputs plus two pilot cycles, training, and administrator handover. Without prices, neither is automatically better value: the right comparison asks who will implement A and what that work requires. Ask both providers to state acceptance criteria, exclusions, and the treatment of changes.')),
                ('Questions to ask before accepting a proposal', ul(['Which workflow and locations are included?', 'What evidence will establish the baseline?', 'Who owns implementation on each side?', 'What work requires a change in scope?', 'What must be true before final handover?', 'What recurring costs remain after the engagement?'])),
                ('Elixir pricing and the next step', p('Elixir scopes fees around the agreed work; this page does not publish a standard rate or market-price estimate. Bring one operating problem, representative records, and the manager who can own the pilot to a consultation. Request a written scope that distinguishes assessment, implementation, and continuing support.')),
            ], ['/services/operational-assessment/', '/guides/consulting-project-vs-retainer/', '/blog/roi-of-hiring-business-consultant-real-numbers/']),
        guide('sop-documentation-cost', 'SOP Documentation Cost: How to Scope a Useful Project',
            'Compare SOP documentation proposals by process complexity, testing, validation, maintenance, and handover rather than page count.',
            'SOP documentation cost should follow the work required to capture, verify, test, and maintain a process. A page count or price per document says little about whether a backup can use the finished procedure.', [
                ('Count processes and decisions, not pages', p('Start with an inventory of the tasks to document. Note their frequency, business impact, known exceptions, and available subject-matter experts. A short approval procedure with several judgment calls can require more validation than a longer sequence of predictable actions. Decide which processes matter most before asking for a fee.')),
                ('The work a proposal should distinguish', table('SOP scope components', ['Component', 'Evidence of completion'], [('Capture', 'Observation or interview checked against real work'), ('Drafting', 'Purpose, prerequisites, steps, decisions, evidence, and exceptions'), ('Validation', 'Named subject-matter expert confirms accuracy'), ('Usability test', 'An intended user attempts a representative task'), ('Handover', 'Current version, owner, review date, and update method')])),
                ('Why existing notes may not reduce the fee', p('Old screenshots, contradictory policies, and undocumented workarounds can increase verification effort. Ask the provider to inspect a sample before treating the existing document library as a complete source. If the underlying process needs redesign, distinguish that decision work from describing an already approved process.')),
                ('Illustrative scope comparison', p('A team requests ten procedures. Four are stable and have experienced owners; six differ by location and have no agreed exception rule. Scope the stable four first or resolve the location differences as a separate workstream. Pricing all ten as identical documents hides the decisions that could prevent completion.')),
                ('Protect the maintenance investment', p('Agree where current procedures live, who can approve edits, and when the team reviews them. Software changes and role changes should trigger a check. A handover that leaves every future edit dependent on the consultant creates a recurring cost that should be visible in the proposal.')),
                ('Prepare a useful request for scope', ul(['Provide a process inventory and a sample of existing instructions.', 'Identify experts who can validate the work and reserve their time.', 'Specify the intended users and required approval roles.', 'Ask how many revision and test cycles are included.', 'Confirm ownership and access to editable source files.'])),
            ], ['/services/sop-documentation/', '/playbooks/sop-rollout/', '/examples/business-process-map/']),
        guide('crm-implementation-cost-small-business', 'CRM Implementation Cost for Small Businesses: Scope Guide',
            'Plan CRM implementation costs across licenses, configuration, data cleanup, migration, integrations, training, and ongoing administration.',
            'CRM implementation cost includes more than a subscription. Data cleanup, workflow decisions, integrations, testing, training, and ongoing administration determine how much work the rollout actually requires.', [
                ('Build the cost inventory before selecting software', table('CRM budget categories', ['Category', 'Scoping question'], [('Licenses', 'Which users need which capabilities, and what renews?'), ('Configuration', 'Which stages, fields, roles, reports, and automations are essential?'), ('Data', 'What must be cleaned, migrated, reconciled, or retained elsewhere?'), ('Integrations', 'What systems exchange data, and who handles failed exchanges?'), ('Adoption', 'Who trains users, resolves issues, and maintains definitions?')])),
                ('Decide whether to repair or replace', p('An unreliable pipeline may come from missing ownership or undefined stages rather than software limitations. Review a sample of real opportunities before committing to migration. If the current platform can support the agreed process, cleanup and configuration may be a smaller project. If a required workflow cannot be supported, document the limitation and test alternatives.')),
                ('State migration assumptions explicitly', p('Record the source systems, record types, activity history, attachments, duplicate rules, and relationships required in the new setup. A contact count alone does not describe migration effort. Ask what reconciliation evidence will show that important records and associations survived, and retain a recoverable source export.')),
                ('Illustrative scope decision', p('A service firm needs lead ownership, next actions, and an accepted delivery handoff. It initially requests every historical attachment and a custom quoting integration. The team can pilot the core workflow first while deciding whether those extra requirements justify their separate implementation and support effort.')),
                ('Review recurring operating costs', p('Include administrator time, new-user onboarding, integration monitoring, backup arrangements, and report maintenance. Ask which vendor charges depend on users, volume, or features. Use current written vendor terms in the final budget rather than assuming a price from an old article.')),
                ('Acceptance questions for a provider', ul(['Can a real inquiry reach the correct seller and backup?', 'Can the team reproduce its agreed forecast and stage reports?', 'Does the delivery owner receive the accepted scope and dependencies?', 'How are duplicates, failed integrations, and missing data handled?', 'Who can maintain fields, permissions, and automations after handover?'])),
            ], ['/services/crm-implementation/', '/services/crm-cleanup/', '/playbooks/crm-rollout/']),
        guide('fractional-coo-vs-operations-consultant', 'Fractional COO vs Operations Consultant: Choosing Support',
            'Compare ongoing operating leadership with a defined improvement project, including authority, accountability, duration, and handover.',
            'A fractional COO generally occupies an ongoing operating leadership role, while an operations consultant may lead a defined assessment or implementation project. Titles vary, so compare the actual authority and responsibilities in the agreement.', [
                ('Compare responsibility rather than title', table('Operating support comparison', ['Decision', 'Fractional operating leader', 'Defined consulting project'], [('Core need', 'Someone to own cross-functional operating decisions', 'A specific workflow or system needs improvement'), ('Authority', 'Must be explicitly delegated for the role', 'Usually limited to agreed project decisions'), ('Duration', 'Continues while the leadership need remains', 'Ends against stated delivery and handover criteria'), ('Internal counterpart', 'Owner and functional managers', 'Sponsor and process owner'), ('Exit question', 'Who takes over the operating role?', 'Can the team sustain the installed process?')])),
                ('Choose leadership when the seat is missing', p('If several teams need daily prioritization and nobody has authority to resolve tradeoffs, a process project alone may leave the management gap intact. Clarify the operating decisions the role will own, the time available, coverage expectations, and how performance will be reviewed. Part-time availability still needs a clear escalation plan.')),
                ('Choose a project when the constraint is bounded', p('If the delivery manager has authority but onboarding fails because handoffs are incomplete, a defined implementation project can address the workflow without installing a new executive role. Set a baseline, pilot the revised process, and transfer maintenance to that manager.')),
                ('Illustrative choice', p('An owner spends each morning resolving competing priorities across three departments. That suggests a leadership and authority question. A second owner has a capable general manager but unreliable CRM-to-delivery transfers. That suggests a bounded system problem. Both businesses may need documentation, but their primary support requirements differ.')),
                ('Ask these questions in either model', ul(['Which decisions will you own, recommend, or escalate?', 'How much operating availability is included?', 'Who manages employees and customer commitments?', 'What evidence defines success?', 'What does the exit or internal succession plan look like?'])),
                ('How this relates to Elixir', p('Elixir’s service pages describe operations and systems implementation. Discuss the operating gap and required authority during scoping rather than assuming a fractional executive appointment is included. A written proposal should state whether ongoing management responsibility is part of the engagement.')),
            ], ['/services/operations/', '/services/leadership-operating-cadence/', '/guides/consultant-vs-operations-manager/']),
        guide('consultant-vs-operations-manager', 'Operations Consultant vs Operations Manager: Which to Hire?',
            'Decide whether you need a defined systems project, an internal operations manager, or a coordinated transition between the two.',
            'An operations manager owns recurring execution inside the business. A consultant can help diagnose a constraint or install a defined system. The right choice depends on whether you lack an operating owner, a working process, or both.', [
                ('Identify the missing responsibility', table('What the business needs', ['Situation', 'Question to resolve'], [('Work waits for daily decisions', 'Who has the ongoing authority and availability to manage it?'), ('A manager exists but workflows fail', 'Which process, information, or tool needs redesign?'), ('A new manager inherits undocumented work', 'Who will support the transition and capture critical knowledge?'), ('The owner wants fewer interruptions', 'What authority, access, and review boundaries will transfer?')])),
                ('What to define in an internal role', p('Specify the operating outcomes, decision authority, direct reports, recurring cadence, and limits of the role. Hiring a manager without authority can move the same approval queue to a new person. Give the manager access to the data and people needed to act, and define when escalation is appropriate.')),
                ('What to define in a consulting project', p('State the workflow under review, deliverables, internal counterpart, testing plan, and handover criteria. A consultant can make a process clearer and help it survive pilot cycles, but an internal person must sustain recurring decisions after the project ends unless ongoing responsibility is explicitly included.')),
                ('When both can make sense', p('A company hiring its first operations manager may need a short transition project to document inherited work and establish a scorecard. Coordinate the consultant’s outputs with the manager’s actual needs. Avoid creating a system before the incoming manager has an opportunity to validate it.')),
                ('Illustrative decision', p('If a team can run the agreed process but needs someone to schedule people, resolve daily conflicts, and coach staff, prioritize the management role. If a capable manager spends time reconciling contradictory reports and chasing missing handoff information, begin by defining and repairing those systems.')),
                ('Questions before spending', ul(['Is the work recurring or does it have a clear end state?', 'Who will have authority when the owner is absent?', 'What capability must remain after the project?', 'Can the current team absorb implementation work?', 'How will the new role or project be evaluated after the first operating cycles?'])),
            ], ['/services/owner-dependency-reduction/', '/playbooks/operations-manager-first-90-days/', '/guides/operations-consulting-cost/']),
        guide('consulting-project-vs-retainer', 'Consulting Project vs Retainer: Scope, Access & Accountability',
            'Compare a defined consulting project with ongoing advisory or implementation support using deliverables, capacity, change control, and exit criteria.',
            'A project organizes work around a defined outcome. A retainer reserves an agreed level of continuing support. Neither arrangement guarantees implementation unless ownership, capacity, and acceptance are explicit.', [
                ('Compare the operating commitments', table('Engagement model checklist', ['Item', 'Project agreement', 'Retainer agreement'], [('Work boundary', 'Named workflows and deliverables', 'Included activities, access, and monthly capacity'), ('Completion', 'Acceptance and handover conditions', 'Review, renewal, and termination conditions'), ('Change control', 'Treatment of additional scope', 'Treatment of work beyond reserved capacity'), ('Availability', 'Milestone and working-session commitments', 'Response expectations and coverage limits'), ('Continuity', 'Who maintains the result after exit', 'What happens if ongoing support ends')])),
                ('When a project is a sensible start', p('Use a project when the problem is sufficiently bounded to define outputs and an acceptance test. A CRM cleanup, an onboarding redesign, or a limited SOP library can have a clear completion point. Keep discovery separate where the evidence is not yet strong enough to specify implementation responsibly.')),
                ('When ongoing support may fit', p('A retainer can fit a business with a continuing review cadence, a changing improvement backlog, or a need for structured implementation support over time. State who prioritizes the queue and how unused or excess capacity is treated. Access to advice is different from ownership of delivery tasks.')),
                ('Illustrative sequencing', p('A firm starts with a project to define its weekly operating dashboard and train the manager. After handover it may need occasional revision support as locations change. That could be a small recurring agreement, a future project, or internal maintenance. The next arrangement should follow the actual work rather than automatic renewal.')),
                ('Require a visible record of work', p('For either model, keep a short log of decisions, completed outputs, open issues, and next actions. Review whether the arrangement is increasing internal capability or leaving the same questions permanently dependent on outside help.')),
                ('Questions to resolve in writing', ul(['What is included and explicitly excluded?', 'Who provides internal information and approval?', 'How is extra scope or demand handled?', 'What response and availability expectations apply?', 'Who owns editable materials and configuration access?', 'What are the handover, renewal, and exit conditions?'])),
            ], ['/guides/operations-consulting-cost/', '/services/operational-assessment/', '/process/']),
    ]


WORKFLOWS = [
 dict(slug='construction-estimating-to-production-handoff', title='Construction Estimating to Production Handoff Checklist', industry='construction-trades',
 intro='A construction estimating-to-production handoff turns the sold job into an executable plan. The production lead needs scope, quantities, exclusions, site conditions, customer commitments, and purchasing dependencies before scheduling crews.',
 trigger='The agreement is accepted, but crew dates remain provisional until the production owner has reviewed the scope and site prerequisites. Distinguish a commercially won job from a job ready to mobilize.',
 rows=[('Scope and quantities', 'Accepted estimate, drawings, inclusions, exclusions, and allowances'), ('Site readiness', 'Access contact, working hours, staging, and known constraints'), ('Labor and equipment', 'Required skills, estimated effort, equipment availability, and subcontractor dependencies'), ('Materials', 'Selections, approved substitutions, order owner, and expected availability'), ('Acceptance', 'Production review, unresolved questions, and confirmed customer next step')],
 procedure=['Estimator prepares the brief from the accepted documents and flags assumptions that need confirmation.', 'Production lead checks feasibility and returns missing information with a named owner.', 'Coordinator confirms the agreed start conditions and communicates the schedule after the readiness decision.'],
 example='Illustrative example: a remodeling estimate assumes clear driveway access for material delivery. The production review finds a restricted access window. The coordinator resolves staging and revises the delivery plan before the crew is scheduled, rather than discovering the issue on arrival.',
 exception='If drawings, selections, or access remain unresolved, record the blocker and the next decision date. Do not turn an estimated start into a firm promise while a critical prerequisite is unknown.',
 measure='Track returned handoffs, unscheduled mobilization delays, and changes caused by missing estimate information. Separate customer-requested changes from estimating omissions.',
 template='sales-to-operations-handoff-checklist', service='business-process-mapping', case='construction-operating-cadence'),
 dict(slug='construction-crew-capacity-planning', title='Construction Crew Capacity Planning by Skill and Week', industry='construction-trades',
 intro='Construction crew capacity planning matches committed jobs with the specific skills, supervision, equipment, and workable site time available. A headcount total can hide the one trade or supervisor constraining the schedule.',
 trigger='Update the plan when a job is accepted, a prerequisite moves, or labor availability changes. Use the same weekly cutoff for demand and capacity so the comparison is meaningful.',
 rows=[('Crew or skill', 'Separate skills that cannot substitute for one another'), ('Available time', 'Scheduled time less leave, training, travel allowances, and other committed work'), ('Job demand', 'Remaining effort by skill and planned week'), ('Readiness', 'Materials, access, inspections, or other prerequisites affecting the work window'), ('Decision', 'Resequence, add approved support, or revise a customer commitment')],
 procedure=['Estimate remaining effort with the foreman rather than repeating the original estimate unchanged.', 'Compare demand against availability for each constrained skill and key equipment item.', 'Resolve overload before accepting another date; record the person authorized to change the plan.'],
 example='Illustrative example: two crews have enough combined hours, but only one foreman can supervise the next installation. Scheduling both jobs concurrently would create a supervision conflict. The planner sequences the work and confirms the revised dates with customers.',
 exception='Weather and unavailable prerequisites can strand capacity. Keep a small list of genuinely ready alternate work, and avoid assuming every lost hour can be recovered through overtime.',
 measure='Review promised versus actual start dates, idle time by cause, and overtime. A fuller calendar is not an improvement if rework and missed commitments rise.',
 template='service-business-capacity-planning-template', service='multi-location-operations', case='construction-operating-cadence'),
 dict(slug='construction-change-order-approval', title='Construction Change Order Approval Workflow', industry='construction-trades',
 intro='A change order approval workflow connects a requested field change with the accepted scope, estimated impact, customer decision, and updated job plan. It makes the effect on labor, materials, and timing visible before work proceeds.',
 trigger='Open a change record when a request or discovered condition could alter the agreed work. The contract and responsible advisers determine formal notice and approval requirements; the operating workflow should make those responsibilities visible.',
 rows=[('Change description', 'Requested work and the original scope reference'), ('Field evidence', 'Photos, measurements, or notes supporting the request'), ('Impact estimate', 'Labor, materials, subcontractors, schedule, and affected work'), ('Decision evidence', 'Required internal and customer approvals'), ('Job update', 'Revised crew instructions, purchasing action, and billing reference')],
 procedure=['Field lead records the condition and follows the agreed stop or escalation rule.', 'Estimator or project manager assesses scope and delivery effects, including dependencies.', 'Authorized approval is recorded and the coordinator updates production and billing together.'],
 example='Illustrative example: a customer requests a different finish after material has been ordered. The manager identifies the substitution, possible return costs, and schedule implications. Approval addresses those items before purchasing changes the order and the foreman changes the work plan.',
 exception='Urgent safety concerns follow the applicable safety procedure; commercial approval should not be used as a reason to ignore an immediate hazard. Keep emergency action and subsequent change documentation coordinated through responsible roles.',
 measure='Track unapproved additional hours, approval turnaround, and changes missing billing references. Repeated change types can reveal unclear scope language for future estimates.',
 template='change-order-process-template-service-business', service='client-onboarding-systems', case='construction-operating-cadence'),
 dict(slug='professional-services-scope-to-invoice', title='Professional Services Scope-to-Invoice Workflow', industry='professional-services',
 intro='A scope-to-invoice workflow links what was sold, what was delivered, what the client accepted, and what finance can bill. It is useful for agencies, consultancies, and other firms where extra effort can disappear between project management and invoicing.',
 trigger='Create the project record from the accepted scope. Billing milestones and customer acceptance requirements should be visible before the team begins delivery.',
 rows=[('Commercial baseline', 'Accepted scope, fee basis, exclusions, and billing milestones'), ('Delivery plan', 'Work packages, owners, dependencies, and expected effort'), ('Scope changes', 'Requests, estimates, approval evidence, and revised work'), ('Completion evidence', 'Deliverable status and agreed acceptance record'), ('Invoice readiness', 'Approved charges, billing contact, reference information, and open issues')],
 procedure=['Project manager checks that the delivery plan matches the scope and billing structure.', 'Team records actual effort and flags scope requests while there is time to resolve them.', 'Project and finance owners reconcile completion, approved changes, and invoice prerequisites.'],
 example='Illustrative example: a client adds a workshop midway through a project. The delivery team records the request and obtains acceptance for the additional session. At closeout, finance can trace the approved addition to a delivered workshop and the invoice line.',
 exception='If acceptance or a billing prerequisite is missing, assign the item rather than labeling the project fully closed. Keep commercial disputes separate from administrative missing information.',
 measure='Review unbilled approved work, time between milestone completion and invoice readiness, and quoted versus actual effort. Use a consistent margin definition with finance.',
 template='professional-services-project-closeout-checklist', service='client-onboarding-systems', case='professional-services-close-rate'),
 dict(slug='professional-services-recurring-client-capacity', title='Capacity Planning for Recurring Professional Services Clients', industry='professional-services',
 intro='Recurring-client capacity planning looks beyond this week’s project list. It reserves the skills and review time needed for repeat commitments, seasonal demand, onboarding, and exception work.',
 trigger='Review capacity before adding a retainer, changing a service package, or approving leave during a busy period. Count recurring obligations even when individual tasks have not yet been created.',
 rows=[('Client commitment', 'Deliverables, service frequency, and agreed response responsibilities'), ('Role demand', 'Preparation, production, review, and client communication effort'), ('Timing pattern', 'Monthly peaks, deadlines, and known seasonality'), ('Available capacity', 'Role hours after leave, internal work, and existing commitments'), ('Acceptance decision', 'Start date, staffing change, adjusted scope, or waitlist decision')],
 procedure=['Translate service packages into recurring work by role and period.', 'Compare actual effort with planned effort for a representative client sample.', 'Test the next client against the constrained role, including onboarding and review demand.'],
 example='Illustrative example: junior staff have spare capacity but the senior reviewer is fully committed. Selling another recurring package without adjusting review capacity creates a bottleneck despite apparent headcount availability. The firm changes the start date or adds qualified review coverage.',
 exception='Client delays can bunch work into the same week. Record input deadlines and the effect of late inputs on scheduling; do not assume all deferred work can be completed at once.',
 measure='Track backlog by role, deadline reliability, and review corrections. Compare recurring fees with delivery effort under a consistent cost method before assuming every additional client improves contribution.',
 template='service-business-capacity-planning-template', service='kpi-dashboard-setup', case='professional-services-close-rate'),
 dict(slug='professional-services-client-renewal', title='Client Renewal Workflow for Professional Services Firms', industry='professional-services',
 intro='A client renewal workflow connects delivered value, unresolved issues, future needs, and commercial approval before the end of an agreement. It gives the team time to resolve a delivery concern rather than discovering it during a renewal request.',
 trigger='Choose the review date from the actual agreement and the client’s decision process. Work backward from any relevant notice or approval deadline instead of using one generic reminder for every account.',
 rows=[('Agreement record', 'Term, scope, relevant dates, and the owner of commercial review'), ('Delivery evidence', 'Completed commitments, open issues, and client feedback'), ('Client decision map', 'Working contact, budget owner, and required reviewers'), ('Next-period scope', 'Changed needs, capacity implications, and proposed exclusions'), ('Outcome', 'Renewed scope, revised plan, non-renewal, or unresolved decision')],
 procedure=['Account owner reviews the current delivery record with the project lead.', 'Discuss the client’s priorities and unresolved concerns before presenting the next scope.', 'Record the decision and update delivery, billing, and access arrangements through the appropriate process.'],
 example='Illustrative example: a recurring client wants faster turnaround next quarter. The team reviews the present response pattern and staffing before proposing a new commitment. Renewal becomes a scope and capacity decision, not an automatic continuation of an outdated package.',
 exception='Do not assume silence equals acceptance. Follow the agreement and approved commercial process, and assign responsibility for uncertain or disputed terms to the appropriate person.',
 measure='Track reviews completed before decision deadlines, unresolved delivery concerns, and documented renewal reasons. Separate voluntary non-renewal from cases where the firm deliberately exits a poor fit.',
 template='project-margin-review-template-service-firms', service='sales-process-implementation', case='professional-services-close-rate'),
 dict(slug='manufacturing-production-scheduling-handoff', title='Manufacturing Order-to-Production Scheduling Handoff', industry='manufacturing',
 intro='An order-to-production handoff verifies that an accepted order has the information, material readiness, routing, and capacity needed for scheduling. It distinguishes an order in the system from an order ready for release.',
 trigger='The commercial order is accepted, but release follows a readiness review appropriate to the operation. Requirements depend on the product and production environment; use approved technical and quality controls.',
 rows=[('Order definition', 'Current specification, quantities, required dates, and approved revisions'), ('Routing', 'Required operations, sequence, setup needs, and responsible work centers'), ('Material readiness', 'Availability, purchasing status, and approved alternatives'), ('Capacity review', 'Constraint work center, expected effort, and planned release window'), ('Release decision', 'Accepted, blocked, or conditionally released with a responsible approver')],
 procedure=['Planning verifies that the order information agrees with the current approved specification.', 'Production and purchasing review the constraints affecting the release window.', 'The authorized owner releases the job and records unresolved conditions through the approved exception process.'],
 example='Illustrative example: an order has sufficient assembly capacity but a required upstream operation is fully loaded. Planning checks that work center before confirming a ship commitment and sequences the order around the actual constraint.',
 exception='A missing revision or unresolved quality requirement should reach the appropriate technical owner. Avoid informal substitutions or schedule promises that bypass required approval.',
 measure='Track jobs released with missing prerequisites, schedule changes by cause, and waiting time at the constrained work center. Review whether better release discipline reduces expediting.',
 template='vendor-performance-scorecard-template-small-business', service='business-process-mapping', case='manufacturing-delivery-delays'),
 dict(slug='manufacturing-order-change-control', title='Manufacturing Order Change Control Workflow', industry='manufacturing',
 intro='Manufacturing order change control links a commercial request to the production version actually in use. It makes effects on purchasing, work in progress, inspection, scheduling, and customer commitments visible to the responsible decision makers.',
 trigger='Start a change record when quantity, specification, date, or routing may differ from the accepted order. Use the operation’s approved technical and quality process for formal revision control.',
 rows=[('Requested change', 'Order reference, current version, proposed difference, and requestor'), ('Work status', 'Purchased material, released work, completed operations, and affected inventory'), ('Impact review', 'Cost, timing, technical approval, quality, and customer effects'), ('Approval record', 'Authorized commercial and technical decisions as applicable'), ('Communication', 'Updated records and acknowledgement by affected roles')],
 procedure=['Customer-facing staff record the request without promising feasibility.', 'Planning and responsible specialists identify affected work and required decisions.', 'After approval, the owner updates the controlled records and verifies that affected teams received the current instructions.'],
 example='Illustrative example: a buyer changes quantity after a job is released. Planning checks material availability and the constrained operation, while finance and commercial owners review the change in terms. The accepted decision is communicated to production rather than remaining in a seller’s email.',
 exception='If old and new instructions conflict, escalate to the designated owner before proceeding with affected work. Keep the traceable decision in the approved system rather than relying on a chat message.',
 measure='Review changes discovered after release, schedule disruptions caused by late communication, and obsolete instructions found in active work. Investigate the handoff that failed rather than only the final error.',
 template='change-order-process-template-service-business', service='business-process-mapping', case='manufacturing-delivery-delays'),
 dict(slug='manufacturing-late-order-recovery', title='Manufacturing Late Order Recovery and Escalation Plan', industry='manufacturing',
 intro='A late-order recovery plan gives each delayed order a verified cause, feasible next step, owner, and communication commitment. It helps the team distinguish useful recovery action from repeated expediting that moves delays to other customers.',
 trigger='Open a recovery review when the current plan can no longer support the committed date. Confirm the remaining work and prerequisites before issuing a revised promise.',
 rows=[('Current status', 'Completed operations, remaining work, material status, and quality holds'), ('Constraint', 'The specific condition preventing progress'), ('Recovery options', 'Resequence, qualified additional capacity, approved alternative, or revised commitment'), ('Impact check', 'Effects on other orders, cost, quality, and required approvals'), ('Customer update', 'Responsible contact, confirmed information, and next update time')],
 procedure=['Validate the order status with production records and the people doing the work.', 'Choose a feasible recovery option with the required technical, quality, and commercial approvals.', 'Communicate the plan and review whether the action actually changed the constraint.'],
 example='Illustrative example: a missing purchased component is blamed for a late order. The recovery review discovers that a constrained machining step also lacks capacity. Expediting the component alone would not restore the date, so planning addresses both dependencies before proposing a revised commitment.',
 exception='Do not quietly prioritize one urgent order without checking downstream effects. Record which commitments move and who approves the tradeoff; qualified quality and safety controls remain applicable during recovery.',
 measure='Track repeat date changes, recovery actions completed, and causes of lateness. Compare due-date cohorts consistently so rescheduling does not make late orders disappear from the measure.',
 template='weekly-operations-scorecard-template-service-business', service='kpi-dashboard-setup', case='manufacturing-delivery-delays'),
]


def industry_pages():
    return [guide(w['slug'], w['title'], w['intro'].split('. ')[0] + '.', w['intro'], [
        ('Define the start and finish', p(w['trigger'])),
        ('Workflow record and acceptance checklist', table(w['title'], ['Record', 'Information required'], w['rows'])),
        ('Run the workflow', ul(w['procedure'], True)),
        ('Worked example', p(w['example'])),
        ('Handle the exception explicitly', p(w['exception'])),
        ('Measures to review', p(w['measure'])),
        ('Pilot before standardizing', p('Test this workflow on a small set of real cases with the people who send and receive the work. Keep a record of missing information and decisions that were unclear. Assign one owner to revise the operating instructions, then review the next completed case against the revised version.')),
    ], ['/industries/' + w['industry'] + '/', '/services/' + w['service'] + '/', '/blog/' + w['template'] + '/', '/case-studies/' + w['case'] + '/'], kind='Industry workflow') for w in WORKFLOWS]


PLAYBOOKS = [
 dict(slug='crm-rollout', title='Small Business CRM Rollout Playbook',
 intro='Roll out a CRM in controlled stages: define the process, reconcile a sample, pilot real use, then cut over with a fallback. Use this playbook to organize ownership and acceptance rather than scheduling only configuration tasks.',
 phases=[('Define the workflow', 'Sales lead and delivery counterpart', 'Agree lead ownership, stages, buyer evidence, next-action rules, and the delivery handoff.', 'Two users can classify the same opportunity and explain the next action.'), ('Prepare the data', 'Data owner and administrator', 'Export a recoverable source, set duplicate rules, and map required fields and relationships.', 'Sample counts, ownership, activities, and associations reconcile.'), ('Pilot the setup', 'Small seller group', 'Test inquiry routing, follow-up, reporting, permissions, and failed integration handling.', 'Real users complete representative scenarios and record exceptions.'), ('Cut over and stabilize', 'Business sponsor', 'Confirm the system of record, freeze conflicting updates as appropriate, and operate a visible support queue.', 'The team can run the workflow and the administrator can maintain it.')],
 example='Illustrative example: a firm pilots with one seller and one delivery manager. A test lead routes correctly, but the signed deal does not include the promised start dependency. The team fixes the handoff before importing the rest of the active pipeline.',
 stop='Pause expansion if key records do not reconcile, critical permission boundaries fail, or the team cannot identify the system of record. Use a documented recovery plan appropriate to the migration; do not improvise rollback after live data has diverged.',
 sustain='Assign ownership for field changes, new-user training, integration exceptions, and stage definitions. Review data quality after the pilot so cleanup does not become a recurring rescue project.',
 links=['/services/crm-implementation/', '/services/crm-cleanup/', '/guides/crm-implementation-cost-small-business/', '/blog/crm-data-cleanup-checklist-small-business/']),
 dict(slug='sop-rollout', title='SOP Implementation and Rollout Playbook',
 intro='A procedure library changes operations only when people can find, use, and improve it. This SOP rollout playbook tests a small set of procedures before expanding documentation across the company.',
 phases=[('Select a pilot process', 'Process owner', 'Choose repeated work with a clear trigger, finish, and known error pattern.', 'The team agrees which task and intended user the procedure covers.'), ('Capture and validate', 'Experienced operator', 'Observe the work, write decision rules, and obtain the required subject-matter review.', 'Instructions reflect approved practice and identify when to stop.'), ('Test with a backup', 'Qualified intended user', 'Attempt a complete representative task and record questions and missing information.', 'The backup completes the task under the appropriate supervision.'), ('Publish and maintain', 'Document owner', 'Store the current version, retire conflicting copies, and define change triggers.', 'Users can locate the approved version and know how to report a gap.')],
 example='Illustrative example: a scheduling procedure says to prioritize urgent work but never defines urgency. A backup test exposes the missing rule. The manager adds a decision boundary and escalation contact before the procedure becomes the team standard.',
 stop='Do not publish a procedure as approved when a technical or safety decision is unresolved. Distinguish a draft from a usable operating instruction and preserve the appropriate review responsibilities.',
 sustain='Use software changes, role changes, repeated errors, and practice failures as review triggers. Record the last test date as well as the last edit date; a recent edit does not prove the procedure works.',
 links=['/services/sop-documentation/', '/guides/sop-documentation-cost/', '/blog/employee-cross-training-matrix-template/', '/examples/business-process-map/']),
 dict(slug='operations-manager-first-90-days', title='First Operations Manager: A 90-Day Onboarding Plan',
 intro='The first operations manager needs authority, context, and a manageable operating rhythm. This illustrative 90-day plan organizes the transition; adapt the timing to the business and the manager’s experience.',
 phases=[('Before the start', 'Owner', 'Define role outcomes, decision limits, direct reports, and access. Identify critical customer commitments.', 'The manager knows what they own and what remains with the owner.'), ('Days 1–30: understand', 'Manager with team leads', 'Observe real workflows, baseline current commitments, and record recurring exceptions.', 'A short constraint list is supported by records and operator input.'), ('Days 31–60: pilot', 'Manager and process owner', 'Improve one bounded workflow, establish a small scorecard, and run an exception review.', 'The pilot has evidence, an acceptance decision, and a maintenance owner.'), ('Days 61–90: transfer', 'Owner and manager', 'Test delegated decisions and backup coverage; revise unclear authority.', 'Routine decisions remain with the manager within agreed limits.')],
 example='Illustrative example: an owner hires a manager to improve delivery but still approves every scheduling change. The first review identifies this authority gap. The owner and manager agree on scheduling boundaries and examine exceptions after decisions instead of approving every normal change.',
 stop='If the manager lacks necessary authority, access, or qualified support, resolve those constraints before holding them accountable for outcomes they cannot influence. Avoid replacing all inherited systems during the first weeks.',
 sustain='Agree how the owner reviews performance without taking back daily decisions. Keep a visible list of unresolved responsibilities and revisit it as the manager demonstrates readiness.',
 links=['/guides/consultant-vs-operations-manager/', '/services/owner-dependency-reduction/', '/blog/decision-rights-matrix-small-business-template/', '/blog/owner-vacation-business-continuity-checklist/']),
 dict(slug='second-location-opening', title='Second Location Opening: Operations Readiness Playbook',
 intro='Opening a second location tests whether the first location’s performance depends on repeatable systems or a few people’s memory. This playbook covers operational readiness alongside the specialist reviews needed for an opening decision.',
 phases=[('Verify the transferable model', 'Owner and first-site manager', 'Document the workflows, roles, economics, and local conditions behind the first site.', 'The team can distinguish repeatable practice from location-specific advantages.'), ('Prepare people and coverage', 'Receiving manager', 'Assign local authority, train backups, and test central support arrangements.', 'The site can resolve normal decisions without waiting for the founder.'), ('Rehearse the operation', 'Local team and support leads', 'Test intake, scheduling, purchasing, delivery, escalation, and reporting.', 'Critical scenarios work with the people and systems that will operate the site.'), ('Open with a stabilization plan', 'Opening sponsor', 'Track constraints, support requests, staffing, and customer commitments.', 'The site has a clear escalation path and a review cadence.')],
 example='Illustrative example: the original site relies on its manager to approve every unusual order. Before opening the second site, the team documents normal acceptance limits and creates a central escalation path for exceptions. The new manager tests both routes during rehearsal.',
 stop='Do not treat this checklist as approval of the location’s financial, property, licensing, employment, or safety readiness. Resolve required specialist approvals and critical operating gaps before opening.',
 sustain='Compare sites using shared definitions with context for demand and staffing. Keep early support work visible so a successful opening does not quietly overload the original location.',
 links=['/services/multi-location-operations/', '/blog/multi-location-manager-scorecard-template/', '/tools/service-capacity-calculator/', '/services/leadership-operating-cadence/']),
 dict(slug='post-acquisition-operations', title='Post-Acquisition Operations Integration Playbook',
 intro='After an acquisition, protect current commitments while learning how the business actually runs. This operations integration playbook sequences continuity, evidence gathering, a bounded improvement, and handover without assuming every inherited system must change.',
 phases=[('Protect continuity', 'Incoming operator', 'Confirm customer deadlines, essential contacts, authorized access, and critical task coverage.', 'People know who owns the next decision and where to raise an urgent issue.'), ('Understand the current operation', 'Operator and team leads', 'Trace recent work, listen to staff, and compare reports with source records.', 'Key constraints are supported by evidence rather than first impressions.'), ('Pilot one integration change', 'Responsible manager', 'Choose a reversible workflow improvement with a baseline and fallback.', 'The team can show what changed and whether it helped the agreed outcome.'), ('Standardize selectively', 'Leadership team', 'Adopt useful common definitions and document necessary local variation.', 'An internal owner can sustain the practice after transition support ends.')],
 example='Illustrative example: the buyer wants to replace scheduling software immediately. Interviews reveal that one coordinator holds essential customer-access knowledge outside the system. The operator captures and validates that knowledge before testing a new scheduling workflow.',
 stop='Pause changes that could disrupt essential delivery or conflict with transaction, employment, access, or contractual requirements. Coordinate those matters with the responsible advisers; this is an operating sequence rather than transaction advice.',
 sustain='Maintain a decision log with the reason, owner, affected workflow, and review date. Track unresolved employee questions and delivery exceptions so integration work does not obscure the health of the underlying business.',
 links=['/blog/post-acquisition-employee-transition-checklist/', '/services/operational-assessment/', '/services/business-process-mapping/', '/examples/operations-assessment-report/']),
 dict(slug='founder-sales-handoff', title='Founder-Led Sales Handoff Playbook for a Small Team',
 intro='Handing sales to a team requires more than transferring a contact list. Capture customer fit, buying triggers, discovery evidence, offer boundaries, and the decisions the founder currently makes from memory.',
 phases=[('Capture the founder’s judgment', 'Founder and first seller', 'Review real wins, losses, and poor-fit customers; record evidence behind each decision.', 'The seller can explain fit and disqualification using examples.'), ('Define the offer and process', 'Sales lead and delivery lead', 'Set scope boundaries, stages, proposal approvals, and delivery acceptance rules.', 'The seller knows what can be promised and when approval is required.'), ('Practice together', 'Founder and seller', 'Observe calls, then have the seller lead while the founder reviews decisions.', 'The seller can run representative conversations and record useful next actions.'), ('Transfer with review', 'Sales manager', 'Review pipeline evidence, exceptions, and handoff quality on a defined cadence.', 'The founder intervenes at agreed boundaries rather than in every deal.')],
 example='Illustrative example: the founder can recognize customers whose requested timeline is unrealistic, but the first seller cannot. The team documents delivery prerequisites and adds an operations review before promising a compressed date.',
 stop='Do not remove founder involvement solely because a calendar date has arrived. If the seller cannot qualify fit, explain the offer, or respect delivery boundaries, identify the missing training or rule and retest.',
 sustain='Keep a shared library of objections, loss reasons, scope questions, and delivery feedback. Update the playbook as the team learns instead of treating the founder’s current approach as permanently complete.',
 links=['/services/sales-process-implementation/', '/blog/sales-pipeline-stages-and-exit-criteria-for-owner-led-companies/', '/blog/sales-to-operations-handoff-checklist/', '/services/crm-implementation/']),
]


def playbook_pages():
    return [guide(b['slug'], b['title'], b['intro'].split('. ')[0] + '.', b['intro'], [
        ('Phases, owners, and acceptance gates', table(b['title'], ['Phase', 'Owner', 'Work', 'Acceptance evidence'], b['phases'])),
        ('Before the first working session', p('Name a sponsor who can resolve competing priorities and a manager who will maintain the result. Gather a recent normal case, an exception, and the current instructions. Reserve time for the people doing the work; a plan cannot be validated entirely through leadership discussion.')),
        ('Worked example', p(b['example'])),
        ('When to pause or revise the plan', p(b['stop'])),
        ('A practical review rhythm', p('At each phase boundary, review completed evidence, unresolved decisions, and the next owner. If a prerequisite is missing, record who will resolve it and when the team will review it again. Keep acceptance separate from effort spent: a completed meeting is not proof that the new workflow can operate.')),
        ('Handover and continuing ownership', p(b['sustain'])),
    ], b['links'], kind='Implementation playbook', parent='/playbooks/') for b in PLAYBOOKS]


SAMPLES = {
    'operations-assessment-report': {
        'title': 'Sample Operations Assessment Report With Action Plan',
        'caption': 'Illustrative assessment: a fictional service firm',
        'headings': ['Finding', 'Evidence in this example', 'Interpretation', 'Next action', 'Owner'],
        'rows': [
            ['Incomplete delivery handoffs', 'Three of five sampled jobs lacked a recorded prerequisite', 'The receiving team cannot reliably confirm readiness', 'Pilot a minimum accepted handoff on the next five jobs', 'Delivery manager'],
            ['Unclear scope approval', 'Two sampled jobs included extra work without an approval record', 'The team has no shared boundary for additional requests', 'Define request, estimate, and acceptance steps', 'Project lead'],
            ['Capacity measured as headcount', 'The weekly plan does not separate preparation and review roles', 'Review availability may constrain delivery despite spare general hours', 'Compare next-week demand and available hours by role', 'Operations manager'],
            ['No common due-date definition', 'Two reports use different rules for rescheduled jobs', 'The current trend cannot be compared consistently', 'Agree a due-week cohort definition and reconcile a sample', 'Scorecard owner'],
        ],
    },
    'business-process-map': {
        'title': 'Business Process Map Example: Sales to Delivery',
        'caption': 'Illustrative sales-to-delivery process map',
        'headings': ['Step', 'Owner', 'Input', 'Decision or action', 'Output / next step'],
        'rows': [
            ['1. Record accepted scope', 'Seller', 'Accepted agreement and discovery record', 'Capture scope, exclusions, dependencies, and promises', 'Handoff brief to delivery lead'],
            ['2. Check readiness', 'Delivery lead', 'Handoff brief and capacity plan', 'Are scope, access, and capacity sufficiently resolved?', 'Accept or return a named blocker'],
            ['3a. Resolve blocker', 'Assigned owner', 'Specific missing prerequisite', 'Obtain evidence or agree a revised commitment', 'Return to readiness check'],
            ['3b. Schedule kickoff', 'Coordinator', 'Accepted readiness decision', 'Confirm a feasible date and customer responsibilities', 'Customer receives owner, date, and next action'],
            ['4. Review first milestone', 'Project owner', 'Delivery record and acceptance criteria', 'Confirm progress and resolve any remaining handoff gap', 'Normal delivery or an owned exception'],
        ],
    },
    'weekly-operations-dashboard': {
        'title': 'Weekly Operations Dashboard Example With KPI Definitions',
        'caption': 'Illustrative weekly dashboard: fictional service team',
        'headings': ['Measure', 'Definition', 'Example value', 'Interpretation', 'Action owner'],
        'rows': [
            ['On-time due work', 'Jobs completed by agreed due date / jobs in the original due-week cohort', '18 / 20 = 90%', 'Two due commitments were missed; rescheduling does not remove them', 'Delivery lead'],
            ['Review capacity gap', 'Available review hours minus committed review demand', '30 - 38 = -8 hours', 'Resolve eight hours of review overload before promising more work', 'Operations manager'],
            ['Jobs requiring correction', 'Count of jobs with recorded correction work this week', '3 jobs', 'Inspect reasons and effort; this count is not a rate without a denominator', 'Quality owner'],
            ['Unaccepted handoffs', 'Closed-won jobs awaiting delivery acceptance at cutoff', '4 jobs', 'Assign the missing prerequisites before scheduling', 'Sales and delivery leads'],
            ['Overdue operating actions', 'Actions past due without closure evidence at cutoff', '2 actions', 'Resolve the dependency or revise the commitment openly', 'Leadership facilitator'],
        ],
    },
}


def sample_pages():
    return [
        guide('operations-assessment-report', SAMPLES['operations-assessment-report']['title'],
            'Read an illustrative operations assessment report with evidence, findings, priorities, owners, and a pilot acceptance plan. Download the sample CSV.',
            'This sample shows how an operations assessment can move from observations to a testable improvement plan. The company, records, and findings below are fictional teaching examples, not an Elixir client engagement.', [
                ('Scope and method for this example', p('The fictional assessment follows five recent service jobs from accepted sale to first delivery milestone. The sample includes completed and delayed jobs. It is deliberately small: the findings identify questions and pilot opportunities, not statistically representative conclusions about an entire business.')),
                ('Findings and evidence register', table(SAMPLES['operations-assessment-report']['caption'], SAMPLES['operations-assessment-report']['headings'], SAMPLES['operations-assessment-report']['rows'])),
                ('Choose the first intervention', p('In this example, the first pilot is the accepted handoff because missing prerequisites appear before delivery begins and the team can test a change without replacing software. The sponsor assigns a delivery manager, limits the pilot to the next five jobs, and records the readiness decision for each one. Other findings remain visible in the backlog.')),
                ('Define acceptance before the pilot', p('The pilot record must identify the receiving owner, scope reference, required customer inputs, capacity review, and any blocker. The manager checks whether the first milestone begins with fewer missing-information interruptions. A better checklist completion rate alone does not prove better delivery.')),
                ('Keep uncertainty visible', p('The review-capacity constraint remains a hypothesis until the team compares available hours and remaining demand by role. Staff observations are useful leads but should not be presented as measured time savings. The sample report separates findings, interpretations, and tests for this reason.')),
                ('How to adapt the sample', p('Replace the fictional evidence with traceable records from your own workflow. Keep the scope boundary, sample method, limitations, next action, and owner. Add specialist review where a proposed change touches technical, quality, safety, or professional responsibilities.')),
            ], ['/services/operational-assessment/', '/services/business-process-mapping/', '/case-studies/', '/tools/service-capacity-calculator/'], kind='Sample deliverable', parent='/examples/'),
        guide('business-process-map', SAMPLES['business-process-map']['title'],
            'Explore a text-based sales-to-delivery process map with owners, inputs, decisions, exception loops, and handoff acceptance. Download the sample CSV.',
            'This fictional sales-to-delivery process map shows the normal route and the exception loop in a small service business. It is an instructional sample, not a diagram of a particular client’s operation.', [
                ('Set the map boundary', p('The start is an accepted sale; the finish is a first milestone reviewed by the project owner. Lead generation, detailed delivery steps, and final billing sit outside this map. Limiting the boundary keeps the workshop focused on whether sold work can start responsibly.')),
                ('Read the process map', table(SAMPLES['business-process-map']['caption'], SAMPLES['business-process-map']['headings'], SAMPLES['business-process-map']['rows'])),
                ('The decision that matters', p('Step two separates a sold job from an accepted delivery handoff. If readiness is incomplete, the process returns a specific blocker to a named owner. It does not send a vague request to a department or silently proceed to scheduling. After the blocker is resolved, the case returns to the readiness decision.')),
                ('What this map intentionally leaves open', p('The sample does not prescribe exact staffing, a particular CRM, or a universal response deadline. Those depend on the business. The map identifies where those choices must become explicit: who accepts the work, what readiness means, and how the customer receives an agreed next step.')),
                ('Validate with an actual case', p('Select one ordinary job and one difficult job. Ask each participating role to walk the sequence and point to the source record used at each step. Add exceptions the sample omits, such as a cancellation or a changed start date. If two people describe different routes, record the disagreement and verify it rather than voting for the tidier diagram.')),
                ('From map to procedure', p('Once the sequence is agreed, write the instructions for the highest-risk decision or handoff. The map explains the relationship between steps; the procedure explains how an intended user performs a task. Link both to the same owner and review date so they do not drift apart.')),
            ], ['/services/business-process-mapping/', '/services/sop-documentation/', '/blog/sales-to-operations-handoff-checklist/', '/examples/operations-assessment-report/'], kind='Sample deliverable', parent='/examples/'),
        guide('weekly-operations-dashboard', SAMPLES['weekly-operations-dashboard']['title'],
            'Use a fictional operations dashboard to understand KPI formulas, source definitions, capacity gaps, exceptions, and weekly management actions.',
            'This fictional weekly dashboard illustrates how a service team can connect a few operating measures to decisions. The values are worked examples, not client results or benchmark targets.', [
                ('The operating question', p('The team wants to know whether it can meet upcoming commitments without hiding rework or overloading review capacity. Revenue alone cannot answer that question. The dashboard combines due work, a capacity constraint, quality exceptions, handoff readiness, and follow-through on actions.')),
                ('Dashboard and definition register', table(SAMPLES['weekly-operations-dashboard']['caption'], SAMPLES['weekly-operations-dashboard']['headings'], SAMPLES['weekly-operations-dashboard']['rows'])),
                ('Read the numbers together', p('The 90% completion rate shows that two jobs missed their agreed dates. It does not show why. The eight-hour review gap suggests a capacity issue to investigate, while the three correction jobs may add unplanned demand. The manager checks whether those observations concern the same jobs before choosing an action.')),
                ('Avoid misleading denominators', p('A count of three corrections cannot be described as a correction rate without an agreed denominator and cohort. Similarly, removing rescheduled work from the due-week cohort would make missed commitments disappear. Write the definition and reporting cutoff next to the measure before comparing trends.')),
                ('Run the weekly review', p('The owner of each exception states what happened, what evidence supports the explanation, and what decision is needed. Record the action, owner, and review date. Begin the next meeting with prior actions rather than starting a fresh list of issues.')),
                ('Use thresholds from your own operation', p('This sample does not establish a good utilization level, an acceptable defect rate, or a universal response target. Choose thresholds from your commitments, risk, staffing, and baseline history. Revisit them when the workflow or demand mix changes.')),
            ], ['/services/kpi-dashboard-setup/', '/blog/weekly-operations-scorecard-template-service-business/', '/tools/service-capacity-calculator/', '/services/leadership-operating-cadence/'], kind='Sample deliverable', parent='/examples/'),
    ]


TOOLS = {
    'service-capacity-calculator': dict(title='Service Business Capacity Calculator',
        intro='Compare available delivery hours with committed demand for one role and one planning period. Run the calculation separately for different skills; spare administrative hours cannot automatically cover a shortage of technical review time.',
        fields=[('people', 'People in this role', '3', '1', 'whole'), ('hours', 'Scheduled hours per person in the period', '40', '0.25', 'number'), ('unavailable', 'Total team hours unavailable for delivery', '30', '0.25', 'number'), ('buffer', 'Additional delivery buffer (%)', '10', '0.1', 'percent'), ('demand', 'Committed delivery demand (hours)', '95', '0.25', 'number')],
        formula='Scheduled team hours = people × hours per person. Delivery hours = scheduled team hours − unavailable hours. Planned capacity = delivery hours × (1 − buffer / 100). Capacity gap = planned capacity − demand.',
        example='With three people scheduled for 40 hours each and 30 total hours unavailable, there are 90 delivery hours before buffer. A 10% buffer leaves 81 planned hours. Against 95 hours of committed demand, the gap is −14 hours. The demand-to-capacity ratio is 117.3%; it is a planning signal, not a target.',
        interpretation='A negative gap calls for a scheduling or capacity decision. Verify the effort estimates and prerequisites, then consider resequencing, a revised commitment, or qualified support. A positive gap is not automatically sellable time if another required skill or dependency is constrained.',
        limits='Use total team unavailable hours, not unavailable hours per person. Do not count the same interruption both as unavailable time and in the buffer. The tool assumes one comparable role and period and does not model dependencies or scheduling order.',
        links=['/services/kpi-dashboard-setup/', '/blog/service-business-capacity-planning-template/', '/guides/professional-services-recurring-client-capacity/']),
    'project-margin-calculator': dict(title='Service Project Margin Calculator',
        intro='Calculate a project’s contribution after the delivery costs you enter. Use this direct-cost planning model to compare quoted and actual work; it is not a calculation of company net profit.',
        fields=[('revenue', 'Project revenue for this calculation ($)', '20000', '0.01', 'number'), ('laborHours', 'Delivery labor hours', '180', '0.25', 'number'), ('laborRate', 'Internal labor cost per hour ($)', '50', '0.01', 'number'), ('external', 'External project costs ($)', '3000', '0.01', 'number'), ('other', 'Other direct costs, not already counted ($)', '0', '0.01', 'number')],
        formula='Labor cost = delivery hours × internal hourly cost. Direct cost = labor cost + external costs + other direct costs. Contribution = project revenue − direct cost. Contribution margin = contribution / revenue × 100.',
        example='At $20,000 of revenue, 180 hours at an internal cost of $50 per hour create $9,000 of labor cost. Add $3,000 of external costs for $12,000 of total direct cost. Contribution is $8,000 and contribution margin is 40%. General overhead is not included unless you deliberately incorporate it in an entered cost.',
        interpretation='A negative contribution means entered direct costs exceed revenue. Compare planned and actual hours, purchased inputs, and scope changes before choosing a response. A margin percentage alone does not explain whether the cause was pricing, estimation, rework, or delivery efficiency.',
        limits='Use a consistent revenue and cost basis with finance. An employee’s billing rate is not an internal labor cost. Include owner delivery time if you want a replacement-cost view, and avoid duplicating costs in both the hourly rate and other fields. Zero revenue has no defined margin percentage.',
        links=['/blog/project-margin-review-template-service-firms/', '/guides/professional-services-scope-to-invoice/', '/services/operational-assessment/']),
    'rework-cost-calculator': dict(title='Rework Cost Calculator for Service Businesses',
        intro='Estimate the labor and cash cost associated with a defined set of correction incidents. This tool helps make recurring mistakes visible; it does not assume that every estimated cost can be eliminated or recovered.',
        fields=[('incidents', 'Correction incidents in the chosen period', '8', '1', 'whole'), ('hoursPer', 'Average correction labor hours per incident', '2', '0.25', 'number'), ('rate', 'Internal labor cost per hour ($)', '40', '0.01', 'number'), ('cashPer', 'Average additional cash expense per incident ($)', '25', '0.01', 'number'), ('credits', 'Total customer credits in this period ($)', '100', '0.01', 'number')],
        formula='Correction hours = incidents × average hours per incident. Labor cost = correction hours × internal hourly cost. Additional cash expense = incidents × average cash expense per incident. Modeled period cost = labor cost + additional cash expense + customer credits.',
        example='Eight correction incidents at two hours each consume 16 hours. At $40 per hour, labor cost is $640. Cash expenses of $25 per incident add $200, and total customer credits add $100. Modeled cost for the chosen period is $940. The tool does not multiply that result into an annual savings claim.',
        interpretation='Group incidents by cause before choosing an intervention. One missing review step may drive repeated corrections; a group of unrelated one-off issues may need a different response. Check whether preventing the work would release usable capacity or produce an actual cash saving.',
        limits='Use one clearly defined reporting period and count each incident consistently. Credits and cash expenses must be separate, with no duplicate counting. Fixed salary time is an opportunity-cost estimate unless payroll or productive capacity actually changes. Lost revenue and reputation effects are excluded.',
        links=['/services/business-process-mapping/', '/tools/project-margin-calculator/', '/examples/operations-assessment-report/']),
}


def tool_form(slug, tool):
    fields = ''
    for key, label, value, step, kind in tool['fields']:
        maximum = ' max="100"' if kind == 'percent' else ''
        fields += (f'<div class="calc-field"><label for="{key}">{e(label)}</label>'
                   f'<input id="{key}" name="{key}" type="number" min="0"{maximum} step="{step}" value="{value}" required inputmode="decimal"></div>')
    return (f'<form class="calculator" data-calculator="{slug}"><div class="calc-grid">{fields}</div>'
            '<p><button class="btn btn-primary" type="submit" data-calculate disabled>Calculate</button> <button class="btn btn-outline" type="reset">Reset example</button> <button class="btn btn-outline" type="button" data-export disabled>Download result CSV</button></p>'
            '<div class="calc-output" role="status" aria-live="polite" aria-atomic="true"><p>Enter your assumptions, then choose Calculate. Results stay in this browser and are not submitted to Elixir.</p></div>'
            '<noscript><p>The interactive calculator requires JavaScript. You can still use the formula and worked example below.</p></noscript></form>')


def tool_pages():
    return [guide(slug, t['title'], t['intro'].split('. ')[0] + '.', t['intro'], [
        ('Enter your assumptions', tool_form(slug, t)),
        ('Formula and units', p(t['formula'])),
        ('Worked example', p(t['example'])),
        ('How to use the result', p(t['interpretation'])),
        ('Assumptions and limits', p(t['limits'])),
        ('Turn the estimate into an operating decision', p('Use source records where possible and label estimates you cannot yet verify. Save the result with the planning period and the person responsible for checking assumptions. After a real operating cycle, compare the estimate with what happened and update the underlying process before treating the model as reliable.')),
    ], t['links'], kind='Calculator', parent='/tools/') for slug, t in TOOLS.items()]


def all_pages():
    from commercial_content import commercial_pages
    return service_pages() + buying_pages() + industry_pages() + playbook_pages() + sample_pages() + tool_pages() + commercial_pages()
