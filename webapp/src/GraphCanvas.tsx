import cytoscape, { type Core } from "cytoscape";
import { useEffect, useRef } from "react";
import type { GraphData, StatusMap } from "./types";
import { statusColor } from "./graph-utils";

interface Props {
  data: GraphData;
  statuses: StatusMap;
  selectedId: string | null;
  visibleIds: Set<string>;
  onSelect: (id: string) => void;
}

export function GraphCanvas({ data, statuses, selectedId, visibleIds, onSelect }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const graph = useRef<Core | null>(null);
  const selectRef = useRef(onSelect);
  selectRef.current = onSelect;

  useEffect(() => {
    if (!host.current) return;
    const cy = cytoscape({
      container: host.current,
      elements: [
        ...data.nodes.map(node => ({ data: { id: node.id, label: node.title, root: node.root, type: node.type, level: node.level } })),
        ...data.edges.map((edge, index) => ({ data: { id: `e${index}`, source: edge.s, target: edge.t } })),
      ],
      minZoom: .08, maxZoom: 3.2, wheelSensitivity: .18,
      style: [
        { selector: "node", style: { "background-color": "#64748b", "border-width": 2, "border-color": "#0b1020", label: "data(label)", color: "#dce7f7", "font-size": 8, "text-outline-width": 2, "text-outline-color": "#0b1020", "text-valign": "bottom", "text-margin-y": 6, width: 16, height: 16 } },
        { selector: 'node[type="axiom"]', style: { shape: "diamond", width: 12, height: 12 } },
        { selector: "node:selected", style: { "border-width": 4, "border-color": "#ffffff", width: 24, height: 24, "font-size": 11, "z-index": 20 } },
        { selector: "edge", style: { width: .8, "line-color": "#344054", "target-arrow-color": "#344054", "target-arrow-shape": "triangle", "arrow-scale": .45, "curve-style": "bezier", opacity: .62 } },
        { selector: ".faded", style: { opacity: .06 } },
      ],
      layout: { name: "cose", animate: false, randomize: true, nodeRepulsion: () => 5600, idealEdgeLength: () => 48, edgeElasticity: () => 80, nestingFactor: 1.2, gravity: .3, numIter: 1000, initialTemp: 180, coolingFactor: .96, minTemp: 1 },
    });
    cy.on("tap", "node", event => selectRef.current(event.target.id()));
    graph.current = cy;
    return () => { cy.destroy(); graph.current = null; };
  }, [data]);

  useEffect(() => {
    const cy = graph.current; if (!cy) return;
    cy.nodes().forEach(node => {
      const visible = visibleIds.has(node.id());
      node.toggleClass("faded", !visible);
      node.style("background-color", statusColor(statuses[node.id()]?.status));
    });
  }, [visibleIds, statuses]);

  useEffect(() => {
    const cy = graph.current; if (!cy) return;
    cy.$(":selected").unselect();
    if (selectedId) {
      const node = cy.getElementById(selectedId); node.select(); cy.animate({ center: { eles: node }, duration: 280 });
    }
  }, [selectedId]);

  return <div className="graph-canvas" ref={host} aria-label="Interactive Principia knowledge graph" />;
}
