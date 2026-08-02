/* GC Minimal Zine Poster — Album viewer
   Reads ../posters/index.json and renders a contact sheet + detail view. */

const SRC = "../posters/index.json";
const IMG_BASE = "../posters/";

let POSTERS = [];
let SERIES = {};        // series key -> { label, label_zh, note }
let CHAPTERS = [];      // [{ season, label, label_zh, cover, pages[] }]
let VIEW = [];          // currently filtered ids (in order)
let cursor = -1;        // index into VIEW
let filter = { key: null, val: null };
let plates = false;     // show the captioned edition where one exists

// The captioned edition is the sheet as it leaves the studio: title, Chinese
// title and note printed on the paper below the plate, so a set can be handed
// to someone without this viewer around it.
const srcOf = (p) => IMG_BASE + (plates && p.plate ? p.plate : p.file);

const $ = (s) => document.querySelector(s);
const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );

/* ---------------- load ---------------- */
init();

async function init() {
  try {
    const res = await fetch(SRC, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    POSTERS = data.posters || [];
    SERIES = data.series || {};
    CHAPTERS = data.chapters || [];
  } catch (e) {
    $("#err").innerHTML =
      `<div class="err">无法读取 <b>${esc(SRC)}</b>（${esc(e.message)}）。<br><br>` +
      `这个图册需要通过 HTTP 打开，直接双击 file:// 会被浏览器的同源策略拦住。<br>` +
      `请在仓库根目录运行 <b>python3 -m http.server 8080</b>，然后访问 <b>/album/</b>。</div>`;
    return;
  }
  $("#m-count").textContent = String(POSTERS.length).padStart(2, "0");

  // ?series=seasons opens straight into that album, so a chapter is linkable.
  const want = new URLSearchParams(location.search).get("series");
  if (new URLSearchParams(location.search).get("plates") === "1") plates = true;
  if (want && POSTERS.some((p) => (p.series || "singles") === want)) {
    filter = { key: "series", val: want };
  }

  buildFilters();
  apply();
  wireGlobal();
}

/* ---------------- filters ---------------- */
function buildFilters() {
  const layouts = [...new Set(POSTERS.map((p) => p.recipe.layout))].sort();
  const moods = [...new Set(POSTERS.map((p) => p.recipe.mood))].sort();

  const box = $("#filters");
  box.innerHTML = "";

  const addLabel = (t) => {
    const s = document.createElement("span");
    s.className = "flabel";
    s.textContent = t;
    box.appendChild(s);
  };
  const addChip = (label, key, val, swatch) => {
    const b = document.createElement("button");
    b.className = "chip";
    b.type = "button";
    b.innerHTML =
      (swatch ? `<span class="sw" style="background:${esc(swatch)}"></span>` : "") +
      esc(label);
    b.setAttribute("aria-pressed", String(filter.key === key && filter.val === val));
    b.onclick = () => {
      filter =
        filter.key === key && filter.val === val ? { key: null, val: null } : { key, val };
      const url = new URL(location.href);
      if (filter.key === "series") url.searchParams.set("series", filter.val);
      else url.searchParams.delete("series");
      history.replaceState(null, "", url);
      buildFilters();
      apply();
    };
    box.appendChild(b);
  };

  addLabel("all");
  addChip(`全部 ${POSTERS.length}`, null, null);

  // The Seasons set is a bound album, not a pile of singles: read it in order.
  if (CHAPTERS.length) {
    const n = POSTERS.filter((p) => p.series === "seasons").length;
    addLabel("album");
    addChip(`Seasons 影集 ${n}`, "series", "seasons");
  }

  const captioned = POSTERS.filter((p) => p.plate).length;
  if (captioned) {
    addLabel("edition");
    const b = document.createElement("button");
    b.className = "chip toggle";
    b.type = "button";
    b.textContent = `题注版 ${captioned}`;
    b.title = "把标题与介绍印在纸上的版本";
    b.setAttribute("aria-pressed", String(plates));
    b.addEventListener("click", () => {
      plates = !plates;
      const url = new URL(location.href);
      if (plates) url.searchParams.set("plates", "1");
      else url.searchParams.delete("plates");
      history.replaceState(null, "", url);
      buildFilters();
      renderSheet();
      if (cursor >= 0) open(cursor);
    });
    box.appendChild(b);
  }

  // A series is a set made to one locked recipe, so it is worth isolating.
  const seriesKeys = [...new Set(POSTERS.map((p) => p.series || "singles"))]
    .filter((k) => !(CHAPTERS.length && k === "seasons"))
    .sort();
  if (seriesKeys.length) {
    addLabel("series");
    seriesKeys.forEach((k) => {
      const meta = SERIES[k] || {};
      const n = POSTERS.filter((p) => (p.series || "singles") === k).length;
      addChip(`${meta.label || k} ${n}`, "series", k);
    });
  }

  addLabel("layout");
  layouts.forEach((l) => addChip(l, "layout", l));

  addLabel("mood");
  moods.forEach((m) => addChip(m, "mood", m));

  addLabel("accent");
  POSTERS.forEach((p) =>
    addChip(p.recipe.accent.replace(/^saturated\s+/, ""), "id", p.id, p.accent_hex)
  );

  const c = document.createElement("span");
  c.className = "count";
  c.id = "shown";
  box.appendChild(c);
}

function chaptered() {
  return filter.key === "series" && filter.val === "seasons" && CHAPTERS.length > 0;
}

/* Reading order for a chaptered set: each season's cover, then its pages. */
function albumOrder(list) {
  const byId = new Map(list.map((p) => [p.id, p]));
  const out = [];
  CHAPTERS.forEach((ch) => {
    [ch.cover, ...(ch.pages || [])].forEach((id) => {
      if (byId.has(id)) {
        out.push(byId.get(id));
        byId.delete(id);
      }
    });
  });
  return out.concat([...byId.values()]);   // anything unfiled still shows up
}

function apply() {
  VIEW = POSTERS.filter((p) => {
    if (!filter.key) return true;
    if (filter.key === "id") return p.id === filter.val;
    if (filter.key === "series") return (p.series || "singles") === filter.val;
    return p.recipe[filter.key] === filter.val;
  });
  if (chaptered()) VIEW = albumOrder(VIEW);
  const shown = $("#shown");
  if (shown) shown.textContent = `${VIEW.length} / ${POSTERS.length} sheets`;
  renderSheet();
}

/* ---------------- contact sheet ---------------- */
function renderSheet() {
  const sheet = $("#sheet");
  sheet.innerHTML = "";
  const chap = chaptered();
  sheet.classList.toggle("chaptered", chap);
  let grid = null;

  VIEW.forEach((p, i) => {
    if (chap && p.role === "cover") {
      const ch = CHAPTERS.find((c) => c.season === p.season) || {};
      const head = document.createElement("div");
      head.className = "chapter";
      head.innerHTML =
        `<span class="cn">${esc(ch.label || p.season)}</span>` +
        `<span class="cz">${esc(ch.label_zh || "")}</span>` +
        `<span class="cc">${1 + (ch.pages || []).length} sheets</span>`;
      sheet.appendChild(head);
      grid = document.createElement("div");
      grid.className = "grid";
      sheet.appendChild(grid);
    }

    const b = document.createElement("button");
    b.className = "card" + (chap && p.role === "cover" ? " is-cover" : "");
    b.type = "button";
    b.innerHTML = `
      <div class="frame"><img src="${esc(srcOf(p))}" alt="${esc(p.title)}" loading="lazy"></div>
      <div class="cap">
        <div class="n">no. ${String(p.id).padStart(2, "0")}${
          p.series && p.series !== "singles"
            ? ` <span class="badge">${esc(
                p.season
                  ? (SERIES[p.series] || {}).label +
                      " · " +
                      p.season +
                      (p.role === "cover" ? " · cover" : "")
                  : (SERIES[p.series] || {}).label || p.series
              )}</span>`
            : ""
        }</div>
        <div class="t">${esc(p.title)}</div>
        <div class="r"><span class="sw" style="background:${esc(p.accent_hex)}"></span>${esc(
      p.recipe.layout
    )} · ${esc(p.recipe.mood)}</div>
      </div>`;
    b.onclick = () => open(i);
    (chap && grid ? grid : sheet).appendChild(b);
  });
}

/* ---------------- detail ---------------- */
function open(i) {
  cursor = (i + VIEW.length) % VIEW.length;
  const p = VIEW[cursor];
  const r = p.recipe;

  $("#detail").innerHTML = `
    <div class="plate"><img src="${esc(srcOf(p))}" alt="${esc(p.title)}"></div>
    <div class="info">
      <div class="kicker">sheet no. ${String(p.id).padStart(2, "0")}${
        p.series && p.series !== "singles"
          ? ` &nbsp;·&nbsp; ${esc((SERIES[p.series] || {}).label || p.series)}${
              p.season ? ` ${esc(p.season)}${p.role === "cover" ? " cover" : ""}` : ""
            }`
          : ""
      } &nbsp;·&nbsp; ${cursor + 1} of ${VIEW.length}</div>
      <h2>${esc(p.title)}</h2>
      ${p.title_zh && p.title_zh !== p.title ? `<div class="zh">${esc(p.title_zh)}</div>` : ""}
      <div class="recipe">
        <span class="rc accent" style="background:${esc(p.accent_hex)}">${esc(r.accent)}</span>
        <span class="rc">${esc(r.layout)}</span>
        <span class="rc">${esc(r.anchor)}</span>
        <span class="rc">${esc(r.typography)}</span>
        <span class="rc">${esc(r.texture)}</span>
        <span class="rc">${esc(r.mood)}</span>
      </div>
      <p class="note">${esc(p.note)}</p>
      ${
        p.series && p.series !== "singles" && (SERIES[p.series] || {}).note
          ? `<p class="note series-note">${esc(SERIES[p.series].note)}</p>`
          : ""
      }
      <div class="src">source · ${esc(p.source)}</div>
      <h3 class="sec">final prompt</h3>
      <pre class="prompt" id="pr">${esc(p.prompt)}</pre>
      <div class="acts">
        <button class="btn" id="copy">复制 prompt</button>
        <a class="btn" href="${esc(srcOf(p))}" download>下载${
          plates && p.plate ? "题注版" : "图片"
        }</a>
        ${
          /* both editions are downloadable without flipping the switch first,
             because the download is what leaves the site */
          p.plate
            ? `<a class="btn ghost" href="${esc(IMG_BASE + (plates ? p.file : p.plate))}" download>${
                plates ? "下载无字原图" : "下载题注版"
              }</a>`
            : ""
        }
      </div>
    </div>`;

  $("#copy").onclick = async (e) => {
    try {
      await navigator.clipboard.writeText(p.prompt);
      e.target.textContent = "已复制 ✓";
    } catch {
      e.target.textContent = "复制失败，请手动选取";
    }
    setTimeout(() => (e.target.textContent = "复制 prompt"), 1800);
  };

  $("#veil").classList.add("on");
  document.body.style.overflow = "hidden";
  $("#veil").scrollTop = 0;
}

function close() {
  $("#veil").classList.remove("on");
  document.body.style.overflow = "";
  cursor = -1;
}

/* ---------------- wiring ---------------- */
function wireGlobal() {
  $("#close").onclick = close;
  $("#prev").onclick = () => open(cursor - 1);
  $("#next").onclick = () => open(cursor + 1);
  $("#veil").addEventListener("click", (e) => {
    if (e.target.id === "veil") close();
  });
  document.addEventListener("keydown", (e) => {
    if (cursor < 0) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowLeft") open(cursor - 1);
    else if (e.key === "ArrowRight") open(cursor + 1);
  });
}
