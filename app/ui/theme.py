HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gochi+Hand&family=Caveat:wght@400;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
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
   KNOWLEDGEMESH — CHALKBOARD CLASSROOM THEME
   Palette: Dark chalkboard green · Frosted glass · Warm chalk yellow · Neon chalk green
   Texture: Wood border, vignette board, chalk doodles
   ═══════════════════════════════════════════════ */

/* ══ PAGE BACKGROUND — Dark cozy classroom ══ */
.gradio-container {
  min-height: 100vh !important;
  background: radial-gradient(circle at center, #181715 0%, #0a0a09 100%) !important;
  color: #f8fafc !important;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif !important;
  padding: 20px 10px !important;
}

/* ══ NUKE GRADIO STYLING OVERRIDES ══ */
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
  color: inherit;
}

/* ══ CHALKBOARD CONTAINER (FRAME & SURFACE) ══ */
#kh-shell {
  position: relative !important;
  max-width: 1200px !important;
  margin: 30px auto !important;
  padding: 40px 40px 60px 40px !important;
  
  /* Wood Frame border styling */
  border: 14px solid #3d2314 !important;
  border-radius: 12px !important;
  
  /* Multi-layered shadows for frame bevel and board depth */
  box-shadow: 
    0 15px 35px rgba(0,0,0,0.85),
    inset 0 0 20px rgba(0,0,0,0.9),
    inset 0 0 0 1px #4f2f1c,
    0 0 0 1px #1d1009 !important;
  
  /* Multiple backgrounds:
     1. Hanging lamp doodle (top right)
     2. Idea lightbulb (top center)
     3. Atom doodle (left)
     4. Neural Network sketch (left, lower)
     5. Mathematical graph (bottom left)
     6. Equations & math doodle (right)
     7. Tiny star/arrow doodle (top left)
     8. Chalkboard green vignette surface
  */
  background-image: 
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='80' height='180' viewBox='0 0 80 180'><path d='M 40,0 L 40,90' fill='none' stroke='rgba(255,255,255,0.18)' stroke-width='1.5'/><path d='M 25,90 L 55,90 L 60,105 L 20,105 Z' fill='rgba(255,255,255,0.04)' stroke='rgba(255,255,255,0.22)' stroke-width='1.5' stroke-linejoin='round'/><circle cx='40' cy='113' r='8' fill='rgba(255,255,220,0.12)' stroke='rgba(255,255,255,0.25)' stroke-width='1.5'/><path d='M 38,110 L 40,115 L 42,110' fill='none' stroke='rgba(255,255,220,0.5)' stroke-width='1'/><path d='M 20,125 L 10,135 M 30,128 L 25,140 M 50,128 L 55,140 M 60,125 L 70,135' fill='none' stroke='rgba(255,255,220,0.18)' stroke-width='1' stroke-linecap='round'/></svg>"),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='60' height='70' viewBox='0 0 60 70'><path d='M 30,10 C 20,10 15,20 15,30 C 15,40 25,45 25,50 L 35,50 C 35,45 45,40 45,30 C 45,20 40,10 30,10 Z M 25,50 L 35,50 M 27,54 L 33,54 M 29,58 L 31,58' fill='none' stroke='rgba(255,255,255,0.06)' stroke-width='1.2'/><path d='M 10,25 L 5,22 M 12,15 L 7,10 M 30,5 L 30,0 M 48,15 L 53,10 M 50,25 L 55,22' fill='none' stroke='rgba(255,255,255,0.06)' stroke-width='1' stroke-linecap='round'/></svg>"),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'><ellipse cx='50' cy='50' rx='42' ry='12' fill='none' stroke='rgba(255,255,255,0.06)' stroke-width='1.2' transform='rotate(30 50 50)'/><ellipse cx='50' cy='50' rx='42' ry='12' fill='none' stroke='rgba(255,255,255,0.06)' stroke-width='1.2' transform='rotate(-30 50 50)'/><ellipse cx='50' cy='50' rx='42' ry='12' fill='none' stroke='rgba(255,255,255,0.06)' stroke-width='1.2' transform='rotate(90 50 50)'/><circle cx='50' cy='50' r='5' fill='rgba(255,255,255,0.08)'/></svg>"),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='90' height='120' viewBox='0 0 90 120'><circle cx='20' cy='20' r='4' fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1.2'/><circle cx='20' cy='60' r='4' fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1.2'/><circle cx='20' cy='100' r='4' fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1.2'/><circle cx='70' cy='40' r='4' fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1.2'/><circle cx='70' cy='80' r='4' fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1.2'/><line x1='24' y1='20' x2='66' y2='40' stroke='rgba(255,255,255,0.03)' stroke-width='1'/><line x1='24' y1='20' x2='66' y2='80' stroke='rgba(255,255,255,0.03)' stroke-width='1'/><line x1='24' y1='60' x2='66' y2='40' stroke='rgba(255,255,255,0.03)' stroke-width='1'/><line x1='24' y1='60' x2='66' y2='80' stroke='rgba(255,255,255,0.03)' stroke-width='1'/><line x1='24' y1='100' x2='66' y2='40' stroke='rgba(255,255,255,0.03)' stroke-width='1'/><line x1='24' y1='100' x2='66' y2='80' stroke='rgba(255,255,255,0.03)' stroke-width='1'/></svg>"),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='90' height='80' viewBox='0 0 90 80'><path d='M 10,10 L 10,70 L 80,70' fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1.2'/><path d='M 10,60 Q 30,30 50,50 T 80,20' fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1.2' stroke-dasharray='3,3'/><path d='M 10,50 Q 25,20 45,30 T 75,10' fill='none' stroke='rgba(255,255,255,0.07)' stroke-width='1.2'/></svg>"),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'><path d='M 90,20 L 93,27 L 100,27 L 95,31 L 97,38 L 90,34 L 83,38 L 85,31 L 80,27 L 87,27 Z' fill='none' stroke='rgba(255,255,255,0.08)' stroke-width='1.2'/><text x='10' y='70' font-family='&apos;Gochi Hand&apos;, cursive' font-size='15' fill='rgba(255,255,255,0.07)' transform='rotate(-5 10 70)'>e^(i.pi) %2B 1 = 0</text><path d='M 20,90 L 50,90 M 50,90 L 45,86 M 50,90 L 45,94' fill='none' stroke='rgba(255,255,255,0.06)' stroke-width='1.2'/><path d='M 20,90 L 40,110 M 40,110 L 35,110 M 40,110 L 40,105' fill='none' stroke='rgba(255,255,255,0.06)' stroke-width='1.2'/><text x='55' y='93' font-family='&apos;Gochi Hand&apos;, cursive' font-size='12' fill='rgba(255,255,255,0.06)'>F</text></svg>"),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'><path d='M 10,20 Q 25,5 40,20 Q 55,35 40,50 Q 25,65 15,50' fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1.5' stroke-linecap='round'/></svg>"),
    radial-gradient(circle at 50% 30%, #1c3d28 0%, #0d1e13 100%) !important;
  
  background-position: 
    right 35px top 0px,
    center top 20px,
    left 20px top 220px,
    left 30px top 450px,
    left 40px top 650px,
    right 30px top 350px,
    left 30px top 60px,
    center center !important;
  background-repeat: no-repeat !important;
  background-size: auto, auto, auto, auto, auto, auto, auto, cover !important;
  overflow: visible !important;
}
}

/* ══ ROOM TAG ══ */
.kh-room-tag {
  position: absolute;
  top: -12px;
  left: 35px;
  background: #142d1c !important;
  border: 1.5px solid rgba(94, 189, 114, 0.45) !important;
  color: #5ebd72 !important;
  padding: 4px 14px;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.15rem !important;
  border-radius: 6px !important;
  transform: rotate(-1.5deg) !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
  z-index: 10;
  pointer-events: none;
}

/* ══ HEADER & TYPOGRAPHY ══ */
#kh-title {
  padding: 10px 0 15px !important;
  border-bottom: 2px dashed rgba(255, 255, 255, 0.12) !important;
  background: transparent !important;
  text-align: left;
}

#kh-title h1 {
  color: #ffffff !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: clamp(2.8rem, 6vw, 4.8rem) !important;
  font-weight: 400 !important;
  line-height: 1.0;
  margin: 0 0 6px !important;
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.4), 1px 1px 2px rgba(0,0,0,0.6) !important;
}

#kh-title p {
  color: rgba(255, 255, 255, 0.75) !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.35rem !important;
  margin: 0 !important;
  letter-spacing: 0.03em !important;
}

/* ══ CODE CHIPS ══ */
.kh-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 14px 0 24px !important;
  background: transparent !important;
}

.kh-chip {
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 999px !important;
  padding: 4px 12px !important;
  color: rgba(255, 255, 255, 0.7) !important;
  background: rgba(255, 255, 255, 0.03) !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
}

.kh-chip code {
  color: #5ebd72 !important;
  background: rgba(94, 189, 114, 0.08) !important;
  border: 1px solid rgba(94, 189, 114, 0.2) !important;
  border-radius: 4px;
  padding: 1px 4px;
  font-family: "JetBrains Mono", monospace;
  font-size: 0.85em;
}

/* ══ CHALKBOARD TABS NAVIGATION ══ */
.tabs {
  margin-top: 10px !important;
  border: none !important;
}

.tab-nav {
  border-bottom: 2px dashed rgba(255, 255, 255, 0.15) !important;
  margin-bottom: 22px !important;
  gap: 12px !important;
  background: transparent !important;
}

.tab-nav button {
  color: rgba(255, 255, 255, 0.55) !important;
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.45rem !important;
  font-weight: normal !important;
  padding: 6px 20px !important;
  transition: all 0.2s ease !important;
}

.tab-nav button:hover {
  color: #ffffff !important;
  text-shadow: 0 0 6px rgba(255, 255, 255, 0.5) !important;
}

.tab-nav button.selected {
  color: #ffffff !important;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.8) !important;
  border-bottom: 3px solid #5ebd72 !important;
}

/* ══ FROSTED GLASS CARDS ══ */
.kh-panel {
  background: rgba(255, 255, 255, 0.038) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255, 255, 255, 0.09) !important;
  border-radius: 12px !important;
  padding: 24px !important;
  box-shadow: 
    0 8px 32px 0 rgba(0, 0, 0, 0.28),
    inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
  color: #f8fafc !important;
  margin-bottom: 15px !important;
}

.kh-panel h3 {
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.6rem !important;
  font-weight: normal !important;
  color: #ffffff !important;
  margin-top: 0 !important;
  margin-bottom: 8px !important;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.4) !important;
}

.kh-subhead {
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.15rem !important;
  color: rgba(255, 255, 255, 0.55) !important;
  line-height: 1.4 !important;
  margin-bottom: 16px !important;
}

/* ══ INPUTS & TEXTAREAS ══ */
textarea,
input[type="text"],
input[type="number"],
[data-testid="textbox"] input,
[data-testid="textbox"] textarea {
  background: rgba(0, 0, 0, 0.28) !important;
  color: #f8fafc !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  border-radius: 8px !important;
  padding: 10px 14px !important;
  font-size: 0.94rem !important;
  font-family: Inter, ui-sans-serif, sans-serif !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.5) !important;
  transition: all 0.2s ease !important;
}

textarea:focus,
input[type="text"]:focus,
[data-testid="textbox"] input:focus,
[data-testid="textbox"] textarea:focus {
  border-color: rgba(94, 189, 114, 0.5) !important;
  box-shadow: 
    0 0 8px rgba(94, 189, 114, 0.25),
    inset 0 2px 4px rgba(0,0,0,0.5) !important;
  outline: none !important;
}

textarea::placeholder,
input::placeholder {
  color: rgba(255, 255, 255, 0.38) !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.18rem !important;
}

/* Custom styles for Gradio form labels */
.kh-panel label span,
.kh-panel .label-wrap span {
  color: rgba(255, 255, 255, 0.5) !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.15rem !important;
  font-weight: normal !important;
  margin-bottom: 4px !important;
}

/* ══ UPLOAD DRAG/DROP FILE BLOCK ══ */
.upload-container,
.file-preview,
[data-testid="file"],
.file-upload {
  background: rgba(0, 0, 0, 0.2) !important;
  border: 2px dashed rgba(255, 255, 255, 0.14) !important;
  border-radius: 8px !important;
  color: rgba(255, 255, 255, 0.5) !important;
  padding: 14px !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.18rem !important;
  transition: all 0.2s ease !important;
  text-align: center;
}

.upload-container:hover {
  border-color: rgba(94, 189, 114, 0.45) !important;
  background: rgba(94, 189, 114, 0.04) !important;
}

.upload-container *, .file-preview * {
  background: transparent !important;
  color: rgba(255, 255, 255, 0.55) !important;
}

/* ══ BUTTONS ══ */
/* Primary Button — Warm Chalk Yellow, Slight Glow */
button.primary,
button[variant="primary"],
.primary {
  min-height: 42px;
  background: #d9b84a !important;
  color: #1c1605 !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.38rem !important;
  font-weight: bold !important;
  padding: 8px 24px !important;
  box-shadow: 0 0 15px rgba(217, 184, 74, 0.32) !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}

button.primary:hover {
  background: #e4c45a !important;
  box-shadow: 0 0 22px rgba(217, 184, 74, 0.5) !important;
  transform: translateY(-1.5px) !important;
}

button.primary:active {
  transform: translateY(0.5px) !important;
}

/* Secondary Button — Neon Chalk Green Outline */
button.secondary,
button[variant="secondary"],
.secondary {
  min-height: 42px;
  background: transparent !important;
  color: #5ebd72 !important;
  border: 2px dashed #5ebd72 !important;
  border-radius: 8px !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.38rem !important;
  font-weight: bold !important;
  padding: 6px 22px !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}

button.secondary:hover {
  background: rgba(94, 189, 114, 0.08) !important;
  box-shadow: 0 0 12px rgba(94, 189, 114, 0.35) !important;
  border-style: solid !important;
}

/* ══ PIPELINE STATUS WATERMARK ══ */
#kh-status {
  min-height: 100px;
  color: #ffffff !important;
  padding: 10px !important;
}

#kh-status h3 {
  color: #d9b84a !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.38rem !important;
  margin-top: 0;
}

#kh-status p {
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.25rem !important;
  color: rgba(255, 255, 255, 0.85) !important;
  line-height: 1.4 !important;
}

#kh-status code {
  color: #5ebd72 !important;
  background: rgba(94, 189, 114, 0.1) !important;
  border: 1px dashed rgba(94, 189, 114, 0.25) !important;
}

/* ══ STAT BOXES (INGEST STATS) ══ */
.kh-stat {
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 8px !important;
  padding: 8px 12px !important;
  background: rgba(0,0,0,0.18) !important;
}

/* ══ PREVIEW & METADATA SECTIONS ══ */
#kh-text-preview textarea {
  min-height: 400px !important;
  font-family: "JetBrains Mono", monospace !important;
  font-size: 0.86rem !important;
  background: rgba(0,0,0,0.3) !important;
  color: #e2e8f0 !important;
}

#kh-search-results, #kh-answer, #kh-reasoning {
  min-height: 180px;
  background: rgba(0, 0, 0, 0.24) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 8px !important;
  padding: 16px !important;
  color: #f1f5f9 !important;
}

#kh-search-results h3 {
  color: #5ebd72 !important;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.35rem !important;
  margin-top: 10px !important;
}

#kh-reasoning {
  font-family: "JetBrains Mono", monospace !important;
  font-size: 0.85rem !important;
  color: #94a3b8 !important;
}

/* ══ PROSE / MARKDOWN INTERNALS ══ */
.prose, .markdown,
.prose *, .markdown * {
  color: rgba(255, 255, 255, 0.85) !important;
  background: transparent !important;
}

.prose strong, .markdown strong {
  color: #ffffff !important;
}

.prose h3, .markdown h3 {
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif !important;
  font-size: 1.38rem !important;
  color: #ffffff !important;
}

code {
  color: #5ebd72 !important;
  background: rgba(94,189,114,0.08) !important;
  border: 1px solid rgba(94,189,114,0.2) !important;
  border-radius: 4px;
  padding: 1px 4px;
  font-family: "JetBrains Mono", monospace;
}

/* ══ RETRIEVE COLUMN WATERMARK & INDICATORS ══ */
.kh-retrieve-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding: 0 6px;
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif;
  font-size: 1.25rem;
  color: rgba(255,255,255,0.55);
}

.kh-online-status {
  display: flex;
  align-items: center;
  gap: 5px;
}

.kh-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  display: inline-block;
}

.kh-dot.green {
  background: #5ebd72;
  box-shadow: 0 0 6px #5ebd72;
}

.kh-brackets {
  font-size: 1.6rem;
  color: rgba(255, 255, 255, 0.35);
  font-weight: bold;
  letter-spacing: 2px;
}

/* ══ BOTTOM TRAY & COLORED CHALK PIECES ══ */
#kh-bottom-container {
  margin-top: 15px !important;
  background: transparent !important;
}

.kh-bottom-tray {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 10px 10px 0 10px;
  position: relative;
}

/* Wooden Tray Ledge below the board frame */
.kh-bottom-tray::before {
  content: "";
  position: absolute;
  bottom: -32px;
  left: -40px;
  right: -40px;
  height: 13px;
  background: linear-gradient(to bottom, #6d3f27, #442516);
  border-radius: 2px;
  box-shadow: 
    0 10px 18px rgba(0, 0, 0, 0.65), 
    inset 0 1px 0 rgba(255, 255, 255, 0.12);
  z-index: 5;
}

.kh-chalks {
  display: flex;
  gap: 10px;
  position: absolute;
  bottom: -31px;
  left: 20px;
  z-index: 6;
}

.kh-chalk {
  width: 30px;
  height: 7px;
  border-radius: 2px;
  box-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.kh-chalk.white {
  background: #f1f5f9;
  transform: rotate(2deg);
}

.kh-chalk.yellow {
  background: #e2c362;
  transform: rotate(-3deg);
}

.kh-chalk.purple {
  background: #d8b4fe;
  transform: rotate(5deg);
}

.kh-watermark {
  font-family: 'Gochi Hand', 'Caveat', cursive, sans-serif;
  font-size: 1.15rem;
  color: rgba(255, 255, 255, 0.35);
  margin-bottom: -15px;
  z-index: 6;
}

/* ══ SCROLLBARS ══ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.15); }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.25); }

/* ══ RESPONSIVE ══ */
@media (max-width: 768px) {
  #kh-shell { 
    padding: 25px 20px 45px 20px !important;
    border-width: 10px !important;
    margin: 15px auto !important;
  }
  .kh-bottom-tray::before {
    left: -20px;
    right: -20px;
  }
  #kh-title h1 { font-size: 2.3rem !important; }
}
"""
