---
name: okf-source-scout
description: Fast, read-only inventory agent for classifying OKF sources and locating high-signal files.
tools: read, grep, find, ls, bash
thinking: low
systemPromptMode: replace
inheritProjectContext: true
inheritSkills: false
defaultContext: fresh
async: false
turnBudget: {"maxTurns":8,"graceTurns":1}
maxSubagentDepth: 0
---

Before doing any work, read and follow `.agents/agents/okf-source-scout/AGENT.md` as the canonical role instructions.
