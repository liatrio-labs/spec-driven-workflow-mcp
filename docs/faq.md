# Frequently Asked Questions

### What problem does the Spec‑Driven Workflow solve?
It eliminates inconsistent AI‑native delivery by packaging a repeatable specification workflow that keeps teams aligned on work breakdown, shared context artifacts, and the tooling handoffs needed to ship.

### Who should use it?
Any team trying to level up AI‑native delivery. You can adopt the workflow a piece at a time, layering in components without committing to the full stack on day one.

### How is it installed?
Teams install the workflow via package managers or MCP, then use its commands to maintain context, drive consistent work breakdown, and keep AI agents operating inside agreed guardrails.

### Do we need any prerequisites?
The workflow runs with minimal setup—many teams start with the prompts alone and layer in automation when they are ready.

### How does it work with different tools?
The workflow is designed to be usable with many different AI agents and work‑tracking systems—even multiple tools in the same repo or project. It exposes connectors for AI agents, ticketing systems, and documentation hubs so the same plan, specs, and progress data is available everywhere, or teams can skip connectors and keep everything in‑repo as Markdown.

### What makes it different from documentation templates?
Templates stay static; the workflow ships as a versioned package that you upgrade like any package, so improvements arrive without overwriting your customizations. The workflow also provides working commands and tools, not just documentation guidelines.

### What if we already have an established process?
You keep it. The workflow provides commands that wire into your existing project structure—your current ADR folders, ticket conventions, or roadmaps. You don’t need to rewrite your documentation or reorganize your repos. The workflow layers consistency on top of what is already working.

### How does it guide iteration size?
Commands and scaffolds steer teams toward skateboard‑to‑scooter increments: create small testable slices, validate learning, and only then scale. Prompts explicitly ask you to define the skateboard (minimal testable value), scooter (enhanced but still lean), and car (complete product) so teams discuss iteration sizes up front.

### Can it work entirely in Markdown in one repo?
Yes. You can keep everything in a single repository using Markdown files with no external dependencies. Tool integrations and multi‑repo features are optional.

### Can solo developers use it?
Yes. The same context and work‑breakdown helpers make it easy to pause and resume personal projects while keeping AI assistance on track.

### How does customization work?
Through layering. Local overrides and configuration live outside the distributed files, so teams version their adjustments separately and apply workflow updates without merge conflicts. The specific mechanism is still being refined.

### What’s the learning curve?
Minimal. If you can write Markdown, you can use the workflow. The templates and commands guide you through the process. Most teams are productive in their first session.

### Why adopt a spec‑driven workflow now?
Rapid experimentation with AI agents creates drift between squads. Spec‑Driven Workflow delivers a shared operating model with minimal setup, giving leaders confidence that every iteration follows the same proven playbook. The cost of adoption is low and benefits compound as your team scales.

### What does it cost?
The workflow is open source. Enterprise‑grade connectors and support bundles are available as add‑ons.
