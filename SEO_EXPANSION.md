# Elixir search-intent expansion

This release adds 43 URLs to the earlier 19-page template expansion:

| Content | URLs | Purpose |
| --- | ---: | --- |
| Specific implementation services | 12 | Define fit, scope, deliverables, inputs, and acceptance |
| Buying and comparison guides | 6 | Explain costs, responsibilities, and engagement choices |
| Industry workflows | 9 | Address construction, professional-services, and manufacturing problems |
| Implementation playbooks | 6 | Sequence work with owners and acceptance gates |
| Sample deliverables | 3 | Explain fictional assessment, process-map, and dashboard examples |
| Calculators | 3 | Model service capacity, project contribution, and correction costs |
| Discovery hubs | 4 | Connect guides, tools, playbooks, and examples |

`scripts/expansion-manifest.json` lists the exact URLs, content types, parents, and related pages. `expansion_content.py` contains the authored copy. Topic selection reflects distinct operating questions and the services described on the existing site; it is not backed by measured keyword volumes or a ranking forecast.

## Build and maintenance

Run `python3 scripts/build-expansion.py` after editing the authored copy. It rebuilds these pages, sample CSVs, search entries, and the expansion sitemap. It adds marked discovery sections to selected existing pages and footer links across the site. Repeating it produces identical output.

The renderer uses the existing operations page for the shared header, styles, footer, and global organization graph. It removes that page's specific schemas and replaces its title, metadata, canonical, main content, and breadcrumbs. Calculators load one local script; no input is submitted to a server. Calculate remains disabled without JavaScript, while formulas and worked examples remain readable.

The core `generate_site.py` runs the expansion builder after writing core assets so the new routes, contextual links, sitemap entry, and search records survive a full rebuild. The core generator has broader pre-existing effects on old pages, so use the focused expansion builder for this release. Existing static Vercel deployment settings remain unchanged.

The three sample CSVs contain fictional teaching data and say so in both page copy and download. The capacity worksheet's unavailable time is a **team total**. The margin tool calculates contribution under the entered direct-cost basis, not company net profit. Rework cost is for the user-defined period and does not claim annual savings.

## Validation

```sh
python3 scripts/verify-expansion.py
python3 scripts/validate-long-tail.py
node --test scripts/calculators.test.cjs
git diff --check
```

Before this release was committed, `python3 scripts/verify-expansion.py --compare-ref 6d2c5ed` also checked preservation of all existing HTML copy and styles outside the marked additions. A repeated expansion build was byte-stable, and a full generator build passed both validators in an isolated copy with deployment settings retained.

Browser checks covered all three worked calculations, invalid capacity input, zero revenue, export invalidation after editing, CSV download contents, desktop layout, and a 390px phone viewport. The tested calculator and sample-table pages had no horizontal page overflow; the wide sample table scrolls within its region.

## Editorial boundaries and follow-up

No market fee ranges, vendor certifications, new client outcomes, or guaranteed performance claims were invented. Service fees and exact responsibilities require an agreed scope. Existing case-study narratives were preserved and linked to relevant workflows; no new evidence was fabricated.

After deployment, evaluate the new URL groups using Search Console impressions, query intent, organic consultation inquiries, and useful tool engagement. Use observed overlap before consolidating existing articles. Additional documented case studies require actual engagement records and permission to publish their details.
