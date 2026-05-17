"""Register the Obsidian Agent plugin."""

from coco_codes.callbacks import register_callback

from .agent_obsidian import ObsidianAgent


def register_agents() -> list[dict[str, object]]:
    """Register the Obsidian Agent with Coco Codes's agent catalog."""
    return [{"name": "obsidian-agent", "class": ObsidianAgent}]


register_callback("register_agents", register_agents)
