import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "katex/dist/katex.min.css";
import "./styles.css";

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
// This is a private live graph.  Do not let an offline app shell hide a fresh
// Neo4j-backed deployment or a study-progress update behind stale assets.
if ("serviceWorker" in navigator) navigator.serviceWorker.getRegistrations().then(registrations => {
  registrations.forEach(registration => registration.unregister());
});
