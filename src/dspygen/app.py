"""Streamlit app."""

from importlib.metadata import version

import streamlit as st

st.title(f"dspygen v{version('dspygen')}")  # type: ignore[no-untyped-call]
