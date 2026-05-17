"""Register the Obsidian Agent plugin."""

from coding_agent.callbacks import register_callback

from .agent_obsidian import ObsidianAgent


def register_agents() -> list[dict[str, object]]:
    """Register the Obsidian Agent with Coding Agent's agent catalog."""
    return [{"name": "obsidian-agent", "class": ObsidianAgent}]


register_callback("register_agents", register_agents)
