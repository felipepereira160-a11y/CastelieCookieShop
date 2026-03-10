from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any

import streamlit as st

CATALOG_PATH = Path(__file__).resolve().parent / "catalog.json"


@st.cache_data(show_spinner=False)
def load_catalog() -> List[Dict[str, Any]]:
    if not CATALOG_PATH.exists():
        return []
    with CATALOG_PATH.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def save_catalog(items: List[Dict[str, Any]]) -> None:
    with CATALOG_PATH.open("w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False, indent=2)

    load_catalog.clear()
