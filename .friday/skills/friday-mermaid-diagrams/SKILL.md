---
name: friday-mermaid-diagrams
description: Reference for Mermaid JS diagram types and their code-block keywords. Use when a diagram is requested in a markdown file, or when asked to create a Mermaid diagram directly, to pick the right diagram type and syntax keyword.
---

# Mermaid Diagram Types

Source: https://mermaid.ai/open-source/intro/

When asked to add a diagram to a markdown file or create a Mermaid diagram, pick the type below that matches the content, then open a fenced code block with the keyword, e.g.:

````markdown
```mermaid
flowchart TD
  A --> B
```
````

| Diagram Type | Keyword | Use for |
|---|---|---|
| Flowchart | `flowchart` | Processes, decision flows |
| Sequence Diagram | `sequenceDiagram` | Interactions between entities over time |
| Gantt Diagram | `gantt` | Timelines, project scheduling |
| Class Diagram | `classDiagram` | Object-oriented structure and relationships |
| Git Graph | `gitgraph` | Version control branching and commits |
| Entity Relationship Diagram | `entityRelationshipDiagram` | Database schema and entity connections (experimental) |
| User Journey Diagram | `userJourney` | User experience flows and interactions |
| Quadrant Chart | `quadrantChart` | Four-quadrant matrix visualization |
| XY Chart | `xyChart` | Scatter and line plotting |
| Swimlanes Diagram | `swimlanes` | Cross-functional process flows |
| State Diagram | `stateDiagram` | State machines and transitions |
| Pie Chart | `pie` | Proportional data representation |
| Mindmaps | `mindmap` | Hierarchical brainstorming structures |
| Timeline | `timeline` | Sequential event visualization |
| Sankey | `sankey` | Flow and distribution diagrams |
| Block Diagram | `block` | Component and system architecture |
| Kanban | `kanban` | Task management boards |

## Guidance

- Prefer `flowchart` over the legacy `graph` keyword for new diagrams.
- Match the diagram type to the content's actual shape (e.g. don't force a sequence diagram onto a hierarchy — use `classDiagram` or `mindmap` instead).
- Keep node/label text concise; Mermaid renders poorly with long free-text labels.
- **For system/component architecture diagrams (multiple grouped systems with labeled edges crossing between groups), use `flowchart` with `subgraph` per group — not `block-beta`.** `block-beta`'s layout engine (at least via the `mermaid-filter`/pandoc/xelatex PDF pipeline used by `paper`) badly overlaps edge labels with node labels when edges cross between blocks; it's fine for simple same-row component boxes with no cross-block labeled edges, but breaks down otherwise. `flowchart` + `subgraph` handles cross-group labeled edges correctly.
- Give cross-subgraph labeled edges extra rank length so the label has room to render without colliding with node boxes: use `----` (2 ranks) or `-----` (3 ranks) instead of a single `-->`/`--`, e.g. `Toggle -- "unix socket, toggle/status" ----> Daemon`.
- Style node groups with `classDef`/`class` instead of per-node `style` lines — define one class per system/group and assign nodes to it:
  ```
  classDef macStyle fill:#ede9fe,stroke:#6d28d9,color:#3730a3;
  class Daemon,Mic,MLX,Parakeet macStyle;
  ```
- Set direction explicitly (`flowchart LR` or `TD`) rather than relying on the default — grouped system diagrams usually read better `LR`.
- If a complex flowchart still overlaps with the default (dagre) renderer, Mermaid supports `defaultRenderer: "elk"` via YAML frontmatter config — but confirm the render pipeline's mermaid-filter version bundles it before relying on it (untested in the `paper` pipeline as of this writing).
