import assert from "node:assert/strict";
import test from "node:test";
import { renderMarkdown } from "./markdown";

test("renders inline math without exposing dollar delimiters", () => {
  const html = renderMarkdown("The value $e^{x}$ is positive.");

  assert.match(html, /class="katex"/);
  assert.doesNotMatch(html, /\$e\^\{x\}\$/);
  assert.match(html, /The value <span class="katex">/);
});

test("renders the exponential-function display equation", () => {
  const source = String.raw`Built on [[arithmetic]]:

$$e^{x} = \sum_{k=0}^{\infty} \frac{x^{k}}{k!}, \qquad e^{x} > 0 \ \text{ for all } x,
\qquad e^{x+y} = e^{x}\,e^{y}$$`;
  const html = renderMarkdown(source);

  assert.match(html, /class="katex-display"/);
  assert.match(html, /href="#node=arithmetic"/);
  assert.doesNotMatch(html, /\$\$/);
  assert.match(html, /∑/);
});

test("leaves unmatched math delimiters as source text", () => {
  const html = renderMarkdown("This is not closed: $e^x");

  assert.match(html, /\$e\^x/);
  assert.doesNotMatch(html, /class="katex"/);
});
