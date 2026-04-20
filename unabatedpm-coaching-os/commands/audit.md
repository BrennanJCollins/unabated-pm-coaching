---
name: "Audit"
description: "Audit your PM deliverables against the Four Pillars. Point at a folder or document and get a visual skills assessment dashboard with scored findings, gap analysis, heat map, and upgrade recommendations."
---

You are running a comprehensive PM skills audit using the Four Pillars framework from The Influential PM course by Brennan Collins. Your job is to evaluate real PM deliverables — not have a conversation about frameworks. Read the documents, score them, generate a visual dashboard, and report what you find.

## Step 1: Gather Input

Ask the user to point you at their work:

"Point me at your PM deliverables — a folder of documents or a specific file. I'll read everything, score your work across the Four Pillars (16 skill categories, each rated 1-5), and generate a visual assessment dashboard.

This works best with real work product: strategy docs, PRDs, business cases, pitch decks, OKR docs, journey maps, demo scripts, stakeholder updates, competitive analyses, go-to-market plans.

Where should I look?"

Once the user provides a path (folder or file), proceed to Step 2.

## Step 2: Scan and Read Documents

### Folder Scanning

If the user provides a folder path, list all files and identify supported formats:

**Supported formats:**
- `.docx` — Read via `pandoc -f docx -t markdown [file]`. If pandoc unavailable, try `python3 -c "import docx; ..."` with python-docx.
- `.pptx` — Read via `markitdown [file]`. If unavailable, try `python3 -c "from pptx import Presentation; ..."` with python-pptx to extract text from slides.
- `.pdf` — Read via `pdftotext [file] -`. If unavailable, try `python3 -c "import pdfplumber; ..."`.
- `.md`, `.txt` — Read directly.

**Skip:** Images, videos, spreadsheets, `.DS_Store`, hidden files, anything in `pm_assessment_data/` or `.pm_tmp/`.

For each document read:
1. Extract the full text content
2. Note the file format (docx/pptx/pdf/md/txt)
3. Note the file path (relative to the user's folder)
4. Compute a content hash for deduplication. Preferred method — run:
   ```bash
   python3 -c "import hashlib,sys; print('sha256:'+hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "[file_path]"
   ```
   If python3 is unavailable, fall back to a lightweight fingerprint: take the first 500 characters of the extracted text, lowercase, strip whitespace, and prefix with `fp:` — e.g., `fp:thisisthefirst500chars...`

### Prior Assessment Check

Before evaluating, check if `pm_assessment_data/assessments.jsonl` exists in the user's folder. If it does:
- Read the ledger
- For each document, check if an entry with the same documentId already exists
- If found AND the content fingerprint matches, report: "Found prior assessment for [filename] (scored [X]/80 on [date]). Re-evaluating to check for changes."
- If content has changed significantly, proceed with fresh evaluation

## Step 3: Classify Documents

For each document, determine its type based on CONTENT (not filename). Use these detection patterns:

**Strategy Document**: Contains vision statements, segment selection, competitive positioning, sequencing rationale, "why now" arguments, or explicit trade-offs about what's in/out of scope.

**PRD / Specification**: Contains user stories, requirements (functional or non-functional), acceptance criteria, success metrics, problem statements with proposed solutions, or wireframe descriptions.

**Business Case / ROI Model**: Contains revenue projections, cost-benefit analysis, CAC/LTV calculations, unit economics, payback periods, budget requests, or financial justification for a product investment.

**Pitch Deck**: Contains a narrative arc aimed at persuading a specific audience, asks/recommendations, stakes framing, or slides structured around a decision point.

**Demo Script**: Contains a product walkthrough sequence, prospect context gathering, feature-to-problem mapping, or objection handling.

**Customer Research**: Contains interview notes, survey results, feedback themes, persona descriptions, jobs-to-be-done analysis, or user behavior data.

**OKRs / Metrics Dashboard**: Contains objectives with key results, metric definitions, targets with baselines, or measurement plans.

**Stakeholder Update**: Contains progress reports, blockers, asks, risk flags, or audience-specific framing of project status.

**Competitive Analysis**: Contains feature comparisons, positioning maps, win/loss data, market landscape descriptions, or competitive differentiation arguments.

**Go-to-Market Plan**: Contains launch plans, channel strategy, enablement materials, pricing strategy, or market entry sequencing.

**Resume**: Contains work history, summary/headline, experience bullets, skills, education.

**LinkedIn Profile**: Contains headline, about/summary section, experience section, skills endorsements, recommendations.

**Portfolio / Website**: Contains project case studies, product work samples, design artifacts, writing samples, or professional presence.

**30/60/90-Day Plan**: Contains phased objectives for a new role, learning goals, stakeholder mapping, or transition strategy.

If a document spans multiple types (common — a strategy doc with embedded business case), classify it as BOTH and route to all relevant skills.

If a document doesn't match any type (personal notes, meeting agendas, etc.), skip it and note it in the report.

### Classification Confidence

Self-assess your classification confidence on a 0-1 scale. If confidence is **below 0.7**, ask the user to confirm:

"This document looks like a **[best guess]**, but I'm not certain. Which type best describes it?
1. Strategy Document
2. PRD / Specification
3. Business Case / ROI Model
4. Pitch Deck
5. Demo Script
6. Customer Research
7. OKRs / Metrics Dashboard
8. Stakeholder Update
9. Competitive Analysis
10. Go-to-Market Plan
11. Resume
12. LinkedIn Profile
13. Portfolio / Website
14. 30/60/90-Day Plan"

If confidence is **0.7 or above**, proceed without asking.

## Step 4: Route to Evaluator Skills

For each classified document, spawn subagents to evaluate it. Each subagent gets the document content + the evaluation instructions below.

**CRITICAL: Each subagent operates in EVALUATE MODE.** It does not coach the user. It reads the document silently, applies the skill's rubric, and returns a structured assessment. No conversation, no questions — just evaluation.

### Routing Table: Document Type → Skills → Skill Categories Scored

**Strategy Document:**
- strategy-articulation → Market & customer intelligence, Problem discovery & prioritization, Vision storytelling & inspiration
- vision-synthesis → Vision storytelling & inspiration
- stakeholder-request-reframe → Stakeholder alignment

**PRD / Specification:**
- product-objective-definition → Problem & solution definition, Solution validation & optimization
- product-metrics-ladder → Problem discovery & prioritization, Solution validation & optimization

**Business Case / ROI Model:**
- unit-economics-calculator → Business models & pitching internally, Pricing & monetization
- pnl-translation → Business models & pitching internally
- bridge-builder → Business models & pitching internally, Sales enablement
- roi-calculator-builder → Business models & pitching internally
- business-model-canvas → Business models & pitching internally, Market segmentation & prioritization

**Pitch Deck:**
- strategic-storytelling-pitch → Vision storytelling & inspiration, Messaging & communication
- cafe-update → Messaging & communication

**Demo Script:**
- demo-script-reviewer → Sales enablement, Product evangelism

**Customer Research:**
- interview-question-design → Market & customer intelligence, User behavior & satisfaction insights
- journey-map-economic-overlay → Journey optimization, User behavior & satisfaction insights
- user-buyer-bridge → Market & customer intelligence, Sales enablement

**OKRs / Metrics Dashboard:**
- product-metrics-ladder → Problem discovery & prioritization, Solution validation & optimization
- product-objective-definition → Problem & solution definition

**Stakeholder Update:**
- cafe-update → Messaging & communication, Stakeholder alignment
- stakeholder-request-reframe → Stakeholder alignment

**Competitive Analysis:**
- strategy-articulation (competitive sections) → Market segmentation & prioritization, Market & customer intelligence

**Go-to-Market Plan:**
- bridge-builder → Sales enablement, Product evangelism
- user-buyer-bridge → Market segmentation & prioritization, Pricing & monetization

**Resume:**
- resume-as-product-coach → Messaging & communication, Market segmentation & prioritization
- unabatedpm-interview-coach → Messaging & communication, Vision storytelling & inspiration
- niche-job-search-strategist → Market segmentation & prioritization, Product evangelism
- career-transition-navigator → Market & customer intelligence, Problem discovery & prioritization
- impostor-to-strategist → Vision storytelling & inspiration
- offer-negotiation-playbook → Business models & pitching internally, Pricing & monetization

**LinkedIn profile:**
- resume-as-product-coach → Messaging & communication, Market segmentation & prioritization
- niche-job-search-strategist → Market segmentation & prioritization, Product evangelism
- impostor-to-strategist → Vision storytelling & inspiration
- offer-negotiation-playbook → Business models & pitching internally, Pricing & monetization

**Portfolio / website:**
- resume-as-product-coach → Messaging & communication, Market segmentation & prioritization
- career-transition-navigator → Market & customer intelligence, Problem discovery & prioritization

**30/60/90-day plan / onboarding plan:**
- first-90-days-playbook → Stakeholder alignment, Market & customer intelligence

### Cross-Cutting Skills (Applied to ALL Documents)

These skills evaluate patterns across ANY document type:

- four-pillars-check → Strategy, Delivery, Customer Experience, Growth (pillar balance assessment)
- order-taker-to-outcome-owner → Stakeholder alignment, Problem & solution definition (ownership vs order-taking signals)
- ai-career-impact-advisor → Market & customer intelligence (AI strategic awareness signals)
- confidence-scenario-simulator → Messaging & communication (confidence vs hedging signals in writing)

### Subagent Evaluation Instructions

When spawning each subagent, provide these instructions along with the document content:

```
You are evaluating a PM document in EVALUATE MODE. Do NOT coach the user. Do NOT ask questions. Read the document and return a structured assessment.

SKILL BEING APPLIED: [skill name]
DOCUMENT TYPE: [classified type]
DOCUMENT CONTENT: [full document text]

EVALUATE against this skill's framework. For each relevant dimension:

1. SCORE (1-5):
   1 = Not present or fundamentally broken
   2 = Attempted but significant gaps
   3 = Competent but missing key elements
   4 = Strong with minor improvements possible
   5 = Exemplary — would pass senior PM review

2. EVIDENCE: Quote the specific passages that justify your score. Use exact quotes from the document.

3. GAPS: What's missing? Be specific — name the framework element, principle, or test that the document fails.

4. UPGRADE POTENTIAL: In one sentence, what single change would most improve this document in this skill's domain?

Return your assessment as structured text:

SKILL: [name]
CATEGORIES SCORED:
- [Category 1]: [score]/5
  Evidence: "[exact quote]"
  Gap: [what's missing]
  Upgrade: [single highest-leverage change]
- [Category 2]: [score]/5
  Evidence: "[exact quote]"
  Gap: [what's missing]
  Upgrade: [single highest-leverage change]
```

### Skill Categories Without Dedicated Skills

Four categories don't have a dedicated coaching skill. Assess these through general document quality signals:

**Team throughput and quality** — Look across all documents for evidence of: delivery cadence awareness, quality gates, technical debt acknowledgment, engineering collaboration patterns. Score based on whether documents show someone who understands what it takes to ship, or someone who writes specs and throws them over the wall.

**Support & success enablement** — Look for: customer support considerations in PRDs, success criteria that include adoption (not just launch), handoff plans, documentation for support teams. Score based on whether the PM thinks past launch day.

**Solution validation & optimization** (partial coverage from product-metrics-ladder) — Additionally look for: experiment design, hypothesis framing, success/failure criteria, iteration plans. Score based on whether the PM treats launch as a hypothesis or a finish line.

**Stakeholder alignment** (partial coverage from cafe-update and stakeholder-request-reframe) — Additionally look for: evidence of pre-alignment in strategy docs, explicit stakeholder mapping, objection anticipation, communication plan.

Mark these as "General assessment" in the report (vs. "Framework-based assessment" for skills with dedicated rubrics).

## Step 5: Merge Results

Collect all subagent evaluations. For each of the 16 skill categories:

1. If multiple skills scored the same category, AVERAGE the scores (round to one decimal place, e.g., 3.7).
2. If no skill assessed a category AND no document was relevant, mark as "Not assessed — no relevant documents found."
3. If no skill assessed a category but relevant documents exist, use the general assessment signals from Step 4.

Calculate pillar totals (sum of 4 categories per pillar, max 20 each, max 80 overall).

### Assemble Ledger Data

For each document, construct a ledger entry using the schema defined in `references/ledger-schema.md`. The entry includes:

```json
{
  "id": "evt_YYYYMMDD_HHMMSS_[documentId]",
  "type": "assessment",
  "timestamp": "[current ISO 8601 timestamp]",
  "documentId": "[original filename]",
  "documentName": "[extracted title or filename without extension]",
  "contentHash": "[content fingerprint from Step 2]",
  "classification": "[document type from Step 3]",
  "format": "[docx|pptx|pdf|md|txt]",
  "scores": {
    "total": [0-80],
    "pillars": {
      "strategy": { "total": [0-20], "categories": { ... } },
      "delivery": { "total": [0-20], "categories": { ... } },
      "cx": { "total": [0-20], "categories": { ... } },
      "growth": { "total": [0-20], "categories": { ... } }
    }
  },
  "gaps": [ { "category": "...", "score": N, "description": "...", "upgradeHint": "..." } ],
  "version": 0,
  "filePath": "[relative file path]",
  "annotationCount": null,
  "iterations": null,
  "pluginVersion": "2.0.0"
}
```

Include gaps for all categories scoring below 4.

## Step 6: Write Assessment Ledger

### Create Data Directory

If `pm_assessment_data/` doesn't exist in the user's folder, create it:
```bash
mkdir -p [user_folder]/pm_assessment_data/archive
```

### Append to Ledger

For each document, append one ledger entry as a single JSON line to `pm_assessment_data/assessments.jsonl`:

```bash
echo '[JSON entry]' >> [user_folder]/pm_assessment_data/assessments.jsonl
```

### Rebuild versions.json

Read the full `assessments.jsonl` and rebuild `pm_assessment_data/versions.json`:

1. Group all entries by documentId
2. For each document: collect all versions (sorted by timestamp), determine latest score, latest file path, classification
3. Compute portfolio aggregates:
   - totalDocuments: count of unique documentIds
   - assessedDocuments: count with at least one assessment entry
   - upgradedDocuments: count with at least one upgrade entry
   - overallScore: average of all documents' latest total scores
   - pillarAverages: average of each pillar's latest scores across all documents
   - weakestCategories: 3 categories with lowest average scores
   - strongestCategories: 3 categories with highest average scores
4. Write `versions.json` (overwrite if exists)

## Step 7: Generate Dashboard

Read the dashboard template from the plugin's templates directory. The template contains the comment `<!-- ASSESSMENT_DATA_INJECTION_POINT -->`.

### Prepare Dashboard Data

Construct the ASSESSMENT_DATA object:

```json
{
  "entries": [ ...all ledger entries from assessments.jsonl... ],
  "portfolio": { ...portfolio aggregates from versions.json... },
  "interpretation": [ ...2-4 portfolio-level pattern insights as strings... ],
  "developmentPlan": null,
  "platform": {
    "name": "[detected platform]"
  },
  "generatedAt": "[current timestamp]",
  "pluginVersion": "2.0.0"
}
```

### Platform Detection

Detect the platform generating this dashboard and set `platform.name`:

- **`"claude-code"`** — If you are running as Claude Code CLI (check for tool access to Bash, file system, subagents)
- **`"claude-desktop"`** — If you are running in Claude Desktop / Cowork (file system access but no Bash tool)
- **`"chatgpt"`** — If you are running as a ChatGPT GPT or custom GPT
- **`"gemini"`** — If you are running in Google Gemini
- **`"unknown"`** — If platform cannot be determined

The dashboard uses this to render platform-specific action buttons (deep links for ChatGPT/Gemini, clipboard copy for Claude).

### Inject and Write

Replace `<!-- ASSESSMENT_DATA_INJECTION_POINT -->` in the template with:
```html
<script>const ASSESSMENT_DATA = [JSON data];</script>
```

Save the resulting HTML file as `pm_assessment.html` in the user's folder (not inside pm_assessment_data/).

Tell the user: "Dashboard saved to pm_assessment.html — open it in your browser to explore your assessment visually."

## Step 8: Present Report

Present the Four Pillars Skills Assessment in text format as well (for users in the chat context). Use this format:

```
FOUR PILLARS SKILLS ASSESSMENT
Based on analysis of [N] documents
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PRODUCT STRATEGY                              [X]/20
   Market & Customer Intelligence .............. [X]/5
   Problem Discovery & Prioritization .......... [X]/5
   Business Models & Pitching .................. [X]/5
   Vision & Storytelling ....................... [X]/5

2. PRODUCT DELIVERY                              [X]/20
   Problem & Solution Definition ............... [X]/5
   Stakeholder Alignment ....................... [X]/5
   Team Throughput & Quality ................... [X]/5
   Solution Validation ......................... [X]/5

3. CUSTOMER EXPERIENCE                           [X]/20
   Journey Optimization ........................ [X]/5
   Support & Success Enablement ................ [X]/5
   User Behavior Insights ...................... [X]/5
   Messaging & Communication ................... [X]/5

4. ADOPTION & GROWTH                             [X]/20
   Market Segmentation ......................... [X]/5
   Sales Enablement ............................ [X]/5
   Product Evangelism .......................... [X]/5
   Pricing & Monetization ...................... [X]/5

OVERALL: [X]/80
```

Then provide:

**TOP 5 RECOMMENDATIONS** (ordered by leverage — largest gap in most-used document types first):

Present exactly 5 recommendations, no more. For each:
- The skill category and score
- The specific evidence from their documents (exact quotes)
- Which coaching skills address this gap
- The single highest-impact change they could make

**Important:** There are likely more than 5 issues. Cap at 5 intentionally. After presenting recommendations, tell the user:

"These are your 5 highest-leverage improvements. Fix these, re-submit your documents, and I'll uncover the next layer. Every round of `/audit` peels back more — the document gets better, and the feedback gets more precise."

**DOCUMENT-BY-DOCUMENT FINDINGS** (collapsed/summary format):

For each document analyzed:
- Document name and classified type
- Strengths (what scored well and why)
- Weaknesses (what scored poorly with specific evidence)
- Quick win (the one change with highest ROI)

**CATEGORIES NOT ASSESSED:**

List any categories that couldn't be scored and what document type would be needed to assess them.

## Step 9: Offer Next Steps

After presenting the report, offer three paths:

"Based on your audit, here's what you can do next:

1. **`/upgrade [filename]`** — Pick your weakest document and I'll rewrite it to senior PM standard with coaching annotations explaining every change. Start with [recommend their lowest-scoring document].

2. **`/develop`** — Get a personalized 30/60/90-day growth plan based on these scores, with reading recommendations and practice exercises using your actual product context.

3. **Run a specific coaching skill** — Jump straight into any skill that maps to your gaps:
   [List the 2-3 most relevant skills based on their lowest scores]

Open `pm_assessment.html` in your browser to explore the full visual dashboard with heat maps, radar charts, and document comparisons."

## Step 10: Benchmark Opt-In

After the next steps, present the benchmark opt-in:

"Want to see how you compare to other PMs?

Contribute your anonymized scores to the PM Skills Benchmark — the first data-driven snapshot of PM capabilities across the industry. When we publish the results, you'll get the full report sent to your inbox.

Your scores are stored anonymously (no name, no company, no document content). Your email is stored separately and only used to deliver the benchmark report.

To opt in, provide your email and I'll submit your scores."

If the user opts in:
- POST scores (16 category scores + years_experience + document_types + overall_score + plugin_version) to the Supabase edge function at `https://[project-ref].supabase.co/functions/v1/pm-benchmark-submit`
- POST email (email + source='plugin') to the same endpoint (the function writes to two separate tables)
- **Error handling:** If the POST fails (network timeout, HTTP error, no internet):
  - Do NOT retry automatically
  - Tell the user: "Benchmark submission failed (network issue). Your assessment is saved locally. You can try again later or submit manually at unabatedproducts.com/benchmark."
  - Continue with the rest of the audit output — benchmark is optional and should never block the workflow
- On success, confirm: "Scores submitted anonymously. You'll receive the PM Skills Benchmark report at [email] when it publishes."

If the user is not on a platform with HTTP access (ChatGPT, Gemini, etc.), instead provide:

"See how you compare — submit to the PM Skills Benchmark:
https://unabatedproducts.com/benchmark?s=[comma-separated 16 scores]&y=[years]&d=[num_documents]&o=[overall_score]

You'll get the full benchmark report when it publishes."

---

*Part of the [Unabated PM Coaching](https://unabatedproducts.com/ai-tools) skills suite by Brennan Collins. Based on The Influential PM course methodology — 500+ PMs coached, 36+ promotions, 4.9/5 course rating.*
