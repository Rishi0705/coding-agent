<div align="center">

# Coding Agent 🤖

**A professional AI-powered code generation agent for software engineering**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## Overview

Coding Agent is an AI-powered agentic coding tool that understands programming tasks, generates high-quality code, and executes changes directly in your codebase. It provides a terminal-based interface similar to tools like Cursor or Windsurf, but runs entirely in your CLI with full transparency.

### Key Features

- **Multi-model support** — OpenAI, Anthropic, Google Gemini, Cerebras, Ollama, and 65+ providers via [models.dev](https://models.dev)
- **Tool-augmented execution** — File operations, shell commands, grep, and more
- **MCP (Model Context Protocol)** — Extend functionality with external tool servers
- **Custom agents** — Create specialized agents via JSON or Python
- **Round-robin model distribution** — Distribute load across multiple API keys/models
- **Session management** — Save, resume, and manage coding sessions
- **Plugin architecture** — Extend with custom commands, hooks, and integrations
- **Privacy-first** — Zero telemetry, zero data collection, fully local option available

---

## Quick Start

```bash
uvx coding-agent
```

## Installation

### UV (Recommended)

```bash
# Install UV if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run directly
uvx coding-agent
```

### Windows

```powershell
# Install UV
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

uvx coding-agent
```

### pip

```bash
pip install coding-agent
```

---

## Configuration

### Environment Variables

Set API keys for the providers you want to use:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."
export CEREBRAS_API_KEY="csk-..."
```

### Custom Models

Add custom model configurations in `~/.coding_agent/extra_models.json`:

```json
{
  "my_model": {
    "type": "custom_openai",
    "name": "gpt-4",
    "custom_endpoint": {
      "url": "https://your-endpoint.com/v1",
      "api_key": "$YOUR_API_KEY"
    }
  }
}
```

### Adding Models from models.dev

```bash
/add_model
```

Browse and add models from 65+ providers with an interactive TUI.

---

## Usage

### Commands

| Command | Description |
|---------|-------------|
| `/model` | Switch between configured AI models |
| `/add_model` | Browse and add models from models.dev |
| `/agent` | View or switch between agents |
| `/mcp` | Manage MCP server connections |
| `/save` | Save current session |
| `/load` | Load a previous session |
| `/truncate N` | Keep only N most recent messages |
| `/help` | Show all available commands |

### Agent System

Coding Agent supports multiple specialized agents:

- **coding-agent** (default) — General-purpose coding assistant
- **agent-creator** — Build custom agents interactively
- Custom JSON agents — Define in `~/.coding_agent/agents/`

#### Creating Custom Agents

Create a JSON file in `~/.coding_agent/agents/`:

```json
{
  "name": "code-reviewer",
  "display_name": "Code Reviewer 🔍",
  "description": "Reviews code for best practices and improvements",
  "system_prompt": [
    "You are a senior software engineer performing code reviews.",
    "Focus on code quality, security, and maintainability.",
    "Provide constructive feedback with specific suggestions."
  ],
  "tools": ["list_files", "read_file", "grep"]
}
```

### MCP Servers

Extend Coding Agent with external tools via MCP:

```bash
/mcp install    # Install a new MCP server
/mcp list       # List configured servers
/mcp status     # Check server health
```

### Round-Robin Model Distribution

Distribute requests across multiple API keys to manage rate limits:

```json
{
  "model_1": { "type": "cerebras", "name": "qwen-3-coder-480b", "custom_endpoint": { "url": "https://api.cerebras.ai/v1", "api_key": "$KEY_1" } },
  "model_2": { "type": "cerebras", "name": "qwen-3-coder-480b", "custom_endpoint": { "url": "https://api.cerebras.ai/v1", "api_key": "$KEY_2" } },
  "round_robin": { "type": "round_robin", "models": ["model_1", "model_2"], "rotate_every": 5 }
}
```

---

## Agent Rules

Coding Agent supports `AGENTS.md` files for defining project-specific coding standards and conventions.

### Search Order

| Priority | Location | Purpose |
|----------|----------|---------|
| 1 | `~/.coding_agent/AGENTS.md` | Global rules |
| 2 | `.coding_agent/AGENTS.md` | Project rules (preferred) |
| 3 | `./AGENTS.md` | Project rules (alternate) |

---

## Architecture

```
coding_agent/
├── agents/          # Agent definitions and management
├── command_line/    # CLI commands and TUI components
├── hook_engine/     # Hook/event system
├── mcp_/           # MCP server management
├── messaging/      # Message bus and rendering
├── plugins/        # Plugin system (extensible)
└── tools/          # Tool implementations (file ops, shell, etc.)
```

### Plugin System

All new functionality is implemented as plugins:

```python
# coding_agent/plugins/my_feature/register_callbacks.py
from coding_agent.callbacks import register_callback

def _on_startup():
    print("my_feature loaded!")

register_callback("startup", _on_startup)
```

---

## Privacy

- **Zero telemetry** — No usage analytics or behavioral tracking
- **Zero prompt logging** — Your code and conversations are never stored remotely
- **Complete local option** — Run with Ollama or local VLLM for fully offline operation
- **Direct LLM communication** — Prompts go only to your configured provider

---

## Requirements

- Python 3.11+
- At least one LLM API key (OpenAI, Anthropic, Gemini, Cerebras, or Ollama)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
