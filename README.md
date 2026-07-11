# okf-crossplane-v2

LLM-wiki in [Open Knowledge Format](https://okf.md/spec/) for the Crossplane v2 ecosystem.

## Codex workflow

The repository contains an opt-in Codex workflow for creating and maintaining the catalog from Crossplane source code, schemas, tests, examples, package metadata, and documentation.

Invoke it explicitly:

```text
$okf build knowledge for function-go-templating and function-kro
```

The `$okf` skill never activates implicitly. Its root agent is the only writer; token-efficient read-only subagents collect evidence for Crossplane and Upjet sources before the catalog is changed.

See:

- [`AGENTS.md`](AGENTS.md) for repository-wide rules
- [`.agents/skills/okf/SKILL.md`](.agents/skills/okf/SKILL.md) for the workflow
- [`.agents/skills/okf/references/sources.yaml`](.agents/skills/okf/references/sources.yaml) for the source inventory
- [`.codex/agents/`](.codex/agents/) for specialist agents
