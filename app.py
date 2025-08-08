import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

page_1 = st.Page("views/demo_1.py", title="Page 1", icon="❄️")
page_2 = st.Page("views/demo_2.py", title="Page 2", icon="🎉")

# Set up navigation
pg = st.navigation([page_1, page_2])

pg.run()