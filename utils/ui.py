"""Shared UI helpers for the 6th Tirumurai blog."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.loader import PageContent, is_filled

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
VALLALAR_IMAGE = ASSETS_DIR / "vallalar.jpg"
LIGHT_WORKER_IMAGES = [
    ASSETS_DIR / "light_worker_1.jpg",
    ASSETS_DIR / "light_worker_2.jpg",
]
MAHAMANTRA_IMAGE = ASSETS_DIR / "mahamantra.png"


def apply_styles() -> None:
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Tiro+Tamil:ital@0;1&family=Noto+Sans+Telugu&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
        <style>
        .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2b1608 0%, #4a2812 55%, #6b3a18 100%);
        }
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown li,
        [data-testid="stSidebar"] .stMarkdown strong,
        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #fff8ef !important;
        }
        [data-testid="stSidebar"] input[type="number"],
        [data-testid="stSidebar"] input[type="text"] {
            background: #fff8ef !important;
            color: #2b1608 !important;
            border: 1px solid #c9923e !important;
            caret-color: #2b1608 !important;
        }
        [data-testid="stSidebar"] input::placeholder {
            color: #8a6135 !important;
        }
        [data-testid="stSidebar"] [data-testid="stNumberInputStepUp"],
        [data-testid="stSidebar"] [data-testid="stNumberInputStepDown"],
        [data-testid="stSidebar"] [data-testid="stNumberInputStepUp"] button,
        [data-testid="stSidebar"] [data-testid="stNumberInputStepDown"] button {
            color: #2b1608 !important;
            background: #f5e6d3 !important;
            border-color: #c9923e !important;
        }
        [data-testid="stSidebar"] .stButton > button {
            background: #fff8ef !important;
            color: #4a2812 !important;
            border: 1px solid #c9923e !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: #f5e6d3 !important;
            border-color: #b8860b !important;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: #fff8ef !important;
            color: #2b1608 !important;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label,
        [data-testid="stSidebar"] [data-testid="stRadio"] label span,
        [data-testid="stSidebar"] [data-testid="stRadio"] label p,
        [data-testid="stSidebar"] [data-testid="stRadio"] label div {
            color: #2b1608 !important;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            background: #fff8ef !important;
            border: 1px solid #c9923e !important;
            border-radius: 0.65rem !important;
            padding: 0.45rem 0.75rem !important;
            margin-bottom: 0.35rem !important;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] > div {
            background-color: #fff8ef !important;
            border-color: #b8860b !important;
        }
        [data-testid="stSidebar"] .nav-active > button {
            background: #b8860b !important;
            color: #fff8ef !important;
            border-color: #d4af37 !important;
        }
        .hero-wrap {
            background: linear-gradient(135deg, #fff8ef 0%, #fdebd0 45%, #f6d7a8 100%);
            border: 1px solid #e8c992;
            border-radius: 1.25rem;
            padding: 2rem 2.25rem;
            box-shadow: 0 12px 40px rgba(107, 58, 24, 0.12);
            margin-bottom: 1.5rem;
        }
        .hero-title {
            font-family: "Merriweather", serif;
            color: #4a2812;
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 0.35rem 0;
        }
        .hero-subtitle {
            color: #7a4b22;
            font-size: 1.05rem;
            margin: 0;
        }
        .hero-image-frame {
            border: 4px solid #c9923e;
            border-radius: 1rem;
            overflow: hidden;
            box-shadow: 0 10px 28px rgba(74, 40, 18, 0.18);
            background: #fff;
            max-width: 300px;
            margin: 0 auto;
        }
        .hero-quote {
            margin-top: 1rem;
            padding: 0.9rem 1.1rem;
            border-left: 4px solid #b8860b;
            background: rgba(255,255,255,0.55);
            border-radius: 0.75rem;
            color: #5c3a16;
            font-style: italic;
        }
        .stat-card {
            background: white;
            border: 1px solid #ecd3a8;
            border-radius: 1rem;
            padding: 1rem 1.1rem;
            box-shadow: 0 6px 18px rgba(107, 58, 24, 0.08);
        }
        .stat-label {
            font-size: 0.8rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #8a6135;
        }
        .stat-value {
            font-size: 1.6rem;
            font-weight: 700;
            color: #4a2812;
            margin-top: 0.2rem;
        }
        .page-header {
            background: linear-gradient(90deg, #4a2812, #8b5a2b);
            color: #fff8ef;
            padding: 1.1rem 1.4rem;
            border-radius: 1rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 8px 24px rgba(74, 40, 18, 0.18);
        }
        .page-header h1 {
            color: #fff8ef !important;
            font-family: "Merriweather", serif;
            font-size: 1.7rem !important;
            margin: 0 !important;
        }
        .page-badge {
            display: inline-block;
            margin-top: 0.45rem;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            background: rgba(255, 248, 239, 0.18);
            border: 1px solid rgba(255, 214, 153, 0.35);
            font-size: 0.85rem;
        }
        .content-card {
            background: #fffdf9;
            border: 1px solid #ead6b5;
            border-radius: 1rem;
            padding: 0.35rem 0.35rem 0.75rem;
            box-shadow: 0 8px 22px rgba(107, 58, 24, 0.07);
            min-height: 220px;
        }
        .tamil-block {
            font-family: "Tiro Tamil", "Noto Sans Tamil", serif;
            font-size: 1.28rem;
            line-height: 1.95;
            padding: 1.1rem 1.25rem;
            border-radius: 0.85rem;
            background: linear-gradient(180deg, #fffdf8 0%, #fff6e8 100%);
            border-left: 5px solid #b45309;
        }
        .pronunciation-block {
            font-size: 1.05rem;
            line-height: 1.85;
            padding: 1.1rem 1.25rem;
            border-radius: 0.85rem;
            background: linear-gradient(180deg, #f8fbff 0%, #eef6ff 100%);
            border-left: 5px solid #2563eb;
            font-family: "Noto Sans Telugu", "Tiro Telugu", sans-serif;
        }
        .telugu-block {
            font-size: 1.15rem;
            line-height: 1.9;
            padding: 1.1rem 1.25rem;
            border-radius: 0.85rem;
            background: linear-gradient(180deg, #f7fff7 0%, #edf9ee 100%);
            border-left: 5px solid #15803d;
            font-family: "Noto Sans Telugu", "Tiro Telugu", sans-serif;
        }
        .section-label {
            font-size: 0.78rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #8a6135;
            margin: 0.5rem 0 0.45rem 0.35rem;
            font-weight: 700;
        }
        .empty-note {
            color: #9a7348;
            font-style: italic;
            padding: 1rem 1.1rem;
            background: rgba(255, 248, 239, 0.75);
            border-radius: 0.85rem;
            border: 1px dashed #d8b985;
        }
        .guide-card {
            background: white;
            border: 1px solid #ecd3a8;
            border-radius: 1rem;
            padding: 1.2rem 1.3rem;
        }
        .light-worker-frame {
            border: 3px solid #d4af37;
            border-radius: 1rem;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(107, 58, 24, 0.12);
            background: #fff;
        }
        .light-worker-caption {
            text-align: center;
            color: #7a4b22;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        .mantra-banner {
            margin: 1rem 0 1.5rem 0;
            padding: 0.75rem 1rem;
            background: linear-gradient(90deg, #fff8ef, #fdebd0);
            border: 1px solid #e8c992;
            border-radius: 0.75rem;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_home(filled: int, total: int) -> None:
    col_img, col_text = st.columns([1, 1.6], gap="large")

    with col_img:
        st.markdown('<div class="hero-image-frame">', unsafe_allow_html=True)
        if VALLALAR_IMAGE.exists():
            st.image(str(VALLALAR_IMAGE), use_container_width=True)
        else:
            st.info("Vallalar image not found in assets/")
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption("Arutprakasa Vallalar — Ramalinga Adigalar")

    with col_text:
        st.markdown(
            """
            <div class="hero-wrap">
                <p class="hero-title">6th Tirumurai — Telugu Translation</p>
                <p class="hero-subtitle">
                    Page-by-page translation from your 500-page original book:
                    Tamil, pronunciation, and Telugu meaning.
                </p>
                <div class="hero-quote">
                    அருட்பெருஞ்ஜோதி அருட்பெరுஞ்ஜோதி தனிப்பெருங்கருணை அருட்பெருஞ்ஜோதி
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Light Workers")
    st.markdown(
        '<p style="color:#7a4b22;margin-top:-0.5rem;">'
        "Arutperunjothi — carrying the divine light through translation and service."
        "</p>",
        unsafe_allow_html=True,
    )

    if MAHAMANTRA_IMAGE.exists():
        st.markdown('<div class="mantra-banner">', unsafe_allow_html=True)
        st.image(str(MAHAMANTRA_IMAGE), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    lw_cols = st.columns(len(LIGHT_WORKER_IMAGES))
    captions = ["Divine Jyoti — Arutperunjothi", "Light workers in service"]
    for col, image_path, caption in zip(lw_cols, LIGHT_WORKER_IMAGES, captions):
        with col:
            st.markdown('<div class="light-worker-frame">', unsafe_allow_html=True)
            if image_path.exists():
                st.image(str(image_path), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(f'<p class="light-worker-caption">{caption}</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">Total pages</div><div class="stat-value">{total}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">Completed</div><div class="stat-value">{filled}</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        pct = round((filled / total) * 100, 1) if total else 0
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">Progress</div><div class="stat-value">{pct}%</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### How to translate")
    st.markdown(
        """
        <div class="guide-card">
        <ol>
            <li>Open your book to the page number you are translating.</li>
            <li>Edit the matching folder under <code>content/page_NNN/</code>.</li>
            <li>Fill <code>tamil.md</code>, <code>pronunciation.md</code>, and <code>telugu.md</code>.</li>
            <li>Use <strong>Read Page</strong> in the sidebar to view your work.</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_block(label: str, text: str, css_class: str) -> None:
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if not text or not is_filled(text):
        st.markdown('<p class="empty-note">Not added yet. Edit this page folder in the repo.</p>', unsafe_allow_html=True)
    else:
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        st.markdown(f'<div class="{css_class}">{safe}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_page(page: PageContent) -> None:
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{page.meta.title}</h1>
            <span class="page-badge">Book page {page.meta.book_page}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if page.meta.notes:
        st.info(page.meta.notes)

    col1, col2, col3 = st.columns(3)
    with col1:
        _render_block("Original Tamil", page.tamil, "tamil-block")
    with col2:
        _render_block("Tamil Pronunciation (Telugu script)", page.pronunciation, "pronunciation-block")
    with col3:
        _render_block("Telugu Meaning", page.telugu, "telugu-block")

    with st.expander("Stacked view (mobile-friendly)"):
        st.subheader("Original Tamil")
        st.markdown(page.tamil or "_Not added yet._")
        st.subheader("Tamil Pronunciation")
        st.markdown(page.pronunciation or "_Not translated yet._")
        st.subheader("Telugu Meaning")
        st.markdown(page.telugu or "_Not translated yet._")
