import assert from "node:assert/strict";
import test from "node:test";
import { loadEntityContent, loadNodeRoadmap, type EntityContent, type RoadmapData } from "./node-panel-data";
import { emptyStatus, type GraphNode } from "./types";

const node = (id: string, prereqs: string[] = []): GraphNode => ({
  id, title: id, prereqs, summary: "", type: "concept", status: "explained",
  tag: "math", tags: [], root: "math", deps: prereqs.length, dependents: 0,
  level: 0, body: `Body for ${id}`, hasFigure: false,
});
const jsonResponse = (body: unknown, status = 200): Response => Response.json(body, { status });

test("uses Neo4j entity content when the API is available", async () => {
  const local = node("live");
  const remote: EntityContent = { entityId: "live", signature: "sig", explanation: "API explanation", wordCount: 2, ordinal: 1, segmentCount: 1, reviewed: true };
  const result = await loadEntityContent(local, async () => jsonResponse(remote));
  assert.deepEqual(result, remote);
});

test("falls back to the bundled lesson or body when entity loading fails", async () => {
  const withLesson = node("lesson");
  withLesson.lesson = "Bundled lesson text";
  withLesson.lessonReviewed = true;
  const unavailable = async (): Promise<Response> => jsonResponse({}, 503);

  const lesson = await loadEntityContent(withLesson, unavailable);
  const body = await loadEntityContent(node("body"), unavailable);
  assert.equal(lesson.explanation, "Bundled lesson text");
  assert.equal(lesson.reviewed, true);
  assert.equal(lesson.wordCount, 3);
  assert.equal(body.explanation, "Body for body");
});

test("uses the Neo4j roadmap ordering when the API is available", async () => {
  const goal = node("goal", ["base"]), base = node("base");
  const byId = new Map([[goal.id, goal], [base.id, base]]);
  const remote: RoadmapData = {
    target: "goal", requiredIds: ["goal", "base"],
    requiredEdges: [{ source: "goal", target: "base", reason: "foundation" }],
  };
  assert.deepEqual((await loadNodeRoadmap(goal, byId, {}, async () => jsonResponse(remote))).map(item => item.id), ["base", "goal"]);
});

test("computes the roadmap from bundled nodes and statuses when the API fails", async () => {
  const goal = node("goal", ["base"]), base = node("base", ["ancestor"]), ancestor = node("ancestor");
  const byId = new Map([goal, base, ancestor].map(item => [item.id, item]));
  const done = { ...emptyStatus(), status: "done" as const };
  const unavailable = async (): Promise<Response> => { throw new Error("offline"); };

  assert.deepEqual((await loadNodeRoadmap(goal, byId, { base: done }, unavailable)).map(item => item.id), ["goal"]);
});
