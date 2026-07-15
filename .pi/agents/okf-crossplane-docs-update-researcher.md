---
name: okf-crossplane-docs-update-researcher
description: Read-only researcher for newly documented capabilities in a stable Crossplane documentation series.
tools: read, grep, find, ls, bash
systemPromptMode: replace
inheritProjectContext: true
inheritSkills: false
defaultContext: fresh
async: false
turnBudget: {"maxTurns":14,"graceTurns":1}
maxSubagentDepth: 0
---

Before doing any work, read and follow `.agents/agents/okf-crossplane-docs-update-researcher/AGENT.md` as the canonical role instructions.
