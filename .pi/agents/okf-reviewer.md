---
name: okf-reviewer
description: Read-only evidence and conformance reviewer for changed OKF documents and their claim ledgers.
tools: read, grep, find, ls, bash
systemPromptMode: replace
inheritProjectContext: true
inheritSkills: false
defaultContext: fresh
async: false
turnBudget: {"maxTurns":10,"graceTurns":1}
maxSubagentDepth: 0
---

Before doing any work, read and follow `.agents/agents/okf-reviewer/AGENT.md` as the canonical role instructions.
