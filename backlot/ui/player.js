const selProject = document.getElementById("selProject");
const selSeq = document.getElementById("selSeq");
const selSceneGroup = document.getElementById("selSceneGroup");
const viewport = document.getElementById("viewport");
const filmstrip = document.getElementById("filmstrip");
const inspector = document.getElementById("inspector");
const audioEl = document.getElementById("audioEl");
const btnPrev = document.getElementById("btnPrev");
const btnPlay = document.getElementById("btnPlay");
const btnNext = document.getElementById("btnNext");
const chkAutoAdvance = document.getElementById("chkAutoAdvance");
const progressBar = document.getElementById("progressBar");
const progressFill = document.getElementById("progressFill");
const lblShotTime = document.getElementById("lblShotTime");
const lblShotCounter = document.getElementById("lblShotCounter");
const backToBoard = document.getElementById("backToBoard");

let projectId = new URLSearchParams(location.search).get("project") || "course-51-esg";
let boardState = null;
let allShots = [];
let filteredShots = [];
let currentIndex = 0;

let audioMode = "dialogue";   // "dialogue" | "video"
let visualMode = "image";     // "image" | "video"
let imgMode = "storyboard";   // "storyboard" | "camera" | "split"

let isPlaying = false;
let fallbackTimer = null;
let fallbackElapsed = 0;
let fallbackDuration = 5;
let activeVideoEl = null;

function mediaUrl(relPath) {
  if (!relPath) return "";
  const clean = String(relPath).replace(/^\/+/, "").split("/").map(encodeURIComponent).join("/");
  return `/media/${encodeURIComponent(projectId)}/${clean}`;
}

function parseShotHierarchy(shotId, sectionLabel, metadata) {
  const m = String(shotId || "").match(/^shot_(\d+)\.(\d+)\.(.+)$/i);
  if (!m) {
    return {
      seqKey: "1",
      seqTitle: "第 1 幕",
      groupKey: "1.1",
      groupTitle: sectionLabel || "場景 1.1",
    };
  }
  const seqKey = m[1];
  const groupKey = `${m[1]}.${m[2]}`;
  let seqTitle = `第 ${seqKey} 幕`;
  let groupTitle = `場景 ${groupKey}`;

  if (sectionLabel) {
    const parts = sectionLabel.split("·").map((s) => s.trim());
    if (parts[0] && parts[0].includes("幕")) seqTitle = parts[0];
    if (parts[1] && parts[1].includes("場景")) groupTitle = parts[1];
  }
  const metaKey = `scene_${m[1]}_${m[2]}`;
  if (metadata && metadata[metaKey] && metadata[metaKey].source_scene) {
    groupTitle = metadata[metaKey].source_scene;
  }
  return { seqKey, seqTitle, groupKey, groupTitle };
}

function buildShotsFromState(state) {
  const artifacts = state.artifacts || {};
  const scenePlan = artifacts.scene_plan || {};
  const script = artifacts.script || {};
  const clpManifest = artifacts.clp_manifest || {};
  const assetManifest = artifacts.asset_manifest || {};
  const sbScenes = (state.storyboard && state.storyboard.scenes) || [];

  const sbById = new Map(sbScenes.map((s) => [String(s.id), s]));
  const secById = new Map(((script.sections) || []).map((s) => [String(s.id), s]));
  const clpById = new Map(((clpManifest.entities) || []).map((e) => [String(e.id), e]));
  const amByPath = new Map(((assetManifest.assets) || []).map((a) => [String(a.path || ""), a]));
  const enrichTake = (t) => (t ? { ...(amByPath.get(String(t.path || "")) || {}), ...t, prompt: t.prompt || (amByPath.get(String(t.path || "")) || {}).prompt } : null);

  const rawScenes = scenePlan.scenes || [];
  return rawScenes.map((sc) => {
    const id = String(sc.id);
    const sb = sbById.get(id) || {};
    const sec = secById.get(String(sc.script_section_id || id)) || {};
    const hier = parseShotHierarchy(id, sec.label, scenePlan.metadata);

    const takes = sb.takes || [];
    const imageTake = enrichTake(takes.find((t) => t.type === "image" && t.exists) || (sb.visual && sb.visual.type === "image" && sb.visual.exists ? sb.visual : null));
    const videoTake = enrichTake(takes.find((t) => t.type === "video" && t.exists) || (sb.visual && sb.visual.type === "video" && sb.visual.exists ? sb.visual : null));
    const audioList = sb.audio || [];
    const dialogueAudio = audioList.find((a) => (a.type === "narration" || a.type === "audio") && a.exists) || null;

    const reqAssets = sc.required_assets || [];
    const camRef = reqAssets.find((r) => r.type === "camera_ref" && r.path) || reqAssets.find((r) => r.type === "camera_ref") || null;

    const clpEntities = [];
    for (const r of reqAssets) {
      if (r.type === "clp" && r.clp_id && clpById.has(r.clp_id)) {
        clpEntities.push(clpById.get(r.clp_id));
      }
    }

    const plannedDur = Math.max(0.5, Number(((sc.end_seconds ?? 0) - (sc.start_seconds ?? 0)).toFixed(2)) || 5);
    const audioDur = dialogueAudio && dialogueAudio.duration_seconds ? Number(dialogueAudio.duration_seconds) : null;

    return {
      id,
      scene: sc,
      scriptSection: sec,
      seqKey: hier.seqKey,
      seqTitle: hier.seqTitle,
      groupKey: hier.groupKey,
      groupTitle: hier.groupTitle,
      imageTake,
      videoTake,
      dialogueAudio,
      camRef,
      clpEntities,
      plannedDur,
      audioDur,
    };
  });
}

async function initProjects() {
  const res = await fetch("/api/projects");
  const projects = await res.json();
  projects.sort((a, b) => (b.scene_count > 0) - (a.scene_count > 0) || a.project_id.localeCompare(b.project_id));
  selProject.innerHTML = "";
  for (const p of projects) {
    const opt = document.createElement("option");
    opt.value = p.project_id;
    opt.textContent = `${p.project_id} (${p.scene_count ? `${p.scene_count} 鏡` : "尚未分鏡"})`;
    if (p.project_id === projectId) opt.selected = true;
    selProject.appendChild(opt);
  }
  await loadProject(projectId);
}

async function loadProject(pid) {
  stopPlayback();
  projectId = pid;
  backToBoard.href = `/p/${encodeURIComponent(projectId)}`;
  const url = new URL(location.href);
  url.searchParams.set("project", projectId);
  history.replaceState(null, "", url);

  const res = await fetch(`/api/project/${encodeURIComponent(projectId)}/state`);
  boardState = await res.json();
  allShots = buildShotsFromState(boardState);
  populateHierarchySelectors();
}

function populateHierarchySelectors() {
  const seqMap = new Map();
  for (const sh of allShots) {
    if (!seqMap.has(sh.seqKey)) seqMap.set(sh.seqKey, sh.seqTitle);
  }
  selSeq.innerHTML = `<option value="ALL">全部幕 (${allShots.length} 鏡)</option>`;
  for (const [k, title] of seqMap.entries()) {
    const count = allShots.filter((s) => s.seqKey === k).length;
    const opt = document.createElement("option");
    opt.value = k;
    opt.textContent = `${title} (${count} 鏡)`;
    selSeq.appendChild(opt);
  }
  updateSceneGroupSelector();
}

function updateSceneGroupSelector() {
  const seqVal = selSeq.value;
  const baseShots = seqVal === "ALL" ? allShots : allShots.filter((s) => s.seqKey === seqVal);

  const groupMap = new Map();
  for (const sh of baseShots) {
    if (!groupMap.has(sh.groupKey)) groupMap.set(sh.groupKey, sh.groupTitle);
  }

  selSceneGroup.innerHTML = `<option value="ALL">全部場 (${baseShots.length} 鏡)</option>`;
  for (const [gk, gtitle] of groupMap.entries()) {
    const count = baseShots.filter((s) => s.groupKey === gk).length;
    const opt = document.createElement("option");
    opt.value = gk;
    opt.textContent = `${gtitle} (${count} 鏡)`;
    selSceneGroup.appendChild(opt);
  }
  if (groupMap.size === 1) {
    selSceneGroup.value = [...groupMap.keys()][0];
  }
  applyFilter();
}

function applyFilter() {
  stopPlayback();
  const seqVal = selSeq.value;
  const grpVal = selSceneGroup.value;
  filteredShots = allShots.filter((s) => {
    if (seqVal !== "ALL" && s.seqKey !== seqVal) return false;
    if (grpVal !== "ALL" && s.groupKey !== grpVal) return false;
    return true;
  });
  currentIndex = 0;
  renderFilmstrip();
  renderCurrentShot();
}

function getShotSubtitleData(sh) {
  const actions = sh.scene.character_actions || [];
  const withDiag = actions.filter((a) => a.dialogue);
  const speakers = withDiag.map((a) => `${a.character_id}${a.emotion ? ` (${a.emotion})` : ""}`).join(" / ");
  const text = withDiag.map((a) => a.dialogue).join(" ") || sh.scriptSection.text || "";
  return { speakers: speakers || sh.scriptSection.speaker_directions || "", text };
}

function renderViewport(sh) {
  viewport.innerHTML = "";
  viewport.classList.remove("split-view");
  activeVideoEl = null;

  if (!sh) {
    viewport.innerHTML = `<div style="color:var(--text-3);font-family:var(--mono)">此專案尚無 scene_plan 分鏡資料</div>`;
    return;
  }

  const sub = getShotSubtitleData(sh);
  let statusNotice = "";

  if (visualMode === "video") {
    if (sh.videoTake) {
      const vid = document.createElement("video");
      vid.src = mediaUrl(sh.videoTake.path);
      vid.playsInline = true;
      vid.controls = false;
      vid.muted = audioMode !== "video";
      viewport.appendChild(vid);
      activeVideoEl = vid;
      statusNotice = `🎞 影片 · ${sh.videoTake.path.split("/").pop()}`;
    } else {
      statusNotice = `⚠ 本鏡尚無完成影片，自動以圖像代用`;
      appendImageStage(sh, true);
    }
  } else {
    appendImageStage(sh, false);
  }

  if (statusNotice) {
    const pill = document.createElement("div");
    pill.className = `status-pill${statusNotice.startsWith("⚠") ? " warn" : ""}`;
    pill.textContent = statusNotice;
    viewport.appendChild(pill);
  }

  if (sub.text) {
    const overlay = document.createElement("div");
    overlay.className = "sub-overlay";
    overlay.innerHTML = `
      ${sub.speakers ? `<div class="sub-speaker">${escapeHtml(sub.speakers)}</div>` : ""}
      <div class="sub-text">${escapeHtml(sub.text)}</div>
    `;
    viewport.appendChild(overlay);
  }

  const playHint = document.createElement("div");
  playHint.className = "play-overlay";
  playHint.innerHTML = `<span>▶ 點擊畫面 / 按空白鍵播放毛片</span>`;
  viewport.appendChild(playHint);
}

function appendImageStage(sh, isFallback) {
  const sbPath = sh.imageTake ? sh.imageTake.path : null;
  const camPath = sh.camRef && sh.camRef.path ? sh.camRef.path : null;

  if (imgMode === "split" && !isFallback) {
    viewport.classList.add("split-view");
    viewport.appendChild(makeImagePane(sbPath, "分鏡圖 (Storyboard)", sh.id));
    viewport.appendChild(makeImagePane(camPath, "Camera 視角圖 / 白模", sh.id));
    return;
  }

  if (imgMode === "camera") {
    const pane = makeImagePane(camPath, "Camera 視角圖 / 白模", sh.id);
    while (pane.firstChild) viewport.appendChild(pane.firstChild);
  } else {
    const chosen = sbPath || camPath;
    const badge = sbPath ? "分鏡圖 (Storyboard)" : camPath ? "分鏡圖未產出 · 暫代 Camera 視角圖" : "尚無圖像";
    const pane = makeImagePane(chosen, badge, sh.id);
    while (pane.firstChild) viewport.appendChild(pane.firstChild);
  }
}

function makeImagePane(relPath, badgeText, shotId) {
  const wrap = document.createElement("div");
  wrap.className = "split-pane";
  if (relPath) {
    const img = document.createElement("img");
    img.src = mediaUrl(relPath);
    img.alt = shotId;
    wrap.appendChild(img);
  } else {
    const empty = document.createElement("div");
    empty.style.cssText = "color:var(--text-3);font-family:var(--mono);font-size:12px;padding:16px;text-align:center";
    empty.textContent = `[${shotId}] 尚無 ${badgeText}`;
    wrap.appendChild(empty);
  }
  const badge = document.createElement("div");
  badge.className = "pane-badge";
  badge.textContent = `${shotId} · ${badgeText}`;
  wrap.appendChild(badge);
  return wrap;
}

function renderFilmstrip() {
  filmstrip.innerHTML = "";
  filteredShots.forEach((sh, idx) => {
    const chip = document.createElement("div");
    chip.className = `shot-chip${idx === currentIndex ? " active" : ""}`;
    const thumbPath = (sh.imageTake && sh.imageTake.path) || (sh.camRef && sh.camRef.path) || "";
    const hasImg = Boolean(sh.imageTake);
    const hasCam = Boolean(sh.camRef && sh.camRef.path);
    const hasAud = Boolean(sh.dialogueAudio);
    const hasVid = Boolean(sh.videoTake);

    chip.innerHTML = `
      <div class="shot-chip-thumb">
        ${thumbPath ? `<img src="${mediaUrl(thumbPath)}" loading="lazy">` : sh.id}
      </div>
      <div class="shot-chip-head">
        <span>${escapeHtml(sh.id.replace(/^shot_/, ""))}</span>
        <span style="color:var(--text-2)">${(sh.audioDur || sh.plannedDur).toFixed(1)}s</span>
      </div>
      <div class="shot-chip-badges">
        <span class="b-tag ${hasAud ? "ok" : ""}" title="對白音檔">AUD</span>
        <span class="b-tag ${hasImg ? "ok" : ""}" title="分鏡圖">IMG</span>
        <span class="b-tag ${hasCam ? "ok" : ""}" title="Camera 視角圖">CAM</span>
        <span class="b-tag ${hasVid ? "ok" : ""}" title="影片">VID</span>
      </div>
    `;
    chip.onclick = () => {
      stopPlayback();
      currentIndex = idx;
      renderCurrentShot();
      startPlayback();
    };
    filmstrip.appendChild(chip);
  });
}

function renderInspector(sh) {
  if (!sh) {
    inspector.innerHTML = "";
    return;
  }
  const sc = sh.scene;
  const sec = sh.scriptSection;
  const sl = sc.shot_language || {};
  const delta = sh.audioDur != null ? (sh.audioDur - sh.plannedDur) : 0;
  const deltaWarn = Math.abs(delta) > 0.5;

  const actionsHtml = (sc.character_actions || []).map((ca) => `
    <div style="margin-bottom:6px;padding:6px 8px;background:var(--panel-2);border-radius:5px;border:1px solid var(--border)">
      <div style="font-family:var(--mono);font-size:11.5px;color:var(--amber)">
        ${escapeHtml(ca.character_id)} · emotion: ${escapeHtml(ca.emotion || "-")} ${ca.target ? `→ ${escapeHtml(ca.target)}` : ""}
      </div>
      <div style="font-family:var(--mono);font-size:11px;color:var(--text-2);margin:2px 0">
        動作: ${(ca.action_sequence || []).map(escapeHtml).join(" → ")}
      </div>
      ${ca.dialogue ? `<div style="color:var(--text);font-weight:600;margin-top:3px">「${escapeHtml(ca.dialogue)}」</div>` : ""}
      ${ca.notes ? `<div style="color:var(--text-3);font-size:11.5px;margin-top:2px">註：${escapeHtml(ca.notes)}</div>` : ""}
    </div>
  `).join("");

  const audioInfo = sh.dialogueAudio
    ? `<span class="mono-path">${escapeHtml(sh.dialogueAudio.path)}</span><br><span style="color:var(--text-2)">來源: ${escapeHtml(sh.dialogueAudio.source_tool || "imported")} · 實測 ${sh.audioDur}s</span>`
    : `<span style="color:var(--text-3)">無對白音檔</span>`;

  const imgInfo = sh.imageTake
    ? `<span class="mono-path">${escapeHtml(sh.imageTake.path)}</span><br><span style="color:var(--text-2)">來源: ${escapeHtml(sh.imageTake.provider || sh.imageTake.source_tool || "-")} · ${escapeHtml(sh.imageTake.resolution || "")}</span>`
    : `<span style="color:var(--text-3)">尚未登記確認採用之分鏡圖</span>`;

  const camInfo = sh.camRef
    ? `${sh.camRef.path ? `<span class="mono-path">${escapeHtml(sh.camRef.path)}</span><br>` : `<span style="color:var(--amber)">[待生成 source=${escapeHtml(sh.camRef.source || "generate")}]</span><br>`}<span style="color:var(--text-2)">${escapeHtml(sh.camRef.description || "")}</span>`
    : `<span style="color:var(--text-3)">本鏡無指定 camera_ref</span>`;

  const vidInfo = sh.videoTake
    ? `<span class="mono-path">${escapeHtml(sh.videoTake.path)}</span>`
    : `<span style="color:var(--text-3)">尚未產出獨立影片</span>`;

  const clpHtml = sh.clpEntities.map((e) => {
    const img = (e.reference_images || [])[0];
    return `
      <div class="clp-pill">
        ${img ? `<img src="${mediaUrl(img)}">` : ""}
        <span><b>${escapeHtml(e.name || e.id)}</b> <span style="color:var(--text-3);font-family:var(--mono)">(${escapeHtml(e.id)})</span></span>
      </div>
    `;
  }).join("");

  const inferredStages = [...(sc.render_stages || [])];
  for (const t of [sh.imageTake, sh.videoTake]) {
    const m = t && t.generation_summary && t.generation_summary.match(/\b(T2I|I2I|R2I|W2I|T2V|I2V|R2V|W2V)\b/);
    if (m && !inferredStages.includes(m[1])) inferredStages.push(m[1]);
  }
  const recipeText = inferredStages.join(" → ") || "未指定";

  const renderPromptBox = (label, take, active) => {
    if (!take) return "";
    const meta = [take.provider, take.model, take.source_tool].filter(Boolean).join(" / ");
    return `
      <div style="margin-bottom:8px;padding:8px 10px;background:var(--panel-2);border-radius:6px;border:1px solid ${active ? "var(--accent)" : "var(--border)"}">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:4px">
          <span style="font-size:12px;font-weight:700;color:${active ? "#93c5fd" : "var(--text)"}">${label}${meta ? ` <span style="font-family:var(--mono);font-weight:400;font-size:11px;color:var(--text-2)">(${escapeHtml(meta)})</span>` : ""}</span>
          ${take.prompt ? `<button type="button" class="btn-copy-prompt" data-prompt="${escapeHtml(take.prompt)}" style="background:var(--panel);color:var(--text-2);border:1px solid var(--border);border-radius:4px;padding:2px 8px;font-size:11px;cursor:pointer">📋 複製 Prompt</button>` : ""}
        </div>
        ${take.generation_summary ? `<div style="font-family:var(--mono);font-size:11px;color:var(--amber);margin-bottom:5px">${escapeHtml(take.generation_summary)}</div>` : ""}
        ${take.prompt
          ? `<div style="font-size:12px;line-height:1.55;color:var(--text);white-space:pre-wrap;background:#090b10;padding:8px 10px;border-radius:5px;border:1px solid var(--border);max-height:240px;overflow-y:auto">${escapeHtml(take.prompt)}</div>`
          : `<div style="font-size:11.5px;color:var(--text-3)">（manifest 僅記錄上方生成摘要，未另存獨立 Prompt 原文）</div>`}
      </div>
    `;
  };

  const promptBlocks = visualMode === "video"
    ? `${renderPromptBox("🎬 影片 Prompt", sh.videoTake, true)}${renderPromptBox("🖼️ 分鏡圖 Prompt", sh.imageTake, false)}`
    : `${renderPromptBox("🖼️ 分鏡圖 Prompt", sh.imageTake, true)}${renderPromptBox("🎬 影片 Prompt", sh.videoTake, false)}`;

  const ESG_MD_LINKS = {
    "shot_4.6.1": "/media/course-51-esg/artifacts/shot_4.6.1_gpt_template_v5.md",
    "shot_4.6.2": "/media/course-51-esg/artifacts/shot_4.6.2_gpt_template_v3.md",
    "shot_4.6.3": "/media/course-51-esg/artifacts/shot_4.6.3_gpt_template_v1.md",
  };
  let historyLink = "";
  if (projectId === "course-51-esg") {
    if (sh.groupKey === "2.1") {
      historyLink = `<span style="display:flex;gap:6px"><button type="button" class="btn-md-link" data-md-url="/media/course-51-esg/artifacts/image_generation_history.md" style="background:rgba(245,158,11,0.12);color:var(--amber);border:1px solid rgba(245,158,11,0.35);border-radius:4px;padding:1px 7px;font-size:11px;cursor:pointer">📄 生圖歷史索引</button><button type="button" class="btn-md-link" data-md-url="/media/course-51-esg/artifacts/shot_prompts_2_1_banana21.md" style="background:rgba(59,130,246,0.12);color:#93c5fd;border:1px solid rgba(59,130,246,0.35);border-radius:4px;padding:1px 7px;font-size:11px;cursor:pointer">📄 W2I 原紀錄</button></span>`;
    } else if (ESG_MD_LINKS[sh.id]) {
      historyLink = `<button type="button" class="btn-md-link" data-md-url="${ESG_MD_LINKS[sh.id]}" style="background:rgba(245,158,11,0.12);color:var(--amber);border:1px solid rgba(245,158,11,0.35);border-radius:4px;padding:1px 7px;font-size:11px;cursor:pointer">📄 試生 Prompt 紀錄 (.md)</button>`;
    }
  }

  inspector.innerHTML = `
    <div class="info-card">
      <h3>
        <span>5A. 鏡頭規格與秒數核對</span>
        <span style="color:var(--text)">${escapeHtml(sh.id)}</span>
      </h3>
      <div class="kv-grid">
        <div class="kv-k">所屬幕 / 場</div>
        <div class="kv-v">${escapeHtml(sh.seqTitle)} · ${escapeHtml(sh.groupTitle)}</div>
        <div class="kv-k">時間槽與秒數</div>
        <div class="kv-v" style="font-family:var(--mono)">
          規劃 ${sh.plannedDur.toFixed(2)}s (${Number(sc.start_seconds || 0).toFixed(2)}s – ${Number(sc.end_seconds || 0).toFixed(2)}s)
          ${sh.audioDur != null ? ` · 音檔 <b>${sh.audioDur.toFixed(2)}s</b> <span style="color:${deltaWarn ? "var(--amber)" : "var(--green)"}">(Δ ${delta >= 0 ? "+" : ""}${delta.toFixed(2)}s)</span>` : ""}
        </div>
        <div class="kv-k">製作配方</div>
        <div class="kv-v" style="font-family:var(--mono)">${escapeHtml(recipeText)} · ${escapeHtml(sc.narrative_role || "")}</div>
        <div class="kv-k">攝影機語言</div>
        <div class="kv-v" style="font-family:var(--mono)">
          景別: ${escapeHtml(sl.shot_size || "-")} · 運鏡: ${escapeHtml(sl.camera_movement || "-")} · 焦距: ${sl.lens_mm ? sl.lens_mm + "mm" : "依描述"} · 景深: ${escapeHtml(sl.depth_of_field || "-")}
        </div>
        <div class="kv-k">分鏡意圖</div>
        <div class="kv-v">${escapeHtml(sc.shot_intent || "-")}</div>
        ${sc.information_role ? `<div class="kv-k">資訊角色</div><div class="kv-v">${escapeHtml(sc.information_role)}</div>` : ""}
      </div>
    </div>

    <div class="info-card">
      <h3><span>5B. 對白與表演動作</span></h3>
      ${actionsHtml || `<div style="color:var(--text)">${escapeHtml(sec.text || "（無角色對白）")}</div>`}
      ${sec.speaker_directions ? `<div style="margin-top:6px;font-size:12px;color:var(--text-2)"><b>劇本動作指示：</b>${escapeHtml(sec.speaker_directions)}</div>` : ""}
    </div>

    <div class="info-card">
      <h3><span>5C. 畫面與構圖描述 (Scene Description)</span></h3>
      <div style="font-size:12.5px;color:var(--text);white-space:pre-wrap">${escapeHtml(
        String(sc.description || "").replace(/\s*(Subject:|Scene:|Framing:|Camera:|Motion:)/g, "\n$1").trim()
      )}</div>
    </div>

    <div class="info-card">
      <h3>
        <span>5D. 圖像 / 影片生成 Prompt</span>
        ${historyLink}
      </h3>
      ${promptBlocks || `<div style="color:var(--text-3);font-size:12px">尚未登記確認採用之圖像或影片素材${ESG_MD_LINKS[sh.id] ? `（已自動載入下方試生 Prompt 紀錄 .md）` : `（待依上方 5A 製作配方與 5C 畫面描述生成）`}</div>`}
      <div id="mdDrawer" style="display:none;margin-top:8px;padding:8px 10px;background:#090b10;border:1px solid rgba(245,158,11,0.45);border-radius:5px;font-size:11.5px;line-height:1.5;color:var(--text);white-space:pre-wrap;max-height:280px;overflow-y:auto"></div>
    </div>

    <div class="info-card">
      <h3><span>5E. 素材來源與 CLP 綁定</span></h3>
      <div class="kv-grid">
        <div class="kv-k">對白音檔</div>
        <div class="kv-v">${audioInfo}</div>
        <div class="kv-k">分鏡圖</div>
        <div class="kv-v">${imgInfo}</div>
        <div class="kv-k">Camera 視角圖</div>
        <div class="kv-v">${camInfo}</div>
        <div class="kv-k">完成影片</div>
        <div class="kv-v">${vidInfo}</div>
      </div>
      ${clpHtml ? `<div class="clp-row">${clpHtml}</div>` : ""}
    </div>
  `;

  inspector.querySelectorAll(".btn-copy-prompt").forEach((btn) => {
    btn.onclick = () => {
      navigator.clipboard.writeText(btn.dataset.prompt || "");
      const old = btn.textContent;
      btn.textContent = "✓ 已複製";
      setTimeout(() => { btn.textContent = old; }, 1200);
    };
  });

  const mdDrawer = document.getElementById("mdDrawer");
  const toggleMd = async (url) => {
    if (!mdDrawer || !url) return;
    if (mdDrawer.style.display === "block" && mdDrawer.dataset.url === url) {
      mdDrawer.style.display = "none";
      mdDrawer.dataset.url = "";
      return;
    }
    mdDrawer.textContent = "載入中...";
    mdDrawer.dataset.url = url;
    mdDrawer.style.display = "block";
    const r = await fetch(url);
    mdDrawer.textContent = r.ok ? await r.text() : `無法讀取 ${url}`;
  };
  inspector.querySelectorAll(".btn-md-link").forEach((btn) => {
    btn.onclick = () => toggleMd(btn.dataset.mdUrl);
  });
  if (!promptBlocks && projectId === "course-51-esg" && ESG_MD_LINKS[sh.id]) {
    toggleMd(ESG_MD_LINKS[sh.id]);
  }
}

function renderCurrentShot() {
  const sh = filteredShots[currentIndex] || null;
  lblShotCounter.textContent = filteredShots.length ? `鏡頭 ${currentIndex + 1} / ${filteredShots.length} (${sh.id})` : "0 / 0";
  const totalDur = sh ? (sh.audioDur || sh.plannedDur) : 0;
  lblShotTime.textContent = `0.00s / ${totalDur.toFixed(2)}s`;
  progressFill.style.width = "0%";

  Array.from(filmstrip.children).forEach((el, i) => {
    el.classList.toggle("active", i === currentIndex);
    if (i === currentIndex) el.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
  });

  renderViewport(sh);
  renderInspector(sh);
}

function startPlayback() {
  const sh = filteredShots[currentIndex];
  if (!sh) return;
  stopPlayback();
  isPlaying = true;
  document.body.classList.add("is-playing");
  btnPlay.textContent = "⏸ 暫停";

  const useVideoAudio = audioMode === "video" && activeVideoEl;
  const useDialogueAudio = !useVideoAudio && sh.dialogueAudio;

  if (activeVideoEl) {
    activeVideoEl.currentTime = 0;
    activeVideoEl.muted = !useVideoAudio;
    activeVideoEl.play().catch(() => {});
  }

  if (useVideoAudio) {
    activeVideoEl.ontimeupdate = () => {
      const d = activeVideoEl.duration || sh.plannedDur;
      const c = activeVideoEl.currentTime || 0;
      progressFill.style.width = `${Math.min(100, (c / d) * 100)}%`;
      lblShotTime.textContent = `${c.toFixed(2)}s / ${d.toFixed(2)}s (影片原音)`;
    };
    activeVideoEl.onended = () => onShotEnded();
    return;
  }

  if (useDialogueAudio) {
    audioEl.src = mediaUrl(sh.dialogueAudio.path);
    audioEl.ontimeupdate = () => {
      const d = audioEl.duration || sh.audioDur || sh.plannedDur;
      const c = audioEl.currentTime || 0;
      progressFill.style.width = `${Math.min(100, (c / d) * 100)}%`;
      lblShotTime.textContent = `${c.toFixed(2)}s / ${d.toFixed(2)}s`;
    };
    audioEl.onended = () => onShotEnded();
    audioEl.play().catch(() => startFallbackTimer(sh.plannedDur));
    return;
  }

  startFallbackTimer(sh.plannedDur);
}

function startFallbackTimer(duration) {
  fallbackDuration = Math.max(0.5, duration || 5);
  fallbackElapsed = 0;
  fallbackTimer = setInterval(() => {
    fallbackElapsed += 0.05;
    const pct = Math.min(100, (fallbackElapsed / fallbackDuration) * 100);
    progressFill.style.width = `${pct}%`;
    lblShotTime.textContent = `${fallbackElapsed.toFixed(2)}s / ${fallbackDuration.toFixed(2)}s (計時預覽)`;
    if (fallbackElapsed >= fallbackDuration) {
      onShotEnded();
    }
  }, 50);
}

function stopPlayback() {
  isPlaying = false;
  document.body.classList.remove("is-playing");
  btnPlay.textContent = "▶ 播放毛片";
  if (fallbackTimer) {
    clearInterval(fallbackTimer);
    fallbackTimer = null;
  }
  audioEl.pause();
  audioEl.ontimeupdate = null;
  audioEl.onended = null;
  if (activeVideoEl) {
    activeVideoEl.pause();
    activeVideoEl.ontimeupdate = null;
    activeVideoEl.onended = null;
  }
}

function onShotEnded() {
  stopPlayback();
  progressFill.style.width = "100%";
  if (chkAutoAdvance.checked && currentIndex + 1 < filteredShots.length) {
    currentIndex += 1;
    renderCurrentShot();
    startPlayback();
  }
}

function escapeHtml(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// Event bindings
selProject.onchange = () => loadProject(selProject.value);
selSeq.onchange = () => updateSceneGroupSelector();
selSceneGroup.onchange = () => applyFilter();

document.querySelectorAll("[data-audio-mode]").forEach((btn) => {
  btn.onclick = () => {
    document.querySelectorAll("[data-audio-mode]").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    audioMode = btn.dataset.audioMode;
    const wasPlaying = isPlaying;
    stopPlayback();
    renderCurrentShot();
    if (wasPlaying) startPlayback();
  };
});

document.querySelectorAll("[data-visual-mode]").forEach((btn) => {
  btn.onclick = () => {
    document.querySelectorAll("[data-visual-mode]").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    visualMode = btn.dataset.visualMode;
    const wasPlaying = isPlaying;
    stopPlayback();
    renderCurrentShot();
    if (wasPlaying) startPlayback();
  };
});

document.querySelectorAll("[data-img-mode]").forEach((btn) => {
  btn.onclick = () => {
    document.querySelectorAll("[data-img-mode]").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    imgMode = btn.dataset.imgMode;
    renderViewport(filteredShots[currentIndex]);
  };
});

btnPrev.onclick = () => {
  if (currentIndex > 0) {
    const wasPlaying = isPlaying;
    stopPlayback();
    currentIndex -= 1;
    renderCurrentShot();
    if (wasPlaying) startPlayback();
  }
};

btnNext.onclick = () => {
  if (currentIndex + 1 < filteredShots.length) {
    const wasPlaying = isPlaying;
    stopPlayback();
    currentIndex += 1;
    renderCurrentShot();
    if (wasPlaying) startPlayback();
  }
};

btnPlay.onclick = () => {
  if (isPlaying) stopPlayback();
  else startPlayback();
};

viewport.onclick = () => btnPlay.click();

window.addEventListener("keydown", (e) => {
  if (e.target.tagName === "SELECT" || e.target.tagName === "INPUT") return;
  if (e.code === "Space") {
    e.preventDefault();
    btnPlay.click();
  } else if (e.code === "ArrowLeft") {
    e.preventDefault();
    btnPrev.click();
  } else if (e.code === "ArrowRight") {
    e.preventDefault();
    btnNext.click();
  }
});

initProjects();
