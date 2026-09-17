const API_ROOT = "/api/workspace/v1";
const app = document.getElementById("workspace-app");
const statusRegion = document.getElementById("workspace-status");

const state = {
  catalogItems: [],
  nextCursor: null,
  catalogError: null,
  shell: null,
  shellError: null,
  routeProjectId: null,
  filter: "",
  loading: false,
  loadGeneration: 0,
  etags: { catalog: null, shell: null },
  refreshInFlight: false,
  refreshTrailing: false,
  refreshProjectIds: new Set(),
  eventSource: null,
  renderCount: 0,
};

function node(tag, attributes = {}, children = []) {
  const element = document.createElement(tag);
  for (const [key, value] of Object.entries(attributes)) {
    if (value === null || value === undefined) continue;
    if (key === "class") element.className = value;
    else if (key === "text") element.textContent = String(value);
    else if (key.startsWith("on")) element.addEventListener(key.slice(2), value);
    else element.setAttribute(key, String(value));
  }
  for (const child of children.flat()) {
    if (child !== null && child !== undefined) element.append(child);
  }
  return element;
}

function routeProjectId() {
  const match = /^\/p\/([^/]+)\/workspace\/?$/.exec(location.pathname);
  if (!match) return null;
  try { return decodeURIComponent(match[1]); } catch { return null; }
}

function selectedStage(shell = state.shell) {
  const requested = new URLSearchParams(location.search).get("stage");
  if (!requested || !shell) return { requested, selected: null };
  const stages = Array.isArray(shell.data?.stages) ? shell.data.stages : [];
  return { requested, selected: stages.some((stage) => stage.name === requested) ? requested : null };
}

async function getJson(url, cacheKey) {
  const headers = { Accept: "application/json" };
  if (state.etags[cacheKey]) headers["If-None-Match"] = state.etags[cacheKey];
  const response = await fetch(url, { headers });
  if (response.status === 304) return { notModified: true, projection: null };
  if (!response.ok) throw new Error(`Request failed (${response.status})`);
  const etag = response.headers.get("ETag");
  if (etag) state.etags[cacheKey] = etag;
  return { notModified: false, projection: await response.json() };
}

function catalogUrl(cursor = null) {
  const params = new URLSearchParams({ limit: "50" });
  if (cursor) params.set("cursor", JSON.stringify(cursor));
  return `${API_ROOT}/catalog?${params}`;
}

function projectUrl(projectId) {
  return `${API_ROOT}/projects/${encodeURIComponent(projectId)}/shell`;
}

function applyCatalog(projection, { append = false } = {}) {
  const items = Array.isArray(projection.data?.items) ? projection.data.items : [];
  const known = new Map((append ? state.catalogItems : []).map((item) => [item.project_ref?.resource_key, item]));
  for (const item of items) {
    if (item.project_ref?.resource_key) known.set(item.project_ref.resource_key, item);
  }
  state.catalogItems = [...known.values()];
  state.nextCursor = projection.data?.pagination?.next_cursor ?? null;
}

async function fetchShell(projectId) {
  if (!projectId) return;
  const result = await getJson(projectUrl(projectId), "shell");
  if (result.notModified) return result;
  const shell = result.projection;
  if (shell.resource_ref?.project_id !== projectId || shell.resource_ref?.kind !== "project") {
    throw new Error("Workspace identity could not be authenticated.");
  }
  return { notModified: false, projection: shell };
}

async function load({ append = false, eventProjectId = null } = {}) {
  const requestedProjectId = routeProjectId();
  const generation = state.loadGeneration + 1;
  state.loadGeneration = generation;
  const projectChanged = requestedProjectId !== state.routeProjectId;
  if (!append) {
    state.routeProjectId = requestedProjectId;
    if (projectChanged) state.shell = null;
    state.shellError = null;
    state.catalogError = null;
  }
  state.loading = true;
  statusRegion.textContent = append ? "Loading more projects." : "Loading read-only Workspace data.";
  let changed = false;
  try {
    const cursor = append ? state.nextCursor : null;
    // Snapshot ETags intentionally identify sources, not page position. Keep
    // validators per transport page so loading page two cannot 304 against
    // page one merely because both bind the same source snapshot.
    const catalog = await getJson(
      catalogUrl(cursor),
      `catalog:${cursor ? JSON.stringify(cursor) : "initial"}`,
    );
    if (generation !== state.loadGeneration) return;
    if (!catalog.notModified) {
      applyCatalog(catalog.projection, { append });
      changed = true;
    }
  } catch (error) {
    if (generation !== state.loadGeneration) return;
    state.catalogError = error.message;
  }
  if (!append && state.routeProjectId && (!eventProjectId || eventProjectId === state.routeProjectId)) {
    try {
      const shell = await fetchShell(state.routeProjectId);
      if (generation !== state.loadGeneration || routeProjectId() !== requestedProjectId) return;
      if (!shell.notModified) {
        state.shell = shell.projection;
        changed = true;
      }
    } catch (error) {
      if (generation !== state.loadGeneration || routeProjectId() !== requestedProjectId) return;
      state.shellError = error.message;
    }
  }
  if (generation !== state.loadGeneration) return;
  state.loading = false;
  statusRegion.textContent = state.shellError || state.catalogError || "Workspace data loaded.";
  if (changed || state.shellError || state.catalogError || projectChanged || append) render();
  if (state.refreshTrailing && !state.refreshInFlight) {
    state.refreshTrailing = false;
    scheduleRefresh();
  }
}

function scheduleRefresh(projectId = null) {
  if (typeof projectId === "string") state.refreshProjectIds.add(projectId);
  if (state.refreshInFlight || state.loading) {
    state.refreshTrailing = true;
    return;
  }
  state.refreshInFlight = true;
  const refreshProjectId = state.refreshProjectIds.size === 1 ? [...state.refreshProjectIds][0] : null;
  state.refreshProjectIds.clear();
  load({ eventProjectId: refreshProjectId }).catch((error) => { state.catalogError = error.message; render(); }).finally(() => {
    state.refreshInFlight = false;
    if (state.refreshTrailing) {
      state.refreshTrailing = false;
      scheduleRefresh();
    }
  });
}

function startWorkspaceEvents() {
  if (state.eventSource || !window.EventSource) return;
  const source = new EventSource(`${API_ROOT}/events`);
  state.eventSource = source;
  source.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      if (payload?.type === "change" && typeof payload.project_id === "string") scheduleRefresh(payload.project_id);
    } catch { /* malformed coarse event is ignored */ }
  };
  source.onerror = () => { /* EventSource reconnects; cached GET remains usable. */ };
}

function navigateProject(projectId) {
  const requested = new URLSearchParams(location.search).get("stage");
  const query = requested ? `?stage=${encodeURIComponent(requested)}` : "";
  history.pushState({}, "", `/p/${encodeURIComponent(projectId)}/workspace${query}`);
  load();
}

function navigateStage(stageName) {
  const params = new URLSearchParams(location.search);
  params.set("stage", stageName);
  history.pushState({}, "", `${location.pathname}?${params}`);
  render();
}

function projectHref(projectId) {
  const requested = new URLSearchParams(location.search).get("stage");
  const query = requested ? `?stage=${encodeURIComponent(requested)}` : "";
  return `/p/${encodeURIComponent(projectId)}/workspace${query}`;
}

function badge(text, variant = "") { return node("span", { class: `badge ${variant}`, text }); }

function filteredCatalogItems() {
  const query = state.filter.trim().toLocaleLowerCase();
  return state.catalogItems.filter((item) => {
    const title = String(item.title || "").toLocaleLowerCase();
    const projectId = String(item.project_ref?.project_id || "").toLocaleLowerCase();
    return !query || title.includes(query) || projectId.includes(query);
  });
}

function updateCatalogList(list, empty) {
  list.textContent = "";
  for (const item of filteredCatalogItems()) {
    const projectId = item.project_ref?.project_id;
    if (typeof projectId !== "string") continue;
    const link = node("a", {
      class: "project",
      href: projectHref(projectId),
      "data-project-id": projectId,
      "aria-current": projectId === state.routeProjectId ? "page" : null,
      onclick: (event) => {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        navigateProject(projectId);
      },
    }, [
      node("span", { class: "project-title", text: item.title }),
      node("span", { class: "project-id", text: projectId }),
      node("span", { class: "label", text: `${item.classification} · ${item.authority?.authority_state || "unavailable"}` }),
    ]);
    list.append(node("li", {}, [link]));
  }
  empty.hidden = Boolean(list.childElementCount) || Boolean(state.catalogError);
}

function renderCatalog() {
  const panel = node("section", { class: "panel", "aria-labelledby": "project-selector-title" });
  panel.append(node("h2", { id: "project-selector-title", text: "Projects" }));
  const label = node("label", { for: "project-search", text: "Search loaded projects" });
  const input = node("input", { id: "project-search", name: "project-search", class: "search", type: "search", value: state.filter, autocomplete: "off" });
  const list = node("ul", { class: "project-list" });
  const empty = node("p", { class: "empty", text: "No loaded projects match this search." });
  input.addEventListener("input", () => {
    state.filter = input.value;
    updateCatalogList(list, empty);
  });
  panel.append(label, input, node("p", { class: "scope", text: `Searches ${state.catalogItems.length} loaded project${state.catalogItems.length === 1 ? "" : "s"}; server-side search is not available in B0.2C.` }));
  if (state.catalogError) panel.append(node("p", { class: "diagnostic error", text: state.catalogError }));
  updateCatalogList(list, empty);
  panel.append(list, empty);
  if (state.nextCursor) panel.append(node("button", { class: "control", type: "button", text: "Load more projects", onclick: () => load({ append: true }) }));
  return panel;
}

function authorityDetails(shell) {
  const authority = shell.authority || {};
  const details = node("div", { class: "details" });
  const capabilityText = Object.entries(shell.capabilities || {}).map(([name, capability]) => `${name}: ${capability?.available ? "available" : capability?.reason || "unavailable"}`).join(" · ") || "unavailable";
  const degradedText = Array.isArray(authority.degraded_reasons) && authority.degraded_reasons.length ? authority.degraded_reasons.join(" · ") : "none";
  for (const [label, value] of [["Authority", authority.authority_state], ["Validation", authority.validation_state], ["Source", authority.source_kind], ["Pipeline", shell.data?.pipeline_type], ["Classification", shell.data?.classification], ["Current stage", shell.data?.current_stage], ["Gate", shell.data?.gate_state], ["Capabilities", capabilityText], ["Degraded reasons", degradedText]]) {
    details.append(node("div", { class: "detail" }, [node("span", { class: "label", text: label }), node("strong", { text: value || "unavailable" })]));
  }
  return details;
}

function renderDiagnostics(shell) {
  const diagnostics = [...(Array.isArray(shell.diagnostics) ? shell.diagnostics : [])];
  if (!diagnostics.length) return null;
  const section = node("section", { class: "panel", "aria-labelledby": "diagnostics-title" });
  section.append(node("h2", { id: "diagnostics-title", text: "Diagnostics" }));
  for (const diagnostic of diagnostics) {
    const severity = diagnostic.severity === "error" ? "error" : "";
    section.append(node("div", { class: `diagnostic ${severity}` }, [
      node("strong", { text: diagnostic.code || "workspace_diagnostic" }),
      node("span", { text: ` — ${diagnostic.message || "Source state is unavailable."}` }),
    ]));
  }
  return section;
}

function renderShell() {
  if (!state.routeProjectId) return node("section", { class: "panel status", text: "Choose an authenticated project to open its read-only Workspace shell." });
  if (state.shellError) return node("section", { class: "panel status" }, [node("h1", { text: "Workspace unavailable" }), node("p", { class: "muted", text: state.shellError })]);
  if (!state.shell) return node("section", { class: "panel status", text: "Loading Workspace shell…" });
  const shell = state.shell;
  const selected = selectedStage(shell);
  const section = node("div");
  const heading = node("section", { class: "panel" });
  heading.append(node("div", { class: "hero" }, [
    node("div", {}, [node("h1", { text: "Director Workspace" }), node("p", { class: "muted", text: `Authenticated project: ${shell.resource_ref.project_id}` })]),
    node("div", { class: "badges" }, [badge(shell.authority?.authority_state || "unavailable", shell.authority?.authority_state === "unavailable" ? "warn" : "good"), badge("Read only")]),
  ]));
  heading.append(authorityDetails(shell));
  section.append(heading);
  if (selected.requested && !selected.selected) section.append(node("p", { class: "selection-warning", role: "status", text: `Requested stage “${selected.requested}” is unavailable for this manifest. No fallback stage was selected.` }));
  const railPanel = node("section", { class: "panel", "aria-labelledby": "stage-rail-title" });
  railPanel.append(node("h2", { id: "stage-rail-title", text: "Manifest stages" }));
  const rail = node("nav", { "aria-label": "Manifest stage rail" }, [node("ul", { class: "rail" })]);
  const list = rail.firstChild;
  const stages = Array.isArray(shell.data?.stages) ? shell.data.stages : [];
  for (const stage of stages) {
    const stageButton = node("button", { class: `stage ${stage.status}`, type: "button", "data-stage": stage.name, "aria-current": selected.selected === stage.name ? "step" : null, onclick: () => navigateStage(stage.name) }, [
      node("span", { class: "stage-name", text: stage.name }),
      node("span", { class: "stage-status", text: stage.status }),
      node("span", { class: "label", text: stage.human_approval_default ? "human gate by manifest" : "no default human gate" }),
    ]);
    list.append(node("li", {}, [stageButton]));
  }
  railPanel.append(rail);
  if (!stages.length) railPanel.append(node("p", { class: "empty", text: "No validated manifest stage rail is available." }));
  section.append(railPanel);
  const diagnostics = renderDiagnostics(shell);
  if (diagnostics) section.append(diagnostics);
  return section;
}

function render() {
  const active = document.activeElement;
  const scrollY = window.scrollY;
  const preserveSearch = active?.id === "project-search";
  const activeProjectId = active?.getAttribute?.("data-project-id");
  const activeStage = active?.getAttribute?.("data-stage");
  const selectionStart = preserveSearch ? active.selectionStart : null;
  const selectionEnd = preserveSearch ? active.selectionEnd : null;
  app.textContent = "";
  const workspace = node("div", { class: "workspace" });
  if (state.loading) workspace.append(node("p", { class: "status", role: "status", text: "Loading read-only Workspace data…" }));
  const grid = node("div", { class: "grid" }, [renderCatalog(), renderShell()]);
  workspace.append(grid);
  app.append(workspace);
  state.renderCount += 1;
  if (preserveSearch) {
    const input = document.getElementById("project-search");
    input?.focus();
    if (selectionStart !== null && selectionEnd !== null) input?.setSelectionRange(selectionStart, selectionEnd);
  }
  if (!preserveSearch && activeProjectId) {
    document.querySelector(`[data-project-id="${CSS.escape(activeProjectId)}"]`)?.focus();
  }
  if (!preserveSearch && activeStage) {
    document.querySelector(`[data-stage="${CSS.escape(activeStage)}"]`)?.focus();
  }
  requestAnimationFrame(() => window.scrollTo(0, scrollY));
}

window.addEventListener("popstate", () => load());
window.addEventListener("beforeunload", () => state.eventSource?.close());
window.__workspaceDebug = {
  get renderCount() { return state.renderCount; },
  scheduleRefresh,
};
render();
startWorkspaceEvents();
load();
