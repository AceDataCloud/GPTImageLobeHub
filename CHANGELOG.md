# 0.1.1

Require python-dotenv>=1.2.4,<2 so the dotenv-disable flag is guaranteed by the supported dependency range. A real dependency test confirms project .env contents cannot set an alternate endpoint. Version 0.1.0 is superseded; existing release artifacts remain immutable.

# 0.1.0

Initial LobeHub desktop distribution of the shared GPT Image profile from mcp-openai-pro 2026.10.18.4. Five tools provide image creation/editing, same-ID task retrieval/listing and free model information. Model selection is explicit. Shared safe HTTP status/code/request ID handling is preserved. The launcher disables dotenv and passes only explicit connector credentials. No public HTTP endpoint or paid generation is included in release validation.
