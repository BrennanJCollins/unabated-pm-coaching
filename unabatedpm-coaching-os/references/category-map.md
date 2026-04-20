# PM Skills Category Map

The Four Pillars framework defines 16 skill categories (4 per pillar). This file is the canonical mapping between category keys, display names, pillar membership, and the coaching skills that evaluate each category.

## Category Keys

Use these exact keys in ledger entries, versions.json, and dashboard data. They must be consistent across all system components.

### Pillar 1: Product Strategy (max 20 points)

| Key | Display Name | Primary Evaluator Skills | General Assessment Signals |
|-----|-------------|-------------------------|---------------------------|
| `market_customer_intelligence` | Market & customer intelligence | strategy-articulation, interview-question-design, user-buyer-bridge, career-transition-navigator, ai-career-impact-advisor | Evidence of market research, customer quotes, competitive awareness |
| `problem_discovery_prioritization` | Problem discovery & prioritization | product-metrics-ladder, product-objective-definition, career-transition-navigator | Problem statements, prioritization rationale, impact sizing |
| `business_models_pitching` | Business models & pitching internally | unit-economics-calculator, pnl-translation, bridge-builder, roi-calculator-builder, business-model-canvas, offer-negotiation-playbook | Unit economics, ROI arguments, budget justification |
| `vision_storytelling` | Vision, storytelling, & inspiration | vision-synthesis, strategic-storytelling-pitch, impostor-to-strategist, unabatedpm-interview-coach | Vision statements, narrative structure, audience adaptation |

### Pillar 2: Product Delivery (max 20 points)

| Key | Display Name | Primary Evaluator Skills | General Assessment Signals |
|-----|-------------|-------------------------|---------------------------|
| `problem_solution_definition` | Problem & solution definition | product-objective-definition, product-metrics-ladder | Requirements clarity, acceptance criteria, solution rationale |
| `stakeholder_alignment` | Stakeholder alignment | stakeholder-request-reframe, cafe-update, first-90-days-playbook, order-taker-to-outcome-owner | Pre-alignment evidence, stakeholder mapping, objection anticipation |
| `team_throughput_quality` | Team throughput and quality | (General assessment) | Delivery cadence awareness, quality gates, tech debt acknowledgment |
| `solution_validation` | Solution validation & optimization | product-metrics-ladder, product-objective-definition | Experiment design, hypothesis framing, iteration plans |

### Pillar 3: Customer Experience (max 20 points)

| Key | Display Name | Primary Evaluator Skills | General Assessment Signals |
|-----|-------------|-------------------------|---------------------------|
| `journey_optimization` | Journey optimization | journey-map-economic-overlay | Journey mapping, touchpoint analysis, experience gaps |
| `support_success_enablement` | Support & success enablement | (General assessment) | Post-launch considerations, adoption metrics, support handoff |
| `user_behavior_insights` | User behavior & satisfaction insights | interview-question-design, journey-map-economic-overlay | User data references, behavioral analysis, feedback integration |
| `messaging_communication` | Messaging & communication | strategic-storytelling-pitch, cafe-update, resume-as-product-coach, confidence-scenario-simulator | Message clarity, audience adaptation, confidence signals |

### Pillar 4: Adoption & Growth (max 20 points)

| Key | Display Name | Primary Evaluator Skills | General Assessment Signals |
|-----|-------------|-------------------------|---------------------------|
| `market_segmentation` | Market segmentation & prioritization | business-model-canvas, user-buyer-bridge, resume-as-product-coach, niche-job-search-strategist | Segment definition, targeting rationale, ICP clarity |
| `sales_enablement` | Sales enablement | bridge-builder, demo-script-reviewer, user-buyer-bridge | Buyer economics, value props, competitive differentiation |
| `product_evangelism` | Product evangelism | demo-script-reviewer, niche-job-search-strategist | Product narrative, demo flow, enthusiasm translation |
| `pricing_monetization` | Pricing & monetization | unit-economics-calculator, user-buyer-bridge, offer-negotiation-playbook | Pricing rationale, monetization model, willingness-to-pay |

## Cross-Cutting Skills

Applied to ALL document types regardless of classification:

| Skill | Categories Scored | What It Detects |
|-------|------------------|-----------------|
| four-pillars-check | All 4 pillar totals | Overall pillar balance — identifies lopsided PMs |
| order-taker-to-outcome-owner | stakeholder_alignment, problem_solution_definition | Order-taking vs. ownership signals in language |
| ai-career-impact-advisor | market_customer_intelligence | AI strategic awareness signals |
| confidence-scenario-simulator | messaging_communication | Confidence vs. hedging patterns in writing |

## Score Scale

Each category is scored 1-5:

| Score | Label | Meaning |
|-------|-------|---------|
| 1 | Not present | Element is missing or fundamentally broken |
| 2 | Attempted | Attempted but significant gaps |
| 3 | Competent | Competent but missing key elements |
| 4 | Strong | Strong with minor improvements possible |
| 5 | Exemplary | Would pass senior PM review |

**Pillar total:** Sum of 4 categories (max 20)
**Overall total:** Sum of 4 pillars (max 80)

## Category Key → Display Name Lookup

For dashboard rendering, use this mapping:

```
market_customer_intelligence     → "Market & Customer Intelligence"
problem_discovery_prioritization → "Problem Discovery & Prioritization"
business_models_pitching         → "Business Models & Pitching"
vision_storytelling              → "Vision & Storytelling"
problem_solution_definition      → "Problem & Solution Definition"
stakeholder_alignment            → "Stakeholder Alignment"
team_throughput_quality          → "Team Throughput & Quality"
solution_validation              → "Solution Validation"
journey_optimization             → "Journey Optimization"
support_success_enablement       → "Support & Success Enablement"
user_behavior_insights           → "User Behavior Insights"
messaging_communication          → "Messaging & Communication"
market_segmentation              → "Market Segmentation"
sales_enablement                 → "Sales Enablement"
product_evangelism               → "Product Evangelism"
pricing_monetization             → "Pricing & Monetization"
```

## Pillar Key → Display Name Lookup

```
strategy → "Product Strategy"
delivery → "Product Delivery"
cx       → "Customer Experience"
growth   → "Adoption & Growth"
```

## Pillar Colors (for dashboard charts)

```
strategy → #3B82F6 (blue)
delivery → #10B981 (green)
cx       → #F59E0B (amber)
growth   → #8B5CF6 (purple)
```
