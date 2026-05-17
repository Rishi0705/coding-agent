"""Plugin: drop user input onto a fresh line below the prompt chrome.

When enabled, transforms

    coco [agent] [model] (~/very/long/cwd) >>> typed text

into

    coco [agent] [model] (~/very/long/cwd) >>>
    typed text

Toggle at runtime with ``/prompt_newline [on|off]``. Persisted in coco.cfg.
"""
