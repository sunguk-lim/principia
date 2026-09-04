export type StudyState = "not_started" | "in_progress" | "blocked" | "done" | "custom";

export interface StudyStatus {
  status: StudyState;
  custom_label: string;
  note: string;
  updated_at: string;
}

export interface GraphNode {
  id: string;
  title: string;
  summary: string;
  type: "concept" | "paper" | "axiom";
  status: "stub" | "explained";
  tag: string;
  tags: string[];
  root: string;
  deps: number;
  dependents: number;
  level: number;
  prereqs: string[];
  body: string;
  hasFigure: boolean;
}

export interface GraphEdge { s: string; t: string }
export interface GraphData { schemaVersion: number; nodes: GraphNode[]; edges: GraphEdge[] }
export type StatusMap = Record<string, StudyStatus>;
export type StoreMode = "server" | "device";

export const emptyStatus = (): StudyStatus => ({
  status: "not_started", custom_label: "", note: "", updated_at: "",
});

export const statusLabel = (value?: StudyStatus): string => {
  if (!value) return "Not started";
  if (value.status === "custom") return value.custom_label || "Custom";
  return ({ not_started: "Not started", in_progress: "In progress", blocked: "Blocked", done: "Done" })[value.status];
};
