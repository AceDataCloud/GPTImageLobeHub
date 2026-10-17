# GPT Image by Ace Data Cloud for LobeHub

[简体中文](README_zh-CN.md) · [Official market search — focused listing pending](https://lobehub.com/mcp?q=GPT%20Image) · [Current API/pricing](https://platform.acedata.cloud/documents/openai-images-generations?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt-image_lobehub_readme_pricing)

GPT Image generation and editing, provided by **Ace Data Cloud**. This is an Ace integration, not an official plugin from the model vendor. It reuses [OpenAIMCP](https://github.com/AceDataCloud/OpenAIMCP) and the existing `mcp-openai-pro` server; no duplicate generation backend or new publisher identity is created.

> Publication status (2026-10-18): **new focused adapter, not published to PyPI or LobeHub yet**. The planned identifier is `acedatacloud-gptimagelobehub`. This is a separate image-only tool surface, not a duplicate copy of OpenAIMCP. The existing broad [OpenAIMCP card](https://lobehub.com/mcp/acedatacloud-openaimcp) remains a fallback until this independent entry is published. Source installation is a developer/manual path, not normal marketplace installation.

The adapter reuses pinned `mcp-openai-pro==2026.10.17.0` as its subprocess. It forwards only image generation/editing and exact task lookup, plus a local schema-derived image-model guide. GPT Image IDs are the only allowed generation models. It never changes price tiers or silently switches models, and passes upstream results/errors/task IDs through unchanged.

For local review, install this repository with `pip install .`, then use `install-stdio.json` with `gpt-image-lobehub`. This adapter is STDIO/desktop only; it has no deployed public HTTP endpoint.

## 1. Install the service

![Official LobeHub MCP marketplace screenshot; historical documentation reference](https://lobehub.com/img/hub/blog/assetsb811f2aae8e8346aef16793d6bd10f88.webp)

This is an unchanged [official documentation image](https://github.com/lobehub/lobehub/blob/43578a9bcc37dbf0ec9beb5f5ab1dcd5ba09daf7/docs/usage/community/mcp-market.mdx), present in the 2026-03-03 documentation commit; its capture date/version is unknown. It illustrates the real search field and service cards, not an Ace install or current card ranking. Reference checked 2026-10-18.

Use [official GPT Image search](https://lobehub.com/mcp?q=GPT%20Image) to check publication. This new focused card is not live yet; do not mistake the broad OpenAIMCP result for it. Search terms are `GPT Image`, `GPTImage`, and `Ace Data Cloud`; exact ranking is not promised. If there are multiple historical cards, use the identifier above rather than creating another one.

The final marketplace entry will run `gpt-image-lobehub` on LobeHub Desktop. Until publication, a developer can install this repo and add **one** STDIO connector using [install-stdio.json](install-stdio.json). Set `ACEDATACLOUD_API_TOKEN` in that connector's environment, not a URL or chat message. Stable quick import reads only the first entry; each service has its own connector. No local command is run in the browser edition.

## 2. Register/sign in and obtain your API Token

1. Sign in or register at [Ace → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt-image_lobehub_readme_api_key).
2. Initialize **General application** if absent, then open it. Check **GPT Image** service entitlement, current balance and pricing. A service-specific key can be restricted to that service.
3. Copy the existing service API Token, or open **Manage Keys** and create a dedicated LobeHub key. Do not use a platform management token or a model vendor's key.

![Copy an API Token in Ace Applications; real historical screenshot, referenced 2026-10-18](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a dedicated key; credentials hidden; historical screenshot](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These images are real Ace Applications screenshots from the linked source commit, not evidence that this LobeHub card installed or ran. Their original capture date is not asserted.

## 3. Paste the Token in LobeHub

For this STDIO adapter, enter the raw token in the connector environment variable `ACEDATACLOUD_API_TOKEN`, without `Bearer `, quotes or masked characters. HTTP Bearer examples for the broad upstream server do not apply to this local adapter. Save/test the connection, then enable it in **Agent Settings → Connectors**. Keep write/generation tools on Ask or Deny until you intend to use them. Never paste tokens into chat or screenshots.

[Official LobeHub MCP setup and permission guide](https://lobehub.com/docs/usage/community/mcp-market) documents the real entry points. A screenshot of the actual GPT Image connector/authorization flow is queued for coordinated capture; this source does not fabricate a screenshot of a successful installation.

## 4. First use and task completion

Call `openai_list_image_models` with no arguments. It returns the pinned upstream schema's GPT Image IDs and makes no generation request. Starting a chat to ask an Agent to run it may still charge the chat model; use a direct tool-test surface if available.

Both generation and editing require an explicit GPT Image model; the broader dependency's DALL-E edit default is deliberately not inherited. For generation, explicitly select a model supported by the installed schema, confirm current pricing and permissions, and submit once. Save the returned task ID and query `openai_get_task` with that **same ID** until the response explicitly reports terminal success or failure. Pending/preview media is not final success. Open the final result URL only after terminal success; keep task and usage records to verify one charge. No paid generation was run to author this directory.

## Troubleshooting

- **401/403:** recopy a service token and check entitlement, expiry and balance. `ACEDATACLOUD_API_TOKEN` is the STDIO variable; old `ACEDATA_API_TOKEN` examples are obsolete.
- **Imported but unauthorized:** set the STDIO connector environment variable `ACEDATACLOUD_API_TOKEN` and restart its process.
- **Connected but no tools in chat:** enable this connector for the current Agent, check Allow/Ask/Deny and the chat model's tool support.
- **Pending:** query the existing task; do not submit a second generation just because it takes time.
- **429/500:** preserve the returned error meaning; do not silently switch model or price tier.

## GPT Image package identity

Use **`mcp-openai-pro`**, maintained by AceDataCloud. The similarly named `mcp-openai` on PyPI belongs to another author. This is a separate focused adapter; its underlying server includes other OpenAI-compatible tools, but this adapter does not expose them. The new display name/keywords emphasize its GPT Image workflow while keeping one source of API behavior and avoiding vendor-official claims.

## Publisher

Existing human publisher login/GitHub ownership verification is required. Confirm this separate focused repository is not listed, then publish its exact owner declaration. No identity registration, new terms, or marketplace publication was performed.
