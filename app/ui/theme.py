HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
"""

JS = """
() => {
  const root = document.querySelector('.gradio-container');
  if (!root) return;
  root.dataset.ready = 'true';
}
"""

CSS = """
/* ═══════════════════════════════════════════════
   KNOWLEDGEHUB — WARM LIGHT THEME
   Palette: parchment bg · sage green · warm amber
   Texture: fine cross-hatch + dot grid overlay
═══════════════════════════════════════════════ */

:root {
  --kh-bg:            #ede8db;
  --kh-bg2:           #e8e2d4;
  --kh-surface:       #faf7f0;
  --kh-surface2:      #f5f1e6;
  --kh-ink:           #1e1b15;
  --kh-muted:         #6b6254;
  --kh-soft:          #3d3828;
  --kh-line:          rgba(80, 65, 35, 0.14);
  --kh-sage:          #3d7a6a;
  --kh-sage-dim:      rgba(61, 122, 106, 0.15);
  --kh-amber:         #b87428;
  --kh-shadow:        rgba(80, 60, 20, 0.10);
  --kh-shadow-md:     rgba(80, 60, 20, 0.16);
}

/* ══ PAGE BACKGROUND — cross-hatch + dot texture ══ */
.gradio-container {
  min-height: 100vh !important;
  background-color: var(--kh-bg) !important;
  /* Cross-hatch lines */
  background-image:
    linear-gradient(rgba(61,122,106,0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(61,122,106,0.07) 1px, transparent 1px),
    linear-gradient(rgba(184,116,40,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(184,116,40,0.04) 1px, transparent 1px),
    radial-gradient(ellipse 65% 45% at 5% 0%,  rgba(61,122,106,0.13) 0%, transparent 60%),
    radial-gradient(ellipse 55% 40% at 96% 4%, rgba(184,116,40,0.11) 0%, transparent 55%),
    radial-gradient(ellipse 80% 55% at 50% 105%, rgba(61,122,106,0.08) 0%, transparent 60%) !important;
  background-size:
    32px 32px,
    32px 32px,
    8px 8px,
    8px 8px,
    100% 100%,
    100% 100%,
    100% 100% !important;
  color: var(--kh-ink) !important;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif !important;
}

/* ══ NUKE ALL DARK BACKGROUNDS from Gradio internals ══ */
/* Every block, wrap, form, and container Gradio might use */
.gradio-container *,
.gradio-container .block,
.gradio-container .form,
.gradio-container .wrap,
.gradio-container .gap,
.gradio-container .container,
.gradio-container .svelte-1f354aw,
.gradio-container .input-wrap,
.gradio-container .component-wrapper,
.gradio-container [data-testid],
.gradio-container .lg,
.gradio-container .sm,
.gradio-container .stretch {
  background-color: transparent !important;
  color: inherit !important;
}

/* Force all Gradio block panels to parchment */
.gradio-container .block.padded,
.gradio-container .block.padded.hide-container,
.gradio-container div.block,
.gradio-container fieldset,
.gradio-container label.block {
  background-color: var(--kh-surface) !important;
  border-color: var(--kh-line) !important;
  color: var(--kh-ink) !important;
}

/* ══ SHELL ══ */
#kh-shell {
  position: relative;
  z-index: 1;
  max-width: 1220px;
  margin: 0 auto;
  padding: 32px 20px 52px;
}

/* ══ TITLE ══ */
#kh-title {
  padding: 36px 0 26px;
  border-bottom: 1px solid var(--kh-line);
  background: transparent !important;
}

#kh-title h1 {
  max-width: 960px;
  color: var(--kh-ink) !important;
  font-family: "Instrument Serif", Georgia, "Times New Roman", serif !important;
  font-size: clamp(2.8rem, 6.5vw, 6.2rem);
  font-weight: 400;
  font-style: italic;
  line-height: 0.92;
  margin: 0 0 16px;
  letter-spacing: -0.01em;
}

#kh-title p {
  max-width: 760px;
  color: var(--kh-muted) !important;
  font-size: 1.02rem;
  line-height: 1.7;
  margin: 6px 0 0;
}

/* ══ CODE CHIPS ══ */
#kh-title code,
.kh-chip code {
  color: var(--kh-sage) !important;
  background: rgba(61, 122, 106, 0.11) !important;
  border: 1px solid rgba(61, 122, 106, 0.22) !important;
  border-radius: 5px;
  padding: 2px 6px;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 0.87em;
}

/* ══ CHIP ROW ══ */
.kh-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  margin-top: 18px;
  background: transparent !important;
}

.kh-chip {
  border: 1px solid var(--kh-line);
  border-radius: 999px;
  padding: 6px 14px;
  color: var(--kh-soft) !important;
  background: rgba(250, 247, 240, 0.85) !important;
  font-size: 0.87rem;
  font-weight: 500;
  box-shadow: 0 1px 3px var(--kh-shadow);
}

/* ══ PANELS — clean lifted paper, no inner texture ══ */
.kh-panel,
.kh-panel.block,
.kh-panel > .block {
  border: 1px solid rgba(80, 65, 35, 0.13) !important;
  border-top: 2.5px solid rgba(61, 122, 106, 0.38) !important;
  border-radius: 14px !important;
  background: #fdfaf3 !important;
  box-shadow:
    0 1px 0 rgba(255,255,255,0.95) inset,
    0 4px 6px -2px rgba(80,60,20,0.06),
    0 12px 32px rgba(80,60,20,0.09);
  padding: 22px !important;
  color: var(--kh-ink) !important;
}

/* Force all children of panels to be light too */
.kh-panel *,
.kh-panel .block,
.kh-panel .wrap,
.kh-panel .form,
.kh-panel fieldset {
  background-color: transparent !important;
  color: var(--kh-ink) !important;
  border-color: var(--kh-line) !important;
  box-shadow: none !important;
}

/* Labels inside panels */
.kh-panel label span,
.kh-panel .label-wrap span,
.kh-panel span.text-gray-500,
.kh-panel span.text-sm {
  color: var(--kh-soft) !important;
  font-weight: 600 !important;
  font-size: 0.89rem !important;
  letter-spacing: 0.01em;
}

.kh-subhead {
  margin: 6px 0 16px;
  color: var(--kh-muted) !important;
  font-size: 0.93rem;
  line-height: 1.6;
}

/* ══ STAT BOXES ══ */
.kh-stat,
.kh-stat > .block,
.kh-stat .wrap {
  min-height: 88px;
  border: 1px solid rgba(80,65,35,0.11) !important;
  border-radius: 10px !important;
  padding: 12px 16px;
  background: rgba(232, 226, 212, 0.6) !important;
  box-shadow: 0 1px 0 rgba(255,255,255,0.85) inset;
}

.kh-stat input,
.kh-stat textarea {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  color: var(--kh-ink) !important;
}

/* ══ TABS ══ */
.tabs {
  margin-top: 22px;
  background: transparent !important;
}

.tab-nav {
  background: transparent !important;
  border-bottom: 1px solid var(--kh-line) !important;
  gap: 4px;
}

.tab-nav button {
  color: var(--kh-muted) !important;
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: 8px 8px 0 0 !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  padding: 9px 20px !important;
  transition: all 0.15s ease;
}

.tab-nav button:hover {
  color: var(--kh-sage) !important;
  background: rgba(61,122,106,0.07) !important;
}

.tab-nav button.selected {
  color: var(--kh-sage) !important;
  background: var(--kh-surface) !important;
  border: 1px solid var(--kh-line) !important;
  border-bottom-color: var(--kh-surface) !important;
}

/* ══ INPUTS & TEXTAREAS ══ */
textarea,
input[type="text"],
input[type="number"],
input[type="search"],
input[type="email"] {
  color: var(--kh-ink) !important;
  background: rgba(255, 252, 244, 0.92) !important;
  border: 1px solid rgba(80,65,35,0.18) !important;
  border-radius: 8px !important;
  font-size: 0.94rem !important;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif !important;
  box-shadow: 0 1px 2px rgba(80,60,20,0.05) inset !important;
  transition: border-color 0.15s, box-shadow 0.15s;
}

textarea:focus,
input[type="text"]:focus {
  border-color: rgba(61,122,106,0.5) !important;
  box-shadow: 0 0 0 3px rgba(61,122,106,0.11), 0 1px 3px rgba(80,60,20,0.06) inset !important;
  outline: none !important;
}

textarea::placeholder,
input::placeholder {
  color: rgba(107,98,84,0.52) !important;
}

/* ══ UPLOAD / FILE BLOCK ══ */
.upload-container,
.file-preview,
[data-testid="file"],
.file-upload {
  background:
    repeating-linear-gradient(
      45deg,
      rgba(61,122,106,0.04) 0px,
      rgba(61,122,106,0.04) 1px,
      transparent 1px,
      transparent 10px
    ) !important;
  border: 1.5px dashed rgba(61,122,106,0.35) !important;
  border-radius: 10px !important;
  color: var(--kh-muted) !important;
}

.upload-container *,
.file-preview * {
  background: transparent !important;
  color: var(--kh-muted) !important;
}

/* ══ BUTTONS ══ */
button.primary,
button[variant="primary"],
.primary {
  min-height: 44px;
  background: linear-gradient(135deg, #3d7a6a 0%, #2e6055 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 9px !important;
  font-weight: 700 !important;
  font-size: 0.94rem !important;
  letter-spacing: 0.01em;
  box-shadow: 0 4px 14px rgba(61,122,106,0.30) !important;
  transition: transform 0.12s, box-shadow 0.12s;
}

button.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 7px 20px rgba(61,122,106,0.38) !important;
}

button.secondary,
button[variant="secondary"],
.secondary {
  background: rgba(232,226,212,0.8) !important;
  color: var(--kh-soft) !important;
  border: 1px solid rgba(80,65,35,0.18) !important;
  border-radius: 9px !important;
  font-weight: 600 !important;
}

button.secondary:hover {
  background: rgba(61,122,106,0.10) !important;
  border-color: rgba(61,122,106,0.32) !important;
  color: var(--kh-sage) !important;
}

/* ══ SLIDER ══ */
input[type="range"] {
  accent-color: var(--kh-sage) !important;
}

/* ══ STATUS BOX ══ */
#kh-status {
  min-height: 130px;
  color: var(--kh-ink) !important;
}

#kh-status h3 {
  color: var(--kh-sage) !important;
  font-family: "Instrument Serif", Georgia, serif !important;
  font-style: italic;
  font-weight: 400;
  font-size: 1.22rem;
  margin-top: 0;
}

/* ══ TEXT PREVIEW ══ */
#kh-text-preview textarea {
  min-height: 430px !important;
  line-height: 1.65 !important;
  font-family: "JetBrains Mono", ui-monospace, monospace !important;
  font-size: 0.87rem !important;
  background: rgba(232,226,212,0.45) !important;
}

/* ══ SEARCH RESULTS / ANSWER / REASONING ══ */
#kh-search-results {
  min-height: 410px;
  color: var(--kh-ink) !important;
}

#kh-search-results h3 {
  color: var(--kh-sage) !important;
  font-family: "Instrument Serif", Georgia, serif !important;
  font-style: italic;
  font-weight: 400;
}

#kh-answer {
  min-height: 240px;
  font-size: 1.02rem;
  line-height: 1.75;
  color: var(--kh-ink) !important;
}

#kh-reasoning {
  min-height: 240px;
  color: var(--kh-muted) !important;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 0.85rem;
  line-height: 1.65;
}

/* ══ MARKDOWN / PROSE ══ */
.prose, .markdown,
.prose *, .markdown * {
  color: var(--kh-soft) !important;
  background: transparent !important;
}

.prose strong, .markdown strong,
.prose h1, .markdown h1,
.prose h2, .markdown h2,
.prose h3, .markdown h3 {
  color: var(--kh-ink) !important;
}

.prose h3, .markdown h3 {
  font-family: "Instrument Serif", Georgia, serif !important;
  font-style: italic;
  font-weight: 400;
  font-size: 1.13rem;
}

code {
  color: var(--kh-sage) !important;
  background: rgba(61,122,106,0.09) !important;
  border: 1px solid rgba(61,122,106,0.18) !important;
  border-radius: 4px;
  padding: 1px 5px;
  font-family: "JetBrains Mono", ui-monospace, monospace;
}

/* ══ SCROLLBAR ══ */
::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: rgba(232,226,212,0.4); }
::-webkit-scrollbar-thumb { background: rgba(61,122,106,0.32); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(61,122,106,0.52); }

/* ══ DIVIDERS / MISC ══ */
hr { border-color: var(--kh-line) !important; }

/* ══ RESPONSIVE ══ */
@media (max-width: 760px) {
  #kh-shell { padding: 18px 12px 36px; }
  #kh-title h1 { font-size: clamp(2.2rem, 13vw, 3.8rem); }
  .kh-panel { padding: 16px !important; }
}
"""
