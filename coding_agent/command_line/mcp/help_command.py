"""
MCP Help Command - Shows help for all MCP commands.
"""

import logging
from typing import List, Optional

from rich.text import Text

from coding_agent.messaging import emit_error, emit_info

from .base import MCPCommandBase

# Configure logging
logger = logging.getLogger(__name__)


class HelpCommand(MCPCommandBase):
    """
    Command handler for showing MCP command help.

    Displays comprehensive help information for all available MCP commands.
    """

    def execute(self, args: List[str], group_id: Optional[str] = None) -> None:
        """
        Show help for MCP commands.

        Args:
            args: Command arguments (unused)
            group_id: Optional message group ID for grouping related messages
        """
        if group_id is None:
            group_id = self.generate_group_id()

        try:
            # Build help text programmatically to avoid markup conflicts
            help_lines = []

            # Title
            help_lines.append(
                Text("MCP Server Management Commands", style="fg:ansibrightgreen bold")
            )
            help_lines.append(Text(""))

            # Registry Commands
            help_lines.append(Text("Registry Commands:", style="fg:ansibrightgreen bold"))
            help_lines.append(
                Text("/mcp search", style="green")
                + Text(" [query]     Search 30+ pre-configured servers")
            )
            help_lines.append(
                Text("/mcp install", style="green")
                + Text(" <id>       Install server from registry")
            )
            help_lines.append(Text(""))

            # Core Commands
            help_lines.append(Text("Core Commands:", style="fg:ansibrightgreen bold"))
            help_lines.append(
                Text("/mcp", style="green")
                + Text("                    List all registered servers")
            )
            help_lines.append(
                Text("/mcp start", style="green")
                + Text(" <name>       Start a specific server")
            )
            help_lines.append(
                Text("/mcp start-all", style="green")
                + Text("          Start all servers")
            )
            help_lines.append(
                Text("/mcp stop", style="green")
                + Text(" <name>        Stop a specific server")
            )
            help_lines.append(
                Text("/mcp stop-all", style="green")
                + Text(" [group_id]  Stop all running servers")
            )
            help_lines.append(
                Text("/mcp restart", style="green")
                + Text(" <name>     Restart a specific server")
            )
            help_lines.append(Text(""))

            # Management Commands
            help_lines.append(Text("Management Commands:", style="fg:ansibrightgreen bold"))
            help_lines.append(
                Text("/mcp status", style="green")
                + Text(" [name]      Show detailed status (all servers or specific)")
            )
            help_lines.append(
                Text("/mcp logs", style="green")
                + Text(" <name> [limit] Show recent events (default limit: 10)")
            )
            help_lines.append(
                Text("/mcp edit", style="green")
                + Text(" <name>        Edit existing server config")
            )
            help_lines.append(
                Text("/mcp remove", style="green")
                + Text(" <name>      Remove/disable a server")
            )
            help_lines.append(
                Text("/mcp help", style="green")
                + Text("               Show this help message")
            )
            help_lines.append(Text(""))

            # Status Indicators
            help_lines.append(Text("Status Indicators:", style="bold"))
            help_lines.append(
                Text("Running    Stopped    Error    Quarantined    Popular")
            )
            help_lines.append(Text(""))

            # Examples
            help_lines.append(Text("Examples:", style="bold"))
            examples_text = """/mcp search database     # Find database servers
/mcp install postgres    # Install PostgreSQL server
/mcp start filesystem    # Start a specific server
/mcp start-all           # Start all servers at once
/mcp stop-all            # Stop all running servers
/mcp edit filesystem     # Edit an existing server config
/mcp remove filesystem # Remove a server"""
            help_lines.append(Text(examples_text, style="dim"))

            # Combine all lines
            final_text = Text()
            for i, line in enumerate(help_lines):
                if i > 0:
                    final_text.append("\n")
                final_text.append_text(line)

            emit_info(final_text, message_group=group_id)

        except Exception as e:
            logger.error(f"Error showing help: {e}")
            emit_error(f"Error showing help: {e}", message_group=group_id)
