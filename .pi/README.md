# Pi model configuration

The project agents in `.pi/agents/` do not pin a provider, model, or thinking level. They inherit the model selected for the Pi session or the model configured through `pi-subagents`.

Keeping model selection outside the repository allows the same OKF workflow to run with hosted reasoning models and local non-thinking models.

## Qwen3-Coder-Next

[Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) is a recommended local model for this repository's source-analysis workflow.

The published model card describes it as an Apache-2.0 open-weight coding-agent model with:

- 80 billion total parameters and 3 billion activated parameters
- a native context length of 262,144 tokens
- tool-calling and agentic coding support
- non-thinking mode only

The project agent definitions therefore do not set `thinking`. Provider-specific reasoning controls belong in the user's Pi model configuration instead.

## Local OpenAI-compatible endpoint

Pi loads custom providers from `~/.pi/agent/models.json`. The following example targets a local OpenAI-compatible endpoint, such as vLLM or SGLang:

```json
{
  "providers": {
    "local-qwen": {
      "baseUrl": "http://localhost:8000/v1",
      "api": "openai-completions",
      "apiKey": "local",
      "compat": {
        "supportsReasoningEffort": false
      },
      "models": [
        {
          "id": "Qwen/Qwen3-Coder-Next",
          "name": "Qwen3-Coder-Next (Local)",
          "reasoning": false,
          "contextWindow": 32768,
          "maxTokens": 16384,
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          }
        }
      ]
    }
  }
}
```

The example intentionally starts with a 32,768-token context window. The model supports a larger native context, but the model card recommends reducing the context length when the inference server runs out of memory.

If the local endpoint rejects the `developer` role, also add:

```json
"supportsDeveloperRole": false
```

under the provider's `compat` object.

See the [Pi custom model documentation](https://pi.dev/docs/latest/models) for all provider and compatibility options.

## Selecting the model for subagents

Select the model interactively with `/model`, or set a user-level default in `~/.pi/agent/settings.json`:

```json
{
  "subagents": {
    "defaultModel": "local-qwen/Qwen/Qwen3-Coder-Next"
  }
}
```

Use the exact provider and model identifier shown by Pi if the local configuration uses a different provider name or served model name.

For an individual run, `pi-subagents` also supports a per-run model override. This can be useful for running the final evidence review with a different model while keeping Qwen3-Coder-Next for source scouting and research.
