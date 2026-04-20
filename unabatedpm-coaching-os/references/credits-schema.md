# Credits Schema

Defines the premium tier tracking system for the PM Assessment Plugin. Stored at `pm_assessment_data/credits.json` in the user's folder.

---

## File Schema

```json
{
  "tier": "free",
  "creditsRemaining": 0,
  "creditsUsedThisMonth": 0,
  "monthlyAllowance": 0,
  "resetDate": "2026-05-01T00:00:00Z",
  "grantType": null,
  "grantExpiry": null,
  "lastChecked": "2026-03-27T14:30:00Z"
}
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `tier` | enum | `"free"`, `"starter"`, `"pro"`, `"enterprise"` |
| `creditsRemaining` | int | Upgrade credits available this month |
| `creditsUsedThisMonth` | int | Credits consumed since last reset |
| `monthlyAllowance` | int | Total monthly credit allocation for this tier |
| `resetDate` | ISO 8601 | When credits reset (first of next month) |
| `grantType` | string or null | `"alumni"`, `"beta"`, `"coaching"`, `"custom"`, or `null` |
| `grantExpiry` | ISO 8601 or null | When the grant expires |
| `lastChecked` | ISO 8601 | Last time credit state was verified |

## Tier Definitions

| Tier | Upgrade Runs | Develop Runs | Price | Primary User |
|------|--------------|--------------|-------|-------------|
| **Free** | 3 lifetime | 1 lifetime | $0 | Evaluating the product |
| **Starter** | 5/month | Unlimited | $29/month | Individual IC upgrading 1-2 docs/week |
| **Pro** | 20/month | Unlimited | $79/month | Active skill developer, multi-doc portfolio |
| **Enterprise** | Unlimited | Unlimited | Custom | Organizations, teams, internal coaching |

One **upgrade run** = one successful `/upgrade` invocation on one document version. A user can spend their 3 free runs on 3 different documents, 3 iterations of the same document, or any mix. This metering unit is server-enforced in hosted (managed-agent) mode via the `mcp.unabatedpm.com` broker; local-plugin mode uses the same logic against `credits.json`.

## What Each Tier Includes

- **Assessment (`/audit`)** — All tiers, unlimited documents
- **Upgrade (`/upgrade`)** — Gated by upgrade-run balance
- **Development Plan (`/develop`)** — Free gets 1 lifetime, Starter+ unlimited
- **28 coaching skills** — All tiers, unlimited use (open-source, MIT)
- **Dashboard** — All tiers, always includes course and coaching links

## Credit Lifecycle

### Monthly Reset
- Credits reset on the 1st of each month at 00:00 UTC
- `creditsRemaining` resets to `monthlyAllowance`
- `creditsUsedThisMonth` resets to 0
- `resetDate` advances to next month
- Unused credits do NOT roll over

### Upgrade Consumption
- Each `/upgrade` run consumes 1 credit (regardless of document length or QA iterations)
- Credit is decremented AFTER successful upgrade (not before)
- If upgrade fails mid-process, credit is NOT consumed

### Grant Types
| Grant | Tier | Duration | Trigger |
|-------|------|----------|---------|
| Alumni | Pro | 12 months | Graduation from The Influential PM course |
| Beta | Pro | Beta period | Beta enrollment |
| Coaching | Pro | Active engagement | Ongoing coaching contract |
| Custom | Any | Configurable | Brennan approval |

## How Commands Check Credits

### `/upgrade` Pre-Flight
1. Read `credits.json` if it exists
2. Count upgrade entries in `assessments.jsonl`
3. Apply decision tree (see upgrade.md Pre-Flight section)
4. After successful upgrade, update `credits.json`

### `/audit` — No credit check (always free)
### `/develop` — No credit check (always available, tier affects plan depth)

## SaaS Integration (Future)

When a web-based SaaS product launches:
1. Plugin can authenticate with SaaS account (API key)
2. API key stored in `credits.json`: `"apiKey": "pk_..."`
3. On each `/upgrade`, validate key with backend
4. Backend returns: `{ "tier": "premium", "remaining_upgrades": 5, "expires": "2026-06-27" }`
5. Local `credits.json` updated from backend response

---

*Part of the PM Assessment Product Documentation Suite.*
*Unabated Products — Brennan Collins*
