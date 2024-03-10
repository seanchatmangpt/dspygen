"""Streamlit app."""

from importlib.metadata import version

import streamlit as st

st.title(f"rdddy v{version('rdddy')}")  # type: ignore[no-untyped-call]
