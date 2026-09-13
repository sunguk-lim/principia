import type { GraphNode, StatusMap } from "./types";

export function learningRoadmap(target: string, byId: Map<string, GraphNode>, statuses: StatusMap = {}): GraphNode[] {
  const seen = new Set<string>();
  const active = new Set<string>();
  const ordered: GraphNode[] = [];
  const visit = (id: string) => {
    if (active.has(id)) throw new Error(`Prerequisite cycle at ${id}`);
    if (seen.has(id)) return;
    const node = byId.get(id);
    if (!node) throw new Error(`Missing prerequisite ${id}`);
    // A learned concept supplies its prerequisites for this goal; do not force
    // the learner to repeat the entire ancestry underneath it.
    if (statuses[id]?.status === "done") { seen.add(id); return; }
    active.add(id);
    node.prereqs.forEach(visit);
    active.delete(id);
    seen.add(id);
    ordered.push(node);
  };
  visit(target);
  return ordered;
}

export function nextStudyNode(roadmap: GraphNode[], statuses: StatusMap): GraphNode | undefined {
  return roadmap.find(node => statuses[node.id]?.status !== "done");
}

export function statusColor(status?: string): string {
  return ({ not_started: "#667085", in_progress: "#f5b942", blocked: "#ff647c", done: "#38d39f", custom: "#a58bff" } as Record<string,string>)[status || "not_started"];
}
