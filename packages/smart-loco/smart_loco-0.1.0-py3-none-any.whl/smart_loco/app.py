import streamlit as st
from smart_loco.components import chat

# Configure page
st.set_page_config(
    page_title="Smart Loco",
    page_icon=" ",
    layout="wide"
)


def set_sidebar_width():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"][aria-expanded="true"] {
                min-width: 30vw !important;
                max-width: 30vw !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    set_sidebar_width()
    
    # Sidebar for tool selection
    tool = st.sidebar.selectbox(
        "Select Tool",
        ["Chat"]
    )
    
    if tool == "Chat":
        # Chat component will handle its own model selection
        chat.show()


if __name__ == "__main__":
    main()