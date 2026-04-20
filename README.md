# Unabated PM Coaching

**28 AI coaching skills that teach you to think like a senior PM.** Not templates that fill in blanks. Coaching that pushes back on your thinking, scores your work, and shows you exactly where it breaks down.

Built from coaching 500+ product managers. Moving PMs from Stuck to Strategic. 4.8/5 course rating on Maven.

---

## What You Get

Most AI "PM tools" apply a framework like a checklist. These skills coach you through it the way a VP of Product would — with scoring rubrics, real coaching exchanges, error correction, and pushback on weak reasoning. They detect your level and adjust.

28 individual skills across four areas, plus guided workflows that chain skills together into complete coaching sessions.

---

## How to Use These Skills

### Claude Desktop (Cowork)

Point Claude to this repository and ask it to install all skills. Once installed, all 28 skills activate automatically based on what you ask. You can also run guided workflows as slash commands:

- `/coach-strategy` — Build your vision, pressure-test your strategy, prepare for stakeholder pushback
- `/coach-business-case` — Connect metrics to outcomes, calculate unit economics, translate to P&L
- `/coach-pitch` — Craft your story, compress to 60 seconds, practice under pressure
- `/coach-career` — Job search or career transition into PM: resume, niche search, interviews, first 90 days

### ChatGPT, Gemini, Claude Web, or Any AI Chat

Each skill is a standalone file you can use with any AI tool:

1. Browse the skill folders below (organized by category)
2. Open the `SKILL.md` for the skill you want
3. Copy the entire contents
4. Paste it into your AI tool as a custom instruction or at the start of a new conversation
5. Add your own context where it says `[Paste your context here]`

No installation, no configuration. The skill turns any AI into your PM coach for that topic.

### Claude Code (CLI)

```
claude plugin add https://github.com/BrennanJCollins/UnabatedPM-coaching
```

All skills and slash commands activate immediately.

---

## Skills by Category

### Strategic Thinking

| Skill | What It Coaches |
|---|---|
| [Order Taker to Outcome Owner](unabatedpm-strategic-thinking/skills/order-taker-to-outcome-owner/SKILL.md) | Stop executing tasks. Start owning outcomes. |
| [Four Pillars Check](unabatedpm-strategic-thinking/skills/four-pillars-check/SKILL.md) | Score yourself across Strategy, Delivery, CX, and Growth. Find your blind spots. |
| [Vision Synthesis](unabatedpm-strategic-thinking/skills/vision-synthesis/SKILL.md) | Build a product vision using the Vision Triangle that passes 4 quality tests. |
| [Strategy Articulation](unabatedpm-strategic-thinking/skills/strategy-articulation/SKILL.md) | Pressure-test your strategy with 5 Questions + the DHM Filter. |
| [Stakeholder Request Reframe](unabatedpm-strategic-thinking/skills/stakeholder-request-reframe/SKILL.md) | Turn "build this feature" demands into strategic conversations using Stakeholder Judo. |
| [AI Career Impact Advisor](unabatedpm-strategic-thinking/skills/ai-career-impact-advisor/SKILL.md) | Navigate AI's impact on your PM career with a concrete positioning strategy. |

### Business Building

| Skill | What It Coaches |
|---|---|
| [Product Metrics Ladder](unabatedpm-business-building/skills/product-metrics-ladder/SKILL.md) | Connect features to business outcomes. Stop pitching vanity metrics. |
| [User-Buyer Bridge](unabatedpm-business-building/skills/user-buyer-bridge/SKILL.md) | Translate what users need into what buyers will pay for. |
| [Business Model Canvas](unabatedpm-business-building/skills/business-model-canvas/SKILL.md) | Stress-test your business model with real unit economics. |
| [Product Objective Definition](unabatedpm-business-building/skills/product-objective-definition/SKILL.md) | Define objectives that drive decisions, not just decorate OKR slides. |
| [Unit Economics Calculator](unabatedpm-business-building/skills/unit-economics-calculator/SKILL.md) | Build CAC, LTV, and LTV:CAC models that survive CFO scrutiny. |
| [P&L Translation](unabatedpm-business-building/skills/pnl-translation/SKILL.md) | Speak the language of finance. Map product impact to P&L lines. |
| [Bridge Builder](unabatedpm-business-building/skills/bridge-builder/SKILL.md) | Connect user jobs to buyer economics through a 5-level bridge. |
| [ROI Calculator Builder](unabatedpm-business-building/skills/roi-calculator-builder/SKILL.md) | Build ROI models using Good/Better/Best that pass the 10X Rule. |

### Stakeholder & Customer Influence

| Skill | What It Coaches |
|---|---|
| [Adversarial Stakeholder Prep](unabatedpm-influence/skills/adversarial-stakeholder-prep/SKILL.md) | Decode the hidden incentive map of the room before you walk in. Risk Shields, Credit Catchers, Tribal Guardians. |
| [Interview Question Design](unabatedpm-influence/skills/interview-question-design/SKILL.md) | Design questions that uncover real problems, not confirmation bias. |
| [Journey Map Economic Overlay](unabatedpm-influence/skills/journey-map-economic-overlay/SKILL.md) | Turn journey maps from process diagrams into economic stories. |
| [Demo Script Reviewer](unabatedpm-influence/skills/demo-script-reviewer/SKILL.md) | Stop touring features. Start closing deals. Five-Act Demo Structure. |
| [Strategic Storytelling Pitch](unabatedpm-influence/skills/strategic-storytelling-pitch/SKILL.md) | Transform forgettable pitches into stories that get to "yes." |
| [Cafe Update](unabatedpm-influence/skills/cafe-update/SKILL.md) | Compress your impact into 60 seconds that land a follow-up meeting. |
| [Confidence Scenario Simulator](unabatedpm-influence/skills/confidence-scenario-simulator/SKILL.md) | Practice high-stakes conversations with realistic pushback before the real thing. |
| [First 90 Days Playbook](unabatedpm-influence/skills/first-90-days-playbook/SKILL.md) | Build influence in a new role by absorbing before directing. |

### Career Growth

| Skill | What It Coaches |
|---|---|
| [Resume as Product](unabatedpm-career-growth/skills/resume-as-product-coach/SKILL.md) | Treat your resume as a conversion funnel, not a biography. |
| [PM Interview Coach](unabatedpm-career-growth/skills/unabatedpm-interview-coach/SKILL.md) | Practice interviews as conversations, not rehearsed STAR performances. |
| [Niche Job Search Strategist](unabatedpm-career-growth/skills/niche-job-search-strategist/SKILL.md) | Fewer applications, better results. Run your search like a product launch. |
| [Career Transition Navigator](unabatedpm-career-growth/skills/career-transition-navigator/SKILL.md) | Map your non-PM background onto the Four Pillars. You already have 3 of 4. |
| [Impostor to Strategist](unabatedpm-career-growth/skills/impostor-to-strategist/SKILL.md) | Convert impostor syndrome into a career development strategy. |
| [Offer Negotiation Playbook](unabatedpm-career-growth/skills/offer-negotiation-playbook/SKILL.md) | Negotiate with leverage and total comp analysis, not emotion. |

---

## Guided Workflows

These chain 3 skills together into a complete coaching session. Available as slash commands in Claude Desktop and Claude Code, or paste the workflow file into any AI tool.

| Workflow | What It Does | Skills Used |
|---|---|---|
| [Coach Strategy](unabatedpm-strategic-thinking/commands/coach-strategy.md) | End-to-end strategy development | Vision Synthesis → Strategy Articulation → Stakeholder Reframe |
| [Coach Business Case](unabatedpm-business-building/commands/coach-business-case.md) | Build a business case that gets funded | Metrics Ladder → Unit Economics → P&L Translation |
| [Coach Pitch](unabatedpm-influence/commands/coach-pitch.md) | Craft and deliver a compelling pitch | Strategic Storytelling → Cafe Update → Confidence Simulator |
| [Coach Career](unabatedpm-career-growth/commands/coach-career.md) | Job search or career transition into PM | Resume → Niche Search → Interviews → Career Mapping → First 90 Days |

---

## Quick Example

Here's what a coaching session looks like. You provide context, the skill coaches you through the framework:

```
I'm pitching a new integration to three stakeholders on Thursday.
VP Sales wants it. VP Engineering just had a production incident.
CMO owns customer messaging. I have a clean ROI deck but I'm
worried about Engineering slowing it down.
```

The **Adversarial Stakeholder Prep** skill will:
1. Archetype each stakeholder (Risk Shield, Credit Catcher, or Tribal Guardian)
2. Ask three diagnostic questions per person (fired / promoted / validated)
3. Build the Adversarial Stakeholder Prompt so you can stress-test your read with AI
4. Read the three objections back — especially the one they'd never say out loud
5. Rewrite your opening sentence for the highest-risk person in the room

No generic advice. Specific coaching that forces you to decode the room, not just polish the deck.

---

## The Proof

500+ PMs coached. 36+ promotions within 6 months. 4.9/5 course rating on Maven. Used by PMs from startups to Fortune 500.

These skills encode 15+ years of product leadership into coaching frameworks that push your thinking — not textbook theory repackaged as AI prompts.

---

## About

Created by [Brennan Collins](https://unabatedproducts.com), founder of Unabated Products and creator of [The Influential PM](https://maven.com/unabated-products/the-influential-pm) course on Maven.

## License

MIT — use these skills however you want. If they help you grow as a PM, that's the goal.
