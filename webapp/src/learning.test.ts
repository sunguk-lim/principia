import assert from "node:assert/strict";
import test from "node:test";
import { lessonSteps } from "./lesson";
import { learningRoadmap } from "./graph-utils";
import { emptyStatus, type GraphNode } from "./types";

const node = (id: string, prereqs: string[] = []): GraphNode => ({
  id, title: id, prereqs, summary: "", type: "concept", status: "explained",
  tag: "math", tags: [], root: "math", deps: prereqs.length, dependents: 0,
  level: 0, body: "", hasFigure: false,
});
const graph = (...nodes: GraphNode[]) => new Map(nodes.map(n => [n.id, n]));

test("roadmap deduplicates shared foundations and excludes optional connections", () => {
  const goal = node("goal", ["left", "right"]);
  goal.relations = [{s: "goal", t: "optional", type: "CONTRASTS_WITH", reason: "comparison", reviewed: true}];
  const result = learningRoadmap("goal", graph(goal, node("left", ["base"]), node("right", ["base"]), node("base")));
  assert.deepEqual(result.map(n => n.id), ["base", "left", "right", "goal"]);
});
test("learned prerequisites prune their ancestry and completed goals need no steps", () => {
  const nodes = graph(node("goal", ["base"]), node("base", ["ancestor"]), node("ancestor"));
  const done = {...emptyStatus(), status: "done" as const};
  assert.deepEqual(learningRoadmap("goal", nodes, {base: done}).map(n => n.id), ["goal"]);
  assert.deepEqual(learningRoadmap("goal", nodes, {goal: done}), []);
});
test("resolved aliases do not create a second roadmap stop", () => {
  const canonical = node("canonical", ["base"]);
  const alias = node("alias");
  alias.canonicalId = "canonical";
  assert.deepEqual(learningRoadmap("alias", graph(alias, canonical, node("base"))).map(n => n.id), ["base", "canonical"]);
});
test("roadmaps expose cycles and missing dependencies", () => {
  assert.throws(() => learningRoadmap("a", graph(node("a", ["b"]), node("b", ["a"]))), /cycle/);
  assert.throws(() => learningRoadmap("a", graph(node("a", ["missing"]))), /Missing prerequisite/);
});
test("reading steps retain headings, code, lists and display math intact", () => {
  const code = '```python\nprint("hello")\nprint("world")\n```';
  const math = '$$\nx + y\n\n= z\n$$';
  const source = `## Example\n\nIntro words.\n\n${code}\n\n${math}\n\n- first item\n- second item\n`;
  const steps = lessonSteps(source, 3);
  assert.equal(steps[0].title, "Example");
  assert.ok(steps.some(s => s.body.includes(code)));
  assert.ok(steps.some(s => s.body.includes(math)));
  assert.ok(steps.some(s => s.body.includes('- first item\n- second item')));
});
test("literal math delimiters in code do not swallow later section boundaries", () => {
  const steps = lessonSteps('```sh\necho $$\n```\n\n## Next\n\nNext lesson.');
  assert.equal(steps.length, 2);
  assert.equal(steps[1].title, "Next");
});
test("empty and Korean lessons produce readable steps", () => {
  assert.equal(lessonSteps("").length, 1);
  const steps = lessonSteps("## 개념\n\n하나의 개념을 설명합니다.");
  assert.equal(steps[0].title, "개념");
  assert.match(steps[0].body, /하나의 개념/);
});
