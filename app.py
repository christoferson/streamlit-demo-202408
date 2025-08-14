import streamlit as st

st.set_page_config(
    page_title="StreamLit Demo App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define pages
home_page = st.Page("views/home.py", title="Home", icon="🏠", default=True)
page_1 = st.Page("views/demo_1.py", title="Components Demo", icon="🎛️")
page_2 = st.Page("views/demo_2.py", title="Charts & Data", icon="📊")
page_3 = st.Page("views/demo_3.py", title="Creative Playground", icon="🎨")
crud_page = st.Page("views/crud_demo.py", title="CRUD Manager", icon="👥")

# Set up navigation with the home page as default
pg = st.navigation([home_page, page_1, page_2, page_3, crud_page])

pg.run()