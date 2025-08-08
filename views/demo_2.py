import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

st.markdown("# Page 1 ❄️")
st.sidebar.markdown("# Page 1 ❄️")

df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

st.bar_chart(df)