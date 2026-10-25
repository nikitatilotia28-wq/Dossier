"""Tiny registry so pages can navigate to one another.

app.py registers the st.Page objects here after building the navigation, and any
page can call ``go_to("scan")`` to jump elsewhere via st.switch_page.
"""

from __future__ import annotations

import streamlit as st

_PAGES: dict[str, object] = {}


def register(pages: dict[str, object]) -> None:
    _PAGES.clear()
    _PAGES.update(pages)


def go_to(key: str) -> None:
    page = _PAGES.get(key)
    if page is not None:
        st.switch_page(page)
