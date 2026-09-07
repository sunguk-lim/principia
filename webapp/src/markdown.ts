import katex from "katex";
import { Marked } from "marked";
import type { Tokens } from "marked";

interface MathToken extends Tokens.Generic {
  type: "math" | "inlineMath";
  raw: string;
  text: string;
}

function renderMath(token: MathToken, displayMode: boolean): string {
  return katex.renderToString(token.text, {
    displayMode,
    output: "htmlAndMathml",
    strict: false,
    throwOnError: false,
  });
}

const parser = new Marked({
  gfm: true,
  extensions: [
    {
      name: "math",
      level: "block",
      start(src) {
        return src.indexOf("$$");
      },
      tokenizer(src) {
        const match = /^\$\$[ \t]*\n?([\s\S]+?)\n?[ \t]*\$\$(?:\n|$)/.exec(src);
        if (!match) return;
        return { type: "math", raw: match[0], text: match[1].trim() } satisfies MathToken;
      },
      renderer(token) {
        return renderMath(token as MathToken, true);
      },
    },
    {
      name: "inlineMath",
      level: "inline",
      start(src) {
        return src.indexOf("$");
      },
      tokenizer(src) {
        const match = /^\$(?!\$)([^\n$]+?)\$(?!\$)/.exec(src);
        if (!match) return;
        return { type: "inlineMath", raw: match[0], text: match[1].trim() } satisfies MathToken;
      },
      renderer(token) {
        return renderMath(token as MathToken, false);
      },
    },
  ],
});

export function renderMarkdown(body: string): string {
  const linked = body
    .replace(/\[\[([a-z0-9][a-z0-9-]*)(?:\|([^\]]+))?\]\]/g, (_match, id, label) => `[${label || id.replaceAll("-", " ")}](#node=${id})`)
    .replace(/\]\(([a-z0-9][a-z0-9-]*\.svg)\)/g, "](./node-assets/$1)");
  return parser.parse(linked) as string;
}
