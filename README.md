# Unabated PM Coaching Skills

**The first coaching-depth PM skills for AI.** Most PM skills tell AI what framework to apply. These teach AI how to coach you through it with scoring rubrics, behavioral markers, real coaching exchanges, and pushback on weak thinking.

Built from training and coaching 500+ product managers, dozens of student promotions and new jobs, and a 4.9/5 rated course on Maven.

## Why These Are Different

| | Template Skills | Coaching Skills (Unabated) |
|---|---|---|
| **Approach** | "Apply this framework" | "Let me push your thinking" |
| **Example exchanges** | None | Dozens per skill |
| **Scoring rubrics** | None | Multi-level with behavioral anchors |
| **Error correction** | None | Symptom / Diagnosis / Fix patterns |
| **Before/after** | None | Full paragraph-level transformations |
| **Practitioner voice** | Textbook | Opinionated, direct, uses real stories |
| **Adaptive behavior** | Same for all levels | Detects user level, adjusts coaching |

Template skills give you a well-organized MBA binder. Coaching skills give you a VP of Product who sits next to you and challenges your thinking in real time.

## Skills

### Strategic Thinking (`pm-strategic-thinking`)

| Skill | What It Coaches | Module |
|---|---|---|
| **Order Taker to Outcome Owner** | Transform from task executor to strategic PM | M1 |
| **Four Pillars PM Check** | Evaluate yourself across Strategy, Delivery, CX, Growth | M1 |
| **Vision Synthesis Coach** | Build a compelling product vision using the Vision Triangle | M4 |
| **Strategy Articulation Coach** | Pressure-test your strategy with the 5 Questions + DHM Filter | M4 |
| **Stakeholder Request Reframe** | Turn stakeholder demands into strategic conversations | M5 |
| **AI Career Impact Advisor** | Navigate AI's impact on PM with feature parity, human ingenuity, and career positioning | — |

### Business Building (`pm-business-building`)

| Skill | What It Coaches | Module |
|---|---|---|
| **Product Metrics Ladder** | Build metrics that ladder to business outcomes | M3 |
| **User-Buyer Bridge Coach** | Connect user needs to buyer economics | M3 |
| **Business Model Canvas Coach** | Stress-test your business model with unit economics | M6 |
| **Product Objective Definition Coach** | Define objectives that drive decisions, not vanity | M6 |
| **Unit Economics Calculator** | Build unit economics that survive CFO scrutiny | M6 |
| **P&L Translation Coach** | Speak the language of finance | M6 |
| **Bridge Builder Coach** | Connect features to revenue through a 5-level bridge | M7 |
| **ROI Calculator Builder** | Build defensible ROI models | M7 |

### Stakeholder & Customer Influence (`pm-influence`)

| Skill | What It Coaches | Module |
|---|---|---|
| **Interview Question Design Coach** | Design questions that reveal truth, not confirmation | M2 |
| **Journey Map Economic Overlay Coach** | Add economic context to journey maps | M2 |
| **Demo Script Reviewer** | Turn feature tours into deals that close | M7 |
| **Strategic Storytelling Pitch Coach** | Transform pitches into compelling stories | M8 |
| **Cafe Update Coach** | Compress impact into 60-second pitches | M8 |
| **Confidence Scenario Simulator** | Practice high-stakes conversations with realistic pushback | M8 |
| **First 90 Days Playbook** | Build influence in a new role through absorb-first strategy | — |

### Career Growth (`pm-career-growth`)

| Skill | What It Coaches |
|---|---|
| **Resume as Product Coach** | Redesign your resume as a conversion funnel with strategic storytelling |
| **PM Interview Coach** | Practice interviews with simulation, not STAR rehearsal |
| **Niche Job Search Strategist** | Narrow your search for fewer applications, better fits |
| **Career Transition Navigator** | Map your non-PM background onto the Four Pillars of PM |
| **Impostor to Strategist** | Convert impostor syndrome into a career development strategy |
| **Offer Negotiation Playbook** | Negotiate offers using leverage and total comp analysis |

## Workflows

Five chained workflows combine skills for end-to-end coaching:

- **Coach Strategy** (`pm-strategic-thinking/commands/coach-strategy.md`): Vision Synthesis → Strategy Articulation → Stakeholder Reframe
- **Coach Business Case** (`pm-business-building/commands/coach-business-case.md`): Metrics Ladder → Unit Economics → P&L Translation
- **Coach Pitch** (`pm-influence/commands/coach-pitch.md`): Strategic Storytelling → Cafe Update → Confidence Simulator
- **Coach Job Search** (`pm-career-growth/commands/coach-job-search.md`): Resume Design → Niche Search → Interview Simulation
- **Coach Career Pivot** (`pm-career-growth/commands/coach-career-pivot.md`): Career Transition → Impostor Strategy → First 90 Days

## Installation

### Claude Code / Cowork / Compatible AI Tools

Clone this repo and add the plugin directories to your configuration:

```bash
git clone https://github.com/BrennanJCollins/unabated-pm-coaching.git
```

Each plugin group (`pm-strategic-thinking`, `pm-business-building`, `pm-influence`, `pm-career-growth`) contains a `.claude-plugin/plugin.json` manifest for auto-discovery.

### Any LLM (ChatGPT, Gemini, etc.)

Each skill is a standalone markdown file. Copy the contents of any `SKILL.md` file and use it as a system prompt or custom instruction in your preferred AI tool.

### Using a Skill

Invoke any skill with your context. For example:

```
/cafe-update My product is a B2B analytics platform. I'm talking to our VP of Sales.
We just shipped a new dashboard that helped Acme Corp identify $2M in at-risk renewals.
```

The skill will coach you through the framework, push back on weak thinking, and help you iterate until your output is strong.

## The Proof

- **500+** PMs coached through mentorship and course cohorts
- **36+** student promotions within 6 months of course completion
- **4.9/5** course rating on Maven
- Used by PMs at companies from startups to Fortune 500

> "These aren't skills that write documents for you. They're skills that challenge your thinking the way a senior PM leader would." — Brennan Collins

## About

Created by [Brennan Collins](https://unabatedproducts.com), founder of Unabated Products and creator of [The Influential PM](https://maven.com/unabated-products/the-influential-pm) course on Maven.

The skills encode practitioner frameworks developed across 15+ years of product leadership — not textbook PM theory. Every coaching exchange, scoring rubric, and failure pattern comes from real mentorship sessions with real PMs facing real challenges.

## License

MIT — use these skills however you want. If they help you grow as a PM, that's the goal.

---

*Part of the [Unabated PM Coaching](https://unabatedproducts.com/ai-tools) skills suite.*
