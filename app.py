import streamlit as st

from utils.loader import is_filled, list_pages, load_page
from utils.ui import apply_styles, render_home, render_page

st.set_page_config(
    page_title="6th Tirumurai — Telugu Translation",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()

pages = list_pages()
filled = sum(
    1
    for p in pages
    if (page := load_page(p.id))
    and is_filled(page.tamil)
    and is_filled(page.pronunciation)
    and is_filled(page.telugu)
)

st.sidebar.markdown("### 🕉️ 6th Tirumurai")
st.sidebar.caption("Tamil · pronunciation · Telugu")
st.sidebar.markdown("---")

view = st.sidebar.radio("Menu", ["Home", "Read Page"], label_visibility="collapsed")

selected_id = None

if view == "Read Page":
    if not pages:
        st.sidebar.warning("No pages yet. Run `python scripts/init_pages.py`.")
    else:
        st.sidebar.caption(f"{filled}/{len(pages)} pages completed")
        page_num = st.sidebar.number_input(
            "Go to book page",
            min_value=1,
            max_value=len(pages),
            value=1,
            step=1,
        )
        by_number = {p.book_page: p.id for p in pages}
        selected_id = by_number.get(int(page_num))

        query = st.sidebar.text_input("Search", placeholder="page title")
        if query:
            filtered = [p for p in pages if query.lower() in p.title.lower() or query in str(p.book_page)]
            if filtered:
                selected_id = st.sidebar.selectbox(
                    "Matches",
                    options=[p.id for p in filtered],
                    format_func=lambda pid: next(p.title for p in pages if p.id == pid),
                )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        **Add one page**
        1. Open `content/page_NNN/`
        2. Edit `tamil.md`
        3. Edit `pronunciation.md`
        4. Edit `telugu.md`
        5. Refresh this app
        """
    )

if view == "Home" or not pages:
    render_home(filled, len(pages) or 500)
elif selected_id is None:
    st.warning("Choose a valid book page from the sidebar.")
else:
    page = load_page(selected_id)
    if page is None:
        st.error("Could not load the selected page.")
    else:
        render_page(page)
