"""Slide content for the onboarding wizard.

Lean, mean, concise slides. 5 slides max!
"""

from typing import List, Tuple

# ============================================================================
# Slide Data Constants
# ============================================================================

# Model subscription options
MODEL_OPTIONS: List[Tuple[str, str, str]] = [
    ("chatgpt", "ChatGPT Plus/Pro/Max", "OAuth login - no API key needed"),
    ("claude", "Claude Code Pro/Max", "OAuth login - no API key needed"),
    ("api_keys", "API Keys", "OpenAI, Anthropic, Google, etc."),
    ("openrouter", "OpenRouter", "Single key for 100+ models"),
    ("skip", "Skip for now", "Configure later with /set or /add_model"),
]


# ============================================================================
# Navigation Footer (shown on ALL slides)
# ============================================================================


def get_nav_footer() -> str:
    """Navigation hints shown at bottom of every slide."""
    return (
        "\n[dim][/dim]\n"
        "[bright_green]→/l[/bright_green] Next  "
        "[bright_green]←/h[/bright_green] Back  "
        "[bright_green]↑↓/jk[/bright_green] Options  "
        "[bright_green]Enter[/bright_green] Select  "
        "[bright_green]ESC[/bright_green] Skip"
    )


# ============================================================================
# Gradient Banner
# ============================================================================


def get_gradient_banner() -> str:
    """Generate the gradient COCO CODES banner."""
    try:
        import pyfiglet

        lines = pyfiglet.figlet_format("COCO CODES", font="ansi_shadow").split("\n")
        colors = ["bright_green"]
        result = []
        for i, line in enumerate(lines):
            if line.strip():
                color = colors[min(i // 2, len(colors) - 1)]
                result.append(f"[{color}]{line}[/{color}]")
        return "\n".join(result)
    except ImportError:
        return "[bold bright_green]COCO CODES [/bold bright_green]"


# ============================================================================
# Slide Content (5 slides total)
# ============================================================================


def slide_welcome() -> str:
    """Slide 1: Welcome - quick intro."""
    content = get_gradient_banner()
    content += "\n\n"
    content += "[bold white]Welcome! [/bold white]\n\n"
    content += "[bright_green]Quick setup:[/bright_green]\n"
    content += "  1. Pick your model provider\n"
    content += "  2. Optional: MCP servers\n"
    content += "  3. Learn when to use which agent\n"
    content += "  4. Start coding!\n\n"
    content += "[dim]Takes ~1 minute. Let's go![/dim]"
    content += get_nav_footer()
    return content


def slide_models(selected_option: int, options: List[Tuple[str, str]]) -> str:
    """Slide 2: Model selection."""
    content = "[bold bright_green]Pick Your Models[/bold bright_green]\n\n"
    content += "[white]How do you want to access LLMs?[/white]\n\n"

    for i, (_, label) in enumerate(options):
        if i == selected_option:
            content += f"[bold bright_green]{label}[/bold bright_green]\n"
        else:
            content += f"[dim]  {label}[/dim]\n"

    content += "\n"

    # Context based on selection
    opt = options[selected_option][0] if options else None
    if opt == "chatgpt":
        content += "[bright_green]ChatGPT OAuth[/bright_green]\n"
        content += "  Uses your existing subscription\n"
        content += "  GPT-5.2, GPT-5.2-codex\n"
    elif opt == "claude":
        content += "[bright_green]Claude OAuth[/bright_green]\n"
        content += "  Uses your existing subscription\n"
        content += "  Opus/Sonnet/Haiku 4.5\n"
    elif opt == "api_keys":
        content += "[bright_green]API Keys[/bright_green]\n"
        content += "  [bright_green]/set OPENAI_API_KEY=sk-...[/bright_green]\n"
        content += "  [bright_green]/add_model[/bright_green] to browse 1500+ models\n"
    elif opt == "openrouter":
        content += "[bright_green]OpenRouter[/bright_green]\n"
        content += "  One API key, all providers\n"
        content += "  [bright_green]/set OPENROUTER_API_KEY=...[/bright_green]\n"
    else:
        content += "[dim]No worries! Use /set or /add_model later[/dim]\n"

    content += get_nav_footer()
    return content


def slide_mcp() -> str:
    """Slide 3: MCP servers (optional power-ups)."""
    content = "[bold bright_green]MCP Servers (Optional)[/bold bright_green]\n\n"
    content += "[white]Supercharge with external tools![/white]\n\n"
    content += "[bright_green]Commands:[/bright_green]\n"
    content += "  [bright_green]/mcp install[/bright_green]  Browse catalog\n"
    content += "  [bright_green]/mcp list[/bright_green]     See your servers\n\n"
    content += "[bright_green]Popular picks:[/bright_green]\n"
    content += "  • GitHub integration\n"
    content += "  • Postgres/databases\n"
    content += "  • Slack, Linear, etc.\n\n"
    content += "[dim]Skip this if you just want to code![/dim]"
    content += get_nav_footer()
    return content


def slide_use_cases() -> str:
    """Slide 4: When to use which agent - THE IMPORTANT ONE."""
    content = "[bold bright_green]When to Use What[/bold bright_green]\n\n"

    content += "[bold bright_green]Coco Codes (default)[/bold bright_green]\n"
    content += "  [bright_green]USE FOR:[/bright_green] Direct coding tasks\n"
    content += "  • Fix this bug\n"
    content += "  • Add a feature to this file\n"
    content += "  • Refactor this function\n"
    content += "  • Write tests for X\n\n"

    content += "[bold bright_green]Planning Agent[/bold bright_green]\n"
    content += "  [bright_green]USE FOR:[/bright_green] Complex multi-step projects\n"
    content += "  • Build me a REST API with auth\n"
    content += "  • Create a CLI tool from scratch\n"
    content += "  • Refactor entire codebase\n"
    content += "  • Multi-file architectural changes\n\n"

    content += "[bright_green]Switch: /agent planning-agent[/bright_green]\n"
    content += "[dim]Planning breaks big tasks into steps,[/dim]\n"
    content += "[dim]then delegates to specialists.[/dim]"
    content += get_nav_footer()
    return content


def slide_done(trigger_oauth: str | None) -> str:
    """Slide 5: You're ready!"""
    content = "[bold bright_green]Ready to Roll![/bold bright_green]\n\n"
    content += "[bold bright_green]Essential commands:[/bold bright_green]\n"
    content += "  [bright_green]/model[/bright_green]   Switch models\n"
    content += "  [bright_green]/agent[/bright_green]   Switch agents\n"
    content += "  [bright_green]/help[/bright_green]    All commands\n\n"

    content += "[bold bright_green]Pro tips:[/bold bright_green]\n"
    content += "  • Be specific in prompts\n"
    content += "  • Use Planning Agent for big tasks\n"
    content += "  • @ for file path completion\n\n"

    if trigger_oauth:
        content += f"[bold bright_green]→ {trigger_oauth.title()} OAuth next![/bold bright_green]\n\n"

    content += "[dim]Re-run anytime: [/dim][bright_green]/tutorial[/bright_green]\n"
    content += "\n[bold bright_green]Press Enter to start coding! [/bold bright_green]"
    content += get_nav_footer()
    return content
