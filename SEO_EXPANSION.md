# Elixir search-intent expansion

The combined expansion adds 102 URLs: the original 19-page template library, the 43-page implementation batch below, and a subsequent 40-page commercial-intent batch.

| Content | URLs | Purpose |
| --- | ---: | --- |
| Specific implementation services | 12 | Define fit, scope, deliverables, inputs, and acceptance |
| Buying and comparison guides | 6 | Explain costs, responsibilities, and engagement choices |
| Industry workflows | 9 | Address construction, professional-services, and manufacturing problems |
| Implementation playbooks | 6 | Sequence work with owners and acceptance gates |
| Sample deliverables | 3 | Explain fictional assessment, process-map, and dashboard examples |
| Calculators | 3 | Model service capacity, project contribution, and correction costs |
| Discovery hubs | 4 | Connect guides, tools, playbooks, and examples |

`scripts/expansion-manifest.json` lists 83 implementation and commercial URLs, content types, parents, related pages, and source identifiers. The 19 original template pages are validated separately. `expansion_content.py` and `commercial_content.py` contain the authored copy. Topic selection reflects distinct operating questions and the services described on the existing site; it is not backed by measured keyword volumes or a ranking forecast.

## Commercial-intent batch

| Content | New URLs | Purpose |
| --- | ---: | --- |
| Comparisons | 10 | Compare operating support and processes, plus HubSpot/Pipedrive, Zoho/monday CRM, and Trainual/Process Street |
| Alternatives | 8 | Evaluate alternatives to hiring, frameworks, coaching, migration, and software choices |
| Pricing guides | 8 | Six vendor subscription/quote guides and two custom implementation scope guides |
| Curated lists | 10 | Selection criteria, deliverables, checks, tools, metrics, and implementation readiness |
| Hubs | 4 | `/compare/`, `/alternatives/`, `/pricing/`, and `/lists/` |

`data/commercial-sources.json` records official URLs, the review date, and observations. Software facts and fit judgments are distinguished in visible copy. Comparisons are editorial selection guides, not claims of hands-on software testing or vendor certification. No invented ratings or competitor engagement results are used.

Pipedrive and Zoho annual USD figures were separately verified in their live US browser views because text extraction returned regional currencies or omitted prices. Only verified annual figures are used for those tables. HubSpot promotions and adjacent billing figures are qualified rather than assumed to apply universally. monday CRM figures are tied to the reviewed yearly/ten-seat view, with no unsupported seat-minimum claim. Trainual and Process Street use quote requirements rather than historical dollar amounts that were not verified. Elixir implementation fees remain explicitly custom-scoped, separate from vendor subscriptions.

All ten curated lists have matching visible counts, anchored entries, and ItemList data. Resource hubs also describe their visible listings with ItemList data. Comparison and pricing pages do not claim review stars, product offers, or guaranteed search-result treatments.

## Build and maintenance

Run `python3 scripts/build-expansion.py` after editing the authored copy. It rebuilds these pages, sample CSVs, search entries, and the expansion sitemap. It adds marked discovery sections to selected existing pages and footer links across the site. Repeating it produces identical output.

The renderer uses the existing operations page for the shared header, styles, footer, and global organization graph. It removes that page's specific schemas and replaces its title, metadata, canonical, main content, and breadcrumbs. Calculators load one local script; no input is submitted to a server. Calculate remains disabled without JavaScript, while formulas and worked examples remain readable.

The core `generate_site.py` runs the expansion builder after writing core assets so the new routes, contextual links, sitemap entry, and search records survive a full rebuild. The core generator has broader pre-existing effects on old pages, so use the focused expansion builder for this release. Existing static Vercel deployment settings remain unchanged.

The three sample CSVs contain fictional teaching data and say so in both page copy and download. The capacity worksheet's unavailable time is a **team total**. The margin tool calculates contribution under the entered direct-cost basis, not company net profit. Rework cost is for the user-defined period and does not claim annual savings.

## Validation

```sh
python3 scripts/verify-expansion.py
python3 scripts/verify-commercial.py
python3 scripts/validate-long-tail.py
node --test scripts/calculators.test.cjs
git diff --check
```

The implementation batch used `python3 scripts/verify-expansion.py --compare-ref 6d2c5ed` to check preservation of existing HTML copy and styles outside marked additions. The commercial batch uses `--compare-ref c255540` and normalizes marked sections in both revisions; authored resource routes are allowed to gain intentional cross-links. Repeated focused builds are byte-stable. Full generator builds are verified in isolated copies with deployment settings retained.

Browser checks covered all three worked calculations, invalid capacity input, zero revenue, export invalidation after editing, CSV download contents, desktop layout, and a 390px phone viewport. The tested calculator and sample-table pages had no horizontal page overflow; the wide sample table scrolls within its region.

Commercial-page browser checks covered the desktop pricing layout and 390px pricing, comparison, and shortlist layouts. Pricing tables remained inside their scroll regions. Section anchor targets use the section's existing scroll margin so headings remain below the fixed header; the comparison anchor was measured at approximately 110px with a 102px header. The temporary phone viewport was reset after testing.

## Editorial boundaries and follow-up

No market fee ranges, vendor certifications, new client outcomes, or guaranteed performance claims were invented. Service fees and exact responsibilities require an agreed scope. Existing case-study narratives were preserved and linked to relevant workflows; no new evidence was fabricated.

After deployment, evaluate the new URL groups using Search Console impressions, query intent, organic consultation inquiries, and useful tool engagement. Use observed overlap before consolidating existing articles. Additional documented case studies require actual engagement records and permission to publish their details.
