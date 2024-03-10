"""Streamlit app."""

from importlib.metadata import version

import streamlit as st

from dspygen.modules.chat_bot_module import chat_bot_call
from dspygen.modules.insight_tweet_module import insight_tweet_call
from dspygen.modules.streamlit_bot_module import streamlit_bot_call
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.file_tools import source_dir, pages_dir

st.title(f"dspygen v{version('dspygen')}")  # type: ignore[no-untyped-call]


# # Streamlit form and display
# st.title("Insight Tweet Generator")
#
# insight_input = st.text_input("Enter your insight:")
#
# if st.button("Generate Tweet"):
#     init_dspy()
#     result = insight_tweet_call(insight_input)
#     st.write(result)

from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be

page_list = [Page(str(source_dir("app.py")), "Home", "🏠")]

# loop through the pages and display them
for page_src in pages_dir().iterdir():
    if page_src.is_file() and page_src.suffix == ".py":
        page_list.append(Page(str(page_src), page_src.stem, ":books:"))

# Remove __init__.py from the list
page_list = [page for page in page_list if page.name != "init"]

# show_pages(page_list)
