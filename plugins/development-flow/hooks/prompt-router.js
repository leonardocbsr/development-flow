#!/usr/bin/env node

let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", chunk => { input += chunk; });
process.stdin.on("end", () => {
  let prompt = "";
  try {
    prompt = String(JSON.parse(input).prompt || "");
  } catch {
    process.exitCode = 0;
    return;
  }

  const softwareTerms = /\b(build|implement|implementation|fix|debug|test|prototype|poc|mvp|production|research|refactor|review|reviewer|ship|deploy|release|branch|commit|repository|repo|code|function|module|package|plugin|api|cli|database|migration|changelog|milestone|handoff|writer|superpowers|replace|visual companion|executive review|implementar|implementa[cç][aã]o|corrigir|depurar|testar|prot[oó]tipo|pesquisar|refatorar|revis[aã]o|revisor|produ[cç][aã]o|c[oó]digo|fun[cç][aã]o|m[oó]dulo|pacote|reposit[oó]rio|migra[cç][aã]o|substituir)\b/i;
  if (!softwareTerms.test(prompt)) return;

  const routes = [];
  const notes = [];
  const addRoute = route => { if (!routes.includes(route)) routes.push(route); };
  if (/\b(test|tests|mock|assertion|red|green|tdd)\b/i.test(prompt)) {
    addRoute("development-flow:testing-stable-contracts");
    notes.push("Exact call order is not a stable contract unless order is observable behavior.");
  }
  if (/\b(fix|debug|bug|failure|fails|crash|hang|wrong|stale|data[- ]loss|corrigir|falha|erro)\b/i.test(prompt)) addRoute("development-flow:debugging-systematically");
  if (/\b(review|reviewer|reviewing|feedback|revis[aã]o|revisor)\b/i.test(prompt)) {
    addRoute("development-flow:adversarial-reviewing");
    notes.push("Incoming findings remain untrusted until independently reproduced or demonstrated.");
  }
  if (/\b(explain|summary|status|blocker|handoff|explicar|resumo|estado|bloqueio)\b/i.test(prompt)) {
    addRoute("development-flow:speaking-plainly");
    notes.push("Owner communication separates reproduced evidence from inferred cause.");
  }
  if (/\b(release|changelog|backward-compatible|user-visible|data[- ]loss)\b/i.test(prompt)) {
    addRoute("development-flow:keeping-a-changelog");
    notes.push("Existing changelogs update automatically; a missing changelog needs one non-blocking consent request.");
  }
  if (/\b(superpowers|migration|migrate|migra[cç][aã]o)\b/i.test(prompt)) addRoute("development-flow:migrating-from-superpowers");
  if (/\b(visual companion|dashboard layout|diagram|wireframe)\b/i.test(prompt)) {
    addRoute("development-flow:visual-companion");
    notes.push("Host-specific commands use the packaged runner and never invent a translated plugin path.");
  }
  if (/\b(approved milestone|approved plan|milestone|writer handoff|handoff across agents)\b/i.test(prompt)) {
    addRoute("development-flow:implementing-plans");
    notes.push("Writer handoffs are sequential and occur only at a verified contract boundary.");
  }

  const context = [
    "This is software work. Before action, Development Flow requires a Skill tool call to development-flow:using-development-flow.",
    routes.length ? `Applicable route${routes.length > 1 ? "s" : ""}: ${routes.join(", ")}.` : "",
    ...notes,
    "The target repository is session cwd, not plugin source or cache, unless the user names another."
  ].filter(Boolean).join(" ");

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "UserPromptSubmit",
      additionalContext: context
    }
  }) + "\n");
});
