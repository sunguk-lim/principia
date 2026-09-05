import { build } from "esbuild";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const out = resolve(root, "web/dist");
rmSync(resolve(out, "assets"), { recursive: true, force: true });
mkdirSync(resolve(out, "assets"), { recursive: true });

await build({
  entryPoints: [resolve(root, "webapp/src/main.tsx")],
  bundle: true,
  minify: true,
  sourcemap: true,
  format: "esm",
  target: ["es2022"],
  outdir: resolve(out, "assets"),
  entryNames: "app",
  assetNames: "[name]-[hash]",
  jsx: "automatic",
});

writeFileSync(resolve(out, "index.html"), `<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#080b12"><meta name="description" content="Explore and study the Principia knowledge graph.">
<link rel="manifest" href="./manifest.webmanifest"><link rel="stylesheet" href="./assets/app.css">
<title>Principia</title></head><body><div id="root"></div><script type="module" src="./assets/app.js"></script></body></html>\n`);
writeFileSync(resolve(out, "manifest.webmanifest"), JSON.stringify({
  name: "Principia Knowledge Graph", short_name: "Principia", start_url: "./", display: "standalone",
  background_color: "#080b12", theme_color: "#080b12", description: "A graph-native learning workspace"
}, null, 2));
const cacheVersion = createHash("sha256").update(readFileSync(resolve(out, "assets/app.js"))).update(readFileSync(resolve(out, "data/graph.json"))).digest("hex").slice(0, 12);
writeFileSync(resolve(out, "sw.js"), `const CACHE='principia-${cacheVersion}';self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['./','./index.html','./assets/app.js','./assets/app.css','./data/graph.json']))));self.addEventListener('fetch',e=>{if(e.request.method==='GET')e.respondWith(fetch(e.request).then(r=>{const x=r.clone();caches.open(CACHE).then(c=>c.put(e.request,x));return r}).catch(()=>caches.match(e.request)))})`);
