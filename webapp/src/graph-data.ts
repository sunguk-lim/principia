import type { GraphData } from "./types";

const LIVE_GRAPH_URL = "/api/neo4j/graph";
const STATIC_GRAPH_URL = "./data/graph.json";

export async function loadGraph(fetchGraph: typeof fetch = fetch): Promise<GraphData> {
  try {
    const response = await fetchGraph(LIVE_GRAPH_URL);
    if (!response.ok) throw new Error("Neo4j graph unavailable");
    return await response.json() as GraphData;
  } catch {
    const response = await fetchGraph(STATIC_GRAPH_URL);
    if (!response.ok) throw new Error("Bundled graph unavailable");
    return await response.json() as GraphData;
  }
}
