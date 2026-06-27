import streamlit as st

from utils.loader import is_filled, list_pages, load_page
from utils.ui import apply_styles, render_home, render_page

st.set_page_config(
    page_title="6th Tirumurai — Telugu Translation",
    page_icon="📖",
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

st.sidebar.markdown("### 6th Tirumurai")
st.sidebar.caption("Tamil · pronunciation · Telugu")
st.sidebar.markdown("---")

if "view" not in st.session_state:
    st.session_state.view = "Home"

st.sidebar.markdown("**Navigate**")
nav_home, nav_read = st.sidebar.columns(2)
with nav_home:
    if st.button("Home", use_container_width=True, key="nav_home"):
        st.session_state.view = "Home"
with nav_read:
    if st.button("Read Page", use_container_width=True, key="nav_read"):
        st.session_state.view = "Read Page"

view = st.session_state.view
st.sidebar.caption(f"Current: **{view}**")
st.sidebar.markdown("---")

selected_id = None

if view == "Read Page":
    if not pages:
        st.sidebar.warning("No pages yet. Run `python scripts/init_pages.py`.")
    else:
        st.sidebar.caption(f"{filled}/{len(pages)} pages completed")

        if "book_page" not in st.session_state:
            st.session_state.book_page = 1

        st.sidebar.markdown("**Go to book page**")
        prev_col, page_col, next_col = st.sidebar.columns([1, 3, 1])

        with prev_col:
            if st.button("−", use_container_width=True, help="Previous page"):
                st.session_state.book_page = max(1, st.session_state.book_page - 1)

        with next_col:
            if st.button("+", use_container_width=True, help="Next page"):
                st.session_state.book_page = min(len(pages), st.session_state.book_page + 1)

        with page_col:
            page_num = st.number_input(
                "Page number",
                min_value=1,
                max_value=len(pages),
                value=st.session_state.book_page,
                step=1,
                label_visibility="collapsed",
            )

        st.session_state.book_page = int(page_num)

        by_number = {p.book_page: p.id for p in pages}
        selected_id = by_number.get(st.session_state.book_page)

        query = st.sidebar.text_input("Search", placeholder="page title")
        if query:
            filtered = [p for p in pages if query.lower() in p.title.lower() or query in str(p.book_page)]
            if filtered:
                picked = st.sidebar.selectbox(
                    "Matches",
                    options=[p.id for p in filtered],
                    format_func=lambda pid: next(p.title for p in pages if p.id == pid),
                )
                selected_id = picked
                match = next(p for p in pages if p.id == picked)
                st.session_state.book_page = match.book_page

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
