import streamlit as st
import json
import pandas as pd
from datetime import datetime

from modules.summarizer import generate_handover
from modules.filter_data import filter_last_12_hours

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Shift Handover Generator",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Full Enterprise CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --navy-950:   #030712;
    --navy-900:   #060d1f;
    --navy-800:   #0a1628;
    --navy-700:   #0f2040;
    --navy-600:   #152a54;
    --blue-500:   #3b82f6;
    --blue-400:   #60a5fa;
    --blue-300:   #93c5fd;
    --purple-500: #8b5cf6;
    --purple-400: #a78bfa;
    --purple-300: #c4b5fd;
    --cyan-400:   #22d3ee;
    --cyan-300:   #67e8f9;
    --emerald-400:#34d399;
    --emerald-500:#10b981;
    --red-500:    #ef4444;
    --red-400:    #f87171;
    --amber-400:  #fbbf24;
    --amber-500:  #f59e0b;
    --glass-bg:        rgba(255,255,255,0.03);
    --glass-border:    rgba(255,255,255,0.07);
    --glass-bg-hover:  rgba(255,255,255,0.06);
    --glass-border-hover: rgba(255,255,255,0.14);
    --text-100: #f1f5f9;
    --text-200: #cbd5e1;
    --text-400: #94a3b8;
    --text-600: #475569;
    --font-sans: 'Inter', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --glow-blue:   0 0 24px rgba(59,130,246,0.35);
    --glow-purple: 0 0 24px rgba(139,92,246,0.35);
    --glow-cyan:   0 0 24px rgba(34,211,238,0.35);
    --r-sm: 8px; --r-md: 12px; --r-lg: 16px; --r-xl: 20px; --r-2xl: 28px;
}

html, body, .stApp {
    background: var(--navy-950) !important;
    font-family: var(--font-sans) !important;
    color: var(--text-200) !important;
}

/* Hide Streamlit branding & sidebar toggle */
#MainMenu, footer, header { visibility: hidden; }
.viewerBadge_container__1QSob { display: none; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(59,130,246,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 80%, rgba(139,92,246,0.08) 0%, transparent 60%),
        linear-gradient(180deg, var(--navy-950) 0%, #040e22 50%, #060820 100%);
    pointer-events: none;
    z-index: 0;
    animation: bg-shift 18s ease-in-out infinite alternate;
}

@keyframes bg-shift { 0%{opacity:1} 50%{opacity:0.7} 100%{opacity:1} }

.block-container {
    max-width: 1280px !important;
    padding: 0 2.5rem 5rem !important;
    position: relative;
    z-index: 1;
}

[data-testid="column"] { padding: 0 0.5rem !important; }

/* ── Hero Header ───────────────────────────────────────────────────────────── */
.hero-wrapper {
    position: relative;
    padding: 3rem 0 2.5rem;
    text-align: center;
    animation: fade-down 0.7s ease both;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--font-mono) !important;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--cyan-400);
    background: rgba(34,211,238,0.08);
    border: 1px solid rgba(34,211,238,0.18);
    border-radius: 20px;
    padding: 5px 14px;
    margin-bottom: 1.5rem;
}

.hero-eyebrow .dot {
    width: 5px; height: 5px;
    background: var(--cyan-400);
    border-radius: 50%;
    box-shadow: 0 0 6px var(--cyan-400);
    animation: blink 2s ease-in-out infinite;
}

.hero-title {
    font-family: var(--font-sans) !important;
    font-size: clamp(2.2rem, 4vw, 3.6rem);
    font-weight: 900;
    letter-spacing: -0.03em;
    line-height: 1.05;
    background: linear-gradient(135deg, var(--blue-300) 0%, var(--purple-300) 40%, var(--cyan-300) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 40px rgba(139,92,246,0.25));
}

.hero-subtitle {
    font-size: 1rem;
    color: var(--text-400);
    font-weight: 400;
    letter-spacing: 0.01em;
    margin-bottom: 2rem;
    max-width: 540px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
}

/* ── Section Label ─────────────────────────────────────────────────────────── */
.section-label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: var(--font-mono) !important;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-400);
    margin-bottom: 1rem;
    margin-top: 0.5rem;
}

.section-label::before {
    content: '';
    display: inline-block;
    width: 16px; height: 2px;
    background: linear-gradient(90deg, var(--blue-400), var(--purple-400));
    border-radius: 2px;
}

/* ── Glass Card ────────────────────────────────────────────────────────────── */
.glass-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--r-xl);
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    transition: border-color 0.25s, box-shadow 0.25s, background 0.25s;
    position: relative;
    overflow: hidden;
}

.glass-card:hover {
    background: var(--glass-bg-hover);
    border-color: var(--glass-border-hover);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), var(--glow-blue);
    transform: translateY(-2px);
}

.glass-card-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--blue-500), transparent);
    opacity: 0;
    transition: opacity 0.25s;
}

.glass-card:hover .glass-card-accent { opacity: 0.6; }

.upload-card-header { display: flex; align-items: center; gap: 0.85rem; margin-bottom: 1rem; }

.upload-icon-wrap {
    width: 40px; height: 40px;
    border-radius: var(--r-md);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}

.upload-icon-wrap.json {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.2));
    border: 1px solid rgba(139,92,246,0.25);
}

.upload-icon-wrap.csv {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(52,211,153,0.18));
    border: 1px solid rgba(52,211,153,0.22);
}

.upload-card-title { font-size: 0.88rem; font-weight: 600; color: var(--text-100); letter-spacing: -0.01em; }
.upload-card-desc  { font-size: 0.73rem; color: var(--text-400); margin-top: 2px; }

.format-pill {
    display: inline-block;
    font-family: var(--font-mono) !important;
    font-size: 0.6rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 2px 7px; border-radius: 4px;
}

.format-pill.json { background: rgba(139,92,246,0.1); color: var(--purple-400); border: 1px solid rgba(139,92,246,0.2); }
.format-pill.csv  { background: rgba(52,211,153,0.08); color: var(--emerald-400); border: 1px solid rgba(52,211,153,0.18); }

[data-testid="stFileUploader"] { background: transparent !important; }

[data-testid="stFileUploader"] > div {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(255,255,255,0.1) !important;
    border-radius: var(--r-md) !important;
    transition: all 0.25s !important;
}

[data-testid="stFileUploader"] > div:hover {
    border-color: rgba(59,130,246,0.4) !important;
    background: rgba(59,130,246,0.04) !important;
}

/* ── Status Banner ─────────────────────────────────────────────────────────── */
.status-banner {
    display: flex; align-items: center; gap: 0.85rem;
    background: rgba(16,185,129,0.07);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: var(--r-md);
    padding: 0.9rem 1.25rem;
    margin: 1.5rem 0;
    font-size: 0.82rem;
    color: var(--emerald-400);
    animation: fade-up 0.4s ease both;
}

.status-icon-ring {
    width: 28px; height: 28px;
    background: rgba(16,185,129,0.12);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; flex-shrink: 0;
}

/* ── AI Status Panel ───────────────────────────────────────────────────────── */
.ai-status-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--r-xl);
    padding: 1.4rem;
    animation: fade-up 0.5s ease both 0.1s;
}

.ai-status-title {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--text-400);
    margin-bottom: 1rem;
}

.ai-status-row {
    display: flex; align-items: center; gap: 0.65rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.78rem; color: var(--text-200);
}

.ai-status-row:last-child { border-bottom: none; }

.status-dot-green {
    width: 7px; height: 7px;
    background: var(--emerald-400);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--emerald-400);
    flex-shrink: 0;
    animation: pulse-green 2s ease-in-out infinite;
}

@keyframes pulse-green { 0%,100%{opacity:1} 50%{opacity:0.5} }

/* ── Pipeline Flow ─────────────────────────────────────────────────────────── */
.pipeline-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--r-xl);
    padding: 1.4rem;
    margin-top: 1rem;
}

.pipeline-title {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--text-400);
    margin-bottom: 1.1rem;
}

.pipeline-node {
    display: flex; align-items: center; gap: 0.7rem;
    padding: 0.45rem 0;
    font-size: 0.77rem; color: var(--text-200);
}

.pipeline-node-dot {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; flex-shrink: 0;
}

.pipeline-node-dot.blue   { background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.3); }
.pipeline-node-dot.purple { background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.3); }
.pipeline-node-dot.cyan   { background: rgba(34,211,238,0.12); border: 1px solid rgba(34,211,238,0.25); }
.pipeline-node-dot.green  { background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.25); }

.pipeline-connector {
    width: 1px; height: 14px;
    background: linear-gradient(to bottom, rgba(59,130,246,0.3), rgba(139,92,246,0.3));
    margin-left: 13.5px;
    position: relative; overflow: hidden;
}

.pipeline-connector::after {
    content: '';
    position: absolute; top: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(to bottom, transparent, var(--cyan-400), transparent);
    animation: flow-down 2.4s linear infinite;
}

@keyframes flow-down { 0%{top:-100%} 100%{top:100%} }

/* ── Generate Section ──────────────────────────────────────────────────────── */
.generate-wrapper {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--r-2xl);
    padding: 2rem 2.25rem;
    position: relative; overflow: hidden;
    animation: fade-up 0.5s ease both 0.15s;
}

.generate-title {
    font-size: 1.05rem; font-weight: 700;
    color: var(--text-100); letter-spacing: -0.02em;
    margin-bottom: 0.35rem;
}

.generate-desc {
    font-size: 0.8rem; color: var(--text-400);
    line-height: 1.6; margin-bottom: 1.75rem; max-width: 500px;
}

.pipeline-steps-row {
    display: flex; gap: 0;
    margin-bottom: 1.75rem;
    border-radius: var(--r-md);
    overflow: hidden;
    border: 1px solid var(--glass-border);
}

.ps-step {
    flex: 1; padding: 0.65rem 0.75rem;
    background: rgba(255,255,255,0.02);
    font-size: 0.7rem; color: var(--text-400);
    text-align: center;
    border-right: 1px solid var(--glass-border);
    font-weight: 500;
    transition: background 0.2s;
}

.ps-step:last-child { border-right: none; }
.ps-step:hover { background: rgba(59,130,246,0.06); color: var(--blue-300); }

.ps-step-num {
    display: block;
    font-family: var(--font-mono) !important;
    font-size: 0.58rem;
    color: var(--text-600);
    margin-bottom: 2px;
}

/* ── Button ────────────────────────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--blue-500), var(--purple-500)) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--r-md) !important;
    padding: 0.9rem 2rem !important;
    font-family: var(--font-sans) !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.3) !important;
}

[data-testid="stButton"] > button:hover {
    box-shadow: 0 8px 32px rgba(59,130,246,0.45), 0 0 0 1px rgba(139,92,246,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── KPI Cards ─────────────────────────────────────────────────────────────── */
.kpi-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--r-xl);
    padding: 1.5rem 1.75rem;
    position: relative; overflow: hidden;
    transition: all 0.25s; cursor: default;
}

.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,0.35); }
.kpi-card.red:hover  { box-shadow: 0 12px 40px rgba(0,0,0,0.35), 0 0 20px rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.3); }
.kpi-card.green:hover{ box-shadow: 0 12px 40px rgba(0,0,0,0.35), 0 0 20px rgba(52,211,153,0.15); border-color: rgba(52,211,153,0.3); }
.kpi-card.blue:hover { box-shadow: 0 12px 40px rgba(0,0,0,0.35), 0 0 20px rgba(59,130,246,0.15); border-color: rgba(59,130,246,0.3); }

.kpi-glow {
    position: absolute; top: 0; right: 0;
    width: 120px; height: 120px;
    border-radius: 50%; pointer-events: none; opacity: 0.08;
}

.kpi-glow.red   { background: radial-gradient(circle, var(--red-500), transparent 70%); }
.kpi-glow.green { background: radial-gradient(circle, var(--emerald-400), transparent 70%); }
.kpi-glow.blue  { background: radial-gradient(circle, var(--blue-500), transparent 70%); }

.kpi-label {
    font-family: var(--font-mono) !important;
    font-size: 0.62rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--text-400); margin-bottom: 0.6rem;
}

.kpi-value { font-family: var(--font-sans) !important; font-size: 2.8rem; font-weight: 900; letter-spacing: -0.04em; line-height: 1; }
.kpi-value.red   { color: var(--red-400);     text-shadow: 0 0 24px rgba(239,68,68,0.35); }
.kpi-value.green { color: var(--emerald-400); text-shadow: 0 0 24px rgba(52,211,153,0.35); }
.kpi-value.blue  { color: var(--blue-400);    text-shadow: 0 0 24px rgba(59,130,246,0.35); }
.kpi-sub { font-size: 0.72rem; color: var(--text-600); margin-top: 0.4rem; }

/* ── Report Viewer ─────────────────────────────────────────────────────────── */
.report-viewer {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--r-2xl);
    padding: 2.5rem 3rem;
    animation: fade-up 0.5s ease both;
    margin-top: 1rem;
}

.report-viewer h1, .report-viewer h2 {
    font-family: var(--font-sans) !important;
    color: var(--text-100) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    border-bottom: 1px solid var(--glass-border) !important;
    padding-bottom: 0.6rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
    background: linear-gradient(135deg, var(--blue-300), var(--purple-300));
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

.report-viewer h3 {
    font-size: 0.95rem !important; font-weight: 600 !important;
    color: var(--text-200) !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    padding-bottom: 0.4rem !important; margin-top: 1.5rem !important; margin-bottom: 0.75rem !important;
}

.report-viewer p, .report-viewer li { font-size: 0.875rem !important; color: var(--text-200) !important; line-height: 1.8 !important; }
.report-viewer strong { color: var(--text-100) !important; font-weight: 600 !important; }
.report-viewer ul { padding-left: 1.25rem !important; }
.report-viewer li { margin-bottom: 0.35rem !important; }

[data-testid="stDownloadButton"] > button {
    background: rgba(59,130,246,0.08) !important;
    color: var(--blue-400) !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
    border-radius: var(--r-md) !important;
    padding: 0.65rem 1.5rem !important;
    font-size: 0.8rem !important; font-weight: 500 !important;
    transition: all 0.2s !important;
}

[data-testid="stMetric"] { display: none !important; }

.warn-banner {
    display: flex; align-items: center; gap: 0.75rem;
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: var(--r-md);
    padding: 0.9rem 1.25rem;
    font-size: 0.82rem; color: var(--amber-400);
    margin-top: 1rem;
}

.idle-state {
    margin-top: 2rem;
    padding: 3.5rem 2rem;
    text-align: center;
    border: 1.5px dashed rgba(255,255,255,0.07);
    border-radius: var(--r-2xl);
    background: var(--glass-bg);
    animation: fade-up 0.5s ease both 0.2s;
}

.idle-ring {
    width: 64px; height: 64px;
    background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.12));
    border: 1.5px solid rgba(139,92,246,0.2);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; margin: 0 auto 1.25rem;
}

.idle-title { font-size: 0.9rem; font-weight: 600; color: var(--text-200); margin-bottom: 0.4rem; }
.idle-desc  { font-size: 0.77rem; color: var(--text-600); }

hr { border-color: var(--glass-border) !important; margin: 2.5rem 0 !important; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(59,130,246,0.25); border-radius: 4px; }

@keyframes fade-up   { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
@keyframes fade-down { from{opacity:0;transform:translateY(-12px)} to{opacity:1;transform:translateY(0)} }
@keyframes blink     { 0%,100%{opacity:1} 50%{opacity:0.3} }
@keyframes shimmer   { 0%{background-position:200% center} 100%{background-position:-200% center} }

.stMarkdown p { color: var(--text-400) !important; font-size: 0.85rem !important; }

.hero-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
    margin: 0 0 2.5rem;
}

.loading-block {
    background: var(--glass-bg); border: 1px solid var(--glass-border);
    border-radius: var(--r-xl); padding: 3rem 2rem;
    text-align: center; animation: fade-up 0.3s ease both;
}

.loading-bar {
    height: 2px;
    background: linear-gradient(90deg, var(--navy-800) 0%, var(--blue-500) 30%, var(--purple-400) 60%, var(--cyan-400) 80%, var(--navy-800) 100%);
    background-size: 200% 100%; border-radius: 2px;
    animation: shimmer 1.5s linear infinite;
    margin: 0 auto 1.25rem; max-width: 380px;
}
</style>
""", unsafe_allow_html=True)


# ─── Spider Widget — injected into parent page via components.html ─────────────
import streamlit.components.v1 as components

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background: transparent; overflow: hidden; }

  #spider-wrap {
    position: fixed;
    top: 0;
    right: 90px;
    z-index: 999999;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    user-select: none;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
  }

  /* Web thread */
  #spider-thread {
    width: 2px;
    height: 55px;
    background: linear-gradient(to bottom, rgba(255,255,255,0.35), rgba(255,255,255,0.06));
    transition: height 0.5s cubic-bezier(0.34,1.4,0.64,1);
  }

  /* Whole spider swings */
  #spider-body {
    animation: swing 3s ease-in-out infinite;
    transform-origin: top center;
    position: relative;
    width: 56px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  @keyframes swing {
    0%,100% { transform: rotate(-7deg); }
    50%      { transform: rotate(7deg); }
  }

  /* HEAD */
  #spider-head {
    width: 24px;
    height: 22px;
    background: radial-gradient(circle at 38% 32%, #303030, #111);
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.18);
    box-shadow: 0 2px 8px rgba(0,0,0,0.6);
    position: relative;
    z-index: 2;
  }

  .eye {
    position: absolute;
    width: 7px;
    height: 7px;
    background: #ef4444;
    border-radius: 50%;
    top: 7px;
    box-shadow: 0 0 7px #ef4444, 0 0 14px rgba(239,68,68,0.55);
    animation: blink 2.6s ease-in-out infinite;
  }
  .eye.L { left: 3px; }
  .eye.R { right: 3px; animation-delay: 0.18s; }

  @keyframes blink {
    0%,88%,100% { transform: scaleY(1);   opacity: 1;   }
    91%,97%     { transform: scaleY(0.08); opacity: 0.25; }
  }

  /* ABDOMEN */
  #spider-abdomen {
    width: 30px;
    height: 34px;
    background: radial-gradient(circle at 38% 28%, #1c1c30, #0c0c18);
    border-radius: 48% 48% 56% 56%;
    border: 1px solid rgba(139,92,246,0.35);
    box-shadow: 0 0 14px rgba(139,92,246,0.22), inset 0 2px 5px rgba(255,255,255,0.06);
    margin-top: -4px;
    position: relative;
    z-index: 1;
  }

  #spider-abdomen::after {
    content: '';
    position: absolute;
    top: 9px; left: 50%;
    transform: translateX(-50%);
    width: 11px; height: 15px;
    background: radial-gradient(ellipse, rgba(139,92,246,0.45), transparent);
    border-radius: 50%;
  }

  /* LEGS — positioned absolutely relative to #spider-body */
  .legs-wrap {
    position: absolute;
    top: 18px;
    width: 100%;
    height: 0;
  }

  .leg {
    position: absolute;
    width: 22px;
    height: 2px;
    background: rgba(255,255,255,0.28);
    border-radius: 2px;
  }

  /* left legs */
  .leg.ll1 { left: -4px; top: -8px;  transform: rotate(-40deg); transform-origin: right center; animation: lw 1.1s ease-in-out infinite alternate; }
  .leg.ll2 { left: -4px; top:  0px;  transform: rotate(-12deg); transform-origin: right center; animation: lw 1.1s ease-in-out infinite alternate 0.1s; }
  .leg.ll3 { left: -4px; top:  8px;  transform: rotate( 16deg); transform-origin: right center; animation: lw 1.1s ease-in-out infinite alternate 0.2s; }

  /* right legs */
  .leg.lr1 { right: -4px; top: -8px; transform: rotate(220deg); transform-origin: left center; animation: lw 1.1s ease-in-out infinite alternate 0.05s; }
  .leg.lr2 { right: -4px; top:  0px; transform: rotate(192deg); transform-origin: left center; animation: lw 1.1s ease-in-out infinite alternate 0.15s; }
  .leg.lr3 { right: -4px; top:  8px; transform: rotate(164deg); transform-origin: left center; animation: lw 1.1s ease-in-out infinite alternate 0.25s; }

  @keyframes lw {
    from { opacity: 0.7; }
    to   { opacity: 1; transform: rotate(calc(var(--r,0deg) + 9deg)); }
  }

  /* TOOLTIP — shown on hover */
  #spider-tooltip {
    position: absolute;
    top: 120px;
    right: -10px;
    background: rgba(4, 10, 24, 0.97);
    border: 1px solid rgba(139,92,246,0.4);
    border-radius: 14px;
    padding: 14px 18px;
    min-width: 175px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6), 0 0 22px rgba(139,92,246,0.18);
    opacity: 0;
    pointer-events: none;
    transform: scale(0.88) translateY(-8px);
    transition: opacity 0.22s ease, transform 0.22s ease;
    white-space: nowrap;
  }

  /* Show tooltip on hover over entire wrap */
  #spider-wrap:hover #spider-tooltip {
    opacity: 1;
    pointer-events: auto;
    transform: scale(1) translateY(0);
  }

  /* Extend thread on hover */
  #spider-wrap:hover #spider-thread {
    height: 85px;
  }

  .tt-label {
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #22d3ee;
    margin-bottom: 5px;
  }

  .tt-time-val {
    font-size: 20px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 0.04em;
    line-height: 1.1;
  }

  .tt-date-val {
    font-size: 11px;
    color: #94a3b8;
    margin-top: 4px;
    letter-spacing: 0.06em;
  }

  .live-row {
    display: flex;
    align-items: center;
    gap: 7px;
    margin-bottom: 6px;
  }

  .live-dot {
    width: 7px; height: 7px;
    background: #ef4444;
    border-radius: 50%;
    box-shadow: 0 0 6px #ef4444;
    animation: pulse 1.4s ease-in-out infinite;
    flex-shrink: 0;
  }

  .live-text {
    font-size: 9px;
    letter-spacing: 0.16em;
    color: #f87171;
    text-transform: uppercase;
  }

  @keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(239,68,68,0.85); }
    50%  { box-shadow: 0 0 0 5px rgba(239,68,68,0); }
    100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
  }
</style>
</head>
<body>

<div id="spider-wrap">
  <div id="spider-thread"></div>
  <div id="spider-body">
    <div class="legs-wrap">
      <div class="leg ll1"></div>
      <div class="leg ll2"></div>
      <div class="leg ll3"></div>
      <div class="leg lr1"></div>
      <div class="leg lr2"></div>
      <div class="leg lr3"></div>
    </div>
    <div id="spider-head">
      <div class="eye L"></div>
      <div class="eye R"></div>
    </div>
    <div id="spider-abdomen"></div>
  </div>

  <div id="spider-tooltip">
    <div class="live-row">
      <div class="live-dot"></div>
      <div class="live-text">Live</div>
    </div>
    <div class="tt-time-val" id="tt-time">--:--:--</div>
    <div class="tt-date-val" id="tt-date">-- --- ----</div>
  </div>
</div>

<script>
  function tick() {
    var now = new Date();
    var h = String(now.getHours()).padStart(2,'0');
    var m = String(now.getMinutes()).padStart(2,'0');
    var s = String(now.getSeconds()).padStart(2,'0');
    var months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
    var day  = String(now.getDate()).padStart(2,'0');
    var mon  = months[now.getMonth()];
    var year = now.getFullYear();
    document.getElementById('tt-time').textContent = h+':'+m+':'+s;
    document.getElementById('tt-date').textContent = day+' '+mon+' '+year;
  }
  tick();
  setInterval(tick, 1000);

  // Inject this widget into the PARENT page so position:fixed works correctly
  var me = document.currentScript || (function(){
    var s = document.getElementsByTagName('script');
    return s[s.length-1];
  })();

  function injectIntoParent() {
    try {
      var parent = window.parent.document;
      if (parent.getElementById('spider-injected')) return;

      // Clone the whole body HTML + styles into parent
      var styleEl = document.createElement('style');
      styleEl.id = 'spider-style-injected';
      var css = '';
      for (var i = 0; i < document.styleSheets.length; i++) {
        try {
          var rules = document.styleSheets[i].cssRules;
          for (var j = 0; j < rules.length; j++) css += rules[j].cssText + '\\n';
        } catch(e){}
      }
      styleEl.textContent = css;
      parent.head.appendChild(styleEl);

      var div = document.createElement('div');
      div.id = 'spider-injected';
      div.innerHTML = document.getElementById('spider-wrap').outerHTML;
      parent.body.appendChild(div);

      // Re-run clock in parent context
      function parentTick() {
        var now = new Date();
        var h = String(now.getHours()).padStart(2,'0');
        var m = String(now.getMinutes()).padStart(2,'0');
        var s = String(now.getSeconds()).padStart(2,'0');
        var months=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
        var day=String(now.getDate()).padStart(2,'0');
        var mon=months[now.getMonth()];
        var year=now.getFullYear();
        var tEl = parent.getElementById('tt-time');
        var dEl = parent.getElementById('tt-date');
        if(tEl) tEl.textContent = h+':'+m+':'+s;
        if(dEl) dEl.textContent = day+' '+mon+' '+year;
      }
      parentTick();
      setInterval(parentTick, 1000);

    } catch(e) {
      // Cross-origin restriction — fallback: keep in iframe but use position:fixed
      document.body.style.overflow = 'visible';
    }
  }

  // Wait for parent DOM
  if (document.readyState === 'complete') {
    injectIntoParent();
  } else {
    window.addEventListener('load', injectIntoParent);
  }
</script>
</body>
</html>
""", height=0, scrolling=False)


# ─── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-eyebrow">
        <span class="dot"></span>
        Enterprise Operations Intelligence
    </div>
    <h1 class="hero-title">Shift Handover Generator</h1>
</div>
<div class="hero-divider"></div>
""", unsafe_allow_html=True)


# ─── Main Layout ───────────────────────────────────────────────────────────────
main_col, side_col = st.columns([3, 1], gap="large")

with side_col:
    st.markdown("""
    <div class="ai-status-card">
        <div class="ai-status-title">🤖 AI System Status</div>
        <div class="ai-status-row">
            <div class="status-dot-green"></div>
            Summarizer Agent
            <span style="margin-left:auto;font-family:var(--font-mono);font-size:0.62rem;color:#22d3ee;">ACTIVE</span>
        </div>
        <div class="ai-status-row">
            <div class="status-dot-green"></div>
            Review Agent
            <span style="margin-left:auto;font-family:var(--font-mono);font-size:0.62rem;color:#22d3ee;">ACTIVE</span>
        </div>
        <div class="ai-status-row">
            <div class="status-dot-green"></div>
            LLM Backend
            <span style="margin-left:auto;font-family:var(--font-mono);font-size:0.62rem;color:#22d3ee;">READY</span>
        </div>
        <div class="ai-status-row">
            <div class="status-dot-green"></div>
            System Status
            <span style="margin-left:auto;font-family:var(--font-mono);font-size:0.62rem;color:#34d399;">OPERATIONAL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="pipeline-card">
        <div class="pipeline-title">⚡ AI Pipeline</div>
        <div class="pipeline-node">
            <div class="pipeline-node-dot blue">📁</div>
            <span>Chat Logs</span>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node">
            <div class="pipeline-node-dot blue">🕐</div>
            <span>12-Hour Filter</span>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node">
            <div class="pipeline-node-dot purple">🤖</div>
            <span>Summarizer Agent</span>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node">
            <div class="pipeline-node-dot purple">⚙</div>
            <span>Deduplication Engine</span>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node">
            <div class="pipeline-node-dot cyan">🔍</div>
            <span>Review Agent</span>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node">
            <div class="pipeline-node-dot green">📋</div>
            <span>Final Report</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


with main_col:
    st.markdown('<div class="section-label">Data Inputs</div>', unsafe_allow_html=True)

    ul_left, ul_right = st.columns(2, gap="medium")

    with ul_left:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:0.5rem;">
            <div class="glass-card-accent"></div>
            <div class="upload-card-header">
                <div class="upload-icon-wrap json">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14,2 14,8 20,8"/>
                        <line x1="8" y1="13" x2="16" y2="13"/>
                        <line x1="8" y1="17" x2="16" y2="17"/>
                    </svg>
                </div>
                <div>
                    <div class="upload-card-title">Chat Logs</div>
                    <div class="upload-card-desc">Engineering channel messages &nbsp;·&nbsp; <span class="format-pill json">JSON</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        chat_file = st.file_uploader("Chat JSON", type=["json"], label_visibility="collapsed")

    with ul_right:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:0.5rem;">
            <div class="glass-card-accent"></div>
            <div class="upload-card-header">
                <div class="upload-icon-wrap csv">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="2"/>
                        <line x1="3" y1="9" x2="21" y2="9"/>
                        <line x1="3" y1="15" x2="21" y2="15"/>
                        <line x1="9" y1="9" x2="9" y2="21"/>
                    </svg>
                </div>
                <div>
                    <div class="upload-card-title">Ticket Records</div>
                    <div class="upload-card-desc">Incident & task tracking data &nbsp;·&nbsp; <span class="format-pill csv">CSV</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        ticket_file = st.file_uploader("Ticket CSV", type=["csv"], label_visibility="collapsed")

    if chat_file and ticket_file:
        chats = json.load(chat_file)
        tickets = pd.read_csv(ticket_file)
        chats, tickets = filter_last_12_hours(chats, tickets)

        st.markdown(f"""
        <div class="status-banner">
            <div class="status-icon-ring">✓</div>
            <div>
                <strong style="color:#34d399;">{len(chats)}</strong> chat messages &nbsp;·&nbsp;
                <strong style="color:#34d399;">{len(tickets)}</strong> ticket records &nbsp;·&nbsp;
                Filtered to last 12 hours — ready to generate
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:1.5rem;">Report Generation</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="generate-wrapper">
            <div class="generate-title">Generate Shift Handover Report</div>
            <div class="generate-desc">
                The AI analyses all inputs, deduplicates incidents, classifies severity,
                and produces a structured report reviewed by a quality agent.
            </div>
            <div class="pipeline-steps-row">
                <div class="ps-step"><span class="ps-step-num">01</span>Summarise</div>
                <div class="ps-step"><span class="ps-step-num">02</span>Classify</div>
                <div class="ps-step"><span class="ps-step-num">03</span>Deduplicate</div>
                <div class="ps-step"><span class="ps-step-num">04</span>Review</div>
                <div class="ps-step"><span class="ps-step-num">05</span>Report</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡  Generate Handover Report", use_container_width=True):
            loading_placeholder = st.empty()
            loading_placeholder.markdown("""
            <div class="loading-block">
                <div style="font-size:0.85rem;color:var(--text-200);font-weight:500;margin-bottom:1.5rem;">⚙ &nbsp; AI Analysis in Progress</div>
                <div class="loading-bar"></div>
                <div style="font-family:var(--font-mono);font-size:0.68rem;color:var(--text-600);letter-spacing:0.05em;">
                    Summarising incidents · Classifying severity · Deduplicating entries · Review agent pass
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("Generating AI handover report..."):
                report = generate_handover(chats, tickets)

            loading_placeholder.empty()

            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            open_issues = len(tickets[tickets["status"].astype(str).str.lower().isin(["open", "critical", "high"])])
            resolved_issues = len(tickets[tickets["status"].astype(str).str.lower().isin(["resolved", "closed", "fixed"])])
            watchlist_items = len(tickets[tickets["status"].astype(str).str.lower().isin(["monitoring", "watchlist"])])

            full_report = f"""# Shift Handover Report\n\n**Generated On:** {current_time}\n\n{report}"""

            import os
            os.makedirs("output", exist_ok=True)
            with open("output/handover_note.md", "w", encoding="utf-8") as f:
                f.write(full_report)

            st.success("✅  Report generated and saved to output/handover_note.md")

            st.markdown('<div class="section-label" style="margin-top:2rem;">Incident Dashboard</div>', unsafe_allow_html=True)

            k1, k2, k3 = st.columns(3, gap="medium")
            with k1:
                st.markdown(f'<div class="kpi-card red"><div class="kpi-glow red"></div><div class="kpi-label">🔴 Open Issues</div><div class="kpi-value red">{open_issues}</div><div class="kpi-sub">Active incidents</div></div>', unsafe_allow_html=True)
            with k2:
                st.markdown(f'<div class="kpi-card green"><div class="kpi-glow green"></div><div class="kpi-label">🟢 Resolved Issues</div><div class="kpi-value green">{resolved_issues}</div><div class="kpi-sub">Closed this shift</div></div>', unsafe_allow_html=True)
            with k3:
                st.markdown(f'<div class="kpi-card blue"><div class="kpi-glow blue"></div><div class="kpi-label">🔵 Watchlist Items</div><div class="kpi-value blue">{watchlist_items}</div><div class="kpi-sub">Under monitoring</div></div>', unsafe_allow_html=True)

            st.divider()

            st.markdown(f'<div class="section-label">Handover Report &nbsp;·&nbsp; {current_time}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="report-viewer">{full_report}</div>', unsafe_allow_html=True)

            dl_col, info_col = st.columns([1, 2], gap="medium")
            with dl_col:
                st.download_button(label="⬇️  Download Report (.md)", data=full_report, file_name="handover_note.md", mime="text/markdown", use_container_width=True)
            with info_col:
                st.info("Report also saved locally at: `output/handover_note.md`")

    elif chat_file or ticket_file:
        missing = "Ticket CSV" if chat_file else "Chat JSON"
        st.markdown(f'<div class="warn-banner"><span>⚠</span><span>Waiting for <strong>{missing}</strong> — both files are required to generate a report.</span></div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="idle-state">
            <div class="idle-ring">📂</div>
            <div class="idle-title">Upload both files to get started</div>
            <div class="idle-desc">Drop a JSON chat log and a CSV ticket export above</div>
        </div>
        """, unsafe_allow_html=True)


# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:4rem;padding:2rem 0 1rem;border-top:1px solid rgba(255,255,255,0.05);text-align:center;">
    <div style="font-size:0.85rem;font-weight:700;color:#f1f5f9;letter-spacing:-0.01em;margin-bottom:0.3rem;">Shift Handover Generator</div>
    <div style="font-size:0.72rem;color:#475569;margin-bottom:0.5rem;">AI-Powered Multi-Source Incident Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)
