import type { GraphNode, StatusMap } from "./types";

export function learningRoadmap(target: string, byId: Map<string, GraphNode>): GraphNode[] {
  const seen = new Set<string>();
  const ordered: GraphNode[] = [];
  const visit = (id: string) => {
    if (seen.has(id)) return;
    seen.add(id);
    const node = byId.get(id);
    if (!node) return;
    node.prereqs.forEach(visit);
    ordered.push(node);
  };
  visit(target);
  return ordered;
}

export function nextStudyNode(roadmap: GraphNode[], statuses: StatusMap): GraphNode | undefined {
  return roadmap.find(node => node.type !== "axiom" && statuses[node.id]?.status !== "done");
}

export function statusColor(status?: string): string {
  return ({ not_started: "#667085", in_progress: "#f5b942", blocked: "#ff647c", done: "#38d39f", custom: "#a58bff" } as Record<string,string>)[status || "not_started"];
}
