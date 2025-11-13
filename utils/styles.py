from pathlib import Path
import streamlit as st


def load_styles(path: str | None = None) -> None:
    try:
        if path is None:
            path = Path(__file__).parent.parent / "assets" / "styles.css"
        else:
            path = Path(path)
        if not path.exists():
            st.warning(f"Style file not found: {path}")
            return
        css = path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load styles: {e}")
