"""Shared UI helpers for the 6th Tirumurai blog."""

from __future__ import annotations

import streamlit as st

from utils.loader import PageContent


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .tamil-block {
            font-size: 1.35rem;
            line-height: 1.9;
            padding: 1rem 1.25rem;
            border-radius: 0.75rem;
            background: #FFFDF8;
            border-left: 4px solid #C17817;
        }
        .pronunciation-block {
            font-size: 1.05rem;
            line-height: 1.8;
            padding: 1rem 1.25rem;
            border-radius: 0.75rem;
            background: #F8FBFF;
            border-left: 4px solid #4A7BA7;
            font-family: "Noto Sans Telugu", "Tiro Telugu", sans-serif;
        }
        .telugu-block {
            font-size: 1.2rem;
            line-height: 1.85;
            padding: 1rem 1.25rem;
            border-radius: 0.75rem;
            background: #F7FFF7;
            border-left: 4px solid #2E7D32;
            font-family: "Noto Sans Telugu", "Tiro Telugu", sans-serif;
        }
        .section-label {
            font-size: 0.85rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #6B4F3A;
            margin-bottom: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page(page: PageContent) -> None:
    st.title(page.meta.title)
    if page.meta.title_roman:
        st.caption(page.meta.title_roman)
    if page.meta.title_telugu:
        st.caption(page.meta.title_telugu)

    if page.meta.path_number is not None:
        st.markdown(f"**பாடல் / Path:** {page.meta.path_number}")

    if page.meta.source_url:
        st.markdown(f"[View Tamil source on thiruarutpa.org]({page.meta.source_url})")

    if page.meta.notes and not page.meta.notes.startswith("Tamil source:"):
        st.info(page.meta.notes)

    st.markdown("---")

    def render_block(label: str, text: str, css_class: str) -> None:
        st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)
        if text.startswith("_") and text.endswith("_"):
            st.markdown(text)
        else:
            safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            st.markdown(f'<div class="{css_class}">{safe}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        render_block("Tamil (from thiruarutpa.org)", page.tamil, "tamil-block")
    with col2:
        render_block("Tamil Pronunciation (Telugu script)", page.pronunciation, "pronunciation-block")
    with col3:
        render_block("Telugu Translation", page.telugu, "telugu-block")

    with st.expander("View as stacked sections (mobile-friendly)"):
        st.subheader("Tamil")
        st.markdown(page.tamil)
        st.subheader("Pronunciation")
        st.markdown(page.pronunciation)
        st.subheader("Telugu")
        st.markdown(page.telugu)
