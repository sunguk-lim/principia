import type { StatusMap, StudyStatus, StoreMode } from "./types";

const KEY = "principia.study-status.v1";
let mode: StoreMode = "device";

function localRead(): StatusMap {
  try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch { return {}; }
}

function localWrite(statuses: StatusMap): void {
  localStorage.setItem(KEY, JSON.stringify(statuses));
}

export async function loadStatuses(): Promise<{ statuses: StatusMap; mode: StoreMode }> {
  try {
    const response = await fetch("/api/status", { headers: { accept: "application/json" } });
    if (response.ok && response.headers.get("content-type")?.includes("application/json")) {
      mode = "server";
      return { statuses: await response.json(), mode };
    }
  } catch { /* GitHub Pages intentionally falls back to device storage. */ }
  mode = "device";
  return { statuses: localRead(), mode };
}

export async function saveStatus(slug: string, value: StudyStatus, all: StatusMap): Promise<StudyStatus> {
  if (mode === "server") {
    const response = await fetch(`/api/status/${slug}`, {
      method: "PUT", headers: { "content-type": "application/json" }, body: JSON.stringify(value),
    });
    if (!response.ok) throw new Error((await response.json()).detail || "Could not save status");
    return response.json();
  }
  const saved = { ...value, updated_at: new Date().toISOString() };
  localWrite({ ...all, [slug]: saved });
  return saved;
}
