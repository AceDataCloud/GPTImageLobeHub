# GPT Image for LobeHub

This repository owns only the focused stdio proxy and LobeHub distribution metadata.
`AceDataCloud/MCPs/openai` and the pinned `mcp-openai-pro` dependency own API, auth,
billing, async response formatting, schema and error implementation. Do not copy
those internals or add fallback models/providers. Only GPT Image model IDs are
accepted for generation/editing. Preserve original task IDs and tool results.

Run `python -m pytest` for tests. Use dummy tokens and direct information tools;
never issue billable generation without current explicit allowance. Keep .env and
credentials out of commits, logs and screenshots. Marketplace publishing requires
an existing human publisher's auth/GitHub connection; do not create duplicate
identities or accept agreements. Code changes ship through Dev bot PRs, no merge.
