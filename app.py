import streamlit as st

from utils.loader import list_pages, load_page
from utils.ui import apply_styles, render_page

st.set_page_config(
    page_title="6th Tirumurai — Telugu Translation",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()

pages = list_pages()
translated = [
    p
    for p in pages
    if load_page(p.id) and not load_page(p.id).telugu.startswith("_Add Telugu")
]

st.sidebar.title("6th Tirumurai")
st.sidebar.caption("Tamil from thiruarutpa.org → Telugu + pronunciation")
st.sidebar.markdown(
    "[Source: Sixth Thirumurai index](https://www.thiruarutpa.org/Thirumurai/sixth/tm)"
)
st.sidebar.markdown("---")

if not pages:
    st.sidebar.warning("No pages yet. Run `python scripts/import_from_thiruarutpa.py`.")
    selected_id = None
else:
    st.sidebar.caption(f"{len(pages)} paths · {len(translated)} translated")
    query = st.sidebar.text_input("Search path", placeholder="e.g. parasiva, jothi")
    filtered = [
        p
        for p in pages
        if not query
        or query.lower() in p.title.lower()
        or query.lower() in p.title_tamil.lower()
        or query.lower() in p.title_roman.lower()
        or query.lower() in p.id.lower()
    ]
    labels = {p.id: p.title for p in filtered}
    if not filtered:
        st.sidebar.warning("No paths match your search.")
        selected_id = None
    else:
        selected_id = st.sidebar.radio(
            "Browse paths",
            options=[p.id for p in filtered],
            format_func=lambda pid: labels[pid],
        )

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Add Telugu for a path**
    1. Open the folder under `content/NNN_slug/`
    2. Edit `pronunciation.md` and `telugu.md`
    3. Refresh this app
    """
)

if selected_id is None and pages:
    selected_id = pages[0].id

if selected_id is None:
    st.title("6th Tirumurai — Telugu Translation Blog")
    st.markdown(
        """
        Tamil hymns from **[thiruarutpa.org Sixth Tirumurai](https://www.thiruarutpa.org/Thirumurai/sixth/tm)**
        with Telugu pronunciation and translation.

        ### Import Tamil source text

        ```bash
        python scripts/import_from_thiruarutpa.py
        streamlit run app.py
        ```
        """
    )
else:
    page = load_page(selected_id)
    if page is None:
        st.error("Could not load the selected page.")
    else:
        render_page(page)
