HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
"""

JS = """
() => {
  const root = document.querySelector('.gradio-container');
  if (!root) return;
  root.dataset.ready = 'true';
  const marker = document.createElement('div');
  marker.className = 'kh-scanline';
  root.prepend(marker);
}
"""

CSS = """
:root {
  --kh-bg: #080b0f;
  --kh-surface: rgba(18, 24, 32, 0.78);
  --kh-surface-strong: rgba(27, 36, 48, 0.92);
  --kh-ink: #f7fbff;
  --kh-muted: #a7b4c2;
  --kh-soft: #d8e1ea;
  --kh-line: rgba(255, 255, 255, 0.12);
  --kh-cyan: #20d6c7;
  --kh-lime: #b8f45d;
  --kh-rose: #ff6b8a;
  --kh-amber: #ffcf5c;
  --kh-shadow: rgba(0, 0, 0, 0.32);
}

.gradio-container {
  min-height: 100vh;
  background:
    radial-gradient(circle at 18% 8%, rgba(32, 214, 199, 0.22), transparent 30%),
    radial-gradient(circle at 86% 12%, rgba(255, 207, 92, 0.16), transparent 28%),
    linear-gradient(135deg, #080b0f 0%, #101720 48%, #0b1017 100%) !important;
  color: var(--kh-ink);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.kh-scanline {
  position: fixed;
  inset: 0;
  pointer-events: none;
  background-image: linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px);
  background-size: 100% 4px;
  mask-image: linear-gradient(to bottom, transparent, black 18%, black 72%, transparent);
  opacity: 0.18;
  z-index: 0;
}

#kh-shell {
  position: relative;
  z-index: 1;
  max-width: 1220px;
  margin: 0 auto;
  padding: 28px 18px 42px;
}

#kh-title {
  padding: 34px 0 22px;
  border-bottom: 1px solid var(--kh-line);
}

#kh-title h1 {
  max-width: 920px;
  color: var(--kh-ink);
  font-size: clamp(2.6rem, 6vw, 6rem);
  font-weight: 800;
  line-height: 0.9;
  margin: 0 0 14px;
  letter-spacing: 0;
}

#kh-title p {
  max-width: 780px;
  color: var(--kh-muted);
  font-size: 1.04rem;
  line-height: 1.65;
}

#kh-title code,
.kh-chip code {
  color: var(--kh-lime);
  background: rgba(184, 244, 93, 0.09);
  border: 1px solid rgba(184, 244, 93, 0.18);
  border-radius: 6px;
  padding: 2px 6px;
  font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}

.kh-panel {
  border: 1px solid var(--kh-line);
  border-radius: 8px;
  background: linear-gradient(180deg, var(--kh-surface-strong), var(--kh-surface));
  box-shadow: 0 24px 70px var(--kh-shadow);
  backdrop-filter: blur(18px);
  padding: 18px !important;
}

.kh-panel label,
.kh-panel .label-wrap span {
  color: var(--kh-soft) !important;
  font-weight: 700 !important;
}

.kh-subhead {
  margin: 8px 0 16px;
  color: var(--kh-muted);
  font-size: 0.95rem;
}

.kh-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}

.kh-chip {
  border: 1px solid var(--kh-line);
  border-radius: 999px;
  padding: 8px 12px;
  color: var(--kh-soft);
  background: rgba(255, 255, 255, 0.055);
  font-size: 0.9rem;
}

.kh-stat {
  min-height: 92px;
  border: 1px solid var(--kh-line);
  border-radius: 8px;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.055);
}

.kh-stat .wrap,
.kh-stat input {
  background: transparent !important;
}

.tabs {
  margin-top: 20px;
}

.tab-nav button {
  color: var(--kh-muted) !important;
  border-radius: 8px !important;
  font-weight: 700 !important;
}

.tab-nav button.selected {
  color: var(--kh-ink) !important;
  background: linear-gradient(135deg, rgba(32, 214, 199, 0.22), rgba(184, 244, 93, 0.12)) !important;
  border: 1px solid rgba(32, 214, 199, 0.34) !important;
}

textarea,
input {
  color: var(--kh-ink) !important;
  background: rgba(3, 7, 12, 0.52) !important;
  border-color: rgba(255, 255, 255, 0.12) !important;
  font-size: 0.96rem !important;
}

textarea::placeholder,
input::placeholder {
  color: rgba(216, 225, 234, 0.46) !important;
}

#kh-status {
  min-height: 130px;
}

#kh-status h3 {
  color: var(--kh-lime);
  margin-top: 0;
}

#kh-text-preview textarea {
  min-height: 430px !important;
  line-height: 1.6 !important;
  font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace !important;
  font-size: 0.9rem !important;
}

#kh-search-results {
  min-height: 410px;
}

#kh-answer,
#kh-reasoning {
  min-height: 240px;
}

#kh-answer {
  font-size: 1.02rem;
  line-height: 1.7;
}

#kh-search-results h3 {
  color: var(--kh-cyan);
}

#kh-reasoning {
  color: var(--kh-muted);
  font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.86rem;
  line-height: 1.6;
}

.prose,
.markdown {
  color: var(--kh-soft) !important;
}

.prose strong,
.markdown strong {
  color: var(--kh-ink) !important;
}

button.primary {
  min-height: 46px;
  background: linear-gradient(135deg, var(--kh-cyan), var(--kh-lime)) !important;
  color: #061015 !important;
  border: 0 !important;
  border-radius: 8px !important;
  font-weight: 800 !important;
  box-shadow: 0 16px 34px rgba(32, 214, 199, 0.2);
}

button.secondary {
  border-radius: 8px !important;
}

.file-preview,
.upload-container {
  border-color: rgba(32, 214, 199, 0.26) !important;
  background: rgba(32, 214, 199, 0.055) !important;
}

@media (max-width: 760px) {
  #kh-shell {
    padding: 18px 10px 32px;
  }

  #kh-title h1 {
    font-size: clamp(2.25rem, 15vw, 4.2rem);
  }

  .kh-panel {
    padding: 14px !important;
  }
}
"""
