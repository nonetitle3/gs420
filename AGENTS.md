# GS420 AI Agents

Flow: User -> Planner -> selected agent -> permitted tools -> result/verification -> memory when appropriate.

Agents are controlled components, not unrestricted autonomous processes. Agent names and tools are allow-listed. Model output must not automatically execute arbitrary shell commands. Untrusted code requires container/VM isolation in production.
