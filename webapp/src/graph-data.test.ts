import assert from "node:assert/strict";
import test from "node:test";
import { loadGraph } from "./graph-data";
import type { GraphData } from "./types";

const graph: GraphData = { schemaVersion: 1, nodes: [], edges: [] };
const jsonResponse = (body: unknown, status = 200): Response => Response.json(body, { status });

test("loads the live Neo4j graph when the API is available", async () => {
  const requests: string[] = [];
  const fetchGraph = async (input: RequestInfo | URL): Promise<Response> => {
    requests.push(String(input));
    return jsonResponse(graph);
  };

  assert.deepEqual(await loadGraph(fetchGraph), graph);
  assert.deepEqual(requests, ["/api/neo4j/graph"]);
});

test("falls back to the bundled graph when the live API fails", async () => {
  const requests: string[] = [];
  const fetchGraph = async (input: RequestInfo | URL): Promise<Response> => {
    const url = String(input);
    requests.push(url);
    return url === "/api/neo4j/graph" ? jsonResponse({}, 503) : jsonResponse(graph);
  };

  assert.deepEqual(await loadGraph(fetchGraph), graph);
  assert.deepEqual(requests, ["/api/neo4j/graph", "./data/graph.json"]);
});

test("falls back when the live API response is not valid JSON", async () => {
  const requests: string[] = [];
  const fetchGraph = async (input: RequestInfo | URL): Promise<Response> => {
    const url = String(input);
    requests.push(url);
    return url === "/api/neo4j/graph"
      ? new Response("not JSON", { status: 200 })
      : jsonResponse(graph);
  };

  assert.deepEqual(await loadGraph(fetchGraph), graph);
  assert.deepEqual(requests, ["/api/neo4j/graph", "./data/graph.json"]);
});
