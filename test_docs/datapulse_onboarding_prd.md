# PRD: Onboarding Flow Redesign

**Author:** Jamie Chen, Senior Product Manager
**Date:** March 2026
**Status:** Draft
**Squad:** Growth Squad

## Background

Our onboarding flow has a 34% completion rate. Industry benchmark for SaaS onboarding is 60-70%. We're losing users in the first 48 hours because the setup process is too complex and doesn't show value fast enough.

New users have to: (1) install the SDK, (2) configure data sources, (3) set up their first dashboard, (4) create alert rules. Most drop off between steps 2 and 3.

## Problem Statement

New DataPulse users struggle to complete onboarding because the current flow requires technical configuration before they can see any value from the product. Users who don't complete onboarding within 48 hours have a 78% churn rate within 30 days.

## Proposed Solution

Redesign the onboarding flow to deliver a "wow moment" within 15 minutes of signup by:

1. **Auto-detect existing data sources** — Scan for common integrations (Segment, Stripe, Intercom) and pre-configure connections
2. **Template dashboards** — Offer 3 pre-built dashboard templates based on company stage (seed, Series A, Series B+) so users see relevant metrics immediately
3. **Guided setup wizard** — Step-by-step flow with progress indicator, contextual help, and skip options for advanced users
4. **Sample data mode** — For users who haven't connected data yet, show the platform with realistic sample data so they can explore features

## User Stories

**As a** new user signing up for DataPulse,
**I want to** see meaningful analytics about my product within 15 minutes,
**So that** I can evaluate whether DataPulse is worth investing time in.

**As a** PM who doesn't have engineering resources available,
**I want to** explore the platform with sample data,
**So that** I can understand the value before asking my team to integrate.

**As a** technical user setting up DataPulse,
**I want** the setup wizard to detect my existing tools and pre-configure connections,
**So that** I don't have to manually configure each integration.

## Requirements

### Must Have (P0)
- Auto-detection for Segment, Stripe, and Intercom integrations
- 3 template dashboards (startup metrics, growth metrics, enterprise metrics)
- Progress bar showing onboarding completion %
- Ability to skip any step and come back later

### Should Have (P1)
- Sample data mode with realistic SaaS metrics
- In-app tooltips explaining each dashboard widget
- Email drip for users who abandon onboarding (day 1, 3, 7)

### Nice to Have (P2)
- Video walkthrough embedded in the wizard
- Slack integration for onboarding notifications
- A/B test capability for different onboarding flows

## Success Metrics

- Onboarding completion rate: 34% -> 55% (within 60 days of launch)
- Time to first dashboard: < 15 minutes for 80% of users
- 7-day retention for new signups: 45% -> 60%
- NPS for onboarding experience: > 40

## Technical Considerations

- Auto-detection requires OAuth flows for each integration
- Sample data needs to be refreshed periodically to look realistic
- Template dashboards need to be maintainable as we add new features
- Should work on mobile (many PMs check analytics on phone)

## Timeline

- Week 1-2: Design + engineering scoping
- Week 3-6: Build auto-detection + templates
- Week 7-8: Sample data mode + testing
- Week 9: Beta with 10 existing customers
- Week 10: GA launch

## Open Questions

- Should we require credit card at signup or keep it free trial?
- How do we handle companies with non-standard data stacks?
- Do we need a separate onboarding for the admin vs. regular users?

## Appendix

Current onboarding funnel:
- Signup: 100%
- SDK installed: 67%
- Data source connected: 48%
- First dashboard created: 34%
- First alert configured: 22%
