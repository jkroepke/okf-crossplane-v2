---
name: okf-crossplane-researcher
description: Read-only researcher for Crossplane CLI, runtime, SDKs, tools, native providers, testing tools, and domains without a dedicated researcher.
tools: read, grep, find, ls, bash
systemPromptMode: replace
inheritProjectContext: true
inheritSkills: false
defaultContext: fresh
async: false
turnBudget: {"maxTurns":12,"graceTurns":1}
maxSubagentDepth: 0
---

Before doing any work, read and follow `.agents/agents/okf-crossplane-researcher/AGENT.md` as the canonical role instructions.
