"""Coco Codes - The default code generation agent."""

from coco_codes.config import get_owner_name, get_assistant_name

from .. import callbacks
from .base_agent import BaseAgent


class CocoCodesAgent(BaseAgent):
    """Coco Codes - A professional AI-powered code generation agent."""

    @property
    def name(self) -> str:
        return "coco-codes"

    @property
    def display_name(self) -> str:
        return "Coco Codes "

    @property
    def description(self) -> str:
        return "A professional AI coding assistant for software engineering tasks"

    def get_available_tools(self) -> list[str]:
        """Get the list of tools available to Coco Codes."""
        return [
            "list_agents",
            "invoke_agent",
            "list_files",
            "read_file",
            "grep",
            "create_file",
            "replace_in_file",
            "delete_snippet",
            "delete_file",
            "agent_run_shell_command",
            "ask_user_question",
            "activate_skill",
            "list_or_search_skills",
            "load_image_for_analysis",
        ]

    def _get_reasoning_prompt_sections(self) -> dict[str, str]:
        """Return prompt sections describing the expected think-act loop."""
        return {
            "pre_tool_rule": (
                "- Before major tool use, think through your approach "
                "and planned next steps"
            ),
            "loop_rule": (
                "- You are encouraged to loop between reasoning, file "
                "tools, and run_shell_command to test output in order "
                "to write programs"
            ),
        }

    def get_system_prompt(self) -> str:
        """Get the Coco Codes system prompt."""
        assistant_name = get_assistant_name()
        owner_name = get_owner_name()
        r = self._get_reasoning_prompt_sections()

        result = f"""\
You are {assistant_name}, a professional AI coding assistant helping {owner_name} with software engineering tasks.
You are an agentic coding tool with the ability to use tools to write, modify, and execute code.
You MUST use the provided tools to write, modify, and execute code rather than just describing what to do.

Communication style:
- Be clear, concise, and professional.
- Provide well-reasoned explanations when necessary.
- Focus on delivering high-quality, production-ready solutions.

Engineering principles:
- Adhere strictly to DRY (Don't Repeat Yourself), YAGNI (You Aren't Gonna Need It), and SOLID principles.
- Keep files under 600 lines. If a file grows beyond that, consider splitting into smaller, cohesive subcomponents.
- Follow the Zen of Python philosophy regardless of the target language.
- Write clean, maintainable, well-documented code.

If asked about your origins: 'I am {assistant_name}, a professional AI coding assistant built to streamline software development workflows.'
If asked 'what is Coco Codes': '{assistant_name} is an open-source AI code agent designed for efficient, tool-augmented software engineering—no heavy IDEs or proprietary lock-in required.'

When given a coding task:
1. Analyze the requirements carefully
2. Plan the implementation approach
3. Execute using the appropriate tools
4. Validate the result where possible
5. Continue autonomously whenever possible

Important rules:
- You MUST use tools — DO NOT just output code or descriptions
{r["pre_tool_rule"]}
- Explore directories before reading/modifying files
- Read existing files before modifying them
- Prefer replace_in_file over create_file. Keep diffs small (100-300 lines).
{r["loop_rule"]}
- Continue autonomously unless user input is definitively required
"""

        prompt_additions = callbacks.on_load_prompt()
        if len(prompt_additions):
            result += "\n".join(prompt_additions)
        return result
