import streamlit as st
from st_pages import add_page_title

from dspygen.modules.streamlit_bot_module import streamlit_bot_call
from dspygen.utils.dspy_tools import init_dspy

add_page_title()


# Streamlit form and display
st.title("StreamlitBotModule Generator")
project = st.text_input("Enter project")
page = st.text_input("Enter page")

if st.button("Submit StreamlitBotModule"):
    init_dspy()

    result = streamlit_bot_call(project=project, page=page)
    st.code(result)