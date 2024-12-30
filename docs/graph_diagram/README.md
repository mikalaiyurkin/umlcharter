# State & Activity (Flowcharts) Diagrams

### Supported DSLs

|                  | Mermaid          |
|------------------|------------------|
| Any limitations? | ✅ No limitations |

For more details about the supported DSLs, please refer to the next links:

- [Mermaid](https://mermaid.js.org/)

[//]: # (- [PlantUML]&#40;https://plantuml.com/&#41;)

[//]: # (- [D2]&#40;https://d2lang.com/tour/intro&#41;)

[//]: # (- [Graphviz]&#40;https://www.graphviz.org/documentation/&#41;)

### Quick Start

Both State and Activity diagrams (aka Flowcharts) are used to represent some complex process that has a direction
and certain granular "units" within the context of this process.

If we are talking about the State diagrams, such units are the "states" of some system and the diagram represents the 
process of transitions across these states.

If we are talking about the Activity diagrams, such units are the "steps" of some process.

But in both cases the representation can be reduced to the directed graph, so the same graphical elements can be re-used
for the visual representation.

*NB!* because of the different meaning put into the State and Activity diagrams, the simple directed graph itself 
might not be good enough to properly describe the complex and feature-rich 
system. So, in order to keep things simple, only the common visual elements suitable for both State and Activity diagrams
will be implemented. 
Thereby the visual elements like [activity partitions](https://www.uml-diagrams.org/activity-diagrams.html#partition) 
for Activity diagrams or the 
[history pseudostates](https://www.uml-diagrams.org/state-machine-diagrams.html#pseudostate) for State diagrams, and other specific elements will 
not be considered for the implementation. 