"""Shared UI helpers for the 6th Tirumurai blog."""

from __future__ import annotations

import streamlit as st

from utils.loader import PageContent, is_filled


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .tamil-block {
            font-size: 1.35rem;
            line-height: 1.9;
            padding: 1.25rem 1.5rem;
            border-radius: 0.75rem;
            background: #FFFDF8;
            border-left: 4px solid #C17817;
        }
        .pronunciation-block {
            font-size: 1.1rem;
            line-height: 1.85;
            padding: 1.25rem 1.5rem;
            border-radius: 0.75rem;
            background: #F8FBFF;
            border-left: 4px solid #4A7BA7;
            font-family: "Noto Sans Telugu", "Tiro Telugu", sans-serif;
        }
        .telugu-block {
            font-size: 1.2rem;
            line-height: 1.9;
            padding: 1.25rem 1.5rem;
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
        .empty-note {
            color: #8a6d55;
            font-style: italic;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_block(label: str, text: str, css_class: str) -> None:
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)
    if not text or not is_filled(text):
        st.markdown('<p class="empty-note">Not translated yet. Edit this page folder in the repo.</p>', unsafe_allow_html=True)
        return
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    st.markdown(f'<div class="{css_class}">{safe}</div>', unsafe_allow_html=True)


def render_page(page: PageContent) -> None:
    st.title(page.meta.title)
    st.caption(f"Book page {page.meta.book_page}")

    if page.meta.notes:
        st.info(page.meta.notes)

    st.markdown("---")

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
