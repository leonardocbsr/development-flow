// Executive review data. Edit only this file; index.html renders it.
//
// Status vocabulary (drives the stamp color and the evidence dots — the only
// color on the page):
//   "confirmed"  — directly supported by fresh evidence      (● full dot)
//   "inferred"   — concluded from indirect evidence          (◐ half dot)
//   "hypothesis" — plausible but untested                    (○ outline dot)
//   "unknown"    — evidence unavailable or contradictory     (◌ dotted)
//
// List entries may be plain strings or { text, status, href }.
// Evidence entries: { claim, proof, proves, status, href } — "proves" states the
// exact scope the proof covers, no more.
// nextSteps is ordered; the first entry is rendered as the immediate action.
window.EXECUTIVE_REVIEW = {
  title: "__TITLE__",
  date: "__DATE__",
  status: "unknown",       // short owner-facing gate label, e.g. "Not ready", "Shipped", "Blocked"
  statusLevel: "unknown",  // one of: confirmed | inferred | hypothesis | unknown
  lane: "Unknown",         // Unknown | Research Spike | PoC | MVP | Production
  snapshot: {
    repository: "Unknown",
    branch: "Unknown",
    base: "Unknown",
    head: "Unknown",
    workingTree: "Unknown"
  },
  summary: "Replace this with the owner-facing truth and current gate.",
  delivered: [],
  inProgress: [],
  evidence: [],
  decisions: [],
  blockers: [],
  risks: [],
  nextSteps: [],
  sourceNote: "List the exact live evidence used for this snapshot."
};
