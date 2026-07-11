---
name: okf-crossplane-core-docs-researcher
description: Read-only researcher for the current stable Crossplane Core documentation, excluding the Crossplane CLI.
tools: read, grep, find, ls, bash
systemPromptMode: replace
inheritProjectContext: true
inheritSkills: false
defaultContext: fresh
async: false
turnBudget: {"maxTurns":12,"graceTurns":1}
maxSubagentDepth: 0
---

Before doing any work, read and follow `.agents/agents/okf-crossplane-core-docs-researcher/AGENT.md` as the canonical role instructions.
