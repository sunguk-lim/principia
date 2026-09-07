import { build } from "esbuild";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const root = resolve(import.meta.dirname, "..");
const temporary = await mkdtemp(join(tmpdir(), "principia-web-test-"));
const output = join(temporary, "markdown.test.mjs");

try {
  await build({
    entryPoints: [resolve(root, "src/markdown.test.ts")],
    bundle: true,
    platform: "node",
    format: "esm",
    outfile: output,
  });
  const result = spawnSync(process.execPath, ["--test", output], { stdio: "inherit" });
  process.exitCode = result.status ?? 1;
} finally {
  await rm(temporary, { recursive: true, force: true });
}
