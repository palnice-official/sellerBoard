**Independent review: sb-sow v0.2 developer hand-off (docs/12) — reviewed only, no files edited**

`python3 engineering/check_register.py` exits 0 and prints "163 features, 182 reqs, 80 screens, 107 calcs, 31 connectors, 36 WPs; 141 golden vectors". `reference_calcs.py` passes 141/141. The hours and cost figures check out against the register and docs/06: R0 1,840 h + R1 3,940 h = 5,780 h; cross-cutting 912 h; total 11,740 h; about ₹2.00 cr initial; cloud ₹1.11 lakh/month. The safety rules are stated correctly: write flags false, kill switch, no IRN, e-way bill or GST filing, no vendor assets, Lucide icons. The PII scan found only `example.test` e-mails, synthetic `B0SYNTH*` ASINs and `SYNTH` GSTINs, and the two names in the hand-off header.

The hand-off is close, but a developer cannot start R0 without guessing. The blocking problems are findings 1–5.

**Findings**

1. **HIGH — The hand-off contradicts the agent rules on production.**
   - Location: docs/12 §1.2, §4 IaC row, §7; against prompts/README.md L59, L81, L169; .claude/rules/safety.md L3; AGENTS.md "Safety"; WP-28 prompt (07/08 ~L4397, L4473).
   - Issue: the hand-off asks for dev, stage and prod deployed by Terraform, with GitHub Actions deploying to prod. The rules say "No production environment exists; do not create one", "no paid provisioning", "no production access from agents or CI", `RCI_ENV` has no `prod`, and WP-28 says "production deferred… No cloud resources created… infra/** not applied".
   - Fix:
     - Add to docs/12 §5 a rule that agents only write Terraform. A named human DevOps engineer runs `terraform apply`, through CI with GitHub environment protection (required reviewers). Prod apply needs written Owner approval recorded in `docs/governance/approvals/`.
     - Amend WP-28 (via `gen_packs.py`) to add an AWS/Terraform slice, "WP-28b (human-applied)".
     - Add `prod` to `RCI_ENV`.
     - Reword README L169 to "no production access from agents; prod deploy only via the approved CI deploy role".

2. **HIGH — The build sequence in docs/12 §3 breaks the prompt-pack dependencies.**
   - WP-06 depends on WP-05 but is placed before it (orders 5 and 6).
   - WP-09 depends on WP-08 but is placed before it (9 vs 12).
   - WP-12 depends on WP-11 but is placed before it (10 vs 14).
   - WP-34 depends on WP-29, and WP-29 depends on WP-25, which is an R5 package. So R1 cannot close.
   - Fix:
     - Reorder to 01 → 03 → 28 → 04 → 02 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 35 → 31 → 32 → 34 → 33.
     - Either drop WP-12's dependency on WP-11 (the R1 tracks text says Shopify follows WP-07) or keep it consistently.
     - Split WP-29 into WP-29a (Sellerboard export import, R1, no WP-25 dependency) and make WP-34 depend on WP-29a. Regenerate the packs.

3. **HIGH — The approval status is understated.**
   - Location: docs/12 §9 bullet 1.
   - Issue: it says only the Finance/CFO items are pending. SOW §29 shows all 8 roles Pending, including Owner and Engineering lead, and says "No signature line is valid until all Pending rows are resolved". Nothing records the claim "R0 can start".
   - Fix:
     - Replace the bullet with: "All eight approval-register rows are Pending; the SOW is unsigned."
     - Record the R0 start as a decision with a budget cap, for example new DC-13 "Owner authorises WP-01/03/28 start, cap ₹X, 2026-10-10", in decision_log.csv and SOW §28. Or state that R0 waits for it.

4. **HIGH — Backups to Singapore contradict the residency reason for choosing Mumbai.**
   - Location: docs/12 §4 Accounts/SCP and Backup rows; spec §9.6.
   - Issue: DC-01 picks ap-south-1 "for India data residency", but backups are copied to ap-southeast-1 (Singapore), outside India.
   - Fix: use ap-south-2 (Hyderabad) as the DR region in docs/12 §4 (SCP allow-list and AWS Backup copy) and in spec §9.6. Or have Finance/legal record why Singapore is acceptable under DISC-20.

5. **HIGH/MED — Settlement reports will be lost before a live system exists.**
   - Location: spec §5.4 and SOW §15.1.4 vs docs/12 §4 environments and §7.
   - Issue: Amazon keeps report documents for 90 days, so they must be captured continuously from R0. But stage is sandbox and anonymised, and prod only exists at the R1 gate. R0 plus R1 is about 22 weeks.
   - Fix: add a docs/12 §6 item, "Ops downloads every settlement flat file monthly from Seller Central starting now (owner: Ops)". Optionally allow a human-applied, read-only prod ingestion slice as soon as SP-API is approved, under Owner approval.

6. **MED — Invoice numbering is contradictory.**
   - Location: DC-10 (SOW §28, decision_log) vs WP-31 prompt "Numbering: gap-free… assigned only at posting", spec §6.4 `doc_no`, spec §10.12.
   - Issue: the DC-10 default is that the app only records numbers issued by the accounting system. Spec and WP-31 have the app issue them. docs/12 §6 only says "numbering source (DC-10)".
   - Fix: decide DC-10 before WP-31a. Either change the default to "app issues the series" or add `numbering_mode = external|internal` to the WP-31 prompt and spec §3.7, defaulting to `external` with `doc_no` entered at posting.

7. **MED — The region-restriction SCP will break the edge setup.**
   - Location: docs/12 §4 Accounts row.
   - Issue: a deny on everything outside ap-south-1 blocks the ACM certificate that CloudFront needs in us-east-1, any CloudFront-scoped WAF, and global services (IAM, Organizations, Route 53, CloudFront, Support).
   - Fix: write the SCP as "deny non-approved regions except global services (`aws:RequestedRegion` NotAction list) and us-east-1 for `acm:*` on CloudFront certs, `wafv2` CLOUDFRONT scope and `cloudfront:*`".

8. **MED — Object Lock compliance mode conflicts with deletion duties.**
   - Location: docs/12 §4 Object storage row; spec §5.5 and §9.6.
   - Issue: compliance mode makes objects undeletable. That conflicts with:
     - the 30-day PII expiry;
     - Shopify `shop/redact` and `customers/redact`;
     - DPDP erasure;
     - courier files kept 2 years with consignee columns redacted.
   - Fix: apply compliance-mode Object Lock only to PII-free settlement and finance report documents (7-year retention). Use governance mode (or no lock) for prefixes that may hold PII. Strip PII before archiving. State the retention period per prefix.

9. **MED — The RPO figure is ambiguous.**
   - Location: docs/12 §4 Backup/DR row.
   - Issue: "RPO 5 min, RTO 4 h" sits next to "cross-region copy". RPO 5 min only holds for PITR in the same region; scheduled snapshot copies give a regional RPO of up to 24 h.
   - Fix: write "RPO 5 min / RTO 4 h for in-region failures (PITR, Multi-AZ). Regional DR: RDS cross-region automated-backup replication to the DR region (RPO ≈ minutes), or snapshot copy (RPO 24 h) — choose in WP-28."

10. **MED — The observability stack differs between documents.**
    - Location: docs/12 §4 (CloudWatch, X-Ray, SNS) vs spec §1.1 and §9.5 (Prometheus metrics, Grafana dashboards, Tempo/Loki).
    - Fix: pick one in docs/12 and spec §9.5. For example: ADOT collector → X-Ray plus Amazon Managed Prometheus/Grafana, so the spec's metric names and dashboards still apply. Or rewrite §9.5 for CloudWatch.

11. **MED — The secrets runtime model doesn't fit AWS.**
    - Location: README L86 and safety.md (`VAULT_ADDR` and `VAULT_ROLE` are the only secret variables) vs docs/12 §4 (Secrets Manager).
    - Issue: on ECS, the IAM task role grants access, so there is no vault address.
    - Fix: define `RCI_SECRETS_BACKEND=aws_sm|vault|devfile`, `AWS_REGION`, `RCI_SECRETS_PREFIX=/{env}/connectors/`. Document separate api and worker task roles (spec §9.3: worker reads, api writes only via the OAuth callback).

12. **MED — Freshness targets are misquoted.**
    - Location: docs/12 §4 Observability row.
    - Issue: "Amazon orders ≤ 2 h; finances ≤ 6 h". Spec §9.5 has orders target 30 min with alert after 2 h, and finances target 6 h with alert after 24 h.
    - Fix: quote both the target and the alert threshold from spec §9.5, or just reference that table.

13. **MED — The WP-31 slice note is wrong.**
    - Location: docs/12 §3 row 11.
    - Issue: it says "slices 31b–31c follow in R2". Per the prompt pack, 31b is R2 and 31c is R5 (CON-33, conditional).
    - Fix: "31a in R1; 31b (receivables/export) in R2; 31c (CON-33 drafts) in R5, conditional."

14. **MED — The "Rama will provide" list (docs/12 §6) lacks infrastructure items.**
    - Missing items:
      - GitHub org, repo and seats;
      - domain/subdomain plus DNS delegation to Route 53;
      - an SES-verified sender domain (SPF/DKIM) — WP-03 needs e-mail OTP for MFA (spec §11) and alerts go out by e-mail;
      - the on-call alert recipients or Slack channel;
      - AWS Budgets/billing alarm recipients.
    - Fix: add each as a row with an owner and the WP it is needed for (WP-03 or WP-28).

15. **MED — The same list lacks business and data inputs that R1 needs.**
    - Missing items:
      - FX source and policy (DC-02 / DISC-27), for WP-07;
      - historical COGS batches (A-07), for WP-09/29;
      - AATO band (A-17);
      - Shopify India plan tier and Shopify Payments availability (DISC-10/11);
      - Razorpay or other gateway settlement CSVs — CON-07 is R2, so India "Auto" payment fees need these files in R1 (WP-35);
      - the accounting-system sales register and B2B opening balances (SOW §15.1.5, §15.2 B2B parallel check);
      - DPDP notice wording for B2B contacts (DISC-32, "before R1 go-live");
      - a named finance controller and deputy (RK-08).
    - Also add a note: "Amazon Ads API not needed for R0/R1; apply during R1 (RK-02)."
    - Fix: add these rows.

16. **MED — The R1 Definition of Done (docs/12 §7) is incomplete.**
    - Missing items:
      - SOW §19.6 settlement-bridge sign-off: 3 consecutive settlements per Amazon store and 3 Shopify payouts;
      - the B2B check against the accounting sales register (§15.2);
      - zero open S1/S2;
      - the compat/CM reconciliation (REQ-176);
      - the Owner's cut-over decision logged.
    - Also add "COD cancellations excluded only by tag (RTO costs missing)" to the §9 list of Sellerboard configuration issues.
    - Fix: add these bullets.

17. **MED — Stale references to DC-01 remain.**
    - Locations:
      - spec §1.1 (object storage "per DC-01: AWS / MinIO / Azure") and §9.1 ("planning assumption to be ratified in WP-28", Hetzner/Azure alternatives);
      - SOW A-09 (provider "[TBC]");
      - doc 09 §5 item 8 (still open).
    - Also, DISC-20 (DPIA for EU data) is still open and docs/12 doesn't mention it.
    - Fix: update the three locations to "AWS ap-south-1 (decided 2026-10-10)" and add DISC-20 to docs/12 §9.

18. **MED — Doc 09 and the SOW deliverables list are out of date.**
    - Location: docs/09_Delivery_Quality_Report.md; SOW §22.
    - Issue: doc 09 is entirely v0.1 — 123 features, 135 requirements, 62 screens, 49 calculations, 29 connectors, 30 WPs, 10,280 h, 72 vectors — against v0.2's 163/182/80/107/31/36/11,740 h/141. SOW §22 still marks 03, 04, 06, 07 and 08 "To be updated to v0.2", and doc 12 is not listed.
    - Fix: regenerate doc 09 for v0.2, update the §22 status column, and add row 12 for docs/12.

19. **MED — The Shopify app path may be outdated (please verify).**
    - Location: docs/12 §6 row 2; CON-05 "custom app (admin-created)".
    - Issue: I believe Shopify stopped allowing new legacy admin-created custom apps from 2026-01-01, with new apps created through the Dev Dashboard. I have not confirmed this.
    - Fix: add to DISC-10 "confirm the current custom-app creation path and how `read_all_orders` is approved for it". Word docs/12 as "custom app via the currently supported path".

20. **MED — SP-API scope for R0 is unclear.**
    - Location: CON-01 acceptance evidence (c) "90-day backfill for IN + UK stores" vs the India-first R0/R1 plan; docs/12 §6 row 1 doesn't name accounts or regions.
    - Fix: docs/12 should say "register and authorise the Amazon.in seller account (EU endpoint) for R0; UK in R2". Change CON-01 (c) to "IN store (UK at R2)".

21. **LOW — The Amazon PII rule is worded loosely.**
    - Location: docs/12 §5.7, "Amazon PII is deleted ≤ 30 days".
    - Issue: the spec's rule is that restricted PII roles are not requested in R0–R4 (§5.5, CON-01).
    - Fix: "Do not request restricted PII roles; if ever held, purge ≤ 30 days after delivery / revocation."

22. **LOW — Runbook counts differ.**
    - Location: WP-28 DoD, AGENTS.md, README and ids.md say RB-01..RB-11; spec §9.8 has RB-01..RB-16 (RB-12–16 cover B2B, compat, courier, HSN and parallel run).
    - Fix: RB-01..RB-16 everywhere; regenerate the packs.

23. **LOW — Coverage gates differ.**
    - Location: SOW §19.1 lists 90 % for ledger, costing, profit, b2b and automation only. Spec §9.4 and CLAUDE.md add `tax` at 90 % and web at 75 %. docs/12 doesn't state the gates.
    - Fix: add `tax` and web 75 % to SOW §19.1, and add a line to docs/12 §5.3.

24. **LOW — Where the SPA is served from differs.**
    - Location: spec §1.1 (static files served by the API container) and WP-28 (Dockerfile `web` target) vs docs/12 and spec §9.1 (CloudFront + S3).
    - Fix: settle on CloudFront + S3 in spec §1.1 and drop or repurpose the `web` image target.

25. **LOW — Environment shape and tooling differ.**
    - Location: spec §9.1 has dev as docker-compose on laptops and stage as "1× Fargate or EC2 t4g.large". docs/12 has a dev AWS account with ×1 of each service. README requires Node 20 LTS, which reached end of life in April 2026.
    - Fix: align spec §9.1 with docs/12 (say whether a dev AWS account exists). Use per-account Terraform root modules and state rather than "one workspace per environment". Move to Node 22 LTS.

26. **LOW — IAM and OIDC are under-specified.**
    - Location: docs/12 §4.
    - Fix: add one GitHub OIDC deploy role per account, trusted only for `repo:<org>/<repo>:environment:<env>`. Prod deploys only from the `prod` GitHub environment with required reviewers. Separate ECS task roles for api, worker and scheduler. Terraform state bucket and lock table per account, encrypted with KMS. A break-glass procedure.

27. **LOW — The reading order (docs/12 §2) leaves out sections the hand-off relies on.**
    - Missing: SOW §15 (parallel run), §18, §26–§29 and spec §10–§11.
    - Fix: add them to rows 1 and 3.

28. **LOW — The cloud cost line looks light for this design.**
    - Location: docs/12 §4 Cost; docs/06 OpEx.
    - Issue: ₹1.11 lakh/month appears to leave out the dev and stage accounts, NAT gateways in 3 AZs, WAF, GuardDuty, Security Hub, Config and Inspector.
    - Fix: add a "security/landing-zone" OpEx line, and keep the "Pricing Calculator before prod apply" gate in §9.

29. **LOW — Synthetic IDs will trip the cassette scanner.**
    - Location: atlas `B0SYNTH001`… and the spec §9.4 scan regex `B0[A-Z0-9]{8}`.
    - Issue: if these synthetic ASINs are reused in cassettes, the CI scan fails. Separately, `check_register.py` doesn't scan `prompts/.claude/rules/*.md`.
    - Fix: use a synthetic pattern the regex doesn't match (for example `X0SYNTH001`) or allow-list `B0SYNTH\d{3}`, and add `prompts/.claude/rules/*.md` to the scanner's glob.

30. **INFO — Personal data and real figures.**
    - Nothing beyond the two header names (Nicepal, Ramesh) in docs/12.
    - Doc 11 and doc 10 §5 carry real audit observations: platform ROAS about 10× attributed, low repeat rate, Tamil Nadu, and Eshopbox as a vendor. These are not personal data. If docs/12 goes to an external developer, decide whether doc 11 should be shared as is.
    - The planning figures in docs/12 (₹2.00 cr, ₹1.11 lakh) are labelled as estimates, not quotations.

Files: /home/claude/sb-sow/docs/12_Developer_Handoff_AWS.md, docs/05_Engineering_Specification.md, docs/01_SOW.md, docs/09_Delivery_Quality_Report.md, prompts/{07_Claude_Code_Prompt_Pack.md, 08_Codex_Prompt_Pack.md, README.md, AGENTS.md, CLAUDE.md, .claude/rules/safety.md}, integration/connector_contracts.md, traceability/decision_log.csv.
