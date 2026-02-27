# Methodology — Research Foundation

This file contains the research claims that back every configuration decision in Ars Contexta.

## Overview

249 interconnected research claims derived from Tools for Thought literature, cognitive science, network theory, and agent architecture research.

## Claim Categories

### Cognitive Architecture

| Claim ID | Claim | Source |
|----------|-------|--------|
| COG-001 | Extended mind: external artifacts become part of cognitive process | Clark & Chalmers 1998 |
| COG-002 | Spreading activation: linked concepts prime each other | Collins & Loftus 1975 |
| COG-003 | Generation effect: self-generated content is better remembered | Slamecka & Graf 1978 |
| COG-004 | Context-switching cost: 15-25 min productivity loss per switch | Leroy 2009 |
| COG-005 | Working memory limit: 4±1 chunks (updated from Miller's 7±2) | Cowan 2001 |
| COG-006 | Forgetting curve: exponential decay without reinforcement | Ebbinghaus 1885 |
| COG-007 | Spaced repetition: optimal intervals improve retention | Ebbinghaus, modern SR systems |
| COG-008 | Retrieval practice: recalling strengthens memory more than re-reading | Karpicke & Roediger 2008 |

### Network Theory

| Claim ID | Claim | Source |
|----------|-------|--------|
| NET-001 | Small-world topology: high clustering + short path lengths | Watts & Strogatz 1998 |
| NET-002 | Betweenness centrality: nodes connecting clusters have high value | Freeman 1977 |
| NET-003 | Preferential attachment: new nodes connect to already-connected nodes | Barabási & Albert 1999 |
| NET-004 | Scale-free networks: follow power-law degree distribution | Barabási & Albert 1999 |
| NET-005 | Network resilience: robust to random failure, vulnerable to hub removal | Albert, Jeong, Barabási 2000 |

### Zettelkasten Principles

| Claim ID | Claim | Source |
|----------|-------|--------|
| ZET-001 | Atomic notes: one idea per note enables recombination | Luhmann |
| ZET-002 | Connection over categorization: links create emergent structure | Luhmann |
| ZET-003 | Numbering system: enables arbitrary insertion while maintaining order | Luhmann |
| ZET-004 | Entry points: hub notes provide multiple access paths | Luhmann |
| ZET-005 | Organic growth: structure emerges from use, not pre-planning | Luhmann |
| ZET-006 | Surprise through connection: unexpected links generate insight | Luhmann |

### Cornell Note-Taking (5 Rs)

| Claim ID | Claim | Source |
|----------|-------|--------|
| COR-001 | Record: capture main ideas during experience | Cornell System |
| COR-002 | Reduce: summarize and distill after experience | Cornell System |
| COR-003 | Recite: recall from memory (we add: machine-assisted) | Cornell System |
| COR-004 | Reflect: connect to prior knowledge and experience | Cornell System |
| COR-005 | Review: spaced repetition for long-term retention | Cornell System |

### Evergreen Notes

| Claim ID | Claim | Source |
|----------|-------|--------|
| EVE-001 | Evergreen notes: written for future self, not present moment | Andy Matuschak |
| EVE-002 | Concept-oriented: titles as questions or assertions | Andy Matuschak |
| EVE-003 | Dense linking: every note should connect to several others | Andy Matuschak |
| EVE-004 | Iterative refinement: notes evolve over time | Andy Matuschak |
| EVE-005 | Context-specific: notes written for specific context | Andy Matuschak |

### PARA Method

| Claim ID | Claim | Source |
|----------|-------|--------|
| PAR-001 | Projects: active efforts with clear goal and deadline | Tiago Forte |
| PAR-002 | Areas: ongoing responsibilities without deadlines | Tiago Forte |
| PAR-003 | Resources: topics of ongoing interest | Tiago Forte |
| PAR-004 | Archives: inactive items from other categories | Tiago Forte |
| PAR-005 | Action-orientation: organize by when you need it, not what it is | Tiago Forte |

### Agent Architecture

| Claim ID | Claim | Source |
|----------|-------|--------|
| AGT-001 | Context window limits: degrade with filling (position matters) | LLM research |
| AGT-002 | Session boundaries: each session starts fresh, need persistence | Agent design |
| AGT-003 | Subagent patterns: fresh context per subagent maintains quality | Agent design |
| AGT-004 | Hook automation: enforce quality without manual intervention | Agent design |
| AGT-005 | Tool-augmented memory: external storage exceeds context limits | Agent design |

### Maps of Content (MOCs)

| Claim ID | Claim | Source |
|----------|-------|--------|
| MOC-001 | Hub structure: MOCs serve as navigational hubs | Zettelkasten practice |
| MOC-002 | Multiple access: same content reachable from multiple MOCs | Network theory |
| MOC-003 | Hierarchical + lateral: MOCs provide both hierarchy and cross-links | Practice |
| MOC-004 | Dynamic: MOCs evolve as knowledge grows | Practice |
| MOC-005 | Annotation: MOCs should include brief context for each link | Practice |

## How Claims Back Decisions

Each kernel primitive includes `cognitive_grounding` linking to specific research:

### Example: MOC Hierarchy

**Decision**: Use hierarchical MOCs (hub → domain → topic)  
**Grounding**: COG-004 (context-switching cost) + NET-002 (betweenness centrality)  
**Reasoning**: Hub MOCs reduce search time by providing high-level navigation, minimizing context-switching. Topic MOCs connect clusters, benefiting from betweenness centrality.

### Example: Atomic Notes

**Decision**: One idea per note with explicit links  
**Grounding**: ZET-001 (atomic notes) + EVE-003 (dense linking) + COG-002 (spreading activation)  
**Reasoning**: Atomic notes enable recombination. Dense links create spreading activation paths. Together, they form a generative system.

### Example: Fresh Context Per Phase

**Decision**: Spawn subagent per pipeline phase  
**Grounding**: AGT-001 (context window limits) + AGT-003 (subagent patterns)  
**Reasoning**: LLM attention degrades as context fills. Fresh subagent per phase keeps each phase in the "smart zone."

## Querying Claims

Ask questions like:
- "Why does my system use atomic notes?" → ZET-001, EVE-003, COG-002
- "Why MOC hierarchy?" → MOC-001 through MOC-005, COG-004
- "Why fresh context per phase?" → AGT-001, AGT-003

The skill will load relevant claims and explain the reasoning.

---

*Note: This is a condensed version. The full research graph contains 249 interconnected claims with detailed citations and cross-references.*