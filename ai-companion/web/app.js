const STORAGE_KEY = "language-landscapes-companion-threads-v1";

const state = {
  config: null,
  currentView: "landing",
  chapterCache: {},
  currentChapterId: null,
  currentPassageId: null,
  glossary: null,
  glossaryQuery: "",
  activeGlossarySlug: null,
  indexEntries: null,
  indexQuery: "",
  activeIndexId: null,
  modalSource: null,
  ask: {
    threads: [],
    activeThreadId: null,
    draft: "",
    topK: 5,
    useOpenAI: false,
    model: "",
    pending: false,
    selectedMessageId: null,
  },
  read: {
    drawerOpen: true,
    draft: "",
    pending: false,
    messages: [],
    scope: { mode: "chapter", value: null, label: "" },
    selectedMessageId: null,
  },
};

document.addEventListener("DOMContentLoaded", init);
document.addEventListener("click", handleClick);
document.addEventListener("submit", handleSubmit);
document.addEventListener("input", handleInput);

async function init() {
  try {
    const config = await fetchJSON("/api/config");
    state.config = config;
    state.ask.useOpenAI = config.openai_available;
    state.ask.model = config.default_model;
    state.currentChapterId = config.chapters[0]?.id || null;
    state.read.scope = {
      mode: "chapter",
      value: state.currentChapterId,
      label: chapterLabel(state.currentChapterId),
    };
    restoreThreads();
    render();
  } catch (error) {
    console.error(error);
    document.getElementById("view-root").innerHTML = `
      <section class="panel loading-panel">
        <p>Failed to load the local companion.</p>
        <p class="status-note">${escapeHTML(String(error))}</p>
      </section>
    `;
  }
}

async function fetchJSON(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${text}`);
  }
  return response.json();
}

function restoreThreads() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return;
    }
    const parsed = JSON.parse(raw);
    state.ask.threads = Array.isArray(parsed.threads) ? parsed.threads : [];
    state.ask.activeThreadId = parsed.activeThreadId || state.ask.threads[0]?.id || null;
  } catch (_error) {
    state.ask.threads = [];
    state.ask.activeThreadId = null;
  }
}

function persistThreads() {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      threads: state.ask.threads,
      activeThreadId: state.ask.activeThreadId,
    }),
  );
}

function ensureActiveThread(scope) {
  if (state.ask.activeThreadId && currentThread()) {
    return currentThread();
  }
  const thread = makeThread(scope || { mode: "book", value: null, label: "Whole book" });
  state.ask.threads.unshift(thread);
  state.ask.activeThreadId = thread.id;
  persistThreads();
  return thread;
}

function makeThread(scope) {
  const id = `thread-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`;
  return {
    id,
    title: "New thread",
    updatedAt: new Date().toISOString(),
    scope: scope || { mode: "book", value: null, label: "Whole book" },
    messages: [],
  };
}

function currentThread() {
  return state.ask.threads.find((thread) => thread.id === state.ask.activeThreadId) || null;
}

function activeChapterSummary() {
  return state.config?.chapters.find((chapter) => chapter.id === state.currentChapterId) || null;
}

function chapterLabel(chapterId) {
  return state.config?.chapters.find((chapter) => chapter.id === chapterId)?.title || "Whole book";
}

async function ensureChapter(chapterId) {
  if (!chapterId) {
    return null;
  }
  if (!state.chapterCache[chapterId]) {
    state.chapterCache[chapterId] = await fetchJSON(`/api/read?chapter_id=${encodeURIComponent(chapterId)}`);
  }
  return state.chapterCache[chapterId];
}

async function ensureGlossary() {
  if (!state.glossary) {
    const payload = await fetchJSON("/api/glossary");
    state.glossary = payload.entries;
    state.activeGlossarySlug = state.glossary[0]?.slug || null;
  }
}

async function ensureIndex() {
  if (!state.indexEntries) {
    const payload = await fetchJSON("/api/index");
    state.indexEntries = payload.entries;
    state.activeIndexId = state.indexEntries[0]?.id || null;
  }
}

async function openView(view) {
  state.currentView = view;
  if (view === "read" && state.currentChapterId) {
    await ensureChapter(state.currentChapterId);
  }
  if (view === "glossary") {
    await ensureGlossary();
  }
  if (view === "index") {
    await ensureIndex();
  }
  if (view === "ask") {
    ensureActiveThread();
  }
  render();
}

function render() {
  renderNav();
  renderRuntime();
  renderView();
  renderModal();
  if (state.currentView === "read" && state.currentPassageId) {
    requestAnimationFrame(() => {
      const target = document.getElementById(`passage-${state.currentPassageId}`);
      target?.scrollIntoView({ block: "nearest" });
    });
  }
}

function renderNav() {
  const nav = document.getElementById("global-nav");
  nav.innerHTML = ["read", "ask", "contents", "glossary", "index"]
    .map((view) => {
      const label = view.charAt(0).toUpperCase() + view.slice(1);
      const active = state.currentView === view ? "active" : "";
      return `<button type="button" class="nav-chip ${active}" data-action="nav" data-view="${view}">${label}</button>`;
    })
    .join("");
}

function renderRuntime() {
  const pill = document.getElementById("runtime-pill");
  if (!state.config) {
    pill.textContent = "Loading…";
    return;
  }
  const status = state.config.openai_available ? "OpenAI available" : "Retrieval only";
  pill.textContent = `${state.config.chunk_count} chunks · ${status}`;
}

function renderView() {
  const root = document.getElementById("view-root");
  if (!state.config) {
    root.innerHTML = `<section class="panel loading-panel"><p>Loading…</p></section>`;
    return;
  }

  switch (state.currentView) {
    case "read":
      root.innerHTML = renderReadView();
      break;
    case "ask":
      root.innerHTML = renderAskView();
      break;
    case "contents":
      root.innerHTML = renderContentsView();
      break;
    case "glossary":
      root.innerHTML = renderGlossaryView();
      break;
    case "index":
      root.innerHTML = renderIndexView();
      break;
    default:
      root.innerHTML = renderLandingView();
      break;
  }
}

function renderLandingView() {
  const source = state.config.landing_source;
  return `
    <section class="panel hero">
      <div class="landing-columns">
        <span class="eyebrow">A local, grounded companion to the manuscript</span>
        <h1>Read quietly.<br>Ask directly.<br>Check the source.</h1>
        <p class="body-copy">
          This companion keeps the book at the center. Use it as a calm digital reading edition,
          a threaded question surface, or a reference desk for the glossary and index.
        </p>
        <div class="hero-actions">
          <button class="primary-button" type="button" data-action="landing-start-read">Start reading</button>
          <button class="secondary-button" type="button" data-action="landing-start-ask">Ask the book</button>
        </div>
      </div>
      <div class="hero-grid">
        <section class="panel hero-card">
          <div class="eyebrow">Try a question</div>
          <div class="prompt-grid">
            ${state.config.example_prompts.map((prompt) => `
              <button type="button" class="utility-chip" data-action="landing-prompt" data-question="${escapeAttr(prompt)}">${escapeHTML(prompt)}</button>
            `).join("")}
          </div>
        </section>
        <section class="panel source-preview-card">
          <div class="eyebrow">Source preview</div>
          <h2 class="source-title">${escapeHTML(source.title)}</h2>
          <div class="source-meta">${escapeHTML(source.path.join(" > "))}</div>
          <p class="source-preview">${escapeHTML(source.preview)}</p>
          <div class="source-actions">
            <button type="button" class="secondary-button" data-action="open-source" data-chunk-id="${escapeAttr(source.chunk_id)}">Inspect source</button>
          </div>
        </section>
      </div>
    </section>
  `;
}

function renderContentsView() {
  return `
    <section class="panel hero">
      <span class="eyebrow">Contents</span>
      <h2 class="view-title">Browse the structure of the book</h2>
      <div class="contents-grid">
        ${state.config.chapters.map((chapter) => `
          <article class="chapter-card">
            <div>
              <div class="chapter-meta">Chapter ${chapter.position} · ${chapter.minutes.toFixed(1)} min · ${chapter.section_count} sections</div>
              <h3 class="source-title">${escapeHTML(chapter.title)}</h3>
            </div>
            <p class="chapter-teaser">${escapeHTML(chapter.teaser || "No teaser available yet.")}</p>
            <div class="card-actions">
              <button type="button" class="primary-button" data-action="open-chapter" data-chapter-id="${chapter.id}">Read chapter</button>
              <button type="button" class="secondary-button" data-action="ask-chapter" data-chapter-id="${chapter.id}">Ask about chapter</button>
            </div>
          </article>
        `).join("")}
      </div>
    </section>
  `;
}

function renderReadView() {
  const chapterData = state.chapterCache[state.currentChapterId];
  if (!chapterData) {
    return `<section class="panel loading-panel"><p>Loading chapter…</p></section>`;
  }

  const chapter = chapterData.chapter;
  const passages = chapterData.passages;
  const selectedSources = selectedReadSources();

  return `
    <section class="read-grid">
      <aside class="panel chapter-rail">
        <span class="eyebrow">Read</span>
        <div class="chapter-list">
          ${state.config.chapters.map((item) => `
            <button type="button" class="${item.id === chapter.id ? "active" : ""}" data-action="open-chapter" data-chapter-id="${item.id}">
              <div>${escapeHTML(item.title)}</div>
              <div class="chapter-meta">${item.minutes.toFixed(1)} min</div>
            </button>
          `).join("")}
        </div>
        <div class="reference-box">
          <div class="eyebrow">In this chapter</div>
          <div class="thread-list">
            ${chapter.toc_items.length ? chapter.toc_items.map((item) => `
              <button type="button" class="toc-jump ghost-chip" data-action="jump-passage" data-anchor="${escapeAttr(item.anchor)}">${escapeHTML(item.title)}</button>
            `).join("") : `<div class="status-note">This chapter has no subordinate section headings in the export.</div>`}
          </div>
        </div>
      </aside>

      <section class="panel reader-panel">
        <header class="reader-header">
          <div>
            <div class="eyebrow">Chapter ${chapter.position}</div>
            <h2 class="chapter-title">${escapeHTML(chapter.title)}</h2>
            <div class="chapter-meta">${chapter.minutes.toFixed(1)} minutes · ${chapter.word_count.toLocaleString()} words</div>
          </div>
          <div class="inline-actions">
            <button type="button" class="utility-chip" data-action="nav" data-view="contents">Contents</button>
            <button type="button" class="utility-chip" data-action="nav" data-view="glossary">Glossary</button>
            <button type="button" class="utility-chip" data-action="nav" data-view="ask">Ask</button>
          </div>
        </header>

        <div class="reader-body">
          ${passages.map((passage) => `
            <article class="passage ${passage.block_type === "box" ? "box" : ""} ${passage.passage_id === state.currentPassageId ? "active" : ""}" id="passage-${passage.passage_id}">
              <div class="passage-kicker">${escapeHTML(passage.path.join(" > "))}</div>
              ${passage.block_type === "chapter" ? "" : `<h3 class="passage-heading">${escapeHTML(passage.heading || passage.anchor)}</h3>`}
              <div class="passage-text">${renderRichText(passage.text)}</div>
              <div class="card-actions" style="margin-top:14px;">
                <button type="button" class="secondary-button" data-action="scope-passage" data-passage-id="${passage.passage_id}">Ask about this section</button>
                <button type="button" class="ghost-chip" data-action="open-source" data-chunk-id="${passage.chunk_ids[0]}">Inspect source</button>
              </div>
            </article>
          `).join("")}
        </div>

        <section class="guide-drawer ${state.read.drawerOpen ? "open" : "collapsed"}">
          <div class="drawer-top">
            <div>
              <div class="eyebrow">Guide</div>
              <div class="chapter-meta">Current scope: ${escapeHTML(state.read.scope.label || "Whole book")}</div>
            </div>
            <div class="inline-actions">
              <button type="button" class="ghost-chip" data-action="toggle-drawer">${state.read.drawerOpen ? "Collapse" : "Expand"}</button>
              <button type="button" class="ghost-chip" data-action="guide-to-ask">Continue in Ask</button>
            </div>
          </div>
          <div class="drawer-body">
            <div class="scope-row">
              ${renderReadScopeChips()}
            </div>
            <div class="drawer-messages">
              ${state.read.messages.length ? state.read.messages.map(renderMessageCard).join("") : `
                <div class="message assistant">
                  <div class="message-header">
                    <span class="message-role">Guide</span>
                    <span class="message-meta">Scoped to the current reading context</span>
                  </div>
                  <div class="message-body"><p>Ask about the current section, widen to the chapter, or broaden to the whole book.</p></div>
                </div>
              `}
            </div>
            ${selectedSources.length ? `
              <div class="sources-list">
                ${selectedSources.map(renderSourceCard).join("")}
              </div>
            ` : ""}
            <form id="read-form" class="composer">
              <textarea id="read-draft" class="drawer-input" placeholder="Ask about what you are reading right now.">${escapeHTML(state.read.draft)}</textarea>
              <div class="drawer-controls">
                <button type="submit" class="primary-button" ${state.read.pending ? "disabled" : ""}>${state.read.pending ? "Working…" : "Ask from Read"}</button>
                <button type="button" class="secondary-button" data-action="clear-read-guide">Clear guide</button>
              </div>
            </form>
          </div>
        </section>
      </section>
    </section>
  `;
}

function renderReadScopeChips() {
  const chapter = activeChapterSummary();
  const passage = currentChapterPassage();
  const options = [
    { mode: "chapter", value: chapter?.id, label: chapter?.title || "Chapter" },
    { mode: "book", value: null, label: "Whole book" },
  ];
  if (passage) {
    options.unshift({ mode: "passage", value: passage.passage_id, label: "This section" });
  }
  return options.map((option) => {
    const active = state.read.scope.mode === option.mode && String(state.read.scope.value || "") === String(option.value || "");
    return `<button type="button" class="scope-chip ${active ? "active" : ""}" data-action="set-read-scope" data-mode="${option.mode}" data-value="${escapeAttr(option.value || "")}">${escapeHTML(option.label)}</button>`;
  }).join("");
}

function renderAskView() {
  const thread = ensureActiveThread();
  const sources = selectedAskSources();
  return `
    <section class="ask-grid">
      <aside class="panel threads-panel">
        <div class="eyebrow">Ask</div>
        <div class="card-actions" style="margin-top:12px;">
          <button type="button" class="primary-button" data-action="new-thread">New thread</button>
        </div>
        <div class="thread-list">
          ${state.ask.threads.map((item) => `
            <button type="button" class="thread-card ${item.id === thread.id ? "active" : ""}" data-action="activate-thread" data-thread-id="${item.id}">
              <div>${escapeHTML(item.title)}</div>
              <div class="thread-meta">${escapeHTML(item.scope?.label || "Whole book")} · ${formatTimestamp(item.updatedAt)}</div>
            </button>
          `).join("")}
        </div>
      </aside>

      <section class="panel conversation-panel">
        <header class="conversation-header">
          <div class="eyebrow">Thread</div>
          <h2 class="view-title">${escapeHTML(thread.title)}</h2>
          <div class="chapter-meta">Scope: ${escapeHTML(thread.scope?.label || "Whole book")}</div>
        </header>
        <div class="conversation-body">
          ${thread.messages.length ? thread.messages.map(renderMessageCard).join("") : `
            <div class="message assistant">
              <div class="message-header">
                <span class="message-role">Guide</span>
                <span class="message-meta">No messages yet</span>
              </div>
              <div class="message-body"><p>Ask a direct question, or start from a chapter, glossary term, or index entry.</p></div>
            </div>
          `}
        </div>
        <form id="ask-form" class="composer">
          <textarea id="ask-draft" class="composer-input" placeholder="Ask a question about the book.">${escapeHTML(state.ask.draft)}</textarea>
          <div class="composer-row">
            <label class="field-inline"><input type="checkbox" id="ask-openai" ${state.ask.useOpenAI ? "checked" : ""}> Use OpenAI generation</label>
            <label class="field-inline">Model <input type="text" id="ask-model" value="${escapeAttr(state.ask.model)}"></label>
            <label class="field-inline">Top chunks <input type="number" id="ask-top-k" min="1" max="12" value="${state.ask.topK}"></label>
          </div>
          <div class="composer-row">
            <button type="submit" class="primary-button" ${state.ask.pending ? "disabled" : ""}>${state.ask.pending ? "Working…" : "Ask the book"}</button>
            ${thread.scope?.mode !== "book" ? `<button type="button" class="secondary-button" data-action="clear-thread-scope">Widen to whole book</button>` : ""}
          </div>
        </form>
      </section>

      <aside class="panel sources-panel">
        <div>
          <div class="eyebrow">Sources</div>
          <div class="chapter-meta">${sources.length ? "Click a citation to inspect the full passage." : "Sources appear here for the selected answer."}</div>
        </div>
        <div class="sources-list">
          ${sources.length ? sources.map(renderSourceCard).join("") : `<div class="empty-state">No source cards yet.</div>`}
        </div>
      </aside>
    </section>
  `;
}

function renderGlossaryView() {
  if (!state.glossary) {
    return `<section class="panel loading-panel"><p>Loading glossary…</p></section>`;
  }

  const filtered = state.glossary.filter((entry) => {
    if (!state.glossaryQuery.trim()) {
      return true;
    }
    const q = state.glossaryQuery.toLowerCase();
    return entry.term.toLowerCase().includes(q) || entry.definition.toLowerCase().includes(q);
  });
  const active = filtered.find((entry) => entry.slug === state.activeGlossarySlug) || filtered[0] || null;

  return `
    <section class="reference-grid">
      <aside class="panel reference-list-panel">
        <div class="reference-toolbar">
          <span class="eyebrow">Glossary</span>
        </div>
        <div style="padding:0 18px 14px;">
          <input id="glossary-query" class="reference-search" type="search" placeholder="Search glossary terms" value="${escapeAttr(state.glossaryQuery)}">
        </div>
        <div class="reference-list">
          ${filtered.map((entry) => `
            <button type="button" class="reference-list-item ${active?.slug === entry.slug ? "active" : ""}" data-action="select-glossary" data-slug="${entry.slug}">
              <div>${escapeHTML(entry.term)}</div>
              <div class="thread-meta">${escapeHTML(entry.excerpt)}</div>
            </button>
          `).join("") || `<div class="empty-state">No glossary entries match that search.</div>`}
        </div>
      </aside>

      <section class="panel reference-detail-panel">
        ${active ? `
          <header class="reference-detail-header">
            <div class="eyebrow">Term</div>
            <h2 class="reference-term">${escapeHTML(active.term)}</h2>
            <div class="detail-meta">${escapeHTML(active.plain_hint)}</div>
          </header>
          <div class="reference-detail-body">
            <div class="reference-box">
              <div class="eyebrow">Book definition</div>
              <div class="reference-definition">${renderRichText(active.definition)}</div>
            </div>
            <div class="reference-box">
              <div class="eyebrow">Related chapters</div>
              <div class="card-actions" style="margin-top:12px;">
                ${(active.related_chapters || []).length ? active.related_chapters.map((chapter) => `
                  <button type="button" class="utility-chip" data-action="open-chapter" data-chapter-id="${chapter.id}">${escapeHTML(chapter.title)}</button>
                `).join("") : `<div class="status-note">No related chapter hints yet.</div>`}
              </div>
            </div>
            <div class="card-actions">
              <button type="button" class="primary-button" data-action="ask-term" data-question="Define ${escapeAttr(active.term)} as the book uses it.">Ask about this term</button>
            </div>
          </div>
        ` : `<div class="empty-state">Select a glossary term.</div>`}
      </section>
    </section>
  `;
}

function renderIndexView() {
  if (!state.indexEntries) {
    return `<section class="panel loading-panel"><p>Loading index…</p></section>`;
  }

  const filtered = state.indexEntries.filter((entry) => {
    if (!state.indexQuery.trim()) {
      return true;
    }
    const q = state.indexQuery.toLowerCase();
    return entry.path_display.toLowerCase().includes(q);
  }).slice(0, 240);

  const active = filtered.find((entry) => entry.id === state.activeIndexId) || filtered[0] || null;

  return `
    <section class="reference-grid">
      <aside class="panel reference-list-panel">
        <div class="reference-toolbar">
          <span class="eyebrow">Subject index</span>
        </div>
        <div style="padding:0 18px 14px;">
          <input id="index-query" class="reference-search" type="search" placeholder="Search the index" value="${escapeAttr(state.indexQuery)}">
        </div>
        <div class="reference-list">
          ${filtered.map((entry) => `
            <button type="button" class="reference-list-item ${active?.id === entry.id ? "active" : ""}" data-action="select-index" data-index-id="${entry.id}">
              <div>${escapeHTML(entry.term)}</div>
              <div class="thread-meta">${escapeHTML(entry.path_display)}</div>
            </button>
          `).join("") || `<div class="empty-state">No index entries match that search.</div>`}
        </div>
      </aside>
      <section class="panel reference-detail-panel">
        ${active ? `
          <header class="reference-detail-header">
            <div class="eyebrow">Index entry</div>
            <h2 class="reference-term">${escapeHTML(active.term)}</h2>
            <div class="detail-meta">${escapeHTML(active.path_display)}</div>
          </header>
          <div class="reference-detail-body">
            <div class="reference-box">
              <div class="eyebrow">Cross-references</div>
              <div class="card-actions" style="margin-top:12px;">
                ${active.see?.length ? active.see.map((item) => `<span class="utility-chip">See: ${escapeHTML(item)}</span>`).join("") : ""}
                ${active.seealso?.length ? active.seealso.map((item) => `<span class="ghost-chip">See also: ${escapeHTML(item)}</span>`).join("") : ""}
                ${!active.see?.length && !active.seealso?.length ? `<div class="status-note">No explicit cross-reference note on this entry.</div>` : ""}
              </div>
            </div>
            <div class="card-actions">
              <button type="button" class="primary-button" data-action="ask-term" data-question="Where does the book treat ${escapeAttr(active.term)}?">Ask about this entry</button>
            </div>
          </div>
        ` : `<div class="empty-state">Select an index entry.</div>`}
      </section>
    </section>
  `;
}

function renderMessageCard(message) {
  return `
    <article class="message ${message.role}">
      <div class="message-header">
        <span class="message-role">${message.role === "user" ? "You" : "Guide"}</span>
        <span class="message-meta">${formatTimestamp(message.createdAt || new Date().toISOString())}</span>
      </div>
      <div class="message-body">${renderRichText(message.content)}</div>
      ${message.sources?.length ? `
        <div class="citation-row">
          ${message.sources.map((source, index) => `
            <button type="button" class="cite-chip" data-action="select-message-source" data-message-id="${message.id}" data-chunk-id="${source.chunk_id}">
              [${index + 1}] ${escapeHTML(source.title)}
            </button>
          `).join("")}
        </div>
      ` : ""}
      ${message.weakMatch && message.relatedChapters?.length ? `
        <div class="citation-row">
          ${message.relatedChapters.map((chapter) => `
            <button type="button" class="ghost-chip" data-action="open-chapter" data-chapter-id="${chapter.id}">Try ${escapeHTML(chapter.title)}</button>
          `).join("")}
        </div>
      ` : ""}
    </article>
  `;
}

function renderSourceCard(source) {
  const scoreText = typeof source.score === "number" ? ` · score ${source.score.toFixed(3)}` : "";
  return `
    <article class="source-card">
      <div class="eyebrow">${escapeHTML(source.path.join(" > "))}</div>
      <h3 class="source-title">${escapeHTML(source.title)}</h3>
      <div class="source-meta">${escapeHTML(source.source_path)}${scoreText}</div>
      <p class="source-preview">${escapeHTML(source.preview)}</p>
      <div class="source-actions">
        <button type="button" class="secondary-button" data-action="open-source" data-chunk-id="${source.chunk_id}">Inspect source</button>
      </div>
    </article>
  `;
}

function renderModal() {
  const root = document.getElementById("modal-root");
  if (!state.modalSource) {
    root.innerHTML = "";
    return;
  }
  const source = state.modalSource.source;
  const context = state.modalSource.context;
  root.innerHTML = `
    <div class="modal-backdrop">
      <section class="panel modal">
        <header class="modal-header">
          <div>
            <div class="eyebrow">Source inspector</div>
            <h2 class="modal-title">${escapeHTML(source.title)}</h2>
            <div class="detail-meta">${escapeHTML(source.path.join(" > "))}</div>
          </div>
          <div class="inline-actions">
            <button type="button" class="secondary-button" data-action="open-source-in-read" data-chapter-id="${source.chapter_id}" data-passage-id="${source.passage_id}">Open in Read</button>
            <button type="button" class="ghost-chip" data-action="close-modal">Close</button>
          </div>
        </header>
        <div class="modal-body">
          <div class="modal-copy">
            <div class="detail-meta">${escapeHTML(source.source_path)} · chunk ${escapeHTML(source.chunk_id)}</div>
            <div class="reference-box" style="margin-top:14px;">
              <div class="eyebrow">Selected evidence</div>
              <div class="reference-definition">${renderRichText(source.selected_text)}</div>
            </div>
            <div class="reference-box" style="margin-top:14px;">
              <div class="eyebrow">Full passage</div>
              <div class="reference-definition">${renderRichText(source.passage_text)}</div>
            </div>
          </div>
          <aside class="modal-side">
            <div class="reference-box">
              <div class="eyebrow">Location</div>
              <div class="detail-meta">${escapeHTML(source.chapter_title)}</div>
              <div class="detail-meta">${escapeHTML(source.block_type)}</div>
              <div class="detail-meta">Part ${source.chunk_position} of ${source.chunk_total}</div>
            </div>
            ${context.previous ? `
              <div class="context-card">
                <div class="eyebrow">Previous passage</div>
                <div>${escapeHTML(context.previous.title)}</div>
                <div class="thread-meta">${escapeHTML(context.previous.preview)}</div>
              </div>
            ` : ""}
            ${context.next ? `
              <div class="context-card">
                <div class="eyebrow">Next passage</div>
                <div>${escapeHTML(context.next.title)}</div>
                <div class="thread-meta">${escapeHTML(context.next.preview)}</div>
              </div>
            ` : ""}
          </aside>
        </div>
      </section>
    </div>
  `;
}

function selectedAskSources() {
  const thread = currentThread();
  if (!thread) {
    return [];
  }
  const selected = thread.messages.find((message) => message.id === state.ask.selectedMessageId && message.sources?.length);
  if (selected) {
    return selected.sources;
  }
  const fallback = [...thread.messages].reverse().find((message) => message.sources?.length);
  return fallback?.sources || [];
}

function selectedReadSources() {
  const selected = state.read.messages.find((message) => message.id === state.read.selectedMessageId && message.sources?.length);
  if (selected) {
    return selected.sources;
  }
  const fallback = [...state.read.messages].reverse().find((message) => message.sources?.length);
  return fallback?.sources || [];
}

function currentChapterPassage() {
  const chapterData = state.chapterCache[state.currentChapterId];
  if (!chapterData) {
    return null;
  }
  return chapterData.passages.find((passage) => passage.passage_id === state.currentPassageId) || null;
}

function historyPayload(messages) {
  return messages.map((message) => ({
    role: message.role,
    content: message.content,
  }));
}

async function submitAsk(question, scopeOverride) {
  const thread = ensureActiveThread(scopeOverride || currentThread()?.scope);
  const text = question.trim();
  if (!text) {
    return;
  }

  if (scopeOverride) {
    thread.scope = scopeOverride;
  }

  const userMessage = {
    id: `msg-${Date.now()}-${Math.random().toString(16).slice(2, 6)}`,
    role: "user",
    content: text,
    createdAt: new Date().toISOString(),
  };
  thread.messages.push(userMessage);
  thread.updatedAt = userMessage.createdAt;
  if (thread.title === "New thread") {
    thread.title = truncate(text, 64);
  }

  state.ask.draft = "";
  state.ask.pending = true;
  state.ask.selectedMessageId = null;
  persistThreads();
  render();

  try {
    const payload = await fetchJSON("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: text,
        history: historyPayload(thread.messages),
        top_k: state.ask.topK,
        use_openai: state.ask.useOpenAI,
        model: state.ask.model,
        scope: thread.scope || { mode: "book" },
      }),
    });
    const assistantMessage = {
      id: `msg-${Date.now()}-${Math.random().toString(16).slice(2, 6)}`,
      role: "assistant",
      content: payload.answer,
      createdAt: new Date().toISOString(),
      sources: payload.sources || [],
      weakMatch: payload.weak_match,
      relatedChapters: payload.related_chapters || [],
    };
    thread.messages.push(assistantMessage);
    thread.updatedAt = assistantMessage.createdAt;
    state.ask.selectedMessageId = assistantMessage.id;
    thread.scope = payload.scope || thread.scope;
  } catch (error) {
    thread.messages.push({
      id: `msg-${Date.now()}-${Math.random().toString(16).slice(2, 6)}`,
      role: "assistant",
      content: `The request failed.\n\n${String(error)}`,
      createdAt: new Date().toISOString(),
    });
  } finally {
    state.ask.pending = false;
    persistThreads();
    render();
  }
}

async function submitReadGuide(question) {
  const text = question.trim();
  if (!text) {
    return;
  }
  const userMessage = {
    id: `guide-${Date.now()}-${Math.random().toString(16).slice(2, 6)}`,
    role: "user",
    content: text,
    createdAt: new Date().toISOString(),
  };
  state.read.messages.push(userMessage);
  state.read.pending = true;
  state.read.draft = "";
  render();

  try {
    const payload = await fetchJSON("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: text,
        history: historyPayload(state.read.messages),
        top_k: state.ask.topK,
        use_openai: state.ask.useOpenAI,
        model: state.ask.model,
        scope: state.read.scope,
      }),
    });
    const assistantMessage = {
      id: `guide-${Date.now()}-${Math.random().toString(16).slice(2, 6)}`,
      role: "assistant",
      content: payload.answer,
      createdAt: new Date().toISOString(),
      sources: payload.sources || [],
      weakMatch: payload.weak_match,
      relatedChapters: payload.related_chapters || [],
    };
    state.read.messages.push(assistantMessage);
    state.read.selectedMessageId = assistantMessage.id;
  } catch (error) {
    state.read.messages.push({
      id: `guide-${Date.now()}-${Math.random().toString(16).slice(2, 6)}`,
      role: "assistant",
      content: `The request failed.\n\n${String(error)}`,
      createdAt: new Date().toISOString(),
    });
  } finally {
    state.read.pending = false;
    render();
  }
}

async function openSource(chunkId) {
  state.modalSource = await fetchJSON(`/api/source?chunk_id=${encodeURIComponent(chunkId)}`);
  renderModal();
}

function renderRichText(text) {
  return text
    .split(/\n\s*\n/)
    .map((block) => `<p>${escapeHTML(block.trim()).replace(/\n/g, "<br>")}</p>`)
    .join("");
}

function truncate(text, limit) {
  if (text.length <= limit) {
    return text;
  }
  return `${text.slice(0, limit - 1).trimEnd()}…`;
}

function formatTimestamp(value) {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  return date.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function escapeHTML(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttr(value) {
  return escapeHTML(value).replaceAll("'", "&#39;");
}

function handleInput(event) {
  const target = event.target;
  if (target.id === "ask-draft") {
    state.ask.draft = target.value;
  } else if (target.id === "read-draft") {
    state.read.draft = target.value;
  } else if (target.id === "ask-model") {
    state.ask.model = target.value;
  } else if (target.id === "ask-top-k") {
    state.ask.topK = Math.max(1, Math.min(12, Number(target.value || 5)));
  } else if (target.id === "ask-openai") {
    state.ask.useOpenAI = target.checked;
  } else if (target.id === "glossary-query") {
    state.glossaryQuery = target.value;
    render();
    requestAnimationFrame(() => {
      const input = document.getElementById("glossary-query");
      input?.focus();
      input?.setSelectionRange(state.glossaryQuery.length, state.glossaryQuery.length);
    });
  } else if (target.id === "index-query") {
    state.indexQuery = target.value;
    render();
    requestAnimationFrame(() => {
      const input = document.getElementById("index-query");
      input?.focus();
      input?.setSelectionRange(state.indexQuery.length, state.indexQuery.length);
    });
  }
}

async function handleSubmit(event) {
  event.preventDefault();
  if (event.target.id === "ask-form") {
    await submitAsk(state.ask.draft);
  } else if (event.target.id === "read-form") {
    await submitReadGuide(state.read.draft);
  }
}

async function handleClick(event) {
  const button = event.target.closest("[data-action]");
  if (!button) {
    return;
  }

  const action = button.dataset.action;

  if (action === "go-home") {
    state.currentView = "landing";
    render();
    return;
  }

  if (action === "nav") {
    await openView(button.dataset.view);
    return;
  }

  if (action === "landing-start-read") {
    await openView("read");
    return;
  }

  if (action === "landing-start-ask") {
    await openView("ask");
    ensureActiveThread();
    render();
    return;
  }

  if (action === "landing-prompt") {
    await openView("ask");
    const scope = { mode: "book", value: null, label: "Whole book" };
    const thread = makeThread(scope);
    state.ask.threads.unshift(thread);
    state.ask.activeThreadId = thread.id;
    persistThreads();
    await submitAsk(button.dataset.question, scope);
    return;
  }

  if (action === "open-chapter") {
    state.currentChapterId = button.dataset.chapterId;
    state.currentPassageId = null;
    await ensureChapter(state.currentChapterId);
    state.read.scope = {
      mode: "chapter",
      value: state.currentChapterId,
      label: chapterLabel(state.currentChapterId),
    };
    state.currentView = "read";
    render();
    return;
  }

  if (action === "ask-chapter") {
    await openView("ask");
    const chapterId = button.dataset.chapterId;
    const scope = { mode: "chapter", value: chapterId, label: `Chapter: ${chapterLabel(chapterId)}` };
    const thread = makeThread(scope);
    state.ask.threads.unshift(thread);
    state.ask.activeThreadId = thread.id;
    persistThreads();
    await submitAsk("Give me a concise orientation to this chapter.", scope);
    return;
  }

  if (action === "jump-passage") {
    const chapterData = state.chapterCache[state.currentChapterId];
    const passage = chapterData?.passages.find((item) => item.anchor === button.dataset.anchor);
    if (passage) {
      state.currentPassageId = passage.passage_id;
      state.read.scope = {
        mode: "passage",
        value: passage.passage_id,
        label: `Section: ${passage.anchor}`,
      };
      render();
    }
    return;
  }

  if (action === "scope-passage") {
    const chapterData = state.chapterCache[state.currentChapterId];
    const passage = chapterData?.passages.find((item) => item.passage_id === button.dataset.passageId);
    if (passage) {
      state.currentPassageId = passage.passage_id;
      state.read.scope = {
        mode: "passage",
        value: passage.passage_id,
        label: `Section: ${passage.anchor}`,
      };
      state.read.drawerOpen = true;
      render();
    }
    return;
  }

  if (action === "set-read-scope") {
    const mode = button.dataset.mode;
    if (mode === "book") {
      state.read.scope = { mode: "book", value: null, label: "Whole book" };
    } else if (mode === "chapter") {
      state.read.scope = {
        mode: "chapter",
        value: state.currentChapterId,
        label: chapterLabel(state.currentChapterId),
      };
    } else if (mode === "passage" && button.dataset.value) {
      const passage = currentChapterPassage() || state.chapterCache[state.currentChapterId]?.passages.find((item) => item.passage_id === button.dataset.value);
      if (passage) {
        state.currentPassageId = passage.passage_id;
        state.read.scope = {
          mode: "passage",
          value: passage.passage_id,
          label: `Section: ${passage.anchor}`,
        };
      }
    }
    render();
    return;
  }

  if (action === "toggle-drawer") {
    state.read.drawerOpen = !state.read.drawerOpen;
    render();
    return;
  }

  if (action === "clear-read-guide") {
    state.read.messages = [];
    state.read.selectedMessageId = null;
    render();
    return;
  }

  if (action === "guide-to-ask") {
    await openView("ask");
    const scope = state.read.scope;
    const thread = makeThread(scope);
    thread.title = scope.mode === "passage" ? "Section follow-up" : scope.mode === "chapter" ? `About ${chapterLabel(scope.value)}` : "Reading follow-up";
    thread.messages = state.read.messages.map((message) => ({ ...message }));
    thread.updatedAt = new Date().toISOString();
    state.ask.threads.unshift(thread);
    state.ask.activeThreadId = thread.id;
    state.ask.selectedMessageId = [...thread.messages].reverse().find((message) => message.sources?.length)?.id || null;
    persistThreads();
    render();
    return;
  }

  if (action === "new-thread") {
    const thread = makeThread({ mode: "book", value: null, label: "Whole book" });
    state.ask.threads.unshift(thread);
    state.ask.activeThreadId = thread.id;
    state.ask.selectedMessageId = null;
    persistThreads();
    render();
    return;
  }

  if (action === "activate-thread") {
    state.ask.activeThreadId = button.dataset.threadId;
    state.ask.selectedMessageId = null;
    persistThreads();
    render();
    return;
  }

  if (action === "clear-thread-scope") {
    const thread = ensureActiveThread();
    thread.scope = { mode: "book", value: null, label: "Whole book" };
    persistThreads();
    render();
    return;
  }

  if (action === "select-message-source") {
    const thread = currentThread();
    if (thread?.messages.some((message) => message.id === button.dataset.messageId)) {
      state.ask.selectedMessageId = button.dataset.messageId;
      render();
    } else {
      state.read.selectedMessageId = button.dataset.messageId;
      render();
    }
    await openSource(button.dataset.chunkId);
    return;
  }

  if (action === "open-source") {
    await openSource(button.dataset.chunkId);
    return;
  }

  if (action === "close-modal") {
    state.modalSource = null;
    renderModal();
    return;
  }

  if (action === "open-source-in-read") {
    const anchor = state.modalSource?.source?.anchor || "";
    state.currentChapterId = button.dataset.chapterId;
    await ensureChapter(state.currentChapterId);
    state.currentPassageId = button.dataset.passageId;
    state.currentView = "read";
    state.modalSource = null;
    state.read.scope = {
      mode: "passage",
      value: button.dataset.passageId,
      label: `Section: ${anchor}`,
    };
    render();
    return;
  }

  if (action === "select-glossary") {
    state.activeGlossarySlug = button.dataset.slug;
    render();
    return;
  }

  if (action === "select-index") {
    state.activeIndexId = button.dataset.indexId;
    render();
    return;
  }

  if (action === "ask-term") {
    await openView("ask");
    const scope = { mode: "book", value: null, label: "Whole book" };
    const thread = makeThread(scope);
    state.ask.threads.unshift(thread);
    state.ask.activeThreadId = thread.id;
    persistThreads();
    await submitAsk(button.dataset.question, scope);
  }
}
