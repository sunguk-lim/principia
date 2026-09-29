import { learningRoadmap } from "./graph-utils";
import type { GraphNode, StatusMap } from "./types";

export interface EntityContent { entityId: string; signature: string; explanation: string; wordCount: number; ordinal: number; segmentCount: number; reviewed: boolean }
export interface RoadmapData { target: string; requiredIds: string[]; requiredEdges: { source: string; target: string; reason: string }[] }

export function orderedRoadmap(result: RoadmapData, byId: Map<string, GraphNode>): GraphNode[] {
  const prerequisites = new Map(result.requiredIds.map(id => [id, [] as string[]]));
  for (const edge of result.requiredEdges) prerequisites.get(edge.source)?.push(edge.target);
  const ordered: GraphNode[] = [], seen = new Set<string>(), active = new Set<string>();
  const visit = (id: string) => {
    if (seen.has(id) || active.has(id)) return;
    active.add(id); (prerequisites.get(id) || []).forEach(visit); active.delete(id); seen.add(id);
    const entity = byId.get(id); if (entity) ordered.push(entity);
  };
  visit(result.target); return ordered;
}

export async function loadEntityContent(node: GraphNode, fetchContent: typeof fetch = fetch): Promise<EntityContent> {
  try {
    const response = await fetchContent(`/api/neo4j/entities/${encodeURIComponent(node.id)}`);
    if (!response.ok) throw new Error("Explanation unavailable");
    return await response.json() as EntityContent;
  } catch {
    const explanation = node.lesson || node.body;
    return {
      entityId: node.id,
      signature: node.id,
      explanation,
      wordCount: explanation.trim() ? explanation.trim().split(/\s+/).length : 0,
      ordinal: 1,
      segmentCount: 1,
      reviewed: Boolean(node.lessonReviewed),
    };
  }
}

export async function loadNodeRoadmap(node: GraphNode, byId: Map<string, GraphNode>, statuses: StatusMap, fetchRoadmap: typeof fetch = fetch): Promise<GraphNode[]> {
  try {
    const response = await fetchRoadmap(`/api/neo4j/roadmap/${encodeURIComponent(node.id)}`);
    if (!response.ok) throw new Error("Roadmap unavailable");
    return orderedRoadmap(await response.json() as RoadmapData, byId);
  } catch {
    return learningRoadmap(node.id, byId, statuses);
  }
}
