import streamlit as st
from streamlit_url_fragment import get_fragment


fragment = get_fragment()
st.write(fragment)