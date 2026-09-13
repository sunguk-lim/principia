import { Lexer } from "marked";

export interface LessonStep { title: string; body: string; minutes: number }

/** Keep Markdown blocks intact: never cut equations, lists, tables, or code. */
export function lessonSteps(markdown: string, targetWords = 220): LessonStep[] {
  const tokens = Lexer.lex(markdown);
  const steps: LessonStep[] = [];
  let title = "The idea";
  let content = "";
  let words = 0;
  const flush = () => {
    if (content.trim()) steps.push({ title, body: content.trim(), minutes: Math.max(1, Math.ceil(words / 180)) });
    content = ""; words = 0;
  };
  // Marked treats display math as paragraphs; blank lines inside $$ blocks must
  // remain together too, so track their delimiter balance across tokens.
  let mathOpen = false;
  for (const token of tokens) {
    if (token.type === "heading" && token.depth <= 2 && !mathOpen) {
      flush(); title = token.text; continue;
    }
    const count = token.raw.trim().split(/\s+/).filter(Boolean).length;
    if (words && words + count > targetWords && !mathOpen) {
      flush(); title = `${title.replace(/ · continued$/, "")} · continued`;
    }
    content += token.raw;
    words += count;
    const delimiters = token.type === "code" ? 0 : token.raw.match(/\$\$/g)?.length || 0;
    if (delimiters % 2) mathOpen = !mathOpen;
  }
  flush();
  return steps.length ? steps : [{title: "The idea", body: markdown, minutes: 1}];
}
