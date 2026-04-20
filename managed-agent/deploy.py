#!/usr/bin/env python3
"""
Deploy the Unabated PM Coach managed agent to Anthropic.

Reads agent.json + system-prompt.md + environment.json from this directory and:
  - Creates or updates the agent (if AGENT_ID env var is set, update; else create)
  - Creates or updates the environment (by name lookup)
  - Writes the resulting IDs to state.json so the MCP broker can reference them

Usage:
    export ANTHROPIC_API_KEY=...
    python deploy.py [--env staging|production] [--dry-run]

Requires: pip install anthropic>=0.45.0
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    sys.exit("anthropic SDK not installed. Run: pip install 'anthropic>=0.45.0'")

HERE = Path(__file__).resolve().parent
STATE_FILE = HERE / "state.json"


def load_agent_config() -> dict:
    config = json.loads((HERE / "agent.json").read_text())
    prompt_path = HERE / config.pop("system_prompt_file")
    config["system"] = prompt_path.read_text()
    return config


def load_environment_config() -> dict:
    return json.loads((HERE / "environment.json").read_text())


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"environments": {}, "agents": {}}


def save_state(state: dict) -> None:
    state["last_deployed_at"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def upsert_environment(client: Anthropic, env_config: dict, state: dict, env_tag: str) -> str:
    name = f"{env_config['name']}-{env_tag}"
    existing_id = state["environments"].get(env_tag)

    if existing_id:
        try:
            client.beta.environments.retrieve(existing_id)
            print(f"[env] reusing {existing_id} ({name})")
            return existing_id
        except Exception as e:
            print(f"[env] stored id {existing_id} not retrievable ({e}); creating new")

    env = client.beta.environments.create(name=name, config=env_config["config"])
    print(f"[env] created {env.id} ({name})")
    state["environments"][env_tag] = env.id
    return env.id


def upsert_agent(client: Anthropic, agent_config: dict, state: dict, env_tag: str) -> tuple[str, int]:
    base_name = agent_config.pop("name")
    agent_config["name"] = f"{base_name}-{env_tag}"
    existing = state["agents"].get(env_tag)

    if existing:
        agent_id = existing["id"]
        try:
            current = client.beta.agents.retrieve(agent_id)
            updated = client.beta.agents.update(
                agent_id,
                version=current.version,
                system=agent_config["system"],
                description=agent_config.get("description"),
                tools=agent_config.get("tools", []),
                mcp_servers=agent_config.get("mcp_servers", []),
                skills=agent_config.get("skills", []),
                metadata=agent_config.get("metadata", {}),
            )
            print(f"[agent] updated {agent_id} → version {updated.version}")
            state["agents"][env_tag] = {"id": agent_id, "version": updated.version}
            return agent_id, updated.version
        except Exception as e:
            print(f"[agent] stored id {agent_id} not updatable ({e}); creating new")

    agent = client.beta.agents.create(**agent_config)
    print(f"[agent] created {agent.id} version {agent.version}")
    state["agents"][env_tag] = {"id": agent.id, "version": agent.version}
    return agent.id, agent.version


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default="staging", choices=["staging", "production"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if "ANTHROPIC_API_KEY" not in os.environ:
        sys.exit("ANTHROPIC_API_KEY is not set")

    agent_config = load_agent_config()
    env_config = load_environment_config()

    if args.dry_run:
        print("=== DRY RUN ===")
        print(f"[env] would create/update {env_config['name']}-{args.env}")
        print(f"[agent] would create/update {agent_config['name']}-{args.env} (system prompt: {len(agent_config['system'])} chars)")
        return

    client = Anthropic()
    state = load_state()

    env_id = upsert_environment(client, env_config, state, args.env)
    agent_id, agent_version = upsert_agent(client, agent_config, state, args.env)

    save_state(state)

    print("\n=== deploy complete ===")
    print(f"env:   {args.env}")
    print(f"agent: {agent_id} v{agent_version}")
    print(f"environment: {env_id}")
    print(f"state saved: {STATE_FILE}")
    print("\nNext: point the MCP broker at these IDs via env vars:")
    print(f"  UNABATED_AGENT_ID={agent_id}")
    print(f"  UNABATED_ENVIRONMENT_ID={env_id}")


if __name__ == "__main__":
    main()
