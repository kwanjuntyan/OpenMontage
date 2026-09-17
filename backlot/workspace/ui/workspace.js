const API_ROOT = "/api/workspace/v1";
// A NUL-prefixed control value cannot collide with a schema-valid project ID.
const LOAD_MORE_OPTION = "\u0000workspace_load_more";
const app = document.getElementById("workspace-app");
const statusRegion = document.getElementById("workspace-status");

const state = {
  catalogItems: [],
  nextCursor: null,
  catalogError: null,
  shell: null,
  shellError: null,
  course: null,
  courseError: null,
  script: null,
  scriptError: null,
  style: null,
  styleError: null,
  routeProjectId: null,
  statusExpanded: false,
  loading: false,
  loadGeneration: 0,
  responseCache: new Map(),
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

async function getJson(url, cacheKey, validateProjection = null, force = false) {
  const headers = { Accept: "application/json" };
  const cached = state.responseCache.get(cacheKey);
  if (!force && cached?.etag) headers["If-None-Match"] = cached.etag;
  const response = await fetch(url, { headers });
  if (response.status === 304) {
    if (cached?.projection) return { notModified: true, projection: cached.projection };
    state.responseCache.delete(cacheKey);
    if (!force) return getJson(url, cacheKey, validateProjection, true);
    throw new Error("Conditional response had no validated Workspace representation.");
  }
  if (!response.ok) throw new Error(`Request failed (${response.status})`);
  const etag = response.headers.get("ETag");
  const projection = await response.json();
  if (validateProjection) validateProjection(projection);
  if (etag) state.responseCache.set(cacheKey, { etag, projection });
  else state.responseCache.delete(cacheKey);
  return { notModified: false, projection };
}

function catalogUrl(cursor = null) {
  const params = new URLSearchParams({ limit: "50" });
  if (cursor) params.set("cursor", JSON.stringify(cursor));
  return `${API_ROOT}/catalog?${params}`;
}

function projectUrl(projectId) {
  return `${API_ROOT}/projects/${encodeURIComponent(projectId)}/shell`;
}

function courseUrl(projectId) { return `${API_ROOT}/projects/${encodeURIComponent(projectId)}/course`; }
function scriptUrl(projectId) { return `${API_ROOT}/projects/${encodeURIComponent(projectId)}/script`; }
function styleUrl(projectId) { return `${API_ROOT}/projects/${encodeURIComponent(projectId)}/style`; }

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
  return getJson(projectUrl(projectId), `shell:${projectId}`, (shell) => {
    if (shell.resource_ref?.project_id !== projectId || shell.resource_ref?.kind !== "project") {
      throw new Error("Workspace identity could not be authenticated.");
    }
  });
}

async function load({ append = false, eventProjectId = null } = {}) {
  const requestedProjectId = routeProjectId();
  const generation = state.loadGeneration + 1;
  state.loadGeneration = generation;
  const projectChanged = requestedProjectId !== state.routeProjectId;
  if (!append) {
    state.routeProjectId = requestedProjectId;
    if (projectChanged) {
      state.shell = null;
      state.course = null;
      state.courseError = null;
      state.script = null;
      state.scriptError = null;
      state.style = null;
      state.styleError = null;
      state.statusExpanded = false;
    }
    state.shellError = null;
    state.catalogError = null;
  }
  state.loading = true;
  statusRegion.textContent = append ? "Loading more projects." : "Loading read-only Workspace data.";
  // A new opaque route must never keep the previous authenticated shell on
  // screen while its own request is in flight.  Appending catalog pages keeps
  // the active shell, deep link, and focus intact.
  if (!append && projectChanged) render();
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
    if (catalog.projection && (!catalog.notModified || !state.catalogItems.length)) {
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
      if (shell.projection?.resource_ref?.project_id !== requestedProjectId || shell.projection?.resource_ref?.kind !== "project") throw new Error("Workspace identity could not be authenticated.");
      if (shell.projection && (!shell.notModified || !state.shell)) {
        state.shell = shell.projection;
        changed = true;
      }
      if (state.shell && selectedStage(state.shell).selected === "proposal") {
        await loadCourse(state.routeProjectId, generation);
        await loadStyle(state.routeProjectId, generation);
        changed = true;
      }
      if (state.shell && selectedStage(state.shell).selected === scriptOwnerStage(state.shell)) {
        await loadScript(state.routeProjectId, generation);
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
  const query = location.search;
  history.pushState({}, "", `/p/${encodeURIComponent(projectId)}/workspace${query}`);
  load();
}

function navigateStage(stageName) {
  const params = new URLSearchParams(location.search);
  params.set("stage", stageName);
  history.pushState({}, "", `${location.pathname}?${params}`);
  render();
  if (stageName === "proposal" && state.routeProjectId) loadCourse(state.routeProjectId, state.loadGeneration);
  if (stageName === "proposal" && state.routeProjectId) loadStyle(state.routeProjectId, state.loadGeneration);
  if (stageName === scriptOwnerStage() && state.routeProjectId) loadScript(state.routeProjectId, state.loadGeneration);
}

function scriptOwnerStage(shell = state.shell) {
  if (typeof shell?.data?.script_owner_stage === "string") return shell.data.script_owner_stage;
  const stages = Array.isArray(shell?.data?.stages) ? shell.data.stages : [];
  // Without an explicit manifest owner, fail closed rather than guessing from a stage label.
  return null;
}

async function loadCourse(projectId, generation) {
  try {
    const result = await getJson(courseUrl(projectId), `course:${projectId}`, (projection) => {
      if (projection?.resource_ref?.project_id !== projectId || projection?.resource_ref?.kind !== "course") throw new Error("Course identity could not be authenticated.");
    });
    if (generation !== state.loadGeneration || routeProjectId() !== projectId || selectedStage().selected !== "proposal") return;
    if (result.projection?.resource_ref?.project_id !== projectId || result.projection?.resource_ref?.kind !== "course") throw new Error("Course identity could not be authenticated.");
    if (result.projection && (!result.notModified || !state.course)) state.course = result.projection;
    state.courseError = null;
  } catch (error) {
    if (generation !== state.loadGeneration || routeProjectId() !== projectId || selectedStage().selected !== "proposal") return;
    state.courseError = error.message;
  }
  if (generation === state.loadGeneration) render();
}

async function loadScript(projectId, generation) {
  const owner = scriptOwnerStage();
  if (!owner) return;
  try {
    const result = await getJson(scriptUrl(projectId), `script:${projectId}`, (projection) => {
      if (projection?.resource_ref?.project_id !== projectId || projection?.resource_ref?.kind !== "stage" || projection?.resource_ref?.stage !== owner || projection?.resource_ref?.local_id !== owner) throw new Error("Script identity could not be authenticated.");
    });
    if (generation !== state.loadGeneration || routeProjectId() !== projectId || selectedStage().selected !== owner) return;
    if (result.projection?.resource_ref?.project_id !== projectId || result.projection?.resource_ref?.kind !== "stage" || result.projection?.resource_ref?.stage !== owner || result.projection?.resource_ref?.local_id !== owner) throw new Error("Script identity could not be authenticated.");
    if (result.projection && (!result.notModified || !state.script)) state.script = result.projection;
    state.scriptError = null;
  } catch (error) {
    if (generation !== state.loadGeneration || routeProjectId() !== projectId || selectedStage().selected !== owner) return;
    state.scriptError = error.message;
  }
  if (generation === state.loadGeneration) render();
}

async function loadStyle(projectId, generation) {
  try {
    const result = await getJson(styleUrl(projectId), `style:${projectId}`, (projection) => {
      if (projection?.resource_ref?.project_id !== projectId || projection?.resource_ref?.kind !== "project" || projection?.resource_ref?.local_id !== projectId) throw new Error("Style identity could not be authenticated.");
    });
    if (generation !== state.loadGeneration || routeProjectId() !== projectId || selectedStage().selected !== "proposal") return;
    if (result.projection?.resource_ref?.project_id !== projectId || result.projection?.resource_ref?.kind !== "project" || result.projection?.resource_ref?.local_id !== projectId) throw new Error("Style identity could not be authenticated.");
    if (result.projection && (!result.notModified || !state.style)) state.style = result.projection;
    state.styleError = null;
  } catch (error) {
    if (generation !== state.loadGeneration || routeProjectId() !== projectId || selectedStage().selected !== "proposal") return;
    state.styleError = error.message;
  }
  if (generation === state.loadGeneration) render();
}

function badge(text, variant = "") { return node("span", { class: `badge ${variant}`, text }); }

function renderProjectSelector() {
  const selector = node("select", {
    id: "project-selector",
    name: "project-selector",
    class: "project-selector",
    "aria-label": "Choose a loaded project / 選擇已載入專案",
  });
  const loadedIds = new Set();
  for (const item of state.catalogItems) {
    const projectId = item.project_ref?.project_id;
    if (typeof projectId !== "string") continue;
    loadedIds.add(projectId);
    selector.append(node("option", {
      value: projectId,
      text: `${item.title} — ${item.classification}`,
      selected: projectId === state.routeProjectId ? "selected" : null,
    }));
  }
  if (!state.catalogItems.length) {
    const text = state.catalogError ? "Project catalog is unavailable" : "Loading project choices…";
    selector.append(node("option", { value: "", text, selected: "selected", disabled: "disabled" }));
  } else if (state.routeProjectId && !loadedIds.has(state.routeProjectId)) {
    // The URL alone is not authenticated project identity.  Do not display it
    // as a project label until catalog or shell evidence returns it.
    selector.append(node("option", { value: "", text: "Current route is awaiting authenticated project data", selected: "selected", disabled: "disabled" }));
  } else if (!state.routeProjectId) {
    selector.insertBefore(node("option", { value: "", text: "Choose a project", selected: "selected", disabled: "disabled" }), selector.firstChild);
  }
  if (state.catalogError && state.catalogItems.length) {
    selector.append(node("option", { value: "", text: "Catalog refresh unavailable", disabled: "disabled" }));
  }
  if (state.nextCursor) selector.append(node("option", { value: LOAD_MORE_OPTION, text: "Load more projects…" }));
  selector.addEventListener("change", () => {
    if (selector.value === LOAD_MORE_OPTION) {
      load({ append: true });
    } else if (selector.value) {
      navigateProject(selector.value);
    }
  });
  return selector;
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

function renderDiagnosticsContent(shell) {
  const diagnostics = [...(Array.isArray(shell?.diagnostics) ? shell.diagnostics : [])];
  const section = node("section", { class: "diagnostics", "aria-labelledby": "diagnostics-title" });
  section.append(node("h3", { id: "diagnostics-title", text: "Diagnostics" }));
  if (!shell) {
    section.append(node("p", { class: "empty", text: "Diagnostics become available when an authenticated project shell is loaded." }));
    return section;
  }
  if (!diagnostics.length) {
    section.append(node("p", { class: "empty", text: "No Workspace diagnostics were reported for this shell." }));
    return section;
  }
  for (const diagnostic of diagnostics) {
    const severity = diagnostic.severity === "error" ? "error" : "";
    section.append(node("div", { class: `diagnostic ${severity}` }, [
      node("strong", { text: diagnostic.code || "workspace_diagnostic" }),
      node("span", { text: ` — ${diagnostic.message || "Source state is unavailable."}` }),
    ]));
  }
  return section;
}

function renderStageInspector(shell, selected) {
  const inspector = node("section", { class: "stage-inspector", "aria-labelledby": "stage-inspector-title" });
  inspector.append(node("h3", { id: "stage-inspector-title", text: "Stage Inspector / 階段檢視" }));
  if (selected.requested && !selected.selected) {
    inspector.append(node("p", { class: "selection-warning", role: "status", text: `Requested stage “${selected.requested}” is unavailable for this manifest. No fallback stage was selected.` }));
    return inspector;
  }
  if (!selected.selected) {
    inspector.append(node("p", { class: "empty", text: "Choose a manifest stage to view its read-only summary. The current stage is not selected automatically." }));
    return inspector;
  }
  const stage = (shell.data?.stages || []).find((entry) => entry.name === selected.selected);
  if (!stage) {
    inspector.append(node("p", { class: "empty", text: "The selected manifest stage is unavailable." }));
    return inspector;
  }
  const details = node("div", { class: "details" });
  for (const [label, value] of [
    ["Stage", stage.name],
    ["State", stage.status],
    ["Manifest human gate", stage.human_approval_default ? "required" : "not required"],
    ["Project gate state", shell.data?.gate_state],
  ]) {
    details.append(node("div", { class: "detail" }, [node("span", { class: "label", text: label }), node("strong", { text: value || "unavailable" })]));
  }
  inspector.append(details);
  if (stage.name !== "proposal" && stage.name !== scriptOwnerStage(shell)) inspector.append(node("p", { class: "empty", text: "Read-only stage summary only. Detailed stage inspectors are a future capability." }));
  if (stage.name === "proposal") inspector.append(renderCourseInspector());
  if (stage.name === "proposal") inspector.append(renderStyleInspector());
  if (stage.name === scriptOwnerStage(shell)) inspector.append(renderScriptInspector());
  return inspector;
}

function renderStyleInspector() {
  const section = node("section", { class: "style-inspector", "aria-labelledby": "style-inspector-title" });
  section.append(node("h4", { id: "style-inspector-title", text: "Style Inspector / 風格檢視" }));
  if (state.styleError) return section.append(node("p", { class: "diagnostic error", text: state.styleError })), section;
  if (!state.style) return section.append(node("p", { class: "empty", text: "Loading Style projection…" })), section;
  const data = state.style.data || {}; const style = data.style;
  if (!style || typeof style !== "object") return section.append(node("p", { class: "empty", text: "Style details are unavailable." })), section;
  const proposal = style.proposal || {}; const observations = style.observations || {}; const resolved = style.resolved_style;
  const proposalLifecycle = style.proposal_authority?.authority_state || "unavailable";
  section.append(node("p", { class: "muted", text: resolved ? "Current catalog Style (not historically frozen)" : `Style unavailable: ${state.style.authority?.degraded_reasons?.join(", ") || "unavailable"}` }));
  if (proposal.selected_concept) section.append(node("p", { text: `Selected concept: ${proposal.selected_concept.concept_id}; visual approach: ${proposal.selected_concept.visual_approach}` }));
  section.append(node("p", { class: "muted", text: `Proposal (${proposalLifecycle}) playbook: ${proposal.playbook || "unavailable"}; renderer: ${proposal.renderer_family || "unavailable"}; runtime: ${proposal.render_runtime || "unavailable"}; composition: ${proposal.composition_mode || "unavailable"}` }));
  if (proposal.art_direction) section.append(node("p", { text: `Art direction: ${proposal.art_direction}` }));
  if (proposal.taste_profile) section.append(node("p", { class: "muted", text: `Proposal taste profile (preferred; not merged): ${JSON.stringify(proposal.taste_profile)}` }));
  if (style.course_style_intent) section.append(node("p", { class: "muted", text: `Course style intent (${style.course_authority?.authority_state || "unavailable"}; separate): tone ${style.course_style_intent.tone}; visual intent ${style.course_style_intent.visual_intent}` }));
  const observationText = Object.entries(observations).map(([name, item]) => `${name}: ${item?.state || "unavailable"}${item?.value ? ` (${item.value})` : ""}`).join(" · ");
  section.append(node("p", { class: "muted", text: `Identity observations: ${observationText}` }));
  const checkpointList = node("ul");
  for (const item of Array.isArray(style.checkpoint_observations) ? style.checkpoint_observations : []) checkpointList.append(node("li", { text: `${item.stage}: ${item.state}${item.value ? ` (${item.value})` : ""}; ${item.authority?.authority_state || "unavailable"}/${item.authority?.checkpoint_status || "none"}` }));
  section.append(node("section", { class: "course-section" }, [node("h5", { text: "Checkpoint style observations" }), checkpointList.children.length ? checkpointList : node("p", { class: "muted", text: "No checkpoint style claims." })]));
  if (!resolved) return section;
  const catalog = resolved.catalog || {}; const details = node("details", { class: "course-detail" }, [node("summary", { text: `${resolved.playbook}: validated current catalog details` })]);
  for (const [label, value] of [["Identity", catalog.identity], ["Visual language", catalog.visual_language], ["Typography", catalog.typography], ["Motion", catalog.motion], ["Audio", catalog.audio], ["Asset generation", catalog.asset_generation], ["Quality rules", catalog.quality_rules], ["Catalog taste profile", catalog.taste_profile]]) if (value !== undefined) details.append(node("p", { class: "muted", text: `${label}: ${JSON.stringify(value)}` }));
  section.append(details); return section;
}

function renderScriptInspector() {
  const section = node("section", { class: "script-inspector", "aria-labelledby": "script-inspector-title" });
  section.append(node("h4", { id: "script-inspector-title", text: "Script Inspector / 劇本檢視" }));
  if (state.scriptError) return section.append(node("p", { class: "diagnostic error", text: state.scriptError })), section;
  if (!state.script) return section.append(node("p", { class: "empty", text: "Loading Script revision set…" })), section;
  const data = state.script.data || {}; const revision = data.current_canonical || data.pending_candidates?.[0];
  if (!revision) return section.append(node("p", { class: "empty", text: `Script unavailable: ${data.current_canonical_unavailable_reason || "script_missing"}` })), section;
  const script = revision.data?.script;
  if (!script || typeof script !== "object") return section.append(node("p", { class: "empty", text: "Validated Script details are unavailable." })), section;
  section.append(node("p", { class: "muted", text: data.current_canonical ? "Canonical script" : "Awaiting-human script candidate" }));
  section.append(node("p", { class: "muted", text: "Shape validation only: no timing-continuity, unique-section-ID, or duration-sum claim. source_ref is free-form and unverified." }));
  section.append(node("h5", { text: script.title }), node("p", { text: `Total duration: ${script.total_duration_seconds} seconds` }));
  if (script.voice_performance) section.append(node("p", { class: "muted", text: `Voice performance: ${Object.entries(script.voice_performance).map(([key, value]) => `${key}: ${typeof value === "object" ? JSON.stringify(value) : value}`).join(" · ")}` }));
  const search = node("input", { class: "script-search", type: "search", placeholder: "Search full script", "aria-label": "Search full script" });
  const controls = node("div", { class: "script-controls", "aria-label": "Script section controls" });
  const expandAll = node("button", { class: "control", type: "button", text: "全部展開", "aria-label": "Expand all script sections" });
  const collapseAll = node("button", { class: "control", type: "button", text: "全部收合", "aria-label": "Collapse all script sections" });
  const resultStatus = node("p", { class: "sr-status", role: "status", "aria-live": "polite" });
  const list = node("div", { class: "script-sections" });
  const requested = new URLSearchParams(location.search).get("section");
  const sections = Array.isArray(script.sections) ? script.sections : [];
  const matches = requested ? sections.filter((item) => item.id === requested) : [];
  if (requested && matches.length !== 1) section.append(node("p", { class: "selection-warning", role: "status", text: `Requested section “${requested}” is ${matches.length ? "ambiguous" : "missing"}; no section was selected.` }));
  const details = sections.map((item) => {
    const selected = matches.length === 1 && item.id === requested;
    const detail = node("details", { class: "script-section", id: selected ? `script-section-${item.id}` : null, open: selected ? "open" : null }, [node("summary", { text: `${item.id}${item.label ? `: ${item.label}` : ""} · ${item.start_seconds}–${item.end_seconds}s` })]);
    detail.append(node("p", { text: item.text }));
    for (const key of ["speaker_directions", "delivery_cues", "enhancement_cues", "pronunciation_guides", "source_ref"]) if (item[key] !== undefined) detail.append(node("p", { class: "muted", text: `${key}: ${typeof item[key] === "object" ? JSON.stringify(item[key]) : item[key]}` }));
    list.append(detail); return { detail, item };
  });
  const setAllOpen = (open) => { for (const { detail } of details) detail.open = open; };
  expandAll.addEventListener("click", () => setAllOpen(true));
  collapseAll.addEventListener("click", () => setAllOpen(false));
  expandAll.disabled = collapseAll.disabled = details.length === 0;
  const filter = () => {
    const query = search.value.trim().toLocaleLowerCase(); let visible = 0;
    for (const { detail, item } of details) {
      const matched = !query || JSON.stringify(item).toLocaleLowerCase().includes(query);
      detail.hidden = !matched; if (matched) visible += 1;
    }
    resultStatus.textContent = query ? `${visible} matching script sections.` : "";
    if (matches.length === 1 && !query) requestAnimationFrame(() => document.getElementById(`script-section-${requested}`)?.scrollIntoView({ block: "center" }));
  };
  search.addEventListener("input", filter); controls.append(expandAll, collapseAll); section.append(search, controls, resultStatus, list); filter(); return section;
}

function renderCourseInspector() {
  const section = node("section", { class: "course-inspector", "aria-labelledby": "course-inspector-title" });
  section.append(node("h4", { id: "course-inspector-title", text: "Course Inspector / 課程檢視" }));
  if (state.courseError) return section.append(node("p", { class: "diagnostic error", text: state.courseError })), section;
  if (!state.course) return section.append(node("p", { class: "empty", text: "Loading Course revision set…" })), section;
  const data = state.course.data || {};
  const revision = data.current_canonical || data.pending_candidates?.[0];
  if (!revision) return section.append(node("p", { class: "empty", text: `Course unavailable: ${data.current_canonical_unavailable_reason || "course_manifest_unavailable"}` })), section;
  const stateLabel = data.current_canonical ? "Canonical course" : "Awaiting-human course candidate";
  const course = revision.data?.course_design;
  if (!course || typeof course !== "object") return section.append(node("p", { class: "empty", text: "Validated Course details are unavailable." })), section;
  const list = (values, label, renderValue = (value) => value) => {
    const wrapper = node("section", { class: "course-section" }, [node("h5", { text: label })]);
    const items = node("ul");
    for (const value of Array.isArray(values) ? values : []) items.append(node("li", { text: renderValue(value) }));
    wrapper.append(items.children.length ? items : node("p", { class: "muted", text: "None declared." }));
    return wrapper;
  };
  const detail = (label, children) => node("details", { class: "course-detail" }, [node("summary", { text: label }), children]);
  const refs = (values) => Array.isArray(values) && values.length ? values.join(", ") : "none";
  section.append(node("p", { class: "muted", text: stateLabel }));
  section.append(node("p", { class: "muted", text: "Course-manifest intent only; this is not resolved Style or delivery/publication evidence." }));
  section.append(node("h5", { text: course.title || "Course" }));
  section.append(node("p", { text: `Target duration: ${course.target_duration_seconds || "?"} seconds` }));
  const promise = course.course_promise || {};
  section.append(detail("Course promise", list([
    `Learner: ${promise.learner || "unavailable"}`,
    `Capability: ${promise.capability || "unavailable"}`,
    `Use context: ${promise.use_context || "unavailable"}`,
    `Success evidence: ${promise.success_evidence || "unavailable"}`,
  ], "Promise")));
  section.append(list(course.audience, "Audience"), list(course.entry_requirements, "Entry requirements"));
  section.append(list(course.objectives, "Objectives", (item) => `${item.id}: ${item.actor} ${item.observable_verb} ${item.object}; conditions: ${item.conditions || "none declared"}; evidence: ${item.success_evidence}; sources: ${refs(item.source_refs)}`));
  const modules = node("section", { class: "course-section" }, [node("h5", { text: "Modules and lessons" })]);
  for (const module of Array.isArray(course.modules) ? course.modules : []) {
    const lessons = node("ul");
    for (const lesson of Array.isArray(module.lessons) ? module.lessons : []) {
      const beats = (lesson.teaching_beats || []).map((beat) => `${beat.kind}: ${beat.intent} (${refs(beat.objective_ids)})`).join("; ");
      lessons.append(node("li", { text: `${lesson.id}: ${lesson.title}; ${lesson.target_duration_seconds}s; objectives ${refs(lesson.objective_ids)}; prerequisites lessons ${refs(lesson.prerequisite_lesson_ids)}, objectives ${refs(lesson.prerequisite_objective_ids)}; outcome ${lesson.expected_outcome}; sources ${refs(lesson.source_refs)}; glossary ${refs(lesson.glossary_ids)}; notation ${refs(lesson.notation_ids)}; teaching beats ${beats || "none"}; export required: ${lesson.export_required ? "yes" : "no"}` }));
    }
    modules.append(detail(`${module.id}: ${module.title} (${module.target_duration_seconds}s)`, node("div", {}, [node("p", { text: `Intermediate capability: ${module.intermediate_capability}; objectives: ${refs(module.objective_ids)}; recap: ${module.recap_intent}` }), lessons])));
  }
  section.append(modules);
  section.append(list(course.assessments, "Assessments", (item) => `${item.id}: ${item.type}; objectives ${refs(item.objective_ids)}; lesson ${item.lesson_id || "none"}; prompt ${item.prompt_intent}; expected evidence ${item.expected_evidence}; pass criteria ${item.pass_criteria}`));
  section.append(list(course.sources, "Sources", (item) => `${item.id}: ${item.title || "untitled"}; URI: ${item.uri}${item.locator ? `; locator: ${item.locator}` : ""}${item.digest ? `; digest: ${item.digest}` : "; digest: none declared"}`));
  section.append(list(course.glossary, "Glossary", (item) => `${item.id}: ${item.preferred_term} — ${item.definition}; aliases ${refs(item.aliases)}; forbidden aliases ${refs(item.forbidden_aliases)}`));
  section.append(list(course.notation, "Notation", (item) => `${item.id}: ${item.symbol} = ${item.meaning}; first lesson ${item.first_lesson_id || "none"}; units ${item.units || "none"}`));
  section.append(detail("Style intent (course-manifest intent; not resolved Style)", list([`Tone: ${course.style_intent?.tone || "unavailable"}`, `Visual intent: ${course.style_intent?.visual_intent || "unavailable"}`], "Style intent")));
  const delivery = course.delivery_requirements || {};
  section.append(detail("Delivery requirements (declarations, not publication evidence)", list([`Full master: ${delivery.full_master ? "required" : "not required"}`, `Lesson exports: ${refs(delivery.lesson_export_ids)}`, `Chapter markers: ${delivery.chapter_markers ? "required" : "not required"}`, `Captions: ${refs(delivery.captions)}`, `Bundle: ${delivery.bundle ? "required" : "not required"}`], "Delivery declarations")));
  return section;
}

function renderProjectStatus() {
  const section = node("details", { id: "project-status", class: "panel project-status", open: state.statusExpanded ? "open" : null });
  section.append(node("summary", { id: "project-status-title", text: "Project status / 專案狀態摘要" }));
  section.addEventListener("toggle", () => { state.statusExpanded = section.open; });
  if (!state.routeProjectId) {
    section.append(
      node("p", { class: "status", text: "Choose an authenticated project to open its read-only Workspace shell." }),
      renderDiagnosticsContent(null),
    );
    return section;
  }
  if (state.shellError) {
    section.append(node("p", { class: "status", text: state.shellError }), renderDiagnosticsContent(null));
    return section;
  }
  if (!state.shell) {
    section.append(node("p", { class: "status", text: "Loading Workspace shell…" }), renderDiagnosticsContent(null));
    return section;
  }
  const shell = state.shell;
  section.append(node("div", { class: "hero" }, [
    node("div", {}, [node("p", { class: "muted", text: `Authenticated project: ${shell.resource_ref.project_id}` })]),
    node("div", { class: "badges" }, [badge(shell.authority?.authority_state || "unavailable", shell.authority?.authority_state === "unavailable" ? "warn" : "good"), badge("Read only")]),
  ]));
  section.append(authorityDetails(shell));
  section.append(renderDiagnosticsContent(shell));
  return section;
}

function renderProductionStages() {
  const railPanel = node("section", { class: "panel", "aria-labelledby": "stage-rail-title" });
  railPanel.append(node("h2", { id: "stage-rail-title", text: "Production stages / 製作階段導覽" }));
  if (!state.shell) {
    railPanel.append(node("p", { class: "empty", text: "Manifest stage navigation is available after the project shell loads." }));
    return railPanel;
  }
  const shell = state.shell;
  const selected = selectedStage(shell);
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
  railPanel.append(renderStageInspector(shell, selected));
  return railPanel;
}

function render() {
  const active = document.activeElement;
  const scrollY = window.scrollY;
  const activeId = active?.id || null;
  const activeProjectId = active?.getAttribute?.("data-project-id");
  const activeStage = active?.getAttribute?.("data-stage");
  app.textContent = "";
  const workspace = node("div", { class: "workspace" });
  const header = node("div", { class: "workspace-header" }, [
    node("h1", { id: "director-workspace-title", text: "Director Workspace" }),
    renderProjectSelector(),
  ]);
  workspace.append(header);
  if (state.loading) workspace.append(node("p", { class: "status", role: "status", text: "Loading read-only Workspace data…" }));
  const layout = node("div", { class: "single-column" }, [
    renderProjectStatus(),
    renderProductionStages(),
  ]);
  workspace.append(layout);
  app.append(workspace);
  state.renderCount += 1;
  if (activeId) document.getElementById(activeId)?.focus();
  if (!activeId && activeProjectId) {
    document.querySelector(`[data-project-id="${CSS.escape(activeProjectId)}"]`)?.focus();
  }
  if (!activeId && activeStage) {
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
