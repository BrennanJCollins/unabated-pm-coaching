# Unabated PM Coach — Managed Agent

Deployable configuration for the Unabated PM Coach running on Anthropic's Managed Agents infrastructure. Not for direct end-user installation — this is the server-side agent that the `mcp.unabatedpm.com` broker invokes on behalf of paying customers.

For the free, open-source version that end users can install directly into Claude Cowork, see the parent repo's `unabatedpm-coaching-os/` plugin. This managed-agent path adds credit metering, ledger persistence, and the hosted workflow.

## What's in this directory

| File | Purpose |
| --- | --- |
| `agent.json` | Agent config manifest (model, tools, MCP servers, skills, metadata). `system_prompt_file` points at the full orchestration prompt. |
| `system-prompt.md` | The orchestration prompt itself. Defines the audit / upgrade / develop modes and the envelope contract with the MCP broker. |
| `environment.json` | Cloud container config: Python + LibreOffice + pandoc + pdf utils, networking locked to `api.unabatedpm.com`. |
| `deploy.py` | Idempotent deploy script. Creates or updates the agent + environment in Anthropic. Writes `state.json` with the resulting IDs. |
| `state.json` | (generated) Deploy state. Maps env tag → agent id + version + environment id. Committed so the broker can read it. |

## Prerequisites

1. Anthropic API key with Managed Agents beta access (enabled by default for all API accounts as of 2026-04-08).
2. Python 3.11+ with `pip install 'anthropic>=0.45.0'`.
3. The `mcp.unabatedpm.com` backend reachable from Anthropic's cloud containers (must be HTTPS, must be in the environment's `allowed_hosts`).

## Deploy

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

# Staging first
python deploy.py --env staging

# Then production after smoke tests pass
python deploy.py --env production
```

The script is idempotent. First run creates; subsequent runs update. Agent versions bump on every non-no-op update. Environment updates are not versioned, so if you change `environment.json`, the next session picks up the new container config.

Dry run (no API calls, just shows what would happen):

```bash
python deploy.py --env staging --dry-run
```

## Test the agent end-to-end

After deploy, smoke-test directly against Anthropic before wiring up the MCP broker:

```python
from anthropic import Anthropic
import json, pathlib

client = Anthropic()
state = json.loads(pathlib.Path("state.json").read_text())
agent_id = state["agents"]["staging"]["id"]
env_id = state["environments"]["staging"]

session = client.beta.sessions.create(
    agent=agent_id,
    environment_id=env_id,
    title="Smoke test — audit a PRD",
)

envelope = {
    "operation": "audit",
    "license_id": "lic_test",
    "user_id": "usr_test",
    "document": {
        "filename": "test_prd.md",
        "format": "md",
        "content_hash": "sha256:TESTHASH",
        "path": "/workspace/test_prd.md",
    },
    "context": {"prior_scores": None},
    "paywall_signal": {"free_upgrade_runs_remaining": 3, "tier": "free"},
}

# TODO: upload the test doc into the container first — see files API
client.beta.sessions.events.send(
    session.id,
    events=[{"type": "user.message", "content": [{"type": "text", "text": json.dumps(envelope)}]}],
)

with client.beta.sessions.events.stream(session.id) as stream:
    for event in stream:
        if event.type == "agent.message":
            for block in event.content:
                print(block.text, end="")
        elif event.type == "session.status_idle":
            break
```

Expected output: a Four Pillars scoring report with 16 category scores, evidence quotes, and 5 leverage recommendations.

## Cost expectations per operation

| Operation | Session runtime | Input tokens | Output tokens | Est. cost |
| --- | --- | --- | --- | --- |
| `audit` | ~5–10 min | ~30K | ~8K | ~$0.36 |
| `upgrade` | ~15–45 min | ~50K | ~20K | ~$0.79 |
| `develop` | ~5–15 min | ~40K | ~12K | ~$0.50 |

Runtime is $0.08/session-hour billed to the millisecond. Tokens are standard Opus 4.7 rates ($5/M input, $25/M output). Prompt caching cuts input costs up to 90% on cache hits — expect real-world input cost to be 50–70% of the nominal rate once traffic warms up.

## Next steps after first successful deploy

1. Build the `mcp.unabatedpm.com` broker (separate repo). It reads `state.json`, spawns sessions on user requests, streams events back via MCP tool progress.
2. Wire the ledger endpoint at `api.unabatedpm.com/v1/ledger` so the agent's outbound HTTP writes persist.
3. Run the verification checklist from `/Users/brennancollins/.claude/plans/we-ve-been-going-back-piped-neumann.md`.

## Branding compliance

This agent surfaces as "Unabated PM Coach Powered by Claude" per Anthropic's Managed Agents brand guidelines. Never present it as "Claude Code" or "Claude Cowork" — that's against the brand policy and risks beta access.
